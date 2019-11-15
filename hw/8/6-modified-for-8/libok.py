#!/usr/bin/env python3
# vim: sta:et:sw=2:ts=2:sts=2

from lib import *

if __name__ == "__main__":
  print(cli())
  for l in file("lib.py"):
    print("["+l+"]")
