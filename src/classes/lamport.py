THREADS_AMOUNT = 10


class Lamport:

	taking = [False for x in range(THREADS_AMOUNT)]
	tickets = [0 for y in range(THREADS_AMOUNT)]

	def __init__(self):
		self.id = None

	def acquire(self, i):
		Lamport.taking[i] = True
		Lamport.tickets[i] = max(Lamport.tickets) + 1
		Lamport.taking[i] = False
		for j in range(THREADS_AMOUNT):
			while Lamport.taking[j]:
				pass
			while Lamport.tickets[j] != 0 and (Lamport.tickets[j], j) < (Lamport.tickets[i], i):
				pass
	    
	def critical_region(self, region):
		pass

	def release(self, i):
		Lamport.tickets[i] = 0

