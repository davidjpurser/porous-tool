from tabulate import tabulate
import math
from function import *
from tree import *
from semilinear import *
from linearset import *
from helpers import *
from functools import reduce
from proof import buildProof
from math import gcd


from tool import buildinv

functions = [
	function(15,-5),
	function(-1,5),
	function(-1,-5),
]

functions = [
	function(2,0),
	function(1,-3),
]


print(functions)
x = 1
target = 22

semi = buildinv(x,target,functions)
print("----------")
print("functions", functions)
print("----------")
print("invariant:" ,semi)
print("----------")
if semi.containsFuzz(linearset(target)):
	print("target:" ,target, "is a member of", semi.getContainsFuzz(linearset(target)))
else:
	print("target:" ,target, "is not in invariant")
print("----------")
print(tabulate(buildProof(semi, functions), headers =["Set", "under", "gives", "","within"]))
print("----------")
