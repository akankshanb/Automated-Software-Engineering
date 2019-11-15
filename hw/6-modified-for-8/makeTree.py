from div2 import Div2
# from data1 import data1
# from data2 import data2
from tbl import *
import csv
import sys

def callFromHw8(filename):
	data = file(filename)

def file(fname):
	"read lines from a file"
	with open(fname) as fs:
		# print("hw6 modified")
		t = Tbl()
		t.read(fs)
		tree  = t.regressionTree()
		# print(tree)
		# tree  = t.decisionTree()
		t.showt(tree)
		

