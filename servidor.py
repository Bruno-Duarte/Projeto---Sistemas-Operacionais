import socket, threading
from os import system

connections = {}
clients_lock = threading.Lock()


class Server(object):

	def __init__(self, capacity):
		self.capacity = capacity
                                                                       
	def handle_client(self, client_conn):
		try:
			while True:
				data = client_conn.recv(1024)
				if not data:
					print(client_conn.getpeername(), 'disconectou-se')
					break
				elif b'client' in data[0:9]:
					print('requisição de {}'.format(client_conn.getpeername()))
					connections[client_conn.getpeername()[1]][1] = True
					if b'request' in data[10:19]:
						if self.printer_available():
							conn = self.find_printer()
							conn.send(b'print')
						else:
							msg = 'Não há impressora disponível, execute "impressora.py"'.encode('utf-8')
							connections[client_conn.getpeername()[1]][0].send(msg)
					else:
						print('Não reconhecido!')
				else:
					print('Não reconhecido!')
		except Exception as erro:
			print(erro)
			client_conn.close()	

	def run(self):
		with socket.socket() as s: 
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                          
			s.bind(('', 50007))
			s.listen(self.capacity)
			while True: 
				connection, address = s.accept()
				with clients_lock:
					connections[address[1]] = []
					connections[address[1]].append(connection)
					connections[address[1]].append(False)
				print('Server conectado por', address)
				threading.Thread(target=self.handle_client, args=(connection,)).start()

	def printer_available(self):
		for key in connections:
			if not connections[key][1]:
				return True
		return False

	def find_printer(self):
		for key in connections:
			if not connections[key][1]:
				return connections[key][0]

	                                                                       
if __name__ == "__main__":
	server = Server(4)
	server.run()
