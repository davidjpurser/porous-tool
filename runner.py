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

from tool import buildinv

def appen(txt, *vartuple):
	vars = list(vartuple)
	txt = txt + " ".join([str(x) for x in vars]) 
	txt += "\n"
	return txt 

def pyprint(data):
	txt = ""
	txt = appen(txt, "----------")
	txt = appen(txt, "start:", data['start'],'target:', data['target'], "functions:", data['functions'])
	txt = appen(txt, "----------")
	txt = appen(txt, "invariant:" ,data['inv'])
	if 'errors' in data:
		txt = appen(txt, "----------")
		txt = appen(txt, "errors:" ,data['errors'])
	txt = appen(txt, "----------")
	txt = appen(txt, 'reachability:',  "reachable" if data['reachable'] else "unreachable")
	if 'expectation' in data:
		txt = appen(txt, 'expecting:', "reachable" if data['expectation'] == "True" else "unreachable")
		txt = appen(txt, 'Expectation=Reality:', data['passtest'])
	txt = appen(txt, data['reach'])
	if 'por' in data:
		txt = appen(txt, 'proof of reachability:', data['por'])
	txt = appen(txt, "----------")
	txt = appen(txt, "Proof of invariance")
	txt = appen(txt, data['proof'])
	txt = appen(txt, "----------")
	print(txt)
	return txt



def service(data):
	x= data['val']
	print(x)
	functions = []
	for i, line in enumerate(x.splitlines()):
		if line.startswith("ENDS"):
			break
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
	inst = instance(start,target,functions)
	inst.setExp(expectation)
	return manual(inst)



def manual(inst):
	start,target,functions,expectation = inst.asTuple()
	semi, start,target,functions = buildinv(start,target,functions)

	errors = Errors()
	print(semi)
	semi.reduction()

	passtest = semi.containsFuzz(linearset(target)) == expectation
	print('reality:', semi.containsFuzz(linearset(target)) , 'expections:', expectation)

	data = {
		'start': start,
		'target': target,
		'functions' : str(functions),
		'inv' :str(semi),
		'semi': semi,
		'proof': tabulate(buildProof(semi, functions, errors), headers =["Set", "under", "gives", "","within"]),
	}
	if semi.containsFuzz(linearset(target)):
		reach = "target: "  + str(target) +  " is a member of " +  str(semi.getContainsFuzz(linearset(target))) + " and can be reached"
		por = " -> ".join([str(x) for x in buildReachProof(start,target,semi,functions, errors)])
		data['por']=por
		data['reachable'] = True
	else:
		data['reachable'] = False
		reach = "target: " + str(target) +  " is not in invariant, so it cannot be reached"

	data['reach']= reach
	if expectation!=None:
		data['passtest'] = str(passtest)
		data['expectation'] = str(expectation)
	if errors.hasErrors():
		data['errors'] = str(errors.getErrors())
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
		pyprint(manual(instance(x,target,functions)))
		