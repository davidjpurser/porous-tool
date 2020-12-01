
# one dimensional N/Z linear set
class object:

	self.base = 0;
	self.periods = set();

	# 1 = N linear, -1 Z linear (i.e. allows negative)
	self.type =1;

	def __init__(self,b,p,t):
		self.base = b
		self.periods = set([p]) 
		self.setType(t)

	def setType(self, t):
		if abs(t) != 1:
			return False
		self.type = t

	def setBase(self, base):
		self.base = base

	def getPeriod(self):
		if len(self.periods) == 0:
			return None;

		return self.periods[0]

	def addPeriod(self,period):
		self.periods.add(period)

		if len(self.periods) > 1:
			self.periods = {lcm(self.periods)}

		if type == -1 and self.base > self.getPeriod():
			self.base = self.base mod self.getPeriod()

	def contains(self, number):

		period = self.getPeriod()

		# singleton object
		if period == None:
			return number == self.base

		base = self.base
		required = (number- base)/periods
		if not isInteger(required):
			return False

		if self.type == 1 and required >= 0:
			return True
		if self.type == -1:
			return True

		return False

	def isEqual(self, object):
		pass
		#two objects are equivalent

	def containsObject(self, object):
		#this is more general (covers) input

	def objectContains(self, object):
		# object is more general (covers) this
		return obejct.containsObject(self)

