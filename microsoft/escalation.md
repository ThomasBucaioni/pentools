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
Get-ItemProperty "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" | select displayname
```

### Processes

```
Get-Process
```


