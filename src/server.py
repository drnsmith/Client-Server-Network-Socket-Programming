import socket

# Return a string containing the hostname of the machine where the Python interpreter is currently executing.
HOST = socket.gethostbyname('localhost')

# Defining a common PORT for the Client and Server
PORT = 5050

# Declaring a variable with the HOST and PORT together
ADDR = (HOST, PORT)

FORMAT = "utf-8"

BUFFER_SIZE = 4096


def main():
    server = socket.socket()
    server.bind(ADDR)
    server.listen()
    print("Server is listening...")

    while True:  # The infinite loop
        try:
            client_socket, address = server.accept()
            print(f"{address} is connected.")

            fileData = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
            fileContent = client_socket.recv(BUFFER_SIZE).decode(FORMAT)

            print(fileData)
            print(fileContent)

        except ConnectionAbortedError:
            print('Connection aborted. Server shutting down...')


if __name__ == "__main__":
    main()
