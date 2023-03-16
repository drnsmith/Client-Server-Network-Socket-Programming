import os
import socket
import pickle
from cryptography.fernet import Fernet
from dict2xml import dict2xml

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

MAIN_DICTIONARY_PATH = "./../data/defaultDictionary.json"

USER_DICTIONARY_XML_PATH = "./../userDictionaries/dictionary.xml"
USER_DICTIONARY_JSON_PATH = "./../userDictionaries/dictionary.json"
USER_DICTIONARY_BIN_PATH = "./../userDictionaries/dictionary.bin"

# Function to connect with the server


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

# Function to encrypt files to the server


def encryptingFile(content):
    # generate a key for encryptio and decryption
    key = Fernet.generate_key()

    # Instance the Fernet class with the key
    fernet = Fernet(key)

    # Encrypting the content
    encMessage = fernet.encrypt(content)

    # Return the encrypted message
    return encMessage

# Function to send files to the server


def sendFileFunction(clientSocket, file_name, encrypt_content, save_method, type):

    # Defining the File Path
    if type == "text":
        filePath = f"./../data/{file_name}"

    if type == "dictionary":
        filePath = f"./../userDictionaries/{file_name}"

    # Calculating the file size
    fileSize = os.path.getsize(filePath)

    # Defining if it is encrypted or not
    contentFile = "ENCRYPTED" if encrypt_content else "TEXT"

    # Sending all the details about the file for the server
    clientSocket.send(
        f"{filePath}{SEPARATOR}{fileSize}{SEPARATOR}{contentFile}{SEPARATOR}{encrypt_content}{SEPARATOR}{save_method}".encode(FORMAT))

    # Opening the file and sending while it is reading the bytes
    with open(filePath, "rb") as file:
        while True:
            # Read the bytes from the file
            bytes_read = file.read(BUFFER_SIZE)

            if not bytes_read:
                # File transmitting is done
                break

            if encrypt_content == True:
                bytes_read = encryptingFile(bytes_read)

            # Use sendall to assure transimission in
            # busy networks
            clientSocket.sendall(bytes_read)

            # Closing the text file
            file.close()

            # Close the socket
            clientSocket.close()

            finalMessage = f"\nThe {file_name} was encrypted and sent to the server" if encrypt_content else f"The {file_name} was sent to the server"

            return print(finalMessage)

# Function to populate the dictionary


def addNewItemDictionary(newItem):
    with open(MAIN_DICTIONARY_PATH, 'r+') as dictonary:
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

# Function to show the dictionary


def showDictionary():
    with open(MAIN_DICTIONARY_PATH, 'r') as dictonary:
        data = json.load(dictonary)
        print(data)

# Function to serialise the dictionary


def serializingDictionary(type):

    # Openning the file the dictionary that users are been populating and picking up the data
    with open(MAIN_DICTIONARY_PATH, 'r+') as dictonary:
        # Reading all the content of the default dictionary
        defaultDictionary = json.load(dictonary)

    # Checking the type choosen by the user
    if type == "json":
        # Opening the user dictionary to serialise the file
        user_dictionary = open(USER_DICTIONARY_JSON_PATH, "w")

        # Writing the data from the populated dictionary and copying on the user dictionary
        json.dump(defaultDictionary, user_dictionary, indent=6)

        # Closing the user dictionary after copied the content
        user_dictionary.close()

    if type == "xml":
        # Converting the data from the dictionary into xml format
        xml_content = dict2xml(
            defaultDictionary, wrap='dictionary', indent="   ")

        # Opening the user dictionary to serialise the file
        user_dictionary = open(USER_DICTIONARY_XML_PATH, "w")

        # Writing the data from the populated dictionary and copying on the user dictionary
        user_dictionary.write(xml_content)

        # Closing the user dictionary after copied the content
        user_dictionary.close()

    if type == "binary":
        # Opening the user dictionary to serialise the file
        user_dictionary = open(USER_DICTIONARY_BIN_PATH, "wb")

        # Writing the data from the populated dictionary and copying on the user dictionary
        pickle.dump(defaultDictionary, user_dictionary)

        # Closing the user dictionary after copied the content
        user_dictionary.close()

    return print("\nSerialization completed. Check your file in the 'userDictionaries' folder.")

# Function to return all the comands available for users


def help():
    # Defining 'help'
    help_instructions = "Input 'sending-file' to send text file\n'new-item-dic' to add a new item in the dictionary\n'show-dic' to show the dictionary"
    return print(help_instructions)


if __name__ == "__main__":

    # Function to check if the user wrote the file name
    # Function needs to return true or false
    def checkingfile_name(inputFromUser):
        # Checking if the input of the file_name is blank or not
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

    # Function to check if the user is typing the correct input for the Sending Dictionary function
    def checkingSendingDictionary(inputFromUser):
        # Necessary to put ".lower()" function because user can type these two inputs in differnt ways
        match inputFromUser.lower():
            case "json" | "bin" | "xml":
                return True

            case _:
                print("Only 'json', 'xml' or 'bin' answers are available.")
                return False

    # Function to render the User Interface for the user decide what they would like to do.
    def userInterface(clientSocket):

        # First command after the client is connected with the server
        user_command = input(
            "\nEnter an input ('help' for all the commands): ")

        if user_command == "help":
            return help()

        # Creating a match system to create different cases for which input from the user
        # If the user need to send a file so it will necessary to validate if the user is sending the name of the file as well
        if user_command == "sending-file":

            # Declaring all the variables that it will be necessary to send to the sendFile Function
            file_name = ""
            encrypt_content = False
            save_method = ""

            # Asking for the file name for the user
            file_name_command = input(
                "\nPlease, input the name of the file: \n(The file should be located at the 'data' folder) \n")

            # Checking if their answer is valid or not
            if checkingfile_name(file_name_command) == False:
                return

            # If the file is not encrypted, so it is necessary to ask if the user would like to encrypt or not
            encrypt_content_command = input(
                "\nWould you like to encrypet your file?: (Yes/ No) \n")

            # Checking if their answer is valid or not
            if checkingYesOrNoAnswers(encrypt_content_command) == False:
                return

            # Asking if the user would like to save or print their results
            save_method_command = input(
                "\nHow do you like to save or print your final result? (print/ save) \n")

            # Checking if their answer is valid or not
            if checkingSaveMethod(save_method_command) == False:
                return

            # Declaring all the variables that it will be necessary to send to the sendFile Function
            type = "text"
            file_name = file_name_command
            save_method = save_method_command
            encrypt_content = True if encrypt_content_command.lower() == "yes" else False

            # Sending File function if the inputs from the user
            return sendFileFunction(clientSocket, file_name,
                                    encrypt_content, save_method, type)

        # Command to populate the dictionary
        if user_command == "new-item-dic":
            # Asking for the new item that will be implemented on the dictionary
            new_item = input(
                "\nAdd a new item to the dictionary: \n")

            return addNewItemDictionary(new_item)

        # Command to show the dictionary content
        if user_command == "show-dic":
            return showDictionary()

        # Command to send the dictionary to the server
        if user_command == "sending-dictionary":

            # Asking for which type of file the user would like to serialise
            format_dictionary = input(
                "\nWhich format you would like to serialise your dictionary? (json/ xml/ bin) \n")

            # Checking user input to see if matches with the options available
            if checkingSendingDictionary(format_dictionary) == False:
                return

            # Checking if the user wants to encrypt their dictionary
            encrypt_dictionary_command = input(
                "\nDo you like to encrypt your dictionary before sending to the server? (yes/ no) \n")

            # Checking if the user input is valid
            if checkingYesOrNoAnswers(encrypt_dictionary_command) == False:
                return

            # Asking if the user would like to save or print their results
            save_method_command = input(
                "\nHow do you like to save or print your final result? (print/ save) \n")

            # Checking if their answer is valid or not
            if checkingSaveMethod(save_method_command) == False:
                return

            # First, serialasing the dictionary
            serializingDictionary(format_dictionary)

            type = "dictionary"
            file_name = f"dictionary.{format_dictionary}"
            save_method = save_method_command
            encrypt_dictionary = True if encrypt_dictionary_command.lower() == "yes" else False

            # Second, sending to the server
            return sendFileFunction(clientSocket, file_name,
                                    encrypt_dictionary, save_method, type)

        # Returning if the user try to type a different command
        return print("Command incorrect. Please, try it again or type help to check the commands available.")

    clientSocket = socket.socket()

    if connectServe(clientSocket):
        userInterface(clientSocket)

    else:
        print("It was not possible to connect to the server. Please, try again.")
