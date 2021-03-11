
# one dimensional N/Z linear set
class linearset:


	# 1 = N linear, -1 Z linear (i.e. allows negative)
	def getTStr(self):
		if self.type == 1:
			return "N"
		else:
			return "Z"

	def __repr__(self):

		left = "{" + "{}".format(self.base) 
		if self.periods:
			left = left + " +{}{}".format(self.periods,self.getTStr())
		left =  left + "}"
		
	
		return left

	def getInverse(self):
		if self.isSingleton():
			return linearset(-self.base)
		else:
			return linearset(-self.base,-self.periods,self.type)


	def explainrepr(self):
		left = __repr__(self)
		if self.periods and self.type == 1 and self.base != self.base % self.periods:
			left += "*{}*".format(self.base % self.periods)
		return left


	def __init__(self,b,p=None,t=1):
		self.periods = None
		self.base = b
		self.setType(t)
		if p != None:
			self.addPeriod(p)		


	def isSingleton(self):
		return self.periods == None

	def setType(self, t):
		if abs(t) != 1:
			return False
		self.type = t

	def getBase(self):
		return self.base

	def setBase(self, base):
		self.base = base

	def getPeriod(self):
		return self.periods

	def addPeriod(self,period):
		if self.periods != None:
			exit("period is already set")

		self.periods = period

		if self.type == -1 and self.periods < 0:
			self.periods = -self.periods

		if self.type == -1 and (abs(self.base) >= self.getPeriod() or self.base < 0):
			self.base = self.base % self.getPeriod()

	def contains(self, number):

		period = self.getPeriod()

		# singleton object
		if period == None:
			return number == self.base

		base = self.base
		required = (number- base)/period
		if not required.is_integer():
			return False

		if self.type == 1 and required >= 0:
			return True
		if self.type == -1:
			return True

		return False

	def isEqual(self, object):
		pass
		if self.base != object.getBase():
			return False
		if self.type != object.type:
			return False

		if self.getPeriod() != object.getPeriod():
			return False
		return True
		#two objects are equivalent

	def containsObject(self, object):

		if not self.contains(object.base):
			# must contain the base element
			return False

		# singleton only, no need to check further
		if not object.periods:
			return True

		# singleton cannot contain an non-singleton
		if not self.periods:
			return False

		if self.type == 1 and object.type == -1:
			# N can't contain Z
			return False

		if not (object.periods / self.periods).is_integer():
			return False

		if self.type == 1 and object.type == 1:
			if object.periods / self.periods < 0:
				return False

		return True


	def objectContains(self, object):
		# object is more general (covers) this
		return object.containsObject(self)

