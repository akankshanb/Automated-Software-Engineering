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
        lst = [col + x for col,x in zip(i.cols.all,lst)]
        i.rows += [Row(lst)]
      else:
        i.cols = Cols(lst)
    return i

  def decisionTree(i):
    return i.tree(i.rows,
                y   = lambda z: z.cells[i.cols.klass.pos],
                yis = Sym)
  def regressionTree(i):
    # print("COL: ", i.cols)
    return i.tree(i.rows,
                y   = lambda z: last(z.cells),
                yis = Num)

  def showt(i, tree, pre= '',rnd=THE.tree.rnd):
    for branch in tree:
      x = branch
      mostl = sorted(x.n for x in x.cols.all)[-1]
      after =""
      s = x.txt + ' = ' + str(x.lo)
      if x.n == mostl:
        after,mostl = "*", None
      if x.lo != x.hi:
        s += ' .. ' + str(x.hi)
        if isa(x.kids,Num):
          print(pre + s,after,
                '('+str(x.kids.n) +')')
        elif isa(x.kids,Sym):
          if x.test == "positive":
            s += "tested_positive"
          else:
            s += "tested_negative"
          print(pre + s,after,
                '('+str(x.kids.n) +')')
        else:
          print(pre + s,after,
                '('+str(x.n) +')')
        print("")
      else:
        print(pre + s,after)
      
      # print("lvl: ", tree[branch].lvl)
      for y in range(branch.lvl):
        print(pre, end="")

      # if x.kids:
      if not isa(x.kids,Num):
        i.showt(x.kids, '|   ')

  def xfunction(row, pos):
    return row.cells[pos]

  def tree(i,row_lst,y,yis,lvl=0):
    # print("list: ", lst)
    if len(row_lst) >= THE.tree.minObs*2:
      # find the best column
      lo, cut, col = 10**32, None, None
      for col1 in i.cols.indep:
        # print("row: ", row_lst)
        x = lambda row: row.cells[col1.pos]
        d = Div2(row_lst, x=x, y=y, yis=yis)
        cut1, lo1 = d.finalcutlow()
        if cut1:
          if lo1 < lo:
            cut, lo, col = cut1, lo1, col1
      # if a cut exists
      if cut:
        # split data on best col, call i.tree on each split
        x = lambda row: row.cells[col.pos]
        if yis == Sym:
          test = i.cols.dep[0]
        return [o(lo   = lo,
                hi   = hi,
                n    = len(kids),
                txt  = col.txt,
                cols  = i.cols,
                lvl = lvl,
                test = "test",
                kids = i.tree(kids,y,yis,lvl+1)
              ) for lo,hi,kids in col.split(row_lst, cut, col)]
    return yis(row_lst,key=y)

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



