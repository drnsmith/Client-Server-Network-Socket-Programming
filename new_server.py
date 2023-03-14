import socket, pickle, os

print("Server is Listening.....")
host = 'localhost'
port = 5050

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)

data = conn.recv(4096)
data_variable = pickle.loads(data)
conn.close()
print(data_variable)
print('Dictionary sent to CLIENT')
s.close()
