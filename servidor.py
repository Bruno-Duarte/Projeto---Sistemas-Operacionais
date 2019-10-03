import socket, threading
from os import system

clients = []
clients_lock = threading.Lock()

class Server(object):
	def __init__(self, capacity):
		self.capacity = capacity

	@staticmethod                                                                        
	def handle_client(client_conn):
		try:
			while True:
				data = client_conn.recv(1024)
				if not data:
					print(client_conn.getpeername(), 'disconectou-se')
					break
				elif data[:-1] == b'done':
					print('Esta avisando que imprimiu')
				elif data[:-1] == b'request':
					print(client_conn.getpeername(), end='')
					print(' esta pedindo para imprimir')
					clients[0].send(b'print')
				else:
					print('Nao reconhecido')
		except Exception as erro:
			print(erro)
			client_conn.close()

	def run(self):
		with socket.socket() as s:
		    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                                                        
		    s.bind(('', 50007))
		    s.listen(10)
		    while True:
		        connection, address = s.accept()
		        with clients_lock:
		        	clients.append(connection)

		        print('Server conectado por', address)
		        threading.Thread(target=self.handle_client, args=(connection,)).start()  
	                                                       
if __name__ == "__main__":
	server = Server(10)
	server.run()
