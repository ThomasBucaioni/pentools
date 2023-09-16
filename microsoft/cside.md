# Client-side attacks

## Dorking

Passive: `site:www.site-to-hack.com filetype:pdf`
Gobuster: `gobuster dir -x pdf -u $TargetIp -w /usr/share/wordlist/dirb/commont.txt`
Exiftool: `exiftool -a -u somefile.pdf`


