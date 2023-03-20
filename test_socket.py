import unittest

s = socket.socket()
HOST = 'local host'
PORT = 5050
try:
    socket.connect((HOST, PORT)) 
except Exception as e: 
    print("Something's wrong with %s:%d. Exception is %s" % (HOST, PORT, e))
finally:
    socket.close()


class SocketTest1(unittest.TestCase):

    def setUp(self): # see https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.PORT = test_support.bind_PORT(self.server)
        self.server.listen(2)

    def tearDown(self):
        self.server.close()
        self.server = None

class SocketTest2(unittest.TestCase):
    def setUp(self):
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(('', PORT))

    def tearDown(self):
        client_socket.close()

    def test_1(self):
        client_socket.send('message1'.encode())
        self.assertEqual(client_socket.recv(1024).decode(), 'reply1')

    def test_2(self):
        client_socket.send('message2'.encode())
        self.assertEqual(client_socket.recv(1024).decode(), 'reply2')

if __name__ == '__main__':
    unittest.main()
