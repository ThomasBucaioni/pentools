# Escalation

## Info

### Users

```
whoami
whoami /priv
whoami /groups
net user
get-localuser
```

### Groups

```
Get-LocalGroup
Get-LocalGroupMember somegroup
```

### System

Windows versions: https://en.wikipedia.org/wiki/List_of_Microsoft_Windows_versions#/media/File:Windows_Version_History.svg
```
ver
systeminfo
```

### Network

```
ipconfig
ipconfig /all
route print
netstat -ano
```

### Programs

Invoke-command: https://devblogs.microsoft.com/scripting/use-powershell-to-find-installed-software/
```
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |  Select-Object DisplayName, DisplayVersion, Publisher, InstallDate |
Format-Table -AutoSize
Get-ItemProperty "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" | select displayname
```
Registry keys: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.3
```
Get-ChildItem -Path HKLM:\HARDWARE
```

### Processes

source: https://stackoverflow.com/questions/31374644/get-process-location-path-using-powershell
```
Get-Process
Get-Process -name someprocess |  % { $_.Path + " " + $_.Id}
Get-Process | Select-Object Path
Get-Process | Select-Object -ExpandProperty Path
Get-Process | ForEach-Object {$_.Path}
(Get-Process -Name someprocess).path
(Get-Process -Id someid).path
```

## Other searches

### Files

```
Get-ChildItem -Path C:\ -Include *.extension -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\*.txt -Recurse -Force
Get-ChildItem -Path C:\xampp -Include *.txt,*.ini -File -Recurse -ErrorAction SilentlyContinue | select-object name
```

### History
```
Get-History
(Get-PSReadlineOption).HistorySavePath
