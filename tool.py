"""
	Code to build Porous 1-d invariants.
	buildinv is the interesting method
"""

import math
from function import *
from tree import *
from semilinear import *
from linearset import *
from functools import reduce
from math import gcd
import heapq


def lgcd(list):
    x = reduce(gcd, list)
    return x

def syn(x):
	if x < 0:
		return  -1
	if  x== 0:
		return 0
	if x > 0:
		return 1

def sign(reference, x):
	return syn(x-reference)

def same_dir(reference, x, y):
	a = sign(reference,x)
	b = sign(reference,y)
	return a==b

assert(same_dir(4, 6,7))
assert(same_dir(4, -2,-3))
assert(same_dir(4, -3,-2))
assert(not same_dir(4, -3,8))
assert(not same_dir(4, 3,8))



def applySet(st, functions):
	ns = set(st)
	for f in functions:
		for s in st:
			ns.add(f.apply(s))

	return ns


def saturateTo(st, functions, C):
	print("saturating", st, 'to', C)
	while True:
		ns = applySet(st, functions)
		ns = { x  for x in ns if abs(x) < C}	
		# print(ns)
		if ns == st: 
			return ns
		st = ns



def dealWithInverters(semi, functions, period):
	nSets = semi.getNsets()
	#non pure inverters
	inverters = [x for x in functions if x.isInverter()]
	print("inverters:" ,inverters)
	for lset in nSets:
		for inverter in inverters:
			second = inverter.apply(lset.getBase())
			nextlset = linearset(second,period,-1)
			semi.add(nextlset)
	
	semi = saturateZ(semi, functions)
	return semi

def saturateZ(semi, functions):

	Q = semi.getZsets()
	if len(Q) > 0:
		period = Q[0].periods
		while len(Q) > 0 :
			top = Q.pop()
			for f in functions:
				b = top.getBase()
				next = f.apply(b)
				myset = linearset(next,period,-1)
				if not semi.contains(myset):
					# print("adding ",next, linearset(next,period,-1))
					semi.add(myset)
					Q.append(myset)
	return semi




def positiveCounters(semi, startpoint, bound, counter, others):

	print(semi)

	Q = [startpoint]
	T = ModuloTree(counter.add)
	# print(T)
	interationnumber =0 
	while len(Q) > 0:
		interationnumber +=1
		# print("iterating at", interationnumber)
		print(Q)
		p = Q.pop(0)
		print(p, others)
		# print(p, Q)
		for f in others:
			next = f.apply(p)
			print(p, f , "=" , next)
			if (bound > 0 and next > bound) or (bound< 0 and next < bound):
				#too big in the wrong direction
				# print(next, "to big")
				pass
			elif semi.containsFuzz(linearset(next,counter.add,-1)):
				# print(next, "already z")
				#already have a z linear set for this guy
				pass
			elif semi.containsFuzz(linearset(next,counter.add,1)):
				#already have  a n linear set for this guy
				# print(next, "already n")
				pass
			else:
				# print(next, "work")
				T.edge(next,p)
				if next not in Q:
					Q.append(next)
				# print(Q,T)
				semi.add(linearset(next,counter.add,1))
				# print("adding N ", next, counter.add)
				if T.search(next,bound):
					newthing = linearset(next,counter.add,-1)
					# print("found a loop, adding new Z set", newthing, "and starting again")
					print(semi)
					semi.add(newthing)
					# print("about to staurateZ's", semi)
					semi = dealWithInverters(semi, others, counter.add)
					# print("saturated Z's",semi)
					pass
					# return positiveCounters(semi, startpoint, bound, counter, others)
				else:
					# didn't find anything in the search, keep looking
					# print("continue working",interationnumber)
					pass
	return semi

def buildinv(startpoint,target, functions):

	if any([x.isRestarter() for x in functions]):
		without = [x for x in functions if not x.isRestarter()]
		invs = []
		invs.append(buildinv(startpoint,target,without))
		starts = set()
		starts.add(startpoint)
		for x in functions:
			if x.isRestarter():
				starts.add(x.add)
				invs.append(buildinv(x.add, target,without))

		firstInv = invs[0][0]
		for x in invs[1:]:
			inv,start,target,functions = x
			for lset in inv.lsets:
				firstInv.add(lset)

		print(firstInv, starts,target,functions)
		return firstInv, starts,target,functions

	if type(target) is int:
		target = linearset(target)

	semilinearTarget = target

	
	if not target.isSingleton():
		period = target.getPeriod()
		semi = semilinear()
		semi.add(linearset(startpoint,period,-1))
		saturateZ(semi,functions)
		return semi,startpoint,semilinearTarget,functions

	else: 
		target = target.getBase()

	##### SINGLE POINT TARGET FROM HERE

	if startpoint < 0:
		newstartpoint = -startpoint
		newtarget = -target
		newfunctions = [x.getReverseFunction() for x in functions]
		print("starting at negative, reversing everything", newstartpoint,newtarget,newfunctions)
		newsemi,newstartpoint,newsemilinearTarget,newfunctions =  buildinv(newstartpoint,newtarget,newfunctions)
		propersemi = semilinear()
		for x in newsemi.lsets:
			propersemi.add(x.getInverse())
		return propersemi,startpoint,semilinearTarget,functions



	

	# strip useless identity function
	functions = [x for x in functions if not x.isIdentity()]
	print(functions)

	#remove duplicates
	uniquefunctions = []
	for x in functions:
		if x not in uniquefunctions:
			uniquefunctions.append(x)
	functions = uniquefunctions
	
	positiveCounter = [x.isPositiveCounter() for x in functions]
	negativeCounter = [x.isNegativeCounter() for x in functions]
	pureInverters = [x.isPureInverter() for x in functions]

	# no useful functions 
	if len(functions) ==0:
		semi = semilinear()
		semi.add(linearset(startpoint))
		return semi, startpoint,semilinearTarget,functions


	# multiple pure inverters, then there are bi-directional counters
	if not any(positiveCounter) and not any(negativeCounter) and sum(pureInverters) > 1:
		inverters = [x for x in functions if x.isPureInverter()]
		a = inverters[0].compose(inverters[1])
		b = inverters[1].compose(inverters[0])
		functionsplus = functions + [a,b]
		return buildinv(startpoint,target, functionsplus)

	# bi-directional counters
	if any(positiveCounter) and any(negativeCounter):
		counters = [x for x in functions if x.isCounter()]
		amounts = [x.getCounterAmount() for x in counters]
		print(amounts)
		period = lgcd(amounts)
		print(period)
		semi = semilinear()
		lset1 = linearset(startpoint,period,-1)
		semi.add(lset1)
		saturateZ(semi,functions)
		return semi, startpoint,semilinearTarget,functions


	# there can only be one pure inverter
	inverter = None
	for x in functions:
		if x.isPureInverter():
			inverter = x
	nonInverters = [x for x in functions if not x.isPureInverter()]
	growStatus = [x.isGrower() for x in nonInverters]

	if len(nonInverters)  == 0:
		# todo!
		semi = semilinear()
		semi.add(linearset(startpoint))
		semi.add(linearset(inverter.apply(startpoint)))
		return semi, startpoint,semilinearTarget,functions

	# all nonInverters growers
	if all(growStatus):
		semi = semilinear()
		if inverter is not None:
			invertadd = inverter.add
		else:
			invertadd = 0

		growPoints =[x.growingFrom(invertadd) for x in nonInverters]
		growPoint = max(growPoints)
		growPoint = max(growPoint, abs(target)+2)
		lowerbound = -growPoint
		upperbound = growPoint
		if invertadd >= 0:
			upperbound += invertadd
		else:
			lowerbound += invertadd

		start = saturateTo(set([startpoint]), functions, max(-lowerbound, upperbound))
		start = [x for x in start if x<=upperbound and x>=lowerbound]
		semi.addPoints(start)
		dir1 = linearset(upperbound,1,1)
		dir2 = linearset(lowerbound,-1,1)
		semi.add(dir1)
		semi.add(dir2)
		return semi,  startpoint,semilinearTarget,functions

	if any(positiveCounter) or any(negativeCounter):
		semi = semilinear()
		counters = [x for x in functions if x.isCounter()]
		possibleInverters = [x for x in functions if x.isInverter()]
		otherfunctions = [x for x in functions if not x.isCounter() and not x.isInverter()]

		counteradds = [x.add for x in counters]
		if counters[0].add > 0:
			counters.sort(key=lambda counter: counter.add)
		else:
			counters.sort(key=lambda counter: counter.add,reverse = True)

		mincounter = counters[0].add
		modulo = abs(mincounter)

		semi = semilinear()
		starter = linearset(startpoint,mincounter, 1)
		semi.add(starter)
		semi = dealWithInverters(semi, functions, mincounter)

		print(semi)
		#maybe everything turns out to be Z sets already
		if not semi.includesNs():
			return semi,  startpoint,semilinearTarget,functions

		# no then we need to deal with Ns?

		# saturate in the good direction
		

		period = starter.getPeriod()
		Q = [starter.getBase()]
		print(Q)
		while len(Q) > 0 :
			b = heapq.heappop(Q)
			for f in nonInverters:
				next = f.apply(b)
				myset = linearset(next,period,1)
				# print(next, myset,len(Q), len(semi.lsets))
				if same_dir(startpoint,next, counters[0].apply(startpoint)):
					if not semi.containsFuzz(myset):
						semi.add(myset)
						semi = dealWithInverters(semi, functions, mincounter)
						Q.append(next)
						heapq.heappush(Q,next)



		#maybe everything turns out to be Z sets already
		if not semi.includesNs():
			return semi,  startpoint,semilinearTarget,functions

		print(semi)

		counter = counters[0]
		others = otherfunctions + counters[1:]
		growers = [x for x in nonInverters if not x.isCounter()]
		bound = max([x.growingFrom() for x in growers] + [startpoint]) +1
		# bound = max(bound, startpoint) + 1
		print("bound",bound)
		if counter.apply(startpoint) - startpoint > 0:
			semi = positiveCounters(semi, startpoint, bound, counter, others)
		else: #negative counters
			print("negativeCounter")
			bound = - bound
			semi = positiveCounters(semi, startpoint, bound, counter, others)

		return semi,  startpoint,semilinearTarget,functions

	## If everything has gone right, this code is unreachable.
	print("I don't know how to handle this case")
	return None

