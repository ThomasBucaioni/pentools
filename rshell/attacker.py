import socket

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 4444))
    s.listen(1)

    print('-- Listening on port 4444')

    conn, addr = s.accept()

    print('-- Connection accepted from', addr)

    while True:
        command = str(input("cmd_prompt> "))
        #print('Type: ', type(command))
        #print('Command: ', command)
        if 'terminate' in command:
            conn.send(bytes('terminate', 'utf-8'))
            conn.close()
            break
        else:
            conn.send(command.encode('utf-8'))
            print(conn.recv(1024).decode('utf-8'))

def main():
    connect()

main()
