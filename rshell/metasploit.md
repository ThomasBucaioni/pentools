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

```

