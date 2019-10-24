from div2 import Div2
from data1 import data1
from data2 import data2
from tbl import *
import csv


def main():
	data = file("hw/6/diabetes.csv")
	# data = file("diabetes.csv")
	# hw/6/diabetes.csv


def file(fname):
	"read lines from a file"
	with open(fname) as fs:
		t = Tbl()
		t.read(fs)
		tree  = t.regressionTree()
		# print(tree)
		t.showt(tree)
		
		

if __name__ == '__main__':
    main()

