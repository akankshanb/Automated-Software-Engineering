from div2 import Div2
# from data1 import data1
# from data2 import data2
from tbl import *
import csv
import sys

def main():
	data = file("auto.csv")
	# data = file("diabetes.csv")

# def callFromHw8(filename):
# 	data = file(filename)

def file(fname):
	"read lines from a file"
	with open(fname) as fs:
		t = Tbl()
		t.read(fs)
		tree  = t.regressionTree()
		# tree  = t.decisionTree()
		t.showt(tree)
		

if __name__ == '__main__':
    main()

