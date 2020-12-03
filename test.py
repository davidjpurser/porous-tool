from linearset import *

assert(linearset(5,10,1).contains(5))
assert(linearset(5,10,1).contains(15))
assert(not linearset(5,10,1).contains(6))
assert(not linearset(5,10,1).contains(-5))

assert(linearset(5,10,1).containsObject(linearset(15,10,1)))
assert(linearset(5,5,1).containsObject(linearset(15,10,1)))
assert(not linearset(5,10,1).containsObject(linearset(15,5,1)))
assert(not linearset(5,10,1).containsObject(linearset(15,-10,1)))
assert(not linearset(5,10,1).containsObject(linearset(15,10,-1)))
assert(linearset(5,10,-1).containsObject(linearset(15,10,1)))
assert(linearset(5,10,-1).containsObject(linearset(15,20,-1)))

assert(linearset(5,10,-1).containsObject(linearset(15)))
assert(linearset(5,10,-1).containsObject(linearset(25)))
assert(linearset(5,10,-1).containsObject(linearset(-5)))
assert(not linearset(5,10,-1).containsObject(linearset(-6)))



assert(linearset(-15,-10,1).containsObject(linearset(-45,-10,1)))
