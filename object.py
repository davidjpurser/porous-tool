
# one dimensional N/Z linear set
class object:

	self.base;
	self.periods = set();

	# 1 = N linear, -1 Z linear (i.e. allows negative)
	self.type;

	def setBase(self, base):
		self.base = base

	def addPeriod(self,period):
		self.periods.add(period)

		if len(self.periods) > 1:
			self.periods = {lcm(self.periods)}

	def setType(self,type):
		self.type = type

	def contains(self, number):
		# singleton object
		if len(self.periods) == 0:
			return number == self.base

		period = list(self.periods)[0]
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

