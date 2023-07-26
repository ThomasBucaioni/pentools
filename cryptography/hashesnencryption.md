# Hashes and Encryption

## Base64

Characters: `A, B, ..., Z, a, b, ..., z, 0, ..., 9, /, +`

## MD5 and SHA hashes

source: https://www.packtpub.com/product/cryptography-with-python-video/9781788397179

### MD5

```
import hashlib
hashlib.new("md5", "Hello").hexdigest()
```

### SHA

```
hashlib.new("sha1", "Hello").hexdigest()
hashlib.new("sha256", "Hello").hexdigest()
hashlib.new("sha512", "Hello").hexdigest()
```

### Windows MD4

```
hashlib.new("md4","P@ssw0rd6".encode("utf-16le")).hexdigest() # utf-16le...
for c in "123456790":
  p = "P@ssw0rd" + c
  h = hashlib.new("md4",p.encode("utf-16le")).hexdigest()
  print(p,h)
```

### Linux cracking

```
from passlib.hash import sha512_crypt
sha512_crypt.using(salt="somesalt", round=5000).hash("P@ssw0rd") # /etc/passwd: $6$ = 5000 rounds
```

## Encryption

### AES (symmetric)

```
from Crypto.Cipher import AES
key = "some key"
plain = "secret string"
cipher = AES.new(key)
cipertext = cipher.encrypt(plain)
print(ciphertext.encode("hex")
cipher.decrypt(ciphertext)
```

### CBC mode

```
iv = "Initialization vector"
cipher = AES.new(key, AES.MODE_CBC, iv)
```

### RSA (asymmetric)

```
from Crypto.PublicKey import RSA
key = RSA.generate(2048)
publickey = key.publickey()
aeskey = 'AES key for symmetric encryption'
aeskeyencrypted = publickey.encrypt(aeskey, 0)[0]
print(aeskeyencrypted.encode("hex")

aeskeydecrypted = key.decrypt(aeskeyencrypted)
print(aeskeydecrypted == aeskey) # expected 'True'
```


