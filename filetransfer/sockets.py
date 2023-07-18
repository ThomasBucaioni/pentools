# Clients and servers

source: "Black Hat Python", Justin Seitz and Tim Arnold

## TCP

### Client

```
import socket

target_host = "www.google.com"
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))

client.send(b'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n')

response = client.recv(1024) # 2048, 4096

print(response.decode())
client.close()


