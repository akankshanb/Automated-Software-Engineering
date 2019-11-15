import csv
import random
import sys
from hw7 import Centroids
from pytablewriter import MarkdownTableWriter
sys.path.insert(0, '../6-modified-for-8/')
from makeTree import callFromHw8
from tbl import *


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

		# # Print dominating values 
		# writer = MarkdownTableWriter()
		# writer.table_name = "Row Best rest"
		# writer.headers = t.header
		# writer.value_matrix = bestlist
		# writer.write_table()

		c = Centroids()
		centroidList = c.getCentroids()

		rowList = []
		clusterList = []
		for index, centerData in enumerate(centroidList):
			mulist = list(map(lambda x : x.mu, centerData["centroid"]))
			rowList += [mulist]
			clusterList += [centerData["clusterData"]]
			
		get_csv("cent.csv", rowList)
		with open("cent.csv") as fs:
			tc = Tbl()
			tc.read(fs)
			for index, selected_row in enumerate(tc.rows):
				clusterDict[index] = {}
				clusterDict[index]["row"] = selected_row
				
				# get most envious centroid for the given centroid 
				getMostEnvy(tc, clusterDict[index])
				envyIndex = clusterDict[index]["mostEnvyIndex"]
				clusterListNew = clusterList[index] + clusterList[envyIndex][1:]
				# print(len(clusterListNew))

				# get cluster data for both the given centroids
				clusterName = "cluster" + str(index)
				get_csv(clusterName, clusterListNew)
			
			# get tree for each cluster thus formed
			for index, selected_row in enumerate(tc.rows):
				clusterName = "cluster" + str(index)
				print("----------- TREE " + str(index) + " -------------")
				callFromHw8(clusterName)
				# break

			
def get_csv(csv_text_name, data):
	out = csv.writer(open(csv_text_name,"w"), delimiter=',')
	out.writerows(data)

def getMostEnvy(tc, centroidDict):
	selected_row = centroidDict["row"]
	mostEnvy = -100000
	envyRow = None
	envyIndex = None

	for index, new_row in enumerate(tc.rows):
		delta = tc.dist(selected_row, new_row, tc.cols)
		epsilon = tc.dominates(selected_row, new_row, tc.cols.goals)
		envy = (1-delta)-epsilon
		if envy > mostEnvy:
			mostEnvy = envy
			envyRow = new_row
			envyIndex = index
			# envyClusterData = clusterDict[index]

	centroidDict["mostEnvy"] = envy
	centroidDict["mostEnvyRow"] = envyRow
	centroidDict["mostEnvyIndex"] = envyIndex
	return centroidDict
	

if __name__ == '__main__':
    main()

