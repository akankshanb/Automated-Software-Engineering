#!/usr/bin/env python3
# vim: sta:et:sw=2:ts=2:sts=2
"""
Manage a list of rows, keep column statitics in Nums or Syms
"""

from lib   import *
from thing import Num,Sym
from cols  import Cols
from row   import Row

class Tbl(Pretty):
  "An object that updates column statistics when a row is added."
  def __init__(i,cols=None):
    i.rows = []
    i.cols = cols
    i.header = None
    i.weight = 1

  def dominates(self, i,j,goals): # i and j are rows.
    z = 0.00001
    s1, s2, n = z,z,z+len(goals)
    for goal in goals:
      a,b = i.cells[goal.pos], j.cells[goal.pos]
      a,b = goal.norm(a), goal.norm(b)
      s1 -= 10**(goal.w * (a-b)/n)
      s2 -= 10**(goal.w * (b-a)/n)
    return s1/n - s2/n # i is better if it losses least (i.e. this number under 0)

  def clone(i):
    "Create an empty table of the same form as self."
    return   Tbl( Cols(i.cols.names) )

  def dist(self,i,j,cols):
    p = THE.row.p
    d = 0
    n = 0
    for col in cols.all:
      n += 1
      d0 = col.dist(i.cells[col.pos], j.cells[col.pos])
      d += d0**p
    # print("do: ", d)
    return d**(1/p) / n**(1/p) # normalize distance 0..1

  def cos(i,x,y,z,distance,cols):
    return (i.dist(x,z,cols)**2 + distance**2 - i.dist(y,z,cols)**2)/(2*distance) 

  def read(i, src):
    "Fo all rows in src, fill in the table."
    for n, lst in enumerate(cells(cols(rows(src)))):
      if n == 0:
        i.header = lst
      if i.cols:
        lst = [col + x for col,x in zip(i.cols.all,lst)]
        i.rows += [Row(lst)]
      else:
        i.cols = Cols(lst)
        
    return i

#-----------------------------------------
# iterators

def rows(src):
  """convert lines into lists, killing whitespace
  and comments. skip over lines of the wrong size"""
  linesize = None
  for n, line in enumerate(src):
    line = re.sub(THE.char.doomed, '', line.strip())
    if line:
      # breakup a string and add the data to a string array
      line = line.split(THE.char.sep)
      if linesize is None:
        linesize = len(line)
      if len(line) == linesize:
        yield line
      else:
        now(False, "E> skipping line %s" % n)

def cols(src):
  "skip columns whose name contains '?'"
  usedCol = None
  for cells in src:
    if usedCol is None:
      usedCol = [n for n, cell in enumerate(cells) 
                if not THE.char.skip in cell]
    yield [cells[n] for n in usedCol]

def cells(src):
  "convert strings into their right types"
  one = next(src)
  fs = [None] * len(one)           # [None, None, None, None]
  yield one                        # the first line
  def ready(n, cell):
    if cell == THE.char.skip:
      return cell                  # skip over '?'
    fs[n] = fs[n] or prep(one[n])  # ensure column 'n' compiles
    return fs[n](cell)             # compile column 'n'
  for _, cells in enumerate(src):
    yield [ready(n, cell) for n, cell in enumerate(cells)]

def prep(x):
  "return a function that can compile things of type 'x'"
  def num(z):
    f = float(z)
    i = int(f)
    return i if i == f else f
  for c in [THE.char.num, THE.char.less, THE.char.more]:
    if c in x:
      return num
  return str
