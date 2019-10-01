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

				print(client_conn.getpeername(), 'conectado')

				if not data:
					print(client_conn.getpeername(), 'disconectou-se')
					break
				elif data[:-1] == b'done':
					print('Esta avisando que imprimiu')
					#client_conn.send(b'print')
				elif data[:-1] == b'request':
					print('Esta pedindo para imprimir')
					clients[0].send(b'print')
				else:
					print('Nao reconhecido')
					print(data)
		except Exception as erro:
			print(erro)
			client_conn.close()

	def run(self):
		with socket.socket() as s: 
		    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
		    s.bind(('', 50007))
		    s.listen(5)
		    while True:
		        conexao, endereco = s.accept()
		        with clients_lock:
		        	clients.append(conexao)

		        print('Server conectado por', endereco)
		        threading.Thread(target=self.handle_client, args=(conexao,)).start() 

server = Server(10)
server.run()
