# Nmap

## Usual scans

### Options

Ports: `-p-`, `-p num1, num2`
No ping: `-Pn`
TCP, UDP: `-sT -sU`
With output file: `-oG` (grep), `-oA` (all)
OS scan: `-O`
Agressive scan: `-A` 
Timeouts: `-T5`
NSE default scripts: `-sC`
NSE category scripts: `--script=auth, broadcast, brute, default, discovery, dos, exploit, external, fuzzer, intrusive, malware, safe, version, vuln`
NSE expression scripts: `--script=http*`
Script help: `nmap --script-help "http-* and vuln"`

### Combined

```
nmap -sS -n -nP $IP -p-
nmap -sT -n -Pn --script=vuln -p $Port $IP
nmap -sU -sT -n -Pn -sC -T5 $IP
nmap -A -oA ${IP}_out $IP
```

### Reddit

https://www.reddit.com/r/oscp/comments/15j4ewd/best_default_nmap_scan_flags/


## Vulnerabily scan

### Principle

1. Host discovery
2. Port scanning
3. Operating system, service, and version detection
4. Check in vulnerability DBs: 
    - https://cve.mitre.org/cve/search_cve_list.html
    - https://nvd.nist.gov/

### NSE scripts



