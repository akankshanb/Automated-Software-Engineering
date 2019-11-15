#!/usr/bin/env python3 -B
# vim: sta:et:sw=2:ts=2:sts=2

from tbl import *

if __name__ == "__main__" :
  t=Tbl()
  t.read(file('../data/weathernom.csv'))
  for x in t.cols.all:
    print(x)
