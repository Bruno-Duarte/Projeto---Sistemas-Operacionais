
class Dekker:

	flag = [False, False]
	turn = 0

	def __init__(self):
		self.this = None
		self.other = None

	def enter_region(self):
		Dekker.flag[self.this] = True
		while Dekker.flag[self.other]:
			if Dekker.turn == self.other:
				Dekker.flag[self.this] = False
				while Dekker.flag[self.other]:
					pass
				Dekker.flag[self.this] = True
	    
	def critical_region(self, region):
		pass

	def leave_region(self):
		Dekker.turn = self.other
		Dekker.flag[self.this] = False
