
def appen(txt, *vartuple):
	vars = list(vartuple)
	txt = txt + " ".join([str(x) for x in vars]) 
	txt += "\n"
	return txt 
	
# just holds the errors
class Errors:
	def __init__(self):
		self.errors = []

	def error(self, txt):
		self.errors.append(txt)

	def getErrors(self):
		return self.errors

	def hasErrors(self):
		return len(self.errors) > 0