import socket, os.path, datetime, sys

def main():
    host = "local host"
    port = 50001

    s = socket.socket()
    s.connect((host, port))

    Filename = input("Type in ur file ")
    s.send(Filename.encode('utf-8'))
    s.shutdown(socket.SHUT_WR)
    data = s.recv(1024).decode('utf-8')
    print(data)
    s.close()

if __name__ == '__main__':
    main()
