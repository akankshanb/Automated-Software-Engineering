#!/usr/bin/env python3
# vim: sta:et:sw=2:ts=2:sts=2
"""
Store one row of data.
"""

from lib import *

class Row(Pretty):
  def __init__(i, cells=[], cooked=[], dom=0):
    i.cells = cells
    i.cooked = cooked
    i.dom = dom
    i.id = None


