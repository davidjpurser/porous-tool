"""
This is an example of how to invoke the system from code.

The example corresponds to the MU Puzzle.
"""

from instance import *
from runner import *

functions = [
	function(2,0),
	function(1,-3),
]

print(functions)
x = 1
target = 0
ins = instance(x,target,functions)
computed = manual(ins)
pyprint(computed)
