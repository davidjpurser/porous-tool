from linearset import * 

class semilinear:
	"""
 	semilinear set, a collection of linear sets
	"""

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

	def getSsets(self):
		return [x.base for x in self.lsets if x.periods == None]

	def __repr__(self):
		if not self.lsets: #empty
			return "{}"
		things = self.getZsets() + self.getNsets() 
		singles=  set(self.getSsets())
		if len(singles) > 0:
			things = things +[singles]
		return " ∪ ".join([str(x) for x in things])			


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

	def getContainsFuzz(self, lset):
		for x in self.lsets:
			if x.containsObject(lset):
				return x
		return False

	# true then is everything
	# false may still be everything, but not through all Z's
	def weaklyIsEverything(self):

		Zs = self.getZsets()
		if len(Zs) == 0:
			return False

		period = Zs[0].periods
		modulos = [x.base for x in Zs]
		allmods = list(range(period))
		if set(modulos) == set(allmods):
			return True
		
		# could add more N analysis
		return False


	def reduction(self):
		return
		print("reducing")
		Zs = self.getZsets()
		Ns = self.getNsets()
		Ss = set(self.getSsets())

		# can ignore Zs
		if len(Ns) > 0:
			period = abs(Ns[0].periods)
		
		print("period", period)
		for i in range(period):
			print("modulo", i)
			mx = None
			mn = None
			for x in Ns:
				if x.periods == period:
					mx = x.base
				if x.periods == - period:
					mn = x.base

			print(mn,mx)
			if mx:
				while True:
					mxm = mx - period
					if mxm in Ss:
						mx = mxm
					else: 
						break

			if mn:
				while True:
					mnm = mn + period
					if mnm in Ss:
						mn = mnm
					else: 
						break
			print(mn,mx)
			
			if mn and mx and mn >= mx:
				self.add(linearset(mn,period,-1))
			elif mx:
				self.add(linearset(mx, period,1))
			elif mn:
				self.add(linearset(mn, -period,1))

		print("reductions")
		print("Z", len(Zs), len(self.getZsets()))
		print("N", len(Ns), len(self.getNsets()))
		print("S", len(Ss), len(self.getSsets()))