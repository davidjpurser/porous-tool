from function import *
from helpers import *

f1 = function(1,6)
f2 = function(1,-9)


functions = [f1,f2]
print(functions)

x0 = set([4])




print(f1.apply(4))
# for _ in range(2):
# 	x0 = applySet(x0, functions)
# 	print(x0)
print(saturateTo(x0, functions, 100))