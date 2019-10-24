#!/usr/bin/env python3
# vim: sta:et:sw=2:ts=2:sts=2
"""
Manage a list of rows, keep column statitics in Nums or Syms
"""

from lib   import *
from thing import Num,Sym
from cols  import Cols
from row   import Row
from the import *
import re
from div2 import Div2

class Tbl(Pretty):
  "An object that updates column statistics when a row is added."
  def __init__(i,cols=None):
    i.rows = []
    i.cols = cols

  def clone(i):
    "Create an empty table of the same form as self."
    return   Tbl( Cols(i.cols.names) )

  def read(i, src):
    "For all rows in src, fill in the table."
    for lst in cells(cols(rows(src))):
      if i.cols:
        # lst = [col + x for col,x in zip(i.cols.all,lst)]
        i.rows += [Row(lst)]
      else:
        i.cols = Cols(lst)
    return i

  def decisionTree(i):
    return i.tree(i.rows, 
                y   = lambda z: z.cells[i.cols.klass.pos],
                yis = "Sym")
  def regressionTree(i):
    return i.tree(i.rows,
                y   = lambda z: last(z.cells),
                yis = "Num")

  def showt(tree,pre= '',rnd=THE.tree.rnd):
    # print("Tree: ", tree)
    # most = sorted(x.n for x in tree)[-1]
    for x  in tree:
      after =""
      s = x.txt + ' = ' + str(x.lo)
      if x.n == most:
        after,most = "*", None
      if x.lo != x.hi:
        s += ' .. ' + str(x.hi)
      if isa(x.kids,Thing):
        print(pre + s,after,
              ":",x.kids.middle(rnd),
              '('+str(x.kids.n) +')')
      else:
        print(pre + s,after)
        showt(x.kids,pre + '|   ')

  def tree(i,lst,y,yis,lvl=0):
    if len(lst) >= THE.tree.minObs*2:
      # find the best column
      lo, cut, col = -10**32, None, None
      for col1 in i.cols.indep:
        x = lambda row: row.cells[col1.pos]
        d = Div2(lst, x=x, y=y, yis=yis)
        cut1, lo1 = d.finalcutlow()
        # print(cut1, lo1)
        if cut1:
          if lo1 < lo:
            cut, lo, col = cut1, lo1, col1
            print("updated: ", cut, lo, col)
      # if a cut exists
      if cut:
        # split data on best col, call i.tree on each split
        x = lambda row: row.cells[col.pos]
        return [o(lo   = lo,
                  hi   = hi,
                  n    = len(kids),
                  txt  = col.txt,
                  kids = i.tree(kids,y,yis,lvl+1)
                ) for lo,hi,kids in col.split(lst, x, cut)]
    if yis == "Num":
      return Num(lst,key=y)
    else:
      return Sym(lst,key=y)

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


