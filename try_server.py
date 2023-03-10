'''
Socket programming, see, 
https://www.geeksforgeeks.org/python-network-programming/
'''

import socket
import pickle


 HOST = socket.gethostbyname(socket.gethostname())
 PORT = 5050
 ADDR = (HOST, PORT)
 FORMAT = "utf-8"
 SIZE = 1024

'''
Need to try:
except Error below
'''


 def main():
 #   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     server = socket.socket() # create the socket this way or as above
     print("Socket is created.")
     server.bind(ADDR) # binding the socket
     server.listen(5) # listens for 5 secs.
     print("LISTENING: Listening/Waiting for clients to connect...")

     while True:
#see, https://stackoverflow.com/questions/2729543/is-a-server-an-infinite-loop-running-as-a-background-process#:~:text=A%20server%20is%20simply%20something%20that%20%22loops%20forever%22%20and%20serves.=
         
         conn, addr = server.accept() # establishing connection
         print(f"NEW CONNECTION from {ADDR} is established.")
    
'''For pickle, see 
https://snyk.io/blog/guide-to-python-pickle/
'''
    
    

# First, encryption, as pickled files not safe, i.e. write the code and place it here
# Then pickling or encrypt a pickled file nstead

# Pickling below
# Dictionary
d = {1: "o", 2: "t", 3: "t", 4: "f"}

# To pickle
pickle.dump(d, open('file_send.p', 'wb'))
# print(d)

## To de-pickle
#d = pickle.load(open("file_send.p", "rb"))
#print(d)

''' See, https://pythonprogramming.net/python-pickle-module-save-objects-serialization/
#:~:text=First%2C%20import%20pickle%20to%20use,into%20opened%20file%2C%20then%20close.&text=Use%20pickle.,-load()%20to
'''
# Below also works
#
# msg = pickle.dumps(d)
# msg = bytes(f"{len(msg): < {SIZE}}", FORMAT) + msg
# print(msg)
# conn.send(f"RECEIVED: {msg} .")

'''Encryption, see documentation here: https://pycryptodome.readthedocs.io/en/latest/src/cipher/cipher.html
#https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/
'''


from cryptography.fernet import Fernet

'''
Need to try:
except Error below
'''
def new_file(file):
#    d = {1: "o", 2: "t", 3: "t", 4: "f"}

# key generation
key = Fernet.generate_key()


if __name__ == "__main__":
main()
