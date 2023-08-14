# Active Directory

## Native enumeration

```
net user /domain
net user someuser /domain
net group /domain
net group "Some Group With Whitespaces" /domain
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

https://powersploit.readthedocs.io/en/latest/Recon/

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

```
Find-LocalAdminAccess
Get-NetSession -ComputerName somehostname
Get-NetSession -ComputerName somehostname -Verbose
Get-Acl -Path HKLM:System\CurrentControlSet\Services\LanmanServer\DefaultSecurity\ | format-list
C:\PSTools\PsLoggedon.exe \\somehostname
```
Warning: PsLoggedon.exe needs the service `Remote Registry` on the target

### Service accounts

```
cmd > setspn -L iis_service
PS > Get-NetUser -SPN | select samaccountname,serviceprincipalname
```

### Object permissions

### Domain shares

## Automated AD enumeration

### SharpHound

### BloodHound

