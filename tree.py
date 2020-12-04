

class ModuloTree:


	def __init__(self,modulo):
		self.mp = {}
		self.modulo = modulo

	def __repr__(self):
		return str(self.mp)

	def edge(self,x,y):
		if x not in self.mp:
			self.mp[x] = set()

		self.mp[x].add(y)

	def search(self, x, bound):

		myclass = x % self.modulo

		Q = [x]
		seen = set(Q)
		#BFS for something in the same modulo class to the right or left depending on the direction of bound
		while len(Q) > 0:
			z = Q.pop(0)
			# print("checking", x,z,z%self.modulo,myclass, "bound", bound)
			if ((bound> 0 and z > x) or (bound< 0 and z < x)) and z %self.modulo == myclass:
				print("path from",x, "to",z, "class", myclass)
				return True
			
			if z in self.mp:
				for y in self.mp[z]:
					if y not in seen:
						seen.add(y)
						Q.append(y)
						# print("appending ", y)
		return False
