import socket, select, sys, queue
from time import sleep
from threading import Thread
from datetime import datetime

THREADS_AMOUNT = 10
BUFFER_SIZE = 10

count = 0

threads = []

class Printer(Thread):
	taking = [
		False, False, False, False, False,
		False, False, False, False, False
	]
	ticket = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	def __init__(self, id):
		self.id = id
		self.buffer = queue.Queue(BUFFER_SIZE) 
		Thread.__init__(self)

	def handle_server(self, data):
		if data == b'print':
			if count == 10:
				return
			else:
				self.pre_protocol(b'print')
				print('Numero de pedidos no buffer {}: '.format(count))
			while True:
				ans = self.print_document()
				if ans == b'done':
					self.pre_protocol(b'done')
					break
			print('Numero de pedidos no buffer {}: '.format(count))
			if not data:
				return

	def run(self):
		with socket.socket() as s:
			s.connect(('', 50007))
			while True:
				io_list = [sys.stdin, s]
				ready_to_read,ready_to_write,in_error = select.select(io_list , [], [])  
				if s in ready_to_read: 
					data = s.recv(1024)
				Thread(target=self.handle_server, args=(data, )).start()
        
	def pre_protocol(self, msg):
		for i in range(THREADS_AMOUNT):
			Printer.taking[i] = True
			Printer.ticket[i] = max(Printer.ticket)
			Printer.taking[i] = False
			for j in range(1, THREADS_AMOUNT):
				while True:
					if not Printer.taking[j]:
						break
				while True:
					if Printer.ticket[j] == 0 or max(Printer.ticket[i], Printer.ticket[j]):
						break
			self.critical_section(msg)
			Printer.ticket[i] = 0
			return

	def critical_section(self, msg):
		global count
		if msg == b'print':
			count += 1
			self.buffer.put(1)
		if msg == b'done':
			count -= 1
			self.buffer.get()

	def print_document(self):
		sleep(10)
		return b'done'

def main():
	create_threads()
	start_threads()
	join_threads()

def create_threads():
	for id in range(THREADS_AMOUNT):
		new_thread = Printer(datetime.now())
		new_thread.run()
		threads.append(new_thread)

def start_threads():
	for thread in threads:
		thread.start()

def join_threads():
	for thread in threads:
		thread.join()

if __name__ == "__main__":
	main()
