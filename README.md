# Brief
This project builds a client/server network. 
1. A dictionary is created, populated, serialised and sent to a server (or user).
2. A text file is created and sent to a server.
# The execution of the project
* This project has two parts.
* First part of this project is coded using socket programming.
* Second part of this project uses Flask as a framework for this application. 
* For reasoning, see report. 
# Results
* Both parts achieve equal result.
* The client (user) can set the pickling format to binary, JSON and XML; and encrypt the text file.
* The server has a configurable option to print the contents of the sent items to the screen and or to a file; and to decrypt files.
* The built network works on both, the separate and same machine.
# Prereq
``` 
python (tested on 3.11)
 ```
# Setup for the application that uses socket
ADD HERE ACCORDINGLY BELOW
```
pip install -r requirements.txt
```
# Setup for the application built with Flask
```
pip install -r requirements_flask.txt
```
 
* to start the server
 
```
python server.py --echo
```
 
* to transfer a dictionary
 
```
python client.py --base_url http://127.0.0.1:5000 dict --format xml
```
 
* to send a file
 
```
python client.py --base_url http://127.0.0.1:5000 file --file test-file.txt
```
 
* PEP conversion
 
```sh
python -m autopep8 --in-place --aggressive --aggressive --recursive .
```
 
* PEP compliance
 
```
pep8 . --ignore=E501
```
# Testing

cProfile is showcased
assertIsInstance is showcased


With socket programming, we tested code using:
```
python -m unittest
``` 

For the Flask applicaiton, we tested using:

```
python -m pytest
```
# Some tests with Flask:
```
python client.py --base_url http://127.0.0.1:5000 dict --format binary
python client.py --base_url http://127.0.0.1:5000 dict --format json
python client.py --base_url http://127.0.0.1:5000 dict --format xml
python client.py --base_url http://127.0.0.1:5000 dict```
```
# Contributing
Patrick Bracebridge;
Sanet Shepperson;
Dr. Natalya Smith

Pull requests are welcome. 
Please update tests as appropriate. 
# License
This project is MIT licensed.
UNLESS YOU WANT TO USE A DIFFERENT ONE
# References
See notes within code. 
