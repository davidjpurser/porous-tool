from math import gcd
from math import lcm

diff = gcd(26,48)
print(lcm(26,48))
print(diff)

stuff = set()

for x in range(48):
	for y in range(26):
		t = x*26 + y*48
		if t > lcm(26,48):
			break
		stuff.add(t)

stuff = list(stuff)
stuff.sort()

last = stuff[0]
for x in stuff[1:]:
	
	if x - last == diff:

		print(x)
		break
	last = x

print(stuff)