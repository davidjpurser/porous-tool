
import time
from tabulate import tabulate
import math
from function import *
from tree import *
from instance import *
from semilinear import *
from linearset import *
from functools import reduce
from proof import buildProof
from proof import buildReachProof
from math import gcd
from errors import *
from runner import *

functions = [
	function(2,0),
	function(1,-3),
]


print(functions)
x = 1
target = 22
ins = instance(x,target,functions)
computed = manual(ins)
pyprint(computed)
