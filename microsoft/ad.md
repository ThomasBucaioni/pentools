# Active Directory

## Enumeration

```
$myPrimaryDomainController = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().PdcRoleOwner.Name

$myDn = ([adsi]'').distinguishedName 

$LdapPath = "LDAP://$myPrimaryDomainController/$myDn"

$direntry = New-Object System.DirectoryServices.DirectoryEntry($LdapPath)

$dirsearcher = New-Object System.DirectoryServices.DirectorySearcher($direntry)
$dirsearcher.FindAll()
```

