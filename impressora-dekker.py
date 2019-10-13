import socket, select, sys, threading, queue
from time import sleep
from random import randint as rand

BUFFER_SIZE = 2

lock = threading.Lock()
count = 0

class Printer(object):

	want_status = [False, False]
	turn = 1

	def __init__(self, name):
		self.name = name
		self.buffer = queue.Queue(BUFFER_SIZE)

	def pre_protocol(self):
		Printer.want_status[0] = True
		while Printer.want_status[1]:
			if Printer.turn == 1:
				Printer.want_status[0] = False
				while Printer.want_status[1]:
					pass
				Printer.want_status[0] = True
	    
	def critical_section(self):
		global count
		count += 1
		self.print_document()
		count -= 1

	def post_protocol(self):
		Printer.turn = 1
		Printer.want_status[0] = False

	def handle_server(self, data):
		if not data:
			return
		elif data == b'print':
			self.pre_protocol()
			self.critical_section()
			self.post_protocol()

	def print_document(self):
		print('{} está esperando...'.format(threading.get_ident()))
		t = rand(2, 10)
		lock.acquire()
		sleep(t)
		lock.release()
		print('{} imprimiu em {}s'.format(threading.get_ident(), t))

	def run(self, buffer):
		while True:
			item = buffer.get()
			if item is None:
				break
			item.start()
			item.join()
			buffer.task_done()


def main():
	global count
	printer = Printer('Impressora')
	with socket.socket() as s:
		s.connect(('', 50007))
		while True:
			io_list = [sys.stdin, s]
			ready_to_read, ready_to_write, in_error = select.select(io_list , [], [])   
			if s in ready_to_read: 
				data = s.recv(1024)
				thread = threading.Thread(target=printer.handle_server, args=(data, ))
				if count <= BUFFER_SIZE - 1:
					printer.buffer.put(thread)
				else:
					print('Impressora ocupada.')
				threading.Thread(target=printer.run, args=(printer.buffer, )).start()


if __name__ == '__main__':
	main()
          
