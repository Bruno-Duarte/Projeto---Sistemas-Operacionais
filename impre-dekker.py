import socket, select, sys, threading
from time import sleep
from random import randint as rand

class Printer(object):

	want_status = [False, False]
	turn = 1

	def __init__(self, name):
		self.name = name

	def pre_protocol(self):
		Printer.want_status[0] = True
		while True:
			if Printer.want_status[1]:
				if Printer.turn == 0:
					break
				Printer.want_status[0] = False
				while True:
					if Printer.turn == 0:
						break
			break
	    
	def critical_section(self):
		self.print_document()

	def post_protocol(self):
		Printer.want_status[0] = False
		Printer.turn = 1	

	def handle_server(self, data):
		if not data:
			return
		elif data == b'print':
			self.pre_protocol()
			self.critical_section()
			self.post_protocol()

	def print_document(self):
		print('Imprimindo documento...')
		t = rand(2, 10)
		sleep(t)
		print('Documento {} imprimiu em {}s'.format(threading.get_ident()*(-1), t))

def main():
	printer = Printer('Impressora')
	with socket.socket() as s:
		s.connect(('', 50007))
		while True:
			io_list = [sys.stdin, s]
			ready_to_read,ready_to_write,in_error = select.select(io_list , [], [])  
			if s in ready_to_read:
				data = s.recv(1024)
				thread = threading.Thread(target = printer.handle_server, args = (data, ))
				thread.start()
				thread.join()

if __name__ == '__main__':
	main()
          
