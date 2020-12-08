from function import *
from random import randint
from instance import *
from linearset import * 
import runner


def saveAs(name, inst, type,data = None):
	with open("problems/" + type + "/" + name +".genproblem", 'w') as f:
		f.write(str(inst))
		if data != None:
			f.write("ENDS")
			f.write(runner.pyprint(data))


def getRand(bot,top):
	if bot > top:
		return randint(top,bot)
	return randint(bot,top)
	
def generateCounter(dir, max):
	val = getRand(dir,max*dir)
	return function(1,val)

def generatePosCounter(max):
	return generateCounter(1,max)

def generateNegCounter(max):
	return generateCounter(-1,max)

def generateGrowing(max):
	mult = getRand(2,max)
	counter = getRand(-max,max)
	return function(mult,counter)

def generateInvertingGrowing(max):
	mult = getRand(2,max)
	counter = getRand(-max,max)
	return function(-mult,counter)

def generatePureInverter(dir, max):
	val = getRand(dir,max*dir)
	return function(-1,val)

def generatePosPureInverter(max):
	return generatePureInverter(1,max)
def generateNegPureInverter(max):
	return generatePureInverter(-1,max)

def generateNullInverter(max):
	return function(-1,0)

from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

types =[generatePosCounter,
generateNegCounter,
generateGrowing,
generateInvertingGrowing,
generatePosPureInverter,
generateNegPureInverter,
generateNullInverter]

max = 50
for x in list(powerset(types)):
	functionTypes = (list(x))
	if len(functionTypes) == 0:
		continue

	nt = ""
	for t in types:
		if t in functionTypes:
			nt += "1"
		else:
			nt += "0"

	functions = []
	print("------")
	for x in functionTypes:
		functions.append(x(max))


	inst = instance(getRand(1,max),getRand(1,4*max),functions)
	data = runner.manual(inst)
	print(data)

	
	if 'errors' in data:
		name = nt + "-" + inst.getName()
		saveAs(name, inst, "errors", data)
	else:
		inst.setExp(data['semi'].containsFuzz(linearset(inst.target)))
		name = nt + "-" + inst.getName()
		saveAs(name, inst, "good",data)
	runner.pyprint(data)
	print(inst)


