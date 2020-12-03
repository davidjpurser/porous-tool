from linearset import * 

class semilinear:

	def __init__(self):
		self.lsets = set()

	def add(self,l):
		if self.containsFuzz(l):
			return False

		self.lsets = {x for x in self.lsets if not l.containsObject(x)}

		self.lsets.add(l)

	def includesNs(self):
		for x in self.lsets:
			if x.type == 1:
				return True

		return False

	def getZsets(self):
		return [x for x in self.lsets if x.type == -1]

	def getNsets(self):
		return [x for x in self.lsets if x.type == 1 and x.periods != None]


	def __repr__(self):

		if not self.lsets: #empty
			return "{}"
		return " U\n".join([str(x) for x in self.lsets])			


	def addPoints(self, points):
		for x in points:
			p = linearset(x)
			self.lsets.add(p)
	
	def contains(self, lset):
		for x in self.lsets:
			if x.isEqual(lset):
				return True
		return False


	def containsFuzz(self, lset):
		for x in self.lsets:
			if x.containsObject(lset):
				return True
		return False