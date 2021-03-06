import time
import math
from function import *
from semilinear import *
from linearset import *
from functools import reduce
from errors import *


## proofs of reachability and invariants

# proof of invariance
def buildProof(semi, functions,errors = None):
	data= []
	print("building proof", len(semi.lsets))
	for ls in semi.lsets:
		for x in functions:
			if ls.periods:
				newperiod = ls.periods * x.mult
			else:
				newperiod = None
			secondls = linearset(x.apply(ls.getBase()), newperiod, ls.type)

			inducts = [x for x in semi.lsets if x.containsObject(secondls)]
			if len(inducts ) == 0:
				if errors:
					errors.error(appen("",[ls,x,secondls, "not found"]))
				print("--------- problem!")
			else:
				data.append([ls,x ,secondls,"⊆", inducts[0]])

	print("proof built")
	return data

#you had better be sure that it is reachable. Otherwise it won't terminate.
def buildReachProof(start, target, semi, functions,errors = None, timeout = 30):
	
	if not semi.containsFuzz(target):
		# you should never have run this.
		if errors:
				errors.error("Target not in semi-linear, you shouldn't have run this ")
		return False
	print("building reachability graph")

	target = target.getBase()

	seen = set()
	before = {}


	if type(start) is int:
		Q = [start]
		start = set()
		start.add(Q[0])
	else:
		Q = list(start)

	if target in Q:
		return [target]

	start_time = time.time()
	while len(Q) > 0:
		#timeout
		if (time.time() - start_time) > timeout:
			print("giving up")
			if errors:
				errors.error("Reachability believed but took longer than " + str(timeout))
			return ['sorry it took too long to build']
		top = Q.pop(0)
		for x in functions:
			next = x.apply(top)
			if next not in seen:
				seen.add(next)
				Q.append(next)
				before[next] = (top, x)
				if next == target:
					print("target found, just need to build the route")
					output = []
					here = next
					while here not in start:
						output.append(here)
						output.append(before[here][1])
						here = before[here][0]

					output.append(here)
					output.reverse()
					print("target found, route made")
					return output
	#this should not happen if its correct
	return None