import socket, select, sys

from src.interface.menus import main_menu, draw_line


class Client(object):

	def __init__(self, name):
		self.name = name

	def connect(self):
		with socket.socket() as s: 
			s.connect(('', 50007))
			while True:
				main_menu()
				io_list = [sys.stdin, s]
				ready_to_read, ready_to_write, in_error = select.select(io_list , [], [])   
				if s in ready_to_read:
					data = s.recv(1024)
					if not data:
						break
					print(data.decode())
				else:
					option = sys.stdin.readline()
					try:
						option = int(option)
						if option == 1:
							s.send('client    request   \n'.encode())
							sys.stdout.flush()
						elif option == 2:
							draw_line()
							break
						else:
							draw_line()
							print('Opção inválida!')
					except Exception as erro:
						print(erro)
						

if __name__ == '__main__':
	client = Client('Cliente')
	try:
		client.connect()
	except ConnectionRefusedError:
		print('Servidor não encontrado, execute o arquivo "servidor.py"')
		
