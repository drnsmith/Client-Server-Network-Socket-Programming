import os
import json
import socket
import pickle
from cryptography.fernet import Fernet
from dict2xml import dict2xml

# Return a string containing the hostname of the machine where the Python interpreter is currently executing.
HOST = socket.gethostbyname("localhost")

# Defining a common PORT for the Client and Server
PORT = 5050

# Declaring a variable with the HOST and PORT together
ADDR = (HOST, PORT)

# Default format for sending files
FORMAT = "utf-8"

# Defining the bufsize to send data from the socket
BUFFER_SIZE = 4096

# Defining a separator to send the file
SEPARATOR = "<SEPARATOR>"

# Defining the paths for the dictionaries
MAIN_DICTIONARY_PATH = "./../data/defaultDictionary.json"

USER_DICTIONARY_XML_PATH = "./../userDictionaries/dictionary.xml"
USER_DICTIONARY_JSON_PATH = "./../userDictionaries/dictionary.json"
USER_DICTIONARY_BIN_PATH = "./../userDictionaries/dictionary.bin"

# Function to connect with the server


def connect_serve(client_socket):
    try:
        # Connecting to the server
        client_socket.connect(ADDR)
        print('Connected.')
        return True
    except:
        # If it is not possible to connect to the server it will return an error message
        print('Connection failed.')
        return False

# Function to encrypt files to the server


def encrypting_file(content, encrypt_key):
    # Instance the Fernet class with the key
    fernet = Fernet(encrypt_key)

    # Encrypting the content
    encMessage = fernet.encrypt(content)

    # Return the encrypted message
    return encMessage

# Function to send files to the server


def send_file(client_socket, file_name, encrypt_content, save_method, file_type):

    # Defining the File Path
    # Needed to identify if it is a text file or the dictionary to change the paths to locate the files
    if file_type == "text":
        filePath = f"./../data/{file_name}"

    if file_type == "dictionary":
        filePath = f"./../userDictionaries/{file_name}"

    # Defining the file name
    file_name = os.path.basename(filePath)

    # Defining the var for the encrypt_key
    # It will be sent to the server as empty string if it is not necessary to decrypt the content
    encrypt_key = ""

    # Defining the encrypt key
    if encrypt_content == True:
        encrypt_key = Fernet.generate_key().decode(FORMAT)

    # Defining if content is encrypted or not
    content_encrypted = "ENCRYPTED" if encrypt_content else "TEXT"

    # Sending all the separate details of the file
    client_socket.send(
        f"{file_name}{SEPARATOR}{content_encrypted}{SEPARATOR}{save_method}{SEPARATOR}{encrypt_key}".encode(FORMAT))

    # Opening the file and sending while it is reading the bytes
    with open(filePath, "rb") as file:
        while True:
            # Read the bytes from the file
            bytes_read = file.read(BUFFER_SIZE)

            if not bytes_read:
                # File transmitting is done
                break

            # Starting the encrypting process for the content
            if encrypt_content == True:
                bytes_read = encrypting_file(bytes_read, encrypt_key)

            # Use sendall to assure transimission in
            # busy networks
            client_socket.sendall(bytes_read)

            # Closing the text file
            file.close()

            # Close the socket
            client_socket.close()

            # Printing the final message after sending a file to the server
            finalMessage = f"\nThe {file_name} was encrypted and sent to the server" if encrypt_content else f"The {file_name} was sent to the server\n"

            return print(finalMessage)

# Function to populate the dictionary


def add_new_item_dictionary(newItem):

    # Openening the dictionary from the user to add a new item
    with open(MAIN_DICTIONARY_PATH, 'r+') as dictonary:
        # Reading all the content of the json
        data = json.load(dictonary)

        # Adding a new item in the json file
        data[len(data)] = newItem

        # Set the pointer to the beginning (Sets the file's current position at the offset)
        dictonary.seek(0)

        # Converting a subset of Python objects into a json string.
        json.dump(data, dictonary, indent=4)

        # Removing remaining part
        dictonary.truncate()

    # Printing the final message
    print(f"\nItem added in the dictionary: {newItem}.")
    print("\nPlease check your dictionary: 'data/defaultDictionary.json'.")

# Function to clean the dictionary


def clean_dictionary():
    with open(MAIN_DICTIONARY_PATH, 'r+') as dictonary:
        # Adding a new item on the json file
        data = {}

        # Set the pointer to the beginning (Sets the file's current position at the offset)
        dictonary.seek(0)

        # Converting a subset of Python objects into a json string.
        json.dump(data, dictonary, indent=4)

        # Removing remaining part
        dictonary.truncate()

    print('\nDictionary cleaned.')

# Function to show the dictionary


def show_dictionary():
    # Opening the dictionary from the user and print it
    with open(MAIN_DICTIONARY_PATH, 'r') as dictonary:
        data = json.load(dictonary)
        print(data)

# Function to serialise the dictionary


def serializing_dictionary(type):

    # Opening the dictionary file that the user populated and picking up the data
    with open(MAIN_DICTIONARY_PATH, 'r+') as dictonary:
        # Reading all the content of the default dictionary
        defaultDictionary = json.load(dictonary)

    # Checking the file format choosen by the user
    if type == "json":
        # Opening the user dictionary to serialise the file
        user_dictionary = open(USER_DICTIONARY_JSON_PATH, "w")

        # Writing the data from the populated dictionary and copying on the user dictionary
        json.dump(defaultDictionary, user_dictionary, indent=2)

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

        # Closing the user dictionary after copying the content
        user_dictionary.close()

    if type == "bin":
        check_file_exists = os.path.isfile(USER_DICTIONARY_BIN_PATH)

        if check_file_exists == False:
            # Opening the user dictionary to serialise the file
            user_dictionary = open(USER_DICTIONARY_BIN_PATH, "w+")

        user_dictionary = open(USER_DICTIONARY_BIN_PATH, "wb")

        # Writing the data from the populated dictionary and copying on the user dictionary
        pickle.dump(defaultDictionary, user_dictionary)

        # Closing the user dictionary after copying the content
        user_dictionary.close()

    return print("\nSerialisation completed. Check your file in the 'userDictionaries' folder.")

# Function to return all the commands available for users


def help():
    # Defining 'help'
    help_instructions = "\n \
        [sending-file] to send text file\n \
        [new-item-dictionary] to add a new item in the dictionary\n \
        [clean-dictionary] serializing and sending a dictionary\n \
        [show-dictionary] to show the dictionary\n \
        [sending-dictionary] serialising and sending a dictionary\n"
    return print(help_instructions)


if __name__ == "__main__":

    # Function to check if the user wrote a file name
    # Function needs to return true or false
    def checking_file_name(input_from_user):
        # Checking if the input of the file_name is blank or not
        if len(input_from_user) == 0:
            print("\nBlank options are not available. Please, try again.")
            return False

        return True

    # Function to check if the user is typed YES or NO as an answer
    def checking_yes_or_no_answers(input_from_user):
        # Necessary to put ".lower()" function because user can type these two inputs in differnt ways
        match input_from_user.lower():
            case "yes" | "no":
                return True

            case _:
                print("\nOnly 'Yes' or 'No' answers are available.")
                return False

    # Function to check if the user is typing the correct input for the Sending File function ("print" or "save")
    def checking_save_method(input_from_user):
        # Necessary to put ".lower()" function because user can type these two inputs in different ways
        match input_from_user.lower():
            case "print" | "save":
                return True

            case _:
                print("\nOnly 'print' or 'save' answers are available.")
                return False

    # Function to check if the user is typing the correct input for the Sending Dictionary function
    def checking_sending_dictionary(input_from_user):
        # Necessary to put ".lower()" function because user can type these two inputs in different ways
        match input_from_user.lower():
            case "json" | "bin" | "xml":
                return True

            case _:
                print("\nOnly 'json', 'xml' or 'bin' answers are available.")
                return False

    # Function to render the User Interface for the user to decide what they would like to do.
    def user_interface(client_socket):

        # First command after the client is connected with the server
        user_command = input(
            "\nEnter an input ('help' for all the commands): ")

        if user_command == "help":
            return help()

        # Creating a match system to create different cases for which input from the user
        # If the user need to send a file so it will necessary to validate if the user is sending the name of the file as well
        if user_command == "sending-file":

            # Declaring all the variables that will be necessary to send to the sendFile Function
            file_name = ""
            encrypt_content = False
            save_method = ""

            # Asking for the file name from the user
            file_name_command = input(
                "\nPlease, input the name of the file: \n(The file should be located at the 'data' folder)\n")

            # Checking if their answer is valid or not
            if checking_file_name(file_name_command) == False:
                return

            # Ask if the user would like to encrypt or not
            encrypt_content_command = input(
                "\nWould you like to encrypt your file?: (Yes/ No)")

            # Checking if their answer is valid or not
            if checking_yes_or_no_answers(encrypt_content_command) == False:
                return

            # Asking if the user would like to save or print their results
            save_method_command = input(
                "\nWould you like to save or print your final result? (print/ save)")

            # Checking if their answer is valid or not
            if checking_save_method(save_method_command) == False:
                return

            # Declaring all the variables that it will be necessary to send to the sendFile Function
            type = "text"
            file_name = file_name_command
            save_method = save_method_command
            encrypt_content = True if encrypt_content_command.lower() == "yes" else False

            # Sending File function if the inputs from the user
            return send_file(client_socket, file_name,
                             encrypt_content, save_method, type)

        # Command to populate the dictionary
        if user_command == "new-item-dictionary":
            # Asking for the new item that will be implemented on the dictionary
            new_item = input(
                "\nAdd a new item to the dictionary:")

            return add_new_item_dictionary(new_item)

        # Command to show the dictionary content
        if user_command == "show-dictionary":
            return show_dictionary()

        # Command to clean the dictionary content
        if user_command == "clean-dictionary":
            return clean_dictionary()

        # Command to send the dictionary to the server
        if user_command == "sending-dictionary":

            # Asking for which type of file the user would like to serialise
            format_dictionary = input(
                "\nWhich format you would like to serialise your dictionary? (json/ xml/ bin)")

            # Checking user input to see if matches with the options available
            if checking_sending_dictionary(format_dictionary) == False:
                return

            # Checking if the user wants to encrypt their dictionary
            encrypt_dictionary_command = input(
                "\nDo you like to encrypt your dictionary before sending to the server? (yes/ no)")

            # Checking if the user input is valid
            if checking_yes_or_no_answers(encrypt_dictionary_command) == False:
                return

            # Asking if the user would like to save or print their results
            save_method_command = input(
                "\nWould you like to save or print your final result? (print/ save)")

            # Checking if their answer is valid or not
            if checking_save_method(save_method_command) == False:
                return

            # First, serialasing the dictionary
            serializing_dictionary(format_dictionary)

            type = "dictionary"
            file_name = f"dictionary.{format_dictionary}"
            save_method = save_method_command
            encrypt_dictionary = True if encrypt_dictionary_command.lower() == "yes" else False

            # Second, sending to the server
            return send_file(client_socket, file_name,
                             encrypt_dictionary, save_method, type)

        # Returning if the user typed a different command
        return print("\nCommand incorrect. Please try again or type help to check the available commands.")

    client_socket = socket.socket()

    if connect_serve(client_socket):
        user_interface(client_socket)

    else:
        print("\nIt was not possible to connect to the server. Please try again.")
