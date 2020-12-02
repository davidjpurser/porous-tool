from linearset import * 

class semilinear:

	def __init__(self):
		self.lsets = set()

	def add(self,l):
		self.lsets.add(l)


	def __repr__(self):

		if not self.lsets: #empty
			return "{}"
		return "U".join([str(x) for x in self.lsets])			


	def addPoints(self, points):
		for x in points:
			p = linearset(x)
			self.lsets.add(p)
	
	def contains(self, lset):
		for x in self.lsets:
			if x.isEqual(lset):
				return True
		return False