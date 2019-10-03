import socket, select, sys, queue
from time import sleep
from threading import Thread

THREADS_AMOUNT = 2
BUFFER_SIZE = 10

count = 0

class Printer(Thread):
	turn = 0
	interested = [False, False]

	def __init__(self, id):
		self.this = id
		self.other = 1 - self.this
		self.buffer = queue.Queue(BUFFER_SIZE) 
		Thread.__init__(self)

	def handle_server(self, data):
		if data == b'print':
			if count == 10:
				return
			else:
				self.pre_protocol()
				self.critical_section(b'print')
				self.post_protocol()
				print('Numero de pedidos no buffer {}: '.format(count))
			while True:
				ans = self.print_document()
				if ans == b'done':
					self.pre_protocol()
					self.critical_section(b'done')
					self.post_protocol()
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
        
	def pre_protocol(self):
		Printer.interested[self.this] = True 
		turn = self.this   
		while Printer.interested[self.other] == True and Printer.turn == self.this:
			pass  

	def critical_section(self, msg):
		global count
		if msg == b'print':
			count += 1
			self.buffer.put(1)
		if msg == b'done':
			count -= 1
			self.buffer.get()

	def post_protocol(self):
		Printer.interested[self.this] = False 

	def print_document(self):
		sleep(10)
		return b'done'

threads = []

def main():
	create_threads()
	start_threads()
	join_threads()

def create_threads():
	for id in range(THREADS_AMOUNT):
		new_thread = Printer(id)
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
