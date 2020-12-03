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
	function(2,0),
	function(30,0),
	function(-1,23),
	function(-1,22),
]
print(functions)
x = 1
target = 22

semi = buildinv(x,target,functions)
print("----------")
print(semi)
print("----------")
print(tabulate(buildProof(semi, functions), headers =["Set", "under", "gives", "","within"]))
print("----------")
