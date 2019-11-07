from tbl import *
import csv
import random
num_times = 10
	
from pytablewriter import MarkdownTableWriter

def main():
	main_csv = "auto.csv"
	data1 = file(main_csv)


def file(fname):
	"read lines from a file"
	with open(fname) as fs:
		t = Tbl()
		t.read(fs)
		# print("len: ", len(t.rows))
		for index, row in enumerate(t.rows):
			newRowList = t.rows.copy()
			del newRowList[index]
			# print("len", len(t.rows))
			sampling = random.choices(newRowList, k=100)
			# print("len1", len(sampling))
			domCount = 0

			for sample in sampling:
				goals = t.cols.goals
				# print("goals: ", goals)
				domValue = t.dominates(row, sample, goals)
				if domValue < 0:
					domCount += 1 

			row.dom = domCount

		# sort all rows on this count
		t.rows.sort(key=lambda x: x.dom)
		bestlist = list(map(lambda x : x.cells, t.rows))
		bestlist = bestlist[-4:] + bestlist[0:4]
		writer = MarkdownTableWriter()
		writer.table_name = "Row Best rest"
		writer.headers = t.header
		writer.value_matrix = bestlist

		writer.write_table()



				

if __name__ == '__main__':
    main()

