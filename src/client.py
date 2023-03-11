import os
import socket
import tqdm

# Return a string containing the hostname of the machine where the Python interpreter is currently executing.
HOST = socket.gethostbyname('localhost')

# Defining a common PORT for the Client and Server
PORT = 5050

# Declaring a variable with the HOST and PORT together
ADDR = (HOST, PORT)

# Default format for sending files
FORMAT = "utf-8"

# Defining the bufsize to receive data from the socket
BUFFER_SIZE = 4096

# Defining a separator to send the file
SEPARATOR = "<SEPARATOR>"


def connectServe(clientSocket):
    try:
        # Connecting to the server
        clientSocket.connect(ADDR)
        print('Connected.')
        return True
    except ConnectionRefusedError:
        # If it is not possible to connect to the server it will return an error message
        print('Connection failed.')
        return False


def helpUser():
    return print("test help user")


def sendFileFunction(clientSocket: socket.socket(), filename, encrypted):

    # Defining the File Path
    filePath = f"./../data/{filename}"

    # Calculating the file size
    fileSize = os.path.getsize(filePath)

    # Defining if it is encrypted or not
    contentFile = "ENCRYPTED" if encrypted else "TEXT"

    # Sending all the details about the file for the server
    clientSocket.send(
        f"{filePath}{SEPARATOR}{fileSize}{SEPARATOR}{contentFile}".encode(FORMAT))

    # Creating a progress bar on the client side to let the user aware about the process
    progress = tqdm.tqdm(range(
        fileSize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    # Opening the file and sending while it is reading the bytes
    with open(filePath, "rb") as file:
        while True:
            # Read the bytes from the file
            bytes_read = file.read(BUFFER_SIZE)
            if not bytes_read:
                # File transmitting is done
                break

            # Use sendall to assure transimission in
            # busy networks
            clientSocket.sendall(bytes_read)
            # Update the progress bar
            progress.update(len(bytes_read))

            # Closing the text file
            file.close()

            # Close the socket
            clientSocket.close()

            return print(f"The {filename} was sent to the server")


if __name__ == "__main__":
    client_socket = socket.socket()

    # Function to check if the user implemented
    # Function needs to return true or false
    def checkingUserParameter(inputsFromUser):

        # Checking if the length is bigger than one
        if (len(inputsFromUser) == 2):
            return True

        # Print message to remember the user to write the file name
        print("Please provide the name of the file that you would like to send.")
        return False

    if connectServe(client_socket):

        # First command after the client is connected with the server
        userCommand = input("Enter an input ('help' for all the commands): ")

        # Split the inputs from the user command to pickup the file name
        # example: inputsFromUser[0] is "sending-file" and inputsFromUser[1] is the <FILENAME>
        inputsFromUser = userCommand.split(" ")

        # Creating a match system to create different cases for which input from the user
        # If the user need to send a file so it will necessary to validate if the user is sending the name of the file as well
        match inputsFromUser[0]:

            # Sending the file to the server
            case "sending-file":
                # Validation to check the file name
                if (checkingUserParameter(inputsFromUser)):
                    sendFileFunction(client_socket, inputsFromUser[1], False)

            # Sending an encrypted file to the server
            case "sending-file-encrypted":

                # Validation to check the file name
                if (checkingUserParameter(inputsFromUser)):
                    sendFileFunction(client_socket, inputsFromUser[1], True)

            # List of the commands that users will be able to use
            case "help":
                helpUser()

            # Any other input, will return the error message
            case _:
                print(
                    "Command incorrect. Please, try it again or type help to check the commands available.")

    else:
        print("It was not possible to connect to the server. Please, try again.")
