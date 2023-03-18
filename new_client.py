import socket, pickle
import unittest  # Testing
from processdata import ProcessData

host = 'localhost'
port = 5050
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Create a socket connection.
s.connect((host, port))

def test_pickle_object(self):  #test that pickle gives a data_string
  var = ProcessData()
  data_string = pickle.dumps(var)
  self.assertIsInstance(data_string, bytes)
  
var = ProcessData()# Create an instance of ProcessData() to send to server.
data_string = pickle.dumps(var)# Pickle the object and send it to the server
s.send(data_string)

s.close()
print('DATA sent to SERVER.')

if__name__== '__main__':  
   unittest.main()
