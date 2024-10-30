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


---

# Building a Robust Client/Server Network with Socket Programming

## Introduction

In today's interconnected world, client/server networks form the backbone of communication between systems. This project provides a hands-on example of a **client/server network** using **Python's socket programming**. It demonstrates how to serialise and transfer data, along with options for encryption and configurable server-side processing.

Socket programming allows two systems to communicate by creating a dedicated connection. Here, we explore the design and features of a network where a client can create data, serialise it in various formats, and send it to a server that handles the data with customizable options.

---

## Project Overview

The goal of this project is to establish a reliable communication channel between a client and a server. It includes:

1. **Creating and serializing data** on the client side.
2. **Encrypting and transmitting text files** from client to server.
3. Allowing the **server to configure output options** like printing or saving data and decrypting encrypted files.

By combining these elements, we create a flexible and powerful network capable of transferring data securely and efficiently.

---

## Key Components

### 1. Data Serialization and Formats

Serialisation is essential in sending data across networks, as it converts structured data into a format suitable for transmission. This project supports three main serialisation formats:

- **Binary**: Ideal for compact, efficient data transfer.
- **JSON**: A popular format due to its human-readable structure.
- **XML**: Useful for applications that require document-like structures.

The client can set any of these formats before sending data, depending on the intended use or compatibility requirements.

### 2. Encryption and Decryption

Security is crucial when transmitting data, especially over networks. The client can encrypt text files before sending them to the server, which adds a layer of security. The server has the option to decrypt these files, ensuring data integrity and security on both ends.

### 3. Configurable Server Output

The server can be configured to handle incoming data in two ways:
- **Display on Console**: Allows for quick, real-time feedback on the incoming data.
- **Save to File**: Suitable for creating logs or storing data for later processing.

These options give the user control over data handling, allowing the network to be customised for different use cases.

---

## How It Works

The client-server network is built using **Python’s socket library**, which provides a low-level networking interface. 
A breakdown of the process:

1. **Establish Connection**: The client initiates a connection to the server, establishing a socket-based channel.
2. **Data Preparation and Serialization**: The client prepares a dictionary, populates it with data, and serialises it in the chosen format (binary, JSON, or XML).
3. **File Encryption and Transfer**: If encryption is enabled, the client encrypts a text file and sends it to the server.
4. **Server Processing**: The server receives the data, decrypts files if needed, and processes it according to the configured settings (display or save).
5. **Completion and Termination**: The connection closes once data transfer and processing are complete.

---

## Project Setup

### Prerequisites

- **Python** (tested on version 3.11)
- Additional dependencies listed in `requirements.txt`

To install the required packages, run:

```bash
pip install -r requirements.txt
```

