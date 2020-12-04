import time
import math
from function import *
from semilinear import *
from linearset import *
from helpers import *
from functools import reduce

def buildProof(semi, functions):
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
				print("--------- problem!")
			else:
				data.append([ls,x ,secondls,"⊆", inducts[0]])

	print("proof built")
	return data

	#you had better be sure
def buildReachProof(start, target, semi, functions):
	
	if not semi.containsFuzz(linearset(target)):
		# you should never have run this.
		return False
	print("building reachability graph")

	seen = set()
	before = {}

	Q = [start]

	start_time = time.time()

	while len(Q) > 0:
		if (time.time() - start_time) > 30:
			print("giving up")
			return ['sorry it took too long to build']
		top = Q.pop(0)
		for x in functions:
			next = x.apply(top)
			if next not in seen:
				seen.add(next)
				Q.append(next)
				before[next] = (top, x)
				if next == target:
					output = []
					here = next
					while here != start:
						output.insert(0, here)
						output.insert(0, before[here][1])
						here = before[here][0]

					output.insert(0,here)
					return output
	#this should not happen if its correct
	return None