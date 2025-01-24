import os
import socket
from cryptography.fernet import Fernet

# Return a string containing the hostname of the machine where the Python interpreter is currently executing.
HOST = socket.gethostbyname("localhost")

# Defining a common PORT for the Client and Server
PORT = 5050

# Declaring a variable with the HOST and PORT together
ADDR = (HOST, PORT)

# Default format for receiving files
FORMAT = "utf-8"

# Defining the bufsize to receive data from the socket
BUFFER_SIZE = 4096

# Defining a separator to send the file
SEPARATOR = "<SEPARATOR>"

# Function to encrypt files to the server
# Receiving the content as 'content_received' from the client
# Receiving the key received from the client to decrypt


def decryptingFile(content_received, encrypt_key):
    # Printing status of the decrypting process
    print('\nYour file is encrypted. ')
    print('\nDecryption process began... ')

    # Getting the key for the decrypting
    # Need to convert into bytes by using encode() function
    key = encrypt_key.encode(FORMAT)

    # Instance the Fernet class with the key
    fernet = Fernet(key)

    # Decrypting the content
    decMessage = fernet.decrypt(content_received)

    # Priting status as done!
    print('\nDecryption process finished.')
    # Return the decrypted message
    return decMessage

# Function to print the content from the file received


def printing_content(content):
    # Checking if the file is binary or not
    try:
        # Converting the content received to a string by using decode function
        content_file = content.decode(FORMAT)

        # Printing the content for the user
        print('\nThe content of the file is:\n')
        print(f'{content_file}\n')

    # Dealing with the error if the file is a binary
    except UnicodeDecodeError:
        return print('Binary content can not be printed out on the screen. Please, consider to save the binary file instead.')

# Function to save files
# It is receiving the content as bytes and path as string with the location of where the file will be created or uploaded


def saving_file(content, path):

    # Printing the initial status
    print('\nSaving process began:\n')

    # Checking if the file exists
    check_file_exists = os.path.isfile(path)

    # Creating a file if the file does not exists from the "path"
    if check_file_exists == False:
        # Need to be "w" parameter to create a new file

        new_file = open(path, "w")

    # Opening the file
    new_file = open(path, "wb")

    # Writing the data from the content received as a parameter
    new_file.write(content)

    # Closing the new file
    new_file.close()

    # Printing the status for the user and showing where is located their new file
    return print(f'Your file as saved at: {path}\n')

# Function to deal with the connetion with the client


def connection_client():

    # Main functions from socket library to create a server
    server = socket.socket()
    server.bind(ADDR)
    server.listen()
    print("Server is listening...")

    while True:  # The infinite loop
        try:
            # Checking if the client will connect with the server
            client_socket, address = server.accept()

            # Priting status for the user
            print(f"{address} is connected.")

            # Receiving the main information related to the file received
            file_received = client_socket.recv(BUFFER_SIZE).decode(FORMAT)

            # Receiving the content file from the client
            content_received = client_socket.recv(BUFFER_SIZE)

            # Priting the status for the user
            # Checking if the file was received
            if file_received:
                print(f'\nFile received!')

            # Spliting the details from the file with the function "split()"
            file_rec_name, file_encrypted, file_rec_save_method, file_rec_encrypt_key = file_received.split(
                SEPARATOR)

            # Checking if the file is encrypted or not
            # If the file is encrypted, it will be necessary to decrypt
            # So, it was necessary to send the content and the key received from the client side
            if file_encrypted == "ENCRYPTED":
                content_received = decryptingFile(
                    content_received, file_rec_encrypt_key)

            # Checking if the user would like to see their content on the screen
            if file_rec_save_method == "print":

                # Returning the function to print the content
                return printing_content(content_received)

            # Checking if the user would like to save their content
            if file_rec_save_method == "save":

                # Defining the folder that will save the new files
                path_files_save = f"./savedFiles/{file_rec_name}"

                # Calling the saving function
                # Sending the content received from the client side
                # Sending the path defined before
                return saving_file(content_received, path_files_save)

        # Dealing with errors and print a message for the user
        except:
            return print('\nConnection aborted. Server shutting down...')


if __name__ == "__main__":
    connection_client()
