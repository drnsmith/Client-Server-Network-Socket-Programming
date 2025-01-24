### **Secure Communication Framework: Client-Server System with Python and Cryptography**

#### **Overview**
This project builds a **client/server network** where the client can:
1. Create a dictionary, populate it with data, serialise it, and send it to a server.
2. Create a text file, optionally encrypt it, and send it to the server.

The server, in turn, provides configurable options to:
- Display or store the content received from the client.
- Decrypt files if encryption is applied by the client.
- Work seamlessly across separate machines or on the same machine.

The project uses **Python’s socket programming** to establish a reliable communication channel, with added flexibility in data formats and encryption options.

---
#### **Key Features**
- **Serialization Formats**:  
  Supports binary, JSON, and XML formats for data serialisation.
- **Encryption and Decryption**:  
  Optional encryption on the client-side for text files, with server-side decryption capability.
- **Configurable Output**:  
  Server can print received data to the console or save it to a file.
- **Interoperability**:  
  Works across local or remote machines.

---

#### **Motivation**
In a world reliant on interconnected systems, client/server networks play a crucial role in data exchange. This project demonstrates:
- Practical use of **Python's socket programming** for real-world communication.
- Secure data transmission using encryption.
- Flexible server-side configurations for customised data handling.

---
### **How It Works**

1. **Establish Connection**:  
   The client initiates a connection to the server using Python’s socket library.
2. **Data Preparation and Serialization**:  
   The client prepares a dictionary, serialises it in a chosen format (binary, JSON, or XML), and sends it to the server.
3. **File Encryption and Transfer**:  
   If enabled, the client encrypts a text file before transmission.
4. **Server Processing**:  
   The server receives the data, decrypts files if needed, and either displays the content or saves it.
5. **Completion and Termination**:  
   The connection is closed after the transfer and processing are complete.

---
### **Setup**

#### Prerequisites
- **Python**: Tested with version 3.11.
- Install required libraries by running:
```bash
  pip install -r requirements.txt
```
### Running the Client and Server
 1. **Start the server:**
 - Run the server script to begin listening for incoming data.

```bash
python server.py
```
2. **Run the client:**
 - Use the client script to send data to the server.

```bash
python client.py
```
### Testing
This project includes unit tests to ensure functionality. Run the tests using:
```bash
python -m unittest
```

### Project Structure
 - `client.py`: Handles data creation, serialisation, and transmission from the client to the server.
 - `server.py`: Processes incoming data from the client and handles encryption/decryption.
 - `requirements.txt`: Lists required Python libraries.
 - `tests/`: Contains unit tests for validating core functionalities.

### Contributors
Natalya Smith; Patrick Bracebridge; Sanet Shepperson
Contributions are welcome! If you have ideas or improvements to share, please follow these steps:

1. **Fork the Repository:**
Create your own copy of the repository by clicking the "Fork" button at the top right of this page.

2. **Create a Feature Branch:**
Work on your changes in a dedicated branch.

```bash
git checkout -b feature/YourFeatureName
```
3. **Commit Your Changes:**
Write clear and concise commit messages explaining what you’ve done.

```bash
git commit -m "Add YourFeatureName"
```
4. **Push Your Changes**:
Push your feature branch to your forked repository.
```bash
git push origin feature/YourFeatureName
```
5. **Open a Pull Request**:
Submit your changes to the main repository by opening a pull request (PR). Ensure your PR description explains your changes clearly.

6. **Review and Feedback**:
We will review your PR and may suggest improvements before merging it into the main branch.

Thank you for your interest in contributing!

### License
This project is licensed under the MIT License. See the LICENSE file for details.

