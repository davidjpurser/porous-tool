import math
from function import *
from semilinear import *
from linearset import *
from helpers import *
from functools import reduce

def buildProof(semi, functions):
	data= []
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
			data.append([ls,x ,secondls,"⊆", inducts[0]])
	return data

