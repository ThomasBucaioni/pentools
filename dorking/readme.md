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

#### SMB (default ports: 139, 445)

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

#### SMTP

#### SNMP




