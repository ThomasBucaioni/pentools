# MD5 and SHA hashes

source: https://www.packtpub.com/product/cryptography-with-python-video/9781788397179

## MD5

```
import hashlib
hashlib.new("md5", "Hello").hexdigest()
```

## SHA

```
hashlib.new("sha1", "Hello").hexdigest()
hashlib.new("sha256", "Hello").hexdigest()
hashlib.new("sha512", "Hello").hexdigest()
```

## Windows MD4

```
hashlib.new("md4","P@ssw0rd6".encode("utf-16le")).hexdigest() # utf-16le...
for c in "123456790":
  p = "P@ssw0rd" + c
  h = hashlib.new("md4",p.encode("utf-16le")).hexdigest()
  print(p,h)
```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

```

## Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```


