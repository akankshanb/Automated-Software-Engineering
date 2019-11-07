from tbl import *
import csv
import random
import sys
from hw7 import Centroids
from pytablewriter import MarkdownTableWriter

def main():
	main_csv = "auto.csv"
	data1 = file(main_csv)


def file(fname):
	clusterDict = {}
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

		# Print dominating values 
		writer = MarkdownTableWriter()
		writer.table_name = "Row Best rest"
		writer.headers = t.header
		writer.value_matrix = bestlist
		writer.write_table()

		c = Centroids()
		centroidList = c.getCentroids()
		rowList = []
		for centerList in centroidList:
			mulist = list(map(lambda x : x.mu, centerList))
			rowList += [mulist]
		
		get_csv("cent.csv", rowList)
		with open("cent.csv") as fs:
			tc = Tbl()
			tc.read(fs)
			for index, selected_row in enumerate(t.rows):
				clusterDict[index] = {}
				clusterDict[index]["row"] = selected_row
				getMostEnvy(t, clusterDict[index])
			
			print("Clusters :", clusterDict)

				
def getMostEnvy(t, centroidDict):
	selected_row = centroidDict["row"]
	# Do not call t.rows here. Our rowlist is list of centroids
	mostEnvy = -100000
	envyRow = None
	for new_row in t.rows:
		delta = t.dist(selected_row, new_row, t.cols)
		epsilon = t.dominates(selected_row, new_row, t.cols.goals)
		envy = (1-delta)-epsilon
		if envy > mostEnvy:
			mostEnvy = envy
			envyRow = new_row

	centroidDict["mostEnvy"] = envy
	centroidDict["mostEnvyRow"] = envyRow
	return centroidDict
	
def get_csv(csv_text_name, data):
	out = csv.writer(open(csv_text_name,"w"), delimiter=',')
	out.writerows(data)

if __name__ == '__main__':
    main()

