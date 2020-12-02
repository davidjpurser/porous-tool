

class function:
	mult = 1
	add = 0

	def __init__(self,m,a):
		self.mult = m
		self.add = a

	def __repr__(self):
		if self.mult ==1 :
			txt = ""
		else:
			txt = self.mult
		return "f(x) = {}x + {}".format(txt,self.add)

	def setMult(self,mult):
		self.mult = mult
	def setAdd(self,add):
		self.add = add

	def getCounterAmount(self):
		return abs(self.add)

	def apply(self, x):
		return self.mult *x + self.add

	def isCounter(self):
		return self.mult == 1

	def isPositiveCounter(self):
		return self.isCounter() and self.add >= 0

	def isNegativeCounter(self):
		return self.isCounter() and self.add < 0

	def isPureInverter(self):
		return self.mult == -1

	def isInverter(self):
		return self.mult < 0

	def isGrower(self):
		return abs(self.mult) > 1

	def growingFrom(self):
		#only makes sense if not counter
		return int(abs(self.add)/(abs(self.mult)-1))

	def isEqual(self, fun):
		return self.mult == fun.mult and self.add == fun.add

	def compose(self, fun):
		a = self.mult
		b = self.add
		c = fun.mult
		d = fun.add
		return function(a*c, a*d + b)

	def isIdentity(self):
		return self.isEqual(function(1,0))



