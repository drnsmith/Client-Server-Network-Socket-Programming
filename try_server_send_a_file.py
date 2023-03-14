import socket, os.path, datetime, sys

def main():
    host = "local host"
    port = 50001

    s = socket.socket()
    s.bind((host,port))
    print("SERVER Started")
    s.listen(2)
    while True:
        c, addr = s.accept()
        print("Connection from: " + str(addr))
        filename = ''
        while True:
            data = c.recv(1024).decode('utf-8')
            if not data:
                break
            filename += data
        print("from CLIENT: " + filename)
        myfile = open(filename, "rb")
        c.send(myfile.read())
        c.close()
        
    if __name__ == "__main__":
    main()
