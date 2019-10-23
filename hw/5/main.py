from div2 import Div2
from data1 import data1
from data2 import data2

def main():

	# data = xnum()
	dNum = Div2(data1, "first", "last", "Num")
	dNum.printValues()

	dSym = Div2(data2, "first", "last", "Sym")
	dSym.printValues()

if __name__ == '__main__':
    main()

