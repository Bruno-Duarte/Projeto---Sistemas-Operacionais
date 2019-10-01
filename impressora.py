import socket, select, sys, queue
from time import sleep
from threading import Thread

THREADS_AMOUNT = 2
BUFFER_SIZE = 10
COUNT_PER_THREAD = BUFFER_SIZE/THREADS_AMOUNT

count = 0

class Printer(Thread):

  turn = 0
  want_status = [False, False]

  def __init__(self, id):
    self.this = id
    self.other = (id + 1) % 2
    self.buffer = queue.Queue(BUFFER_SIZE) 
    Thread.__init__(self)

  def connect_to_server(self):

    with socket.socket() as s: # por default ja abre socket AF_INET e TCP (SOCK_STREAM)
        s.connect(('', 50007))
        while True:
            io_list = [sys.stdin, s]
            ready_to_read,ready_to_write,in_error = select.select(io_list , [], [])
            
            if s in ready_to_read: 
                data = s.recv(1024)
                if data == b'print':
                  self.pre_protocol()
                  self.critical_section(b'print')
                  self.post_protocol()
                  while True:
                    ans = self.print_document()
                    if ans == b'done':
                      self.pre_protocol()
                      self.critical_section(b'done')
                      self.post_protocol()
                      break
                  print('Counter {}: '.format(count))
                  print(self.buffer.qsize())

                if not data: 
                    break
            else: # enviar msg
                msg = sys.stdin.readline() 
                s.send(msg.encode())  
                sys.stdout.flush()

  def pre_protocol(self):
    Printer.want_status[self.this] = True
    while Printer.want_status[self.other]:
      if Printer.turn == self.other:
        Printer.want_status[self.this] = False
        while Printer.want_status[self.other]:
          pass
        Printer.want_status[self.this] = True

  def critical_section(self, msg):
    global count
    if msg == b'print':
      count += 1
      print('Incremento')
      self.buffer.put(1)
    if msg == b'done':
      print('Decremento')
      count -= 1
      self.buffer.get()

  def post_protocol(self):
    Printer.turn = self.other
    Printer.want_status[self.this] = False

  def print_document(self):
    sleep(5)
    return b'done'

threads = []

def main():
  create_threads()
  start_threads()
  join_threads()
  output_result()

def create_threads():
  for id in range(THREADS_AMOUNT):
    new_thread = Printer(id)
    new_thread.connect_to_server()
    threads.append(new_thread)

def start_threads():
  for thread in threads:
    thread.start()

def join_threads():
  for thread in threads:
    thread.join()

def output_result():
  print('Counter value: {}'.format(count))

if __name__ == "__main__":
    main()
