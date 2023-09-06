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

## Gobuster 

### Directory brute force

Documentation on Kali: https://www.kali.org/tools/gobuster/
```
gobuster dir -u $IP -w /path/to/wordlist.txt
```
Kali wordlists: `/usr/share/wordlists/dirb/*.txt`

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

## Javascript (console: `^C+^S+k`)

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


