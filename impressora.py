import socket, select, sys, threading, queue
from time import sleep
from random import randint as rand

from src.classes.dekker import Dekker
from src.classes.peterson import Peterson
from src.classes.lamport import Lamport

from src.interface.menus import secondary_menu, draw_line

BUFFER_SIZE = 2


class Director:

	def __init__(self, builder):
		self._builder = builder

	def build_priter(self):
		self._builder.set_name()
		self._builder.set_buffer()
		self._builder.attach_locks()
		return self._builder.run()

	def get_printer(self):
		return self._builder.get_core()


class Core:

	def __init__(self):
		self.name = None
		self.buffer = None
		self.locks = list()
		self.doc_counter = 0
		self.univ_counter = 0
		self.max_univ_counter = 1000


class Printer:

	def __init__(self):
		self._core = Core()

	def print_document(self):
		t = rand(2, 10)
		sleep(t)
		print('O documento {} foi impresso em {}s'.format(threading.get_ident(), t))

	def handle_document(self, data, id):
		if not data: 
			return
		elif data == b'print':
			print('O documento {} está na fila...'.format(threading.get_ident()))
			self._core.doc_counter += 1
			self._core.locks[id].enter_region()
			self._core.locks[id].critical_region(self.print_document())
			self._core.doc_counter -= 1
			self._core.locks[id].leave_region()

	def handle_buffer(self):
		while True:
			item = self._core.buffer.get()
			if item is None:
				break
			item.start()
			item.join()
			self._core.buffer.task_done()

	def run(self):
		with socket.socket() as s: 
			s.connect(('', 50007))
			while True:
				io_list = [sys.stdin, s]
				ready_to_read, ready_to_write, in_error = select.select(io_list , [], [])   
				if s in ready_to_read: 
					data = s.recv(1024)
					id = self._core.univ_counter % BUFFER_SIZE
					self._core.locks[id].this = id
					self._core.locks[id].other = (id + 1) % BUFFER_SIZE
					self._core.univ_counter += 1
					if self._core.univ_counter == self._core.max_univ_counter:
						self._core.univ_counter = 0
					thread = threading.Thread(target=self.handle_document, args=(data, id, ))
					if self._core.doc_counter < BUFFER_SIZE:
						self._core.buffer.put(thread)
					else:
						print('Buffer cheio!')	
					threading.Thread(target=self.handle_buffer).start()

	def get_core(self):
		return self._core


class DekkerPrinter(Printer):

	def set_name(self):
		self._core.name = 'Dekker Printer'

	def set_buffer(self):
		self._core.buffer = queue.Queue(BUFFER_SIZE)

	def attach_locks(self):
		for i in range(BUFFER_SIZE):
			lock = Dekker()
			self._core.locks.append(lock)
		
	
class PetersonPrinter(Printer):

	def set_name(self):
		self._core.name = 'Peterson Printer'

	def set_buffer(self):
		self._core.buffer = queue.Queue(BUFFER_SIZE)

	def attach_locks(self):
		for i in range(BUFFER_SIZE):
			lock = Peterson()
			self._core.locks.append(lock)


class LamportPrinter(Printer):

	def set_name(self):
		self._core.name = 'Lamport Printer'

	def set_buffer(self):
		self._core.buffer = queue.Queue(BUFFER_SIZE*5)

	def attach_locks(self):
		for i in range(BUFFER_SIZE*5):
			lock = Lamport()
			self._core.locks.append(lock)

	def handle_document(self, data, id):
		if not data: 
			return
		elif data == b'print':
			print('O documento {} está na fila...'.format(threading.get_ident()))
			self._core.doc_counter += 1
			self._core.locks[id].acquire(id)
			self._core.locks[id].critical_region(self.print_document())
			self._core.locks[id].release(id)
			self._core.doc_counter -= 1

	def run(self):
		with socket.socket() as s: 
			s.connect(('', 50007))
			while True:
				io_list = [sys.stdin, s]
				ready_to_read, ready_to_write, in_error = select.select(io_list , [], [])   
				if s in ready_to_read: 
					data = s.recv(1024)
					id = self._core.univ_counter % (BUFFER_SIZE*5)
					self._core.locks[id].id = id
					self._core.univ_counter += 1
					if self._core.univ_counter == self._core.max_univ_counter:
						self._core.univ_counter = 0
					thread = threading.Thread(target=self.handle_document, args=(data, id, ))
					if self._core.doc_counter < BUFFER_SIZE*5:
						self._core.buffer.put(thread)
					else:
						print('Buffer cheio!')	
					threading.Thread(target=self.handle_buffer).start()


def main():
	while True:
		option = secondary_menu()
		draw_line()
		if option == '1':
			builder_director = Director(DekkerPrinter())
		elif option == '2':
			builder_director = Director(PetersonPrinter())
		elif option == '3':
			builder_director = Director(LamportPrinter())
		elif option == '4':
			break
		else:
			print('Opção inválida!')
			draw_line()
		try:
			printer = builder_director.build_priter()
			printer = builder_director.get_printer()
			draw_line()
			print(printer.name)
			print('Tamanho do buffer: {}'.format(len(printer.locks)))
			printer.run()
		except ConnectionRefusedError:
			print('Server não encontrado, execute o arquivo "servidor.py"')
		except UnboundLocalError:
			pass

if __name__ == '__main__':
	main()