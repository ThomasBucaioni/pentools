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


