

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
		txt += str(self.start) + " " + str(self.target)
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