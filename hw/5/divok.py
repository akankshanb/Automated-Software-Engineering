#!/usr/bin/env python3 
#vim: sta:et:sw=2:ts=2:sts=2

from div import Div
from div2 import Div2
from lib import *
import math
from   lib   import THE,Pretty,same,first,last,ordered
from   copy  import deepcopy as kopy
from   thing import Num,Sym
import random
r= random.random
seed=random.seed

def num(i):
  if i<0.4: return [i,     r()*0.1]
  if i<0.6: return [i, 0.4+r()*0.1]
  return           [i, 0.8+r()*0.1]

def x(n):
  seed(1)
  return  [      r()*0.05 for _ in range(n)] + \
          [0.2 + r()*0.05 for _ in range(n)] +  \
          [0.4 + r()*0.05 for _ in range(n)] +   \
          [0.6 + r()*0.05 for _ in range(n)] +    \
          [0.8 + r()*0.05 for _ in range(n)]

def xnum(n):
#   print([one for one in x(n)])
  return  [num(one) for one in x(n)]

if __name__ == "__main__":
	seed(1)
	n = 10000
	# d = Div([      r()*0.05 for _ in range(n)] +
	#         [0.2 + r()*0.05 for _ in range(n)] +
	#         [0.4 + r()*0.05 for _ in range(n)] +
	#         [0.6 + r()*0.05 for _ in range(n)] +
	#         [0.8 + r()*0.05 for _ in range(n)] )
	# print(d)

	allNums = xnum(n)
	# First index
	firstx = [index[0] for index in allNums]
	# dFirst = Div(first)
	# for x in dFirst.ranges:
	#   print("! x.n %5s    x.lo %6.4f    x. hi %6.4f" % (x.n,x.lo,x.hi))
	# print( dFirst.b4.sd(), dFirst.gain)

	print("")
	
	# Last Index
	lasty = [index[1] for index in allNums]
	# dLast = Div(lasty)
	
	# for y in dLast.ranges:
	#   print("! y.n %5s    y.lo %6.4f    y. hi %6.4f" % (y.n,y.lo,y.hi))
	# print( dLast.b4.sd(), dLast.gain)

	# print(first)
	dFinal = Div2([firstx, lasty])

	
	# print("")
	#     #  0                   1
	#     #  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
	# d = Div([1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2])
	# for x in d.ranges:
	#   print("! %5s   %6.4f    %6.4f" % (x.n,x.lo,x.hi))
	# print( d.b4.sd(), d.gain)
	# print("")

    # # print("")
	#     #  0                   1
	#     #  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
	# d = Div([1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1])
	# for x in d.ranges:
	#   print("! %5s   %6.4f    %6.4f" % (x.n,x.lo,x.hi))
	# print( d.b4.sd(), d.gain)
