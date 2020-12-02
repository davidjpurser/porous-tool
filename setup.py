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
	function(-2,0),
	function(1,33),
	function(1,-11)
]
print(functions)

x = 1
x0 = set([x])
target = 8

growStatus = [x.isGrower() for x in functions]
positiveCounter = [x.isPositiveCounter() for x in functions]
negativeCounter = [x.isNegativeCounter() for x in functions]

allGrowers = all(growStatus)
print(growStatus, allGrowers)

if allGrowers:
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

# print(f1.apply(4))
# # for _ in range(2):
# # 	x0 = applySet(x0, functions)
# # 	print(x0)
# print(saturateTo(x0, functions, 100))