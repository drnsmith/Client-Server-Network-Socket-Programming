import os
import socket
import tqdm

import json

# Return a string containing the hostname of the machine where the Python interpreter is currently executing.
HOST = socket.gethostbyname("localhost")

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


def sendFileFunction(clientSocket: socket.socket(), fileName, encryptedFile, encryptContent, saveMethod):

    # Defining the File Path
    filePath = f"./../data/{fileName}"

    # Calculating the file size
    fileSize = os.path.getsize(filePath)

    # Defining if it is encrypted or not
    contentFile = "ENCRYPTED" if encryptedFile else "TEXT"

    # Sending all the details about the file for the server
    clientSocket.send(
        f"{filePath}{SEPARATOR}{fileSize}{SEPARATOR}{contentFile}{SEPARATOR}{encryptContent}{SEPARATOR}{saveMethod}".encode(FORMAT))

    # Creating a progress bar on the client side to let the user aware about the process
    progress = tqdm.tqdm(range(
        fileSize), f"Sending {fileName}", unit="B", unit_scale=True, unit_divisor=1024)

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

            return print(f"The {fileName} was sent to the server")


def addNewItemDictionary(newItem):
    # Defining the Dic Path
    dictonaryPath = "./../data/dictionary.json"

    with open(dictonaryPath, 'r+') as dictonary:
        # Reading all the content of the json
        data = json.load(dictonary)

        # Adding a new item on the json file
        data[len(data)] = newItem

        # Set the pointer to the beginning (Sets the file's current position at the offset)
        dictonary.seek(0)

        # Converting a subset of Python objects into a json string.
        json.dump(data, dictonary, indent=4)

        # Removing remaining part
        dictonary.truncate()


def showDictionary():
    # Defining the Dic Path
    dictonaryPath = "./../data/dictionary.json"

    with open(dictonaryPath, 'r') as dictonary:
        data = json.load(dictonary)
        print(data)


if __name__ == "__main__":

    # Function to check if the user wrote the file name
    # Function needs to return true or false
    def checkingFileName(inputFromUser):
        # Checking if the input of the fileName is blank or not
        if len(inputFromUser) == 0:
            print("Blank options are not available. Please, try again.")
            return False

        return True

    # Function to if the user is typing YES or NO as an answer
    def checkingYesOrNoAnswers(inputFromUser):
        # Necessary to put ".lower()" function because user can type these two inputs in differnt ways
        match inputFromUser.lower():
            case "yes" | "no":
                return True

            case _:
                print("Only 'Yes' or 'No' answers are available.")
                return False

    # Function to check if the user is typing the correct input for the Sending File function ("print" or "save")
    def checkingSaveMethod(inputFromUser):
        # Necessary to put ".lower()" function because user can type these two inputs in differnt ways
        match inputFromUser.lower():
            case "print" | "save":
                return True

            case _:
                print("Only 'print' or 'save' answers are available.")
                return False

    # Function to render the User Interface for the user decide what they would like to do.
    def userInterface(clientSocket):

        # First command after the client is connected with the server
        userCommand = input("\nEnter an input ('help' for all the commands): ")

        # Creating a match system to create different cases for which input from the user
        # If the user need to send a file so it will necessary to validate if the user is sending the name of the file as well
        if userCommand == "sending-file":

            # Declaring all the variables that it will be necessary to send to the sendFile Function
            fileName = ""
            encryptedFile = False
            encryptContent = False
            saveMethod = ""

            # Asking for the file name for the user
            fileNameCommand = input(
                "\nPlease, inform the name of the file: \n(The file should be located at the 'data' folder) \n")

            # Checking if their answer is valid or not
            if checkingFileName(fileNameCommand) == False:
                return

            # Asking if the file that they would like to send is encrypted or not
            encryptedFileCommand = input(
                "\nYour file is encrypeted or not?: (Yes/ No) \n")

            # Checking if their answer is valid or not
            if checkingYesOrNoAnswers(encryptedFileCommand) == False:
                return

            # If the file is not encrypted, so it is necessary to ask if the user would like to encrypt or not
            if encryptedFileCommand.lower() == "no":
                encryptContentCommand = input(
                    "\nWould you like to encrypet your file?: (Yes/ No) \n")

                # Checking if their answer is valid or not
                if checkingYesOrNoAnswers(encryptContentCommand) == False:
                    return
            # Declaring that the content is encrypt
            else:
                encryptContentCommand = True

            # Asking if the user would like to save or print their results
            saveMethodCommand = input(
                "\nHow do you like to save or print your final result? (print/ save) \n")

            # Checking if their answer is valid or not
            if checkingSaveMethod(saveMethodCommand) == False:
                return

            # Declaring all the variables that it will be necessary to send to the sendFile Function
            fileName = fileNameCommand
            saveMethod = saveMethodCommand
            encryptedFile = True if encryptedFileCommand == "yes" else False
            encryptContent = True if encryptContentCommand == "yes" else False

            # Sending File function if the inputs from the user
            sendFileFunction(clientSocket, fileName,
                             encryptedFile, encryptContent, saveMethod)

        # Command to populate the dictionary
        if userCommand == "new-item-dic":
            # Asking for the new item that will be implemented on the dictionary
            newItem = input(
                "\nAdd a new item to the dictionary: \n")

            return addNewItemDictionary(newItem)

        if userCommand == "show-dic":
            return showDictionary()

        # Returning if the user try to type a different command
        return print("Command incorrect. Please, try it again or type help to check the commands available.")

    clientSocket = socket.socket()

    if connectServe(clientSocket):
        userInterface(clientSocket)

    else:
        print("It was not possible to connect to the server. Please, try again.")
