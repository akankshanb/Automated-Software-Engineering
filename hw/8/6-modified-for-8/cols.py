#!/usr/bin/env python3
# vim: sta:et:sw=2:ts=2:sts=2
"""
Convert a list of column names into Sym or Num objects.
"""
from lib import *
from thing import Num,Sym

class Cols(Pretty):
  def __init__(i,inits=[]):
    i.all   = []
    i.nums  = []
    i.syms  = []
    i.names = inits
    i.indep = []
    i.klass = None
    i.xnums = []
    i.xsyms = []
    i.goals = []
    i.w = 1
    [i.add(pos,txt) for pos,txt in enumerate(inits)]

  def klassp(i,x):
    return THE.char.klass in x

  def nump(i,x):
    for y in [THE.char.less, THE.char.more, THE.char.num]:    
      if y in x: return True
    return False

  def dep(i,x):
    for y in [THE.char.less, THE.char.more, THE.char.klass]: 
      if y in x: return True
    return False

  def weight(i,x):
    return  -1 if THE.char.less in x else 1

  def add(i,pos,txt):
    klass  = Num if i.nump(txt) else Sym
    tmp    = klass(txt=txt, pos=pos, w=i.weight(txt))
    # tmp.__add__()
    i.all += [tmp]
    i.w = i.weight(txt)
    if i.klassp(txt): i.klass=tmp
    what   = i.nums if i.nump(txt) else i.syms
    what  += [tmp]
    if not i.dep(txt):
      i.indep += [tmp]
      what     = i.xnums if i.nump(txt) else i.xsyms
      what    += [tmp]
    else:
      i.goals += [tmp]


