import socket, select, sys, threading, queue
from time import sleep
from random import randint as rand

BUFFER_SIZE = 10
MAX_UNIV_COUNT = 1000

doc_count = 0
univ_count = 0

buffer = queue.Queue(BUFFER_SIZE)

taking = [
	False, False, False, False, False, 
	False, False, False, False, False
]

tickets = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

class Printer(object):

	def __init__(self, name):
		self.name = name
		self.__id = None

	def set_id(self, id):
		self.__id = id

	def get_id(self):
		return self.__id

	def acquire(self, i):
		taking[i] = True
		tickets[i] = max(tickets) + 1
		taking[i] = False
		for j in range(BUFFER_SIZE):
			while taking[j]:
				pass
			while tickets[j] != 0 and (tickets[j], j) < (tickets[i], i):
				pass
	    
	def critical_section(self):
		self.print_document()

	def release(self, i):
		tickets[i] = 0

	def handle_server(self, data):
		if not data: 
			return
		elif data == b'print':
			global doc_count
			doc_count += 1
			print('O documento {} está na fila...'.format(threading.get_ident()))
			id = self.get_id()
			self.acquire(id)
			self.critical_section()
			self.release(id)
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
	docs = []
	for i in range(BUFFER_SIZE):
		name = 'D' + str(i)
		doc = Printer(name)
		docs.append(doc)
	with socket.socket() as s: 
		s.connect(('', 50007))
		while True:
			io_list = [sys.stdin, s]
			ready_to_read, ready_to_write, in_error = select.select(io_list , [], [])   
			if s in ready_to_read: 
				data = s.recv(1024)
				id = univ_count % 10
				univ_count += 1
				if univ_count == MAX_UNIV_COUNT:
					univ_count = 0
				docs[id].set_id(id)
				thread = threading.Thread(target=docs[id].handle_server, args=(data, ))
				if doc_count <= BUFFER_SIZE - 1:
					buffer.put(thread)
				else:
					print('Buffer cheio!')
				for i in range(BUFFER_SIZE):
					threading.Thread(target=docs[i].run, args=(buffer, )).start()


if __name__ == '__main__':
	main()
          
