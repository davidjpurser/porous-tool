import math

class function:
	""" 
		A class to hold functions of the form: f(x) = m x + a
	"""

	def __init__(self,m,a):
		self.mult = m
		self.add = a

	def __repr__(self):
		if self.mult ==1 :
			txt = ""
		else:
			txt = self.mult

		answer = "f(x) = {}x".format(txt)
		if self.add > 0:
			answer += " + {}".format(self.add)
		if self.add < 0:
			answer += " - {}".format(-self.add)
		return answer

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

	def isRestarter(self):
		return self.mult == 0

	def growingFrom(self, extra=0):
		#only makes sense if not counter
		return int(math.ceil((abs(self.add) + abs(extra))/(abs(self.mult)-1)))

	def isEqual(self, fun):
		if type(self) != type(fun):
			return False
		return self.mult == fun.mult and self.add == fun.add

	def __eq__(self,fun):
		return self.isEqual(fun)

	def compose(self, fun):
		a = self.mult
		b = self.add
		c = fun.mult
		d = fun.add
		return function(a*c, a*d + b)

	def isIdentity(self):
		return self.isEqual(function(1,0))

	def getReverseFunction(self):
		return function(self.mult, -self.add)

	def simplestr(self):
		return str(self.mult) + " " + str(self.add)
