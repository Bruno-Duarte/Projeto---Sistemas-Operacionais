import socket, select, sys

class Client(object):

	def __init__(self, name):
		self.name = name

	def connect(self):
		with socket.socket() as s:
		    s.connect(('', 50007))
		    while True:
		        io_list = [sys.stdin, s]
		        ready_to_read,ready_to_write,in_error = select.select(io_list , [], [])   
		        if s in ready_to_read: 
		            data = s.recv(1024)
		            if not data:
		                break
		            print(data.decode())
		        else:
		            msg = sys.stdin.readline()
		            s.send(msg.encode())
		            sys.stdout.flush()

client = Client('Cliente')
client.connect()
