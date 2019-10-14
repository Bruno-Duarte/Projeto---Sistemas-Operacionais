import socket, select, sys, threading, queue
from time import sleep
from random import randint as rand

BUFFER_SIZE = 2
MAX_UNIV_COUNT = 1000

doc_count = 0
univ_count = 0

buffer = queue.Queue(BUFFER_SIZE)

flag = [False, False]
turn = 0

class Printer(object):

	def __init__(self, name):
		self.name = name
		self.__this = None
		self.__other = None

	def set_this(self, this):
		self.__this = this

	def get_this(self):
		return self.__this

	def set_other(self, other):
		self.__other = other

	def get_other(self):
		return self.__other

	def enter_region(self):
		flag[self.get_this()] = True
		while flag[self.get_other()]:
			if turn == self.get_other():
				flag[self.get_this()] = False
				while flag[self.get_other()]:
					pass
				flag[self.get_this()] = True
	    
	def critical_region(self):
		self.print_document()

	def leave_region(self):
		turn = self.get_other()
		flag[self.get_this()] = False

	def handle_server(self, data):
		if not data: # ex: caso o servidor se desligue, ou conexao perdida
			return
		elif data == b'print':
			global doc_count
			doc_count += 1
			print('O documento {} está na fila...'.format(threading.get_ident()))
			self.enter_region()
			self.critical_region()
			self.leave_region()
			doc_count -= 1

	def print_document(self):
		t = rand(2, 10)
		sleep(t)
		print('O documento {} imprimiu em {}s'.format(threading.get_ident(), t))

	def run(self, buffer):
		while True:
			item = buffer.get()
			if item is None:
				break
			item.start()
			item.join()
			buffer.task_done()


def main():
	global doc_count
	global univ_count
	d1 = Printer('D1')
	d2 = Printer('D2')
	with socket.socket() as s: # por default ja abre socket AF_INET e TCP (SOCK_STREAM)
		s.connect(('', 50007))
		while True:
			io_list = [sys.stdin, s]
			ready_to_read, ready_to_write, in_error = select.select(io_list , [], [])   # visto que as funcoes input e 
                                                                                      # recv sao 'bloqueadoras' da 
                                                                                      # execucao do codigo seguinte 
                                                                                      # temos de 'seguir' ambos os 
                                                                                      # eventos desta maneira

			if s in ready_to_read: # caso haja dados a chegar
				data = s.recv(1024)

				id = univ_count % 2
				univ_count += 1
				if univ_count == MAX_UNIV_COUNT:
					univ_count = 0
				if id == 0:
					d1.set_this(id)
					d1.set_other((id + 1) % 2)
					thread1 = threading.Thread(target=d1.handle_server, args=(data, ))
					if doc_count <= BUFFER_SIZE - 1:
						buffer.put(thread1)
					else:
						print('Buffer cheio!')
				else:
					d2.set_this(id)
					d2.set_other((id + 1) % 2)
					thread2 = threading.Thread(target=d2.handle_server, args=(data, ))
					if doc_count <= BUFFER_SIZE - 1:
						buffer.put(thread2)
					else:
						print('Buffer cheio!')
				threading.Thread(target=d1.run, args=(buffer, )).start()
				threading.Thread(target=d2.run, args=(buffer, )).start()


if __name__ == '__main__':
	main()
          
