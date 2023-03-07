import socket
import pickle
# from Crypto.Cipher import AES
import tqdm

# CREATE SOCKET
# AF_INET == ipv4
# SOCK_STREAM == TCP


HOST = socket.gethostbyname(socket.gethostname())
PORT = 1212
ADDR = (HOST, PORT)
FORMAT= "utf-8"
SIZE = 1024

def main():
# Connecting
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
# Encrypto
key = b"MyNameIsUnknown1" # setting the key
nonce = b"MyNameIsUnknown2"

cipher = AES.new(key, AES.MODE_EAX, nonce) # creating cipher

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((HOST, PORT)) # this is not a multi-threader receiver; it's only accept 1 connection

# server.listen()
# client, addr = server.accept()

name_of_file = client.recv(1024).decode()
print(name_of_file)
size_of_file = client.recv(1024).decode()
print(size_of_file)


file = open(name_of_file, "wb") # wrting bytes mode
done = False
file_bytes = b"" # we don't know how much/big file we are going to get, below is the while loop to account for this

check = tqdm.tqdm(unit_divisor=1000, total=int(size_of_file))
while not done:
    data = client.recv(1024)
    if bytes_in_file[-5:] == b"<END":
        done = True
    else:
        bytes_in_file += data
    check.update(1024)

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