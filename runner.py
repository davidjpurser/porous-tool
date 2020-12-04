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

def service(data):
	x= data['val']
	print(x)
	functions = []
	for i, line in enumerate(x.splitlines()):
		print(line)
		split = line.split(" ")
		if i == 0:
			start = int(split[0])
			target = int(split[1])
		else:
			functions.append(function(int(split[0]),int(split[1])))
	print(start,target,functions)
	semi = buildinv(start,target,functions)

	if semi.containsFuzz(linearset(target)):
		reach = "target: "  + str(target) +  " is a member of " +  str(semi.getContainsFuzz(linearset(target))) + " so can be reached"
	else:
		reach = "target: " + str(target) +  " is not in invariant, so it cannot be reached"

	data = {
		'functions' : str(functions),
		'inv' :str(semi),
		'proof': tabulate(buildProof(semi, functions), headers =["Set", "under", "gives", "","within"]),
		'reach': reach
	}
	print(data)
	return data



if __name__ == "__main__":

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
