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

functions = [
	function(3,11),
	function(1,3),
	function(1,-43),
]
print(functions)
x = 1
target = 8
def compute(x,target, functions):
	# strip useless identity function
	functions = [x for x in functions if not x.isIdentity()]
	print(functions)
	x0 = set([x])
	growStatus = [x.isGrower() for x in functions]
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

	if all(growStatus):
		semi = semilinear()
		growPoints =[x.growingFrom() for x in functions]
		growPoint = max(growPoints)
		growPoint = max(growPoint, target+2)
		print(growPoints, growPoint)
		start = saturateTo(x0, functions, growPoint)
		semi.addPoints(start)
		dir1 = linearset(growPoint,1,1)
		dir2 = linearset(-growPoint,-1,1)
		semi.add(dir1)
		semi.add(dir2)
		print(semi)
		return semi

	if any(positiveCounter) and any(negativeCounter):
		counters = [x for x in functions if x.isCounter()]
		amounts = [x.getCounterAmount() for x in counters]
		print(amounts)
		period = lgcd(amounts)
		print(period)
		semi = semilinear()
		lset1 = linearset(x,period,-1)
		semi.add(lset1)
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
		print(semi)
		return semi

	print("I don't know how to handle this case")
	return None

compute(x,target,functions)
	# print(f1.apply(4))
	# # for _ in range(2):
	# # 	x0 = applySet(x0, functions)
	# # 	print(x0)
	# print(saturateTo(x0, functions, 100))