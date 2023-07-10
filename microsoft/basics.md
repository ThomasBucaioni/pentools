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



```

