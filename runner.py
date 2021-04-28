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

from tool import buildinv

#methods to invoke the code and make the output pretty



def appen(txt, *vartuple):
	vars = list(vartuple)
	txt = txt + " ".join([str(x) for x in vars]) 
	txt += "\n"
	return txt 

def breaker(txt):
	return appen(txt, "-----------------")

def pyprint(data):
	txt = ""
	txt = breaker(txt)
	txt = appen(txt, "Interpretation of input")
	txt = appen(txt, "start:", data['start'],'target:', data['target'], "functions:", data['functions'])
	txt = breaker(txt)
	if data['everything']:
		txt = appen(txt, "invariant:",'ALL')
	txt = appen(txt, "invariant:",data['inv'])
	if 'errors' in data:
		txt = breaker(txt)
		txt = appen(txt, "errors:" ,data['errors'])
	txt = breaker(txt)
	txt = appen(txt, 'reachability:',  "reachable" if data['reachable'] else "unreachable")
	

	if data['reachable']:
		txt = appen(txt, 'target', data['target'], 'in', data['targetmember'])	
		txt = appen(txt, 'proof of reachability:', data['por'])
	else: 
		txt = appen(txt, 'target', data['target'], 'disjoint from invariant')	

	if 'expectation' in data:
		txt = appen(txt, 'expecting:', "reachable" if data['expectation'] == True else "unreachable")
		txt = appen(txt, 'Expectation=Reality:', data['passtest'])


	txt = breaker(txt)
	txt = appen(txt, "Proof of invariance")
	txt = appen(txt, data['proof'])
	txt = breaker(txt)
	for x in data['time']:
		txt = appen(txt, 'time', x, f"{data['time'][x]:.9f}")
	txt = breaker(txt)
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
			
			targetStr = split[1]
			if '+' in targetStr:
				target = linearset(int(targetStr.split('+')[0]), int(targetStr.split('+')[1]),-1)
			else:
				target = linearset(int(split[1]))

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



def manual(inst,reachtimeout = 30):
	start,target,functions,expectation = inst.asTuple()

	start_time = time.time()
	semi, start,target,functions = buildinv(start,target,functions)
	end_time = time.time()

	errors = Errors()
	print(semi)
	semi.reduction()

	print('reality:', semi.containsFuzz(target) , 'expectations:', expectation)

	data = {
		'start': start,
		'target': target,
		'functions': functions,
		'instance' : instance,
		'inv' : semi,
		'everything': semi.weaklyIsEverything(),
		'time': {
			'invariant': end_time - start_time
		}
	}
	start_time = time.time()
	data['proof'] =  tabulate(buildProof(semi, functions, errors), headers =["Set", "under", "gives", "","within"])
	end_time = time.time()
	data['time']['proofOfInvariant'] = end_time - start_time


	data['reachable'] = semi.containsFuzz(target)

	if  semi.containsFuzz(target):
		data['targetmember'] = semi.getContainsFuzz(target)
		if target.isSingleton():
			if reachtimeout > 0:
				start_time = time.time()
				reachproof = buildReachProof(start,target,semi,functions, errors,reachtimeout)
				end_time = time.time()
				if len(reachproof) > 50:
					data['por']= " -> ".join([str(x) for x in reachproof[:5] + [".... stuff ...."] + reachproof[-5:]])
				else:
					data['por']= " -> ".join([str(x) for x in reachproof])
				data['time']['proofOfReachability'] = end_time - start_time
	
			else:
				data['por'] = "reachability proof disabled"
				data['time']['proofOfReachability'] = 0
		else:
			data['por'] = "reachability of periodic target not supported"
			data['time']['proofOfReachability'] = 0

	if expectation!=None:
		data['passtest'] = semi.containsFuzz(target) == expectation
		data['expectation'] = expectation
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

		