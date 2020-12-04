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

def appen(txt, *vartuple):
	vars = list(vartuple)
	txt = txt + " ".join([str(x) for x in vars]) 
	print(txt)
	txt += "\n"
	return txt 

def pyprint(data):
	txt = ""
	txt = appen(txt, "----------")
	txt = appen(txt, "functions", data['functions'])
	txt = appen(txt, "----------")
	txt = appen(txt, "invariant:" ,data['inv'])
	txt = appen(txt, "----------")
	if 'expectation' in data:
		txt = appen(txt, 'expecting:', "reachable" if data['expectation'] == "True" else "unreachable", 'Passed:', data['passtest'])
	txt = appen(txt, data['reach'])
	txt = appen(txt, "----------")
	txt = appen(txt, data['proof'])
	txt = appen(txt, "----------")
	return txt



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
			if len(split) > 2:
				expectation = split[2] == 'True'
			else:
				expectation = None
		else:
			functions.append(function(int(split[0]),int(split[1])))
	print(start,target,functions)
	return manual(start,target,functions,expectation)

def manual(start,target,functions,expectation = None):
	semi = buildinv(start,target,functions)


	passtest = semi.containsFuzz(linearset(target)) == expectation
	print(semi.containsFuzz(linearset(target)) , expectation)
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
	if expectation!=None:
		data['passtest'] = str(passtest)
		data['expectation'] = str(expectation)
	print(data)
	return data



import sys

if __name__ == "__main__":

	if len(sys.argv) > 1 :
		with open(sys.argv[1], "r")  as f:
			stuff = f.read()
			data = {}
			print(stuff)
			data['val']  = stuff
			pyprint(service(data))		

	else:
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
		pyprint(manual(x,target,functions))
		