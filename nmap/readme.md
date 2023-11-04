# Nmap

## Usual scans

### Options

Also [here](https://github.com/ThomasBucaioni/pentools/tree/main/dorking#nmap):
- Ports: `-p-`, `-p num1, num2`
- No ping: `-Pn`
- TCP, UDP: `-sT -sU`
- With output file: `-oG` (grep), `-oA` (all)
- OS scan: `-O`, `--osscan-guess`
- Agressive scan: `-A` 
- Timeouts: `-T5`
- NSE default scripts: `-sC`
- NSE category scripts: `--script=auth, broadcast, brute, default, discovery, dos, exploit, external, fuzzer, intrusive, malware, safe, version, vuln`
- NSE expression scripts: `--script=http*`
- Script help: `nmap --script-help "http-* and vuln"`

### Combined

```
nmap -sS -n -Pn $IP -p-
nmap -sT -n -Pn --script=vuln -p $Port $IP
nmap -sU -sT -n -Pn -sC -T5 $IP
nmap -A -oA ${IP}_out $IP
nmap -Pn -n -sC -sV -T5 -p- -vvv $IP
nmap -Pn -n -p$port -vvv --script smb-enum-share $IP
nmap -Pn -n -p$port -vvv --script http-enum $IP
nmap -sU --open -vvv $IP
nmap -sU --open -p- -T5 -vvv $IP
```

### Reddit

https://www.reddit.com/r/oscp/comments/15j4ewd/best_default_nmap_scan_flags/


## Vulnerabily scan

### Principle

1. Host discovery
2. Port scanning
3. Operating system, service, and version detection
4. Check in vulnerability DataBases: 
    - https://cve.mitre.org/cve/search_cve_list.html
    - https://nvd.nist.gov/

### NSE scripts

Lua syntax: 
- https://www.lua.org/pil/contents.html
- https://github.com/ThomasBucaioni/pentools/tree/main/programming#lua

#### Directory and help

The NSE scripts are under: `/usr/share/nmap/scripts/*.nse`
Help on a particular one: `nmap --script-help=some-script.nse`

#### By category

```
grep -r '"vuln"' /usr/share/nmap/scripts/
sudo nmap -sV -p 443 --script "vuln" $IP
```

#### Individual scripts

Vulners script: https://svn.nmap.org/nmap/scripts/vulners.nse
```
sudo nmap -sV --script vulners $IP
sudo nmap -sV --script vulners --script-args mincvss=minimumcvssscorefordisplay $IP
```
Then, Google the CVE and try to fix the exploit... Update Nmap database: `sudo nmap --script-updatedb`

---

# Searchsploit

Update the DB...
Path: `/usr/share/exploitdb/`
Research: `searchsploit somestring`
Download: `searchsploit -m path/of/exploit/number.py`

PyInstaller: https://pyinstaller.org/en/stable/
