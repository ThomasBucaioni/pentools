# Active Directory

## Enumeration

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




