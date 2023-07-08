# Powershell

## Basic commands

```
$PSVersionTable
Get-Help
Get-Verb
Get-Help -Name "Get-Help"
Get-Help -Name *adg*
Get-Help -Verb *to*Get-Help -Name "Get-Help" -Examples
Get-Help -Name "Get-Help" -Detailed
help Get-Help
Get-Alias
Get-Alias -Definition "help"
Set-Alias -Name gh -Value Get-Help
Get-Alias -Name gh
gh Get-Help
Get-Command
Get-Command -Noun file
Get-Command -Verb out,edit,export -Noun *file*
Get-Help Out-File
```

## Variables

```
$somevar = "text"
Clear-Variable -Name somevar
```

## Types

```
$array="blue","black","yellow","white","orange"
$array.GetType()
$array[0]
[int]$b + $a # conversion
```
Other:
- https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arrays?view=powershell-7.3
- https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables?view=powershell-7.3
- https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_booleans?view=powershell-7.3


## Operators

Shift bits: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arithmetic_operators?view=powershell-7.3
Comparison: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comparison_operators?view=powershell-7.3

## Conditionals

Switch: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_switch?view=powershell-7.3
```
for (($i = 0), ($j = 0); $i -lt 10; $i++)
{
    "`$i:$i"
    "`$j:$j"
}
```
```
for ($myVar=0; $myVar -lt 5; $myVar++)
{
  Write-Output $myVar;
}
```
```
$myArray = "sometext"
$myArray = $myWord.ToCharArray()
foreach ($myLetter in $myArray)
{
  $myLetter
}
```
```
$count = 0
while ($count -lt 5)
{
  $count
  $count++
}
```
Continue, skip, break: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_break?view=powershell-7.3

## Properties and Methods

```
Get-ChildItem | Get-Member -Name *write*
Get-ScheduledTask | get-member -MemberType Method | Measure-Object -Line
```

## Filtering and Formatting

```
Get-Service | Get-Member
Get-Service | Select-Object -Property "DisplayName","MachineName","ServiceType","StartType","Status"
Get-Service | Select-Object -Property DisplayName,ServiceType,StartType,Status | Sort-Object -Property Status -Descending
Get-Service | Select-Object -Property DisplayName,ServiceType,StartType,Status | Sort-Object -Property Status -Descending | Where-Object StartType -EQ Automatic
Get-Service | Select-Object -Property DisplayName,ServiceType,StartType,Status | Sort-Object -Property Status -Descending | Where-Object StartType -EQ Automatic | Format-List
Get-Service | Select-Object -Property ServiceName,DisplayName,ServiceType,StartType,Status | Sort-Object -Property Status -Descending | Where-Object {$_.StartType -EQ "Automatic" -And $_.ServiceName -Match "^s"}
Get-Service | Select-Object -Property ServiceName,DisplayName,ServiceType,StartType,Status | Sort-Object -Property Status -Descending | Where-Object {$_.StartType -EQ "Automatic" -And $_.ServiceName -Match "^s"} | Format-Table

Get-Item alias:
cd HKLM:
New-Item myKey
New-ItemProperty -Path .\myKey\ -Name Test -Type DWORD -Value 1
Get-Item .\myKey\
```
Quoting: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules?view=powershell-7.3
Regex: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_regular_expressions?view=powershell-7.3
Formating: https://learn.microsoft.com/en-us/powershell/scripting/samples/using-format-commands-to-change-output-view?view=powershell-7.3

## Functions

```
function Get-MrParameterCount {
    param (
        [string[]]$ParameterName
    )

    foreach ($Parameter in $ParameterName) {
        $Results = Get-Command -ParameterName $Parameter -ErrorAction SilentlyContinue

        [pscustomobject]@{
            ParameterName = $Parameter
            NumberOfCmdlets = $Results.Count # ++
        }
    }
}
```

## Scripts

```
Get-ExecutionPolicy
Set-ExecutionPolicy RemoteSigned
powershell.exe -exec bypass .\script.ps1
Get-Module
Get-Module -ListAvailable
Get-Command -Module Defender

```

## Misc

source: https://www.udemy.com/course/powershell-for-active-directory-administrators/
```
get-help get-adcomputer 
get-help Get-ADComputer -Examples
import-csv .\computers.csv | new-adcomputer
import-csv .\computers.csv | Foreach-Object {Remove-ADcomputer -Identity $_.SamAccountName -Confirm:$False }
New-ADComputer -Name PC9 -Path "cn=computers,dc=atlantis,dc=local"
Import-Csv .\Users.csv | Foreach-Object {Remove-ADUser -Identity $_.SamAccountName -Confirm:$False }
Get-ADUser -filter 'department -eq "hr"'| Remove-ADUser -whatif
Get-ADUser -filter 'department -eq "hr"'| Remove-ADUser
Get-ADUser -filter 'department -eq "hr"'| Remove-ADUser -Confirm:$false
Import-Csv ".\users.csv" | New-ADUser -AccountPassword $(convertto-securestring "P@55w0rd" -AsPlainText -Force) -ChangePasswordAtLogon $true -Enabled $true

```
