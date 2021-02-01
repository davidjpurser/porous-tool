
# A problem instance
class instance:


	def __init__(self, start, target,functions ):
		self.start = start
		self.target = target
		self.functions = functions
		self.exp = None

	def asTuple(self):
		return self.start,self.target,self.functions,self.exp

	def setExp(self,exp):
		self.exp = exp

	def __repr__(self):
		txt = ""
		if type(self.target) is int:
			targetString = str(self.target)
		elif self.target.isSingleton():
			targetString = str(self.target.getBase())
		else:
			targetString = str(self.target.getBase()) + "+"+ str(self.target.getPeriod())

		txt += str(self.start) + " " + targetString
		if self.exp is not None:
			txt += " " + str(self.exp)
		txt += "\n"
		for x in self.functions:
			txt += x.simplestr() + "\n"
		return txt

	def getName(self, prefix = None):
		if not prefix:
			prefix= ""
		else:
			prefix +="_"
		if self.exp is not None:
			prefix +=  str(self.exp) + "_"
		return prefix +  self.__repr__().replace(" ","_").replace("\n","_")