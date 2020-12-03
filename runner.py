import math
from function import *
from tree import *
from semilinear import *
from linearset import *
from helpers import *
from functools import reduce
from math import gcd


from tool import buildinv

functions = [
	function(15,-5),
	function(2,0),
]
print(functions)
x = 1
target = 8

semi = buildinv(x,target,functions)
print(semi)
