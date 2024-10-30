# Client/Server Network Project

### Project Overview
This project buiulds a **client/server network** where the client can:
1. Create a dictionary, populate it with data, serialise it, and send it to a server.
2. Create a text file, optionally encrypt it, and send it to the server.
   
The server, in turn, provides configurable options to:
- Display or store the content received from the client.
- Decrypt files if encryption is applied by the client.
- Work seamlessly across separate machines or on the same machine.

This project uses **socket programming** for establishing the client-server connection and provides flexibility in data format and encryption.

---

### Features
- **Serialisation Formats**: The client can choose between binary, JSON, and XML formats to serialise data.
- **Encryption**: Optionally encrypts text files on the client-side.
- **Decryption**: Server can decrypt the received file if encrypted.
- **Configurable Output**: The server can be configured to print the received data to the console or save it to a file.

---

### Prerequisites
This project was developed and tested with Python 3.11. Please ensure you have this version or newer.

---

### Setup

1. Clone this repository and navigate to the project directory.
2. Install the required libraries using:

```bash
   pip install -r requirements.txt
```

### Usage and Testing
## Running the Client and Server
- Start the server: Run the server script to start listening for incoming data.
- Run the client: Use the client script to send the serialised dictionary and text file.

## Testing
The project includes tests, which can be run using:
```
python -m unittest

```
The tests showcase assertions such as **assertIsInstance** to validate types and ensure robust functionality.

## Contributors
Natalya Smith, Patrick Bracebridge, Sanet Shepperson

We welcome contributions via pull requests. Please make sure to update tests as appropriate when making changes.

## License
This project is licensed under the MIT License.
