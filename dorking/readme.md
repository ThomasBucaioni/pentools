# Information gathering

Cyclic process...

## Passive

### OSINT

- https://en.wikipedia.org/wiki/Open-source_intelligence
- https://en.wikipedia.org/wiki/Attack_surface
- ["Open Source Intelligence Methods and Tools" - Hassan & Hijazi](https://link.springer.com/book/10.1007/978-1-4842-3213-2)
- https://osint.link/

### Whois

https://en.wikipedia.org/wiki/WHOIS
https://en.wikipedia.org/wiki/Name_server
https://en.wikipedia.org/wiki/Domain_name_registrar
```
whois some.web-site.com
whois some.web-site.com -h my.whois.server.ip
whois ip.address -h my.whois.ip
```

### Google dorking

- https://usersearch.org/updates/2023/02/05/the-ultimate-google-dorking-cheatsheet-2023/
- https://www.freecodecamp.org/news/google-dorking-for-pentesters-a-practical-tutorial/
- https://www.exploit-db.com/google-hacking-database +++
- https://gist.github.com/sundowndev/283efaddbcf896ab405488330d1bbc06

Examples:
```
site:site-to-hack.com filetype:pdf
-filetype:html
ext:php
intitle:"index of" "parent directory"
```

### Information gathering websites

- https://searchdns.netcraft.com
- source code: GitHub, GitHub Gist, GitLab, SourceForge, ... (search example: `filename:password.txt`)
- https://www.shodan.io/ (search example: `hostname:site-to-hack.com`)
- https://securityheaders.com/

## Active gathering

### DNS

Lists: https://github.com/danielmiessler/SecLists

#### Manual

##### Host

```
host site-to-hack.com # returns the IP address
host -t mx site-to-hack.com # returns the MAIL records with their priority
host -t txt site-to-hack.com # returns the TXT records (useful to upload binaries)
for i in mx txt ftp www mail ; do host $i.site-to-hack.com ; done
for i in {1..254} ; do host 192.168.1.$i ; done | grep -v "not found" # with the site prefix
```

##### Nslookup

```
nslookup ns1.site-to-hack.com # returns the `A` record
nslookup -type=TXT www.site-to-hack.com # returns the `TXT` record
```

#### Automatic

##### DnsRecon

Dnsrecon on GitHub: https://github.com/darkoperator/dnsrecon
```
dnsrecon -d domain.name.com -t std # std = standard enumeration
dnsrecon -d domain.com -D /path/to/dictionary.txt -t brt # brt = brute force with dictionary
```

##### DnsEnum

DnsEnum in Kali: https://www.kali.org/tools/dnsenum/
```
dnsenum domain.name.to.hack.com
```

### Port scanning

Netcat example: `nc -nvv -w 1 -z $IP $PortInit-$PortEnd`
Other tools (more noisy):
- https://www.kali.org/tools/masscan/
- https://rustscan.github.io/RustScan/

#### Nmap

Options:
- `-p`: ports range
- `-sS`: SYN scan
- `-sT`: TCP scan
- `-sU`: UDP scan
- `-sn`: ICMP scan + TCP SYN port 443 + TCP ACK port 80
- `-v`: verbose
- `-oG`: output file, for `grep`
- `-A`: aggressive - OS guess + script scanning + traceroute
- `--top-ports=20`: top 20 ports, as in `/usr/share/nmap/nmap-services`
- `-O --osscan-guess`: OS guess
- `-sV`: service versions
- `--script some-script-name`: NSE script scan, as in `/usr/share/nmap/scripts` (e.g. `http-headers`)
- `--script-help some-script-name`: provides some explanation about the NSE script

NSE: http://nmap.org/book/nse.html

#### Windows PowerShell `Test-NetConnection`

```
Test-NetConnection -Port 80 $IP
1..1024 | ForEach-Object { echo ( (New-Object Net.Sockets.TcpClient).Connect("$IP", $_) ) "TCP port $_ is open"} 2> $null
```
PowerShell special characters: https://stackoverflow.com/questions/56875192/what-does-mean-and-in-powershell

#### SMB (Server Message Block)

Default ports: 139, 445
Other names: NetBIOS, NBT
```
nmap -v -p 139,445 -oG smb_summary.txt $IpRange.1-254
sudo nbtscan -r a.b.c.0/24 # port 137
```

Nmap NSE scripts: `/usr/share/nmap/scripts/smb*`
```
nmap -v -p 139,445 --script smb-os-discovery $IP
```

On Windows (cmd.exe):
```
> net view \\domaincontrollername /all
```

Shares enumeration: 
- https://www.hackingarticles.in/a-little-guide-to-smb-enumeration/
- https://fareedfauzi.gitbook.io/oscp-playbook/services-enumeration/smb

Mount shares locally: `sudo mount //$IP/someshare /mnt`

Enum4Linux: `enum4linux -a $ip` or `enum4linux -u 'guest' -p '' -a $ip`

#### SMTP (Simple Mail Transport Protocol)

##### Manual enumeration

Username manual enumeration:
```
nc -nv $IP 25
VRFY someusername
VRFY otherusername
```

##### Enumeration with a Python socket

Python script:
```
#!/usr/bin/python

import socket
import sys

if len(sys.argv) != 3:
    print("Usage: mysmtppythonscript.py someusernametotest ipaddressofthemailserver")
    sys.exit(0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = sys.argv[2]
connect = s.connect((ip,25)) # usual SMTP port
banner = s.recv(1024)
print(banner)

user = (sys.argv[1]).encode()
s.send(b'VRFY ' + user + b'\r\n')
result = s.recv(1024)
print(result)
s.close()
```
and then: `IP=a.b.c.d ; for name in root user1 user2 user3 ; do python3 mysmtppythonscript.py $name $IP ; done`

##### Windows

With cmdlet `Test-NetConnection`, test the port:
```
Test-Connection -Port 25 $IP
```
then install Telnet (with [Admin privileges](https://learn.microsoft.com/en-us/powershell/module/dism/enable-windowsoptionalfeature?view=windowsserver2022-ps)):
```
PS > dism /online /Enable-Feature /FeatureName:TelnetClient
```
and `VRFY` users:
```
cmd > telnet $IP 25
VRFY root
VRFY someusername
```

#### SNMP (Simple Network Management Protocol)

- https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol
- https://en.wikipedia.org/wiki/Object_identifier

Scan:
```
sudo nmap -sU --open -p 161 $IP -oG open-snmp.txt
```
Community [strings](http://www.phreedom.org/software/onesixtyone/): `public`, `private`, `manager`
Brute force the community strings:
```
kali$ onesixtyone -c communitystringfile.txt -i ipfile.txt
```
then query the community MIBs (Management Information Base) with `snmpwalk`:
```
snmpwalk -c somecommunitystring -v 1 -t 10 $IP # -v = version number of SNMP ; -t = timeout ; somecommunitystring = public, private, management, ...
```
to gather email addresses, hostnames, services running, ...: 
```
snmpwalk -c public -v 1 $IP 1.3.6.1.2.1.25.4.2.1.2 # Service OID
snmpwalk -c public -v 1 $IP 1.3.6.1.4.1.77.1.2.25 # User OID ; decimal, decoded in ASCII https://en.wikipedia.org/wiki/ASCII ; 65.100.109.105.110.105.115.116.114.97.116.111.114 = STRING: "Administrator"
snmpwalk -c public -v 1 $IP 1.3.6.1.2.1.25.6.3.1.2 # Installed software OID
snmpwalk -c public -v 1 $IP 1.3.6.1.2.1.6.13.1.3 # Open TCP port OID ; 1.3.6.1.2.1.6.13.1.3.0.0.0.0.88.0.0.0.0.0 = port 88
```

