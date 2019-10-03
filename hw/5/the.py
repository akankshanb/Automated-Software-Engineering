#!/usr/bin/env python3
# vim: sta:et:sw=2:ts=2:sts=2
"""
Config options
"""

from boot import *

THE= o( 
  char = o( sep = ",",
            num = "$",
            less = "<",
            more = ">",
            skip = "?",
            klass= "!",
            doomed = r'([\n\t\r ]|#.*)'),
  div  = o( trivial = 1.025, 
            cohen   = 0.3, 
            min     = 0.5)
)
