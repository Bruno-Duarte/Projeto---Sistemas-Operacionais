import socket, select, sys

def menu():
	print('1. Imprimir')
	print('2. Sair\n')

class Client(object):
	def __init__(self, name):
		self.name = name

	def connect(self):
		with socket.socket() as s:
		    s.connect(('', 50007))
		    menu()
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
		        	try:
		        		msg = int(msg)
		        		if msg == 1:
			        		s.send('request\n'.encode())
			        		sys.stdout.flush()
			        	else:
			        		break
		        	except Exception as erro:
		        		print(erro)

if __name__ == "__main__":
	client = Client('Cliente')
	client.connect()
