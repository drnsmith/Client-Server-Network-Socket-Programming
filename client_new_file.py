import socket
import pickle
from Crypto.Cipher import AES
import tqdm

# CREATE SOCKET
# AF_INET == ipv4
# SOCK_STREAM == TCP

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)
FORMAT= "utf-8"
SIZE = 1024

def main(): # Connecting
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    # Encrypting
    key = b"MyNameIsUnknown1" # setting the key
    nonce = b"MyNameIsUnknown2"

    cipher = AES.new(key, AES.MODE_EAX, nonce) # creating cipher

    name_of_file = client.recv(SIZE).decode()
    print(name_of_file)
    size_of_file = client.recv(SIZE).decode()
    print(size_of_file)


    # File transfer
    file = open(name_of_file, "wb") # writing, bytes mode
    done = False
    file_bytes = b"" # we don't know how much/big the file/data we are going to get, below is the while loop to account for this

    check = tqdm.tqdm(unit_divisor=1000, total=int(size_of_file))

        while not done:
            data = client.recv(SIZE)
            if bytes_in_file[-5:] == b"<END": # checking the size of the file in bytes
                done = True
            else:
                bytes_in_file += data
            check.update(SIZE)

    print(bytes_in_file)
    file.write(cipher.decrypt(bytes_in_file)) # to decrypt the incoming file


    # Pickling
        while True:
            full_msg = b'' # In bytes
                new_msg = s.recv(SIZE)# how big chunks of data at a time we want to receive
                if new_msg:
                    print("NEW MESSAGE length:", msg[:SIZE])
                    msg_len = int(msg[:SIZE])
                    new_msg = False
                print(f"Full MESSAGE length: {msg_len}")

                full_msg += msg_len
                print(len(full_msg))
                if len(full_msg) - SIZE == msg_len:
                    print("Full MESSAGE received.")
                    print(full_msg[SIZE:])
                    print(pickle.loads(full_msg[SIZE:]))
                    new_msg = True
                    full_msg = b""

    # Receiving files
        file = open("hello.txt", "r")
        data = file.read()
        client.send("hello.txt".encode(FORMAT))
        
        message = client.recv(SIZE).decode(FORMAT)
        print(f"SERVER: {message}")
        client.send(data.encode(FORMAT))

file.close()
client.close()
server.close()

if __name__ == "__main__":
    main()
