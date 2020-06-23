
class Peterson:

	interested = [False, False]
	turn = None

	def __init__(self):
		self.this = None
		self.other = None

	def enter_region(self):
		Peterson.interested[self.this] = True
		Peterson.turn = self.other
		while True:
			if not Peterson.interested[self.other] or Peterson.turn == self.this:
				break
	    
	def critical_region(self, region):
		pass

	def leave_region(self):
		Peterson.interested[self.this] = False
