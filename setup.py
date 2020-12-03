import math
from function import *
from semilinear import *
from linearset import *
from helpers import *
from functools import reduce
from math import gcd

def lgcd(list):
    x = reduce(gcd, list)
    return x


def saturateZs(semi, lset1, functions):
	semi.add(lset1)
	period = lset1.getPeriod()
	Q = [lset1]
	while len(Q) > 0 :
		top = Q.pop()
		for f in functions:
			b = top.getBase()
			next = f.apply(b)
			myset = linearset(next,period,-1)
			print(next, linearset(next,period,-1))
			if not semi.contains(myset):
				semi.add(myset)
				Q.append(myset)
	return semi


functions = [
	function(3,11),
	function(12,2),
	function(-1,-3),
	function(1,-18),
	function(1,-12),
]
print(functions)
x = 1
target = 8
def compute(startpoint,target, functions):
	# strip useless identity function

	x0 = set([startpoint])
	functions = [x for x in functions if not x.isIdentity()]
	print(functions)
	
	positiveCounter = [x.isPositiveCounter() for x in functions]
	negativeCounter = [x.isNegativeCounter() for x in functions]
	pureInverters = [x.isPureInverter() for x in functions]

	# multiple pure inverters, then there are bi-directional counters
	if not any(positiveCounter) and not any(negativeCounter) and sum(pureInverters) > 1:
		inverters = [x for x in functions if x.isPureInverter()]
		a = inverters[0].compose(inverters[1])
		b = inverters[1].compose(inverters[0])
		print("there are counters! in both directions", a,b)
		print("adding both", a,b)
		functionsplus = functions + [a,b]
		return compute(x,target, functionsplus)

	# bi-directional counters
	if any(positiveCounter) and any(negativeCounter):
		counters = [x for x in functions if x.isCounter()]
		amounts = [x.getCounterAmount() for x in counters]
		print(amounts)
		period = lgcd(amounts)
		print(period)
		semi = semilinear()
		lset1 = linearset(x,period,-1)
		saturateZs(semi,lset1,functions)
		print(semi)
		return semi

	# there can only be one inverter
	inverter = None
	for x in functions:
		if x.isPureInverter():
			inverter = x
	nonInverters = [x for x in functions if not x.isPureInverter()]
	growStatus = [x.isGrower() for x in nonInverters]

	# all nonInverters growers
	if all(growStatus):
		semi = semilinear()
		growPoints =[x.growingFrom() for x in nonInverters]
		growPoint = max(growPoints)
		growPoint = max(growPoint, target+2)
		lowerbound = -growPoint
		upperbound = growPoint
		if inverter != None:
			if inverter.add >= 0:
				upperbound += inverter.add
			else:
				lowerbound += inverter.add

		start = saturateTo(x0, functions, max(-lowerbound, upperbound))
		start = [x for x in start if x<=upperbound and x>=lowerbound]
		semi.addPoints(start)
		dir1 = linearset(upperbound,1,1)
		dir2 = linearset(lowerbound,-1,1)
		semi.add(dir1)
		semi.add(dir2)
		print(semi)
		return semi

	if any(positiveCounter) or any(negativeCounter):
		semi = semilinear()
		counters = [x for x in nonInverters if x.isCounter()]
		counteradds = [x.add for x in counters]
		if counters[0].add > 0:
			mincounter = min(counteradds)
		else:
			mincounter = max(counteradds)

		modulo = abs(mincounter)

		Ns = {}
		Zs = {}

		Ns[startpoint % modulo] = startpoint
		
		semi = semilinear()
		starter = linearset(startpoint,mincounter, 1)
		semi.add(starter)
		if inverter:
			second = inverter.apply(startpoint)
			nextlset = linearset(second,mincounter,-1)
			saturateZs(semi, nextlset, functions)
			if not semi.includesNs():
				print(semi)
				return semi

		print("still not done")

		return semi

	print("I don't know how to handle this case")
	return None

semi = compute(x,target,functions)
print(semi)
	# print(f1.apply(4))
	# # for _ in range(2):
	# # 	x0 = applySet(x0, functions)
	# # 	print(x0)
	# print(saturateTo(x0, functions, 100))