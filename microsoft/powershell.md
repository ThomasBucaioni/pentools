# Powershell

## Basics

### Help

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

### Variables

```
$somevar = "text"
Clear-Variable -Name somevar
```

### Types

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


### Operators

- Shift bits: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arithmetic_operators?view=powershell-7.3
- Comparison: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comparison_operators?view=powershell-7.3

### Conditionals

Switch: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_switch?view=powershell-7.3
```
for (($i = 0), ($j = 0); $i -lt 10; $i++)
{
    "`$i:$i"
    "`$j:$j"
}
```
Simple `for`:
```
for ($myVar=0; $myVar -lt 5; $myVar++)
{
  Write-Output $myVar;
}
```
Loop `foreach`:
```
$myArray = "sometext"
$myArray = $myWord.ToCharArray()
foreach ($myLetter in $myArray)
{
  $myLetter
}
```
While loops:
```
$count = 0
while ($count -lt 5)
{
  $count
  $count++
}
```
Continue, skip, break: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_break?view=powershell-7.3

### Properties and Methods

```
Get-ChildItem | Get-Member -Name *write*
Get-ScheduledTask | get-member -MemberType Method | Measure-Object -Line
```

### Filtering and Formatting

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
- Quoting: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules?view=powershell-7.3
- Regex: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_regular_expressions?view=powershell-7.3
- Formating: https://learn.microsoft.com/en-us/powershell/scripting/samples/using-format-commands-to-change-output-view?view=powershell-7.3

### Functions

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

### Scripts

```
Get-ExecutionPolicy
Set-ExecutionPolicy RemoteSigned
powershell.exe -exec bypass .\script.ps1
Get-Module
Get-Module -ListAvailable
Get-Command -Module Defender

```

## Misc

### AD

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

### Enumeration

```
Get-WmiObject win32_product | Select-Object Name, Version, PackageName, InstallDate | Format-Table 
Get-CmiInstance -Namespace root/SecurityCenter -ClassName AntivirusProduct
Get-MpComputerStatus
net users
net localgroup
```

### Sessions

```
Invoke-Command -ScriptBlock { $gonevariable = "This variable will be gone when the commands is torn down" }
$session = New-PSSession -ComputerName otherserver
Get-PSSession
Invoke-Command -Session $session -ScriptBlock { $persistentvariable = "This variable will remain" }
Get-PSSession | Disconnect-PSSession
Connect-PSSession -ComputerName otherserver
Get-PSSession | Remove-PSSession
```
Double hops with `CredSSP`:
```
Enable-WSManCredSSP -Role Client -DelegateComputer otherserver -Force
Invoke-Command -ComputerName otherserver -ScriptBlock { Enable-WSManCredSSP -Role Server }
Invoke-Command -ComputerName otherserver -ScriptBlock ( Get-ChildItem -Path '\\thedomaincontrollername\c$' } -Authentication Credssp -Credential (Get-Credential)
```

### Pester

On GitHub: https://github.com/pester/Pester/wiki/
Example:
```
describe 'Checks if the webserver is running' {
    context 'Webserver install' {
        it 'Checks the installation' {
            $parameters = @{
                ComputerName = 'otherserver'
                Name = 'Web-Server'
            }
            (Get-WindowsFeature @parameters).Installed | should -Be $true
        }
    }
}
```
Invoke with: `PS > Invoke-Pester -Path c:\path\to\SomeCheck.Tests.ps1`

### WMI and CMI objects

```
Get-WmiObject --list *print*
Get-WmiObject -Class win32_diskdrive # Physical
Get-WmiObject -Class win32_logicaldisk # C:, D:
Get-WmiObject -Class win32_logicaldisk | format-table
get-wmiobject -class cim_printer # Printers installed on the computer
get-wmiobject -list # lengthy...
```

### Finding environment variables

Find:
```
Get-Variables
$true
$false
$null
Get-PSDrive # environment drive: `ENV`
cd env: # as `cd c:` or `cd d:`
    dir # list env vars
$env:computername
```
Creation
```
$thing
Get-Variable $thing # error
(get-date).day
$day = (get-date).day
$tomorrow = (get-date).adddays(1).day
New-Variable thing -value "some string"
```

### Pipelines

Tips: use `Help` and `Get-Member` to get information
```
new-item c:\new_file1.txt
ni c:\new_file2.txt # same as above
ni c:\somedir -itemtype directory
help move-item -parameter path # help on the path param of move-item
get-item c:\file.txt | gm # Get-Member
get-item c:\file.txt | move-item -dest c:\somedir
```

### Queries

```
get-item * | select-object name
get-item * | select name # same as above
get-item * | select name, length | sort-object -descending # sorts files by size
ni test.txt -value 'some text in file'
Get-WmiObject win32_logicaldisk | select deviceid, freespace
Get-WmiObject win32_logicaldisk | select deviceid, freespace, @{name = "Gb free"; expression = {$_.freespace / 1Gb}} # displays the size in Gb as well
```

### Formatting

```
get-alias -def where-object
get-wmiobject cim_printer | ? name -ne $null
get-wmiobject cim_printer | ? name -ne $null | select -property name, location

get-childitem c:\somedir | ? name -like "*file*" | format-wide
get-childitem -path "c:\somedir\*file*" | format-wide # same result
measure-command {get-childitem -path "c:\somedir\*file*" | format-wide} # same result} # time of execution of the command
gsv # alias for get-service
gsv | format-list
gsv b* | format-list
```

### Reporting

```
dir * | select -pr name, length | sort -de # aliases...
dir * | select -pr name, length | sort -de | out-host # default output, in terminal
dir * | select -pr name, length | sort -de | out-file .\report_file.txt
get-content .\report_file.txt
dir * | select -pr name, length | sort -de | Out-GridView # spawns a GUI
dir * | select -pr name, length | sort -de | out-printer # to the default printer
dir * | select -pr name, length | sort -de | out-printer -name "other printer name"
```

## Administration

### Remote connexion

```
> Enable-PSRemoting
> enter-pssession dcname # connects to the Domain Controller `dcname`
[dcname]: > hostname # dcname
> enter-pssession dcname -credential (get-credential)
```
Hopping deactivated by default

### Remote cmdlets execution

```
Get-Service bits -computername dcname, pcname
invoke-command -computername pcname -scriptblock {Get-ChildItem c:\}
invoke-command -computername pcname -scriptblock {$env:computername} # remote computer name
```

### Sessions

```
New-PSSession dcname
Get-PSSession # get the session number
Enter-PSSession $some_session_number
$sessionvar = Get-PSSession pcname
```

### Import cmdlets

```
$dcsession = get-pssession -computername dcname
import-pssession -session $dcsession -module ActiveDirectory -Prefix somedcprefix
Get-somedcprefixADUser someADuser
get-aduser # NOT working without the prefix
Get-somedcprefixADUser -Filter * | select name
Remove-PSSession $dcsession
```


