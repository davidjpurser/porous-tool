from function import *
from semilinear import *
from linearset import *
from helpers import *

f1 = function(3,6)
f2 = function(-2,-9)


functions = [f1,f2]
print(functions)

x0 = set([1])
target = 8

growStatus = [x.isGrower() for x in functions]

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

print(f1.apply(4))
# for _ in range(2):
# 	x0 = applySet(x0, functions)
# 	print(x0)
print(saturateTo(x0, functions, 100))