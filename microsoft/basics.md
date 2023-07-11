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

listdlls
listdlls -u # unsigned

set PATH=%PATH%;C:\Users\myuser\Downloads\SysinternalsSuite

dir /s *somefile*

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


```

