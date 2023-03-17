# Brief
 
For this summative assignment, build a simple client/server network. Once the network is established, please complete the following tasks:
1.    Create a dictionary, populate it, serialize it and send it to a server.
2.    Create a text file and send it to a server.
 
With the dictionary, the user should be able to set the pickling format to one of the following: binary, JSON and XML. Also, the user will need to have the option to encrypt the text in a text file.
 
The server should have a configurable option to print the contents of the sent items to the screen and or to a file. Also, the server will need to be able to handle encrypted contents.
 
The client and server can be on separate machines or on the same machine.
 
Make sure that the code is written to PEP standard and uses exception handling to handle potential errors.
 
Write unit tests.
 
Upload the project to your source control website (aka GITHUB). Make sure that the commits have
messages that describe the changes.
 
Make sure the code is documented.
 
Your code submission should include your directory tree as well as code documentation. This should include as a minimum a Readme.md and requirements.txt as well as other documentation that you may see fit to include. In addition, the log of Github/GitLab push comments and code reviews should be included.
 
# Prereq
 
1. python (tested on 3.11)
 
# Setup
 
`pip install -r requirements.txt`
 
# to start the server
 
`python server.py --echo`
 
# to transfer a dict
 
`python client.py --base_url http://127.0.0.1:5000 dict --format xml`
 
# to send a file
 
`python client.py --base_url http://127.0.0.1:5000 file --file test-file.txt`
 
# PEP conversion
 
```sh
python -m autopep8 --in-place --aggressive --aggressive --recursive .
```
 
# PEP compliance
 
```
pep8 . --ignore=E501
```
 
# Some tests
 
```
python client.py --base_url http://127.0.0.1:5000 dict --format binary
python client.py --base_url http://127.0.0.1:5000 dict --format json
python client.py --base_url http://127.0.0.1:5000 dict --format xml
python client.py --base_url http://127.0.0.1:5000 dict
 
python client.py --encrypt --base_url http://127.0.0.1:5000 dict --format binary
python client.py --encrypt --base_url http://127.0.0.1:5000 dict --format json
python client.py --encrypt --base_url http://127.0.0.1:5000 dict --format xml
python client.py --encrypt --base_url http://127.0.0.1:5000 dict
 
python client.py --base_url http://127.0.0.1:5000 file --file test-file.txt
python client.py --encrypt --base_url http://127.0.0.1:5000 file --file test-file.txt
```

# Unit tests

`python -m pytest`
