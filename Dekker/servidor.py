import socket, threading
from os import system

clients = []
clients_lock = threading.Lock()

count = 0

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
				elif data[:-1] == b'request':
					global count
					count += 1
					print(client_conn.getpeername(), end='')
					print(' esta pedindo para imprimir')
					if count <= 2:
						clients[0].send(b'print')
					else:
						client_conn.send(b'Impressora ocupada!')
						count -= 3
				else:
					print('Nao reconhecido')
		except Exception as erro:
			print(erro)
			client_conn.close()

	def run(self):
		with socket.socket() as s: 
		    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                          
		    s.bind(('', 50007))
		    s.listen(2)
		    while True: # aceitar todas as conexoes que possam vir
		        connection, address = s.accept() # a espera de conexao
		        with clients_lock:
		        	clients.append(connection)
		        print('Server conectado por', address)
		        threading.Thread(target=self.handle_client, args=(connection,)).start()
	                                                                       
if __name__ == "__main__":
	server = Server(2)
	server.run()
