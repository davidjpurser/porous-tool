from function import *
from random import randint
from instance import *
from linearset import * 
import runner
import csv
import random

## randomly generated problems according to the paper

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

ordering = list(powerset(types))
random.shuffle(list(powerset(types)))
print(ordering)

def getWork(largest):
	for _ in range(8):
		for x in ordering:
			functionTypes = (list(x))
			if len(functionTypes) == 0:
				continue

			functions = []
			nt = ""
			stcode = ""
			for t in types:
				if t in functionTypes:

					number = getRand(1,2)
					# 50% chance of just 1
					if number ==2:
						number = getRand(2,9)
					nt += str(number)
					stcode += "1"

					for i in range(number):
						functions.append(t(largest))
				else:
					nt += "0"
					stcode += "0"

			inst = instance(getRand(1,largest),linearset(getRand(1,4*largest)),functions)
			yield (inst,stcode, nt,largest)

import os
if not os.path.exists("problems/errors"):
    os.makedirs("problems/errors")
if not os.path.exists("problems/good"):
    os.makedirs("problems/good")

if not os.path.exists("document.csv"):
	with open('document.csv','w') as f:
		writer = csv.writer(f)
		row = ['stcode','ntcode','size','name','reachable','errors','errorlist','time1','time2','time3']
		writer.writerow(row)


# print(list[getWork()])
import time
def work(tpl):
	inst,stcode, nt,largest = tpl

	with open('log.csv','a') as f:
		f.write(inst.getName() +"\n")

	data = runner.manual(inst, 30)
	print(data)

	name = "-".join([str(x) for x in [stcode,nt,data['reachable'],'errors' in data, time.time()
]])
	if 'errors' in data:
		
		saveAs(name, inst, "errors", data)
		errors = str(data['errors'])
	else:
		inst.setExp(data['inv'].containsFuzz(inst.target))
		saveAs(name, inst, "good",data)
		errors = str([])

	with open('document.csv','a') as f:
		writer = csv.writer(f)
		row = [stcode,nt,largest,name, data['reachable'],'errors' in data,errors]
		for x in ['invariant', 'proofOfInvariant','proofOfReachability']:
			row.append(f"{data['time'][x]:.9f}" if x in data['time'] else -1)
		writer.writerow(row)



	runner.pyprint(data)
	print(inst)


from multiprocessing import Pool
if __name__ == '__main__':
	with Pool(8) as p:
	    p.map(work, getWork(8))
	    p.map(work, getWork(16))
	    p.map(work, getWork(32))
	    p.map(work, getWork(64))
	    p.map(work, getWork(128))
	    p.map(work, getWork(256))
	    p.map(work, getWork(512))
	    p.map(work, getWork(1024))
