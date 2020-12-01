

def applySet(st, functions):
	ns = set(st)
	for f in functions:
		for s in st:
			ns.add(f.apply(s))

	return ns


def saturateTo(st, functions, C):
	
	while True:
		ns = applySet(st, functions)
		ns = { x  for x in ns if abs(x) < C}	
		# print(ns)
		if ns == st: 
			return ns
		st = ns
