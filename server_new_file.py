import socket
import pickle
from Crypto.Cipher import AES
import tqdm

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050 # use any appropriate/unused
ADDR = (HOST, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("LISTENING: SERVER is listening...")

    while True: # The infinite loop
        conn, addr = server.accept()
        print(f"NEW CONNECTION from {addr} is established.")

        d = {1: "Hello", 2:"there!"}# create dic, populate and serialise it (using pickling).
        msg = pickle.dumps(d)
        msg = bytes(f"{len(msg): < {SIZE}}", FORMAT) + msg
        print(msg)
        conn.send(f"RECEIVED: {msg} .")

        file_name = conn.recv(SIZE).decode(FORMAT)
        print("RECEIVED: File.")
        file = open(file_name, "w")
        conn.send("RECEIVED: FILE NAME.".encode(FORMAT))

        data = conn.recv(SIZE).decode(FORMAT)
        print(f"File data received.")
        file.write(data)
        conn.send("RECEIVED: FILE DATA.".encode(FORMAT))

#Encryption

    key = b"MyNameIsUnknown1"  # setting the key
    nonce = b"MyNameIsUnknown2"

    cipher = AES.new(key, AES.MODE_EAX, nonce)  # creating cipher
    size_of_file = os.path.getsize("file")  # calculating file size we want to send

    with open("hello", "rb") as f:
        data = f.read()  # loading data of the file in the form of bytes

        encrypted = cipher.encrypt(data)  # encrypting these data and
        client.send("hello.txt".encode())  # sending the name of the file that is going to be transmited
        client.send(str(size_of_file).encode())  # sending file size
        client.sendall(encrypted)  # sending all the encypted data
        client.send(b"<END")  # telling that the file was sent fully
        client.close()  # close communication

        file.close()
        conn.close()
        server.close()
        client.close()
        print(f"DISCONNECTED: {addr} disconnected.")

if __name__ == "__main__":
    main()
