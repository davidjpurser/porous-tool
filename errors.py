class errors:
	def __init__(self):
		self.errors = []

	def error(self, txt):
		self.errors.append(txt)

	def getErrors(self):
		return self.errors

	def hasErrors(self):
		return len(self.errors) > 0