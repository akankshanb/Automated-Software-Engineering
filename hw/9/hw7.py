import sys
sys.path.insert(0, '6-modified-for-8/')
from tbl import *
import csv
import random
num_times = 10
centroidRows = []

class PTree:
	def __init__(i, isRoot=False):
		i.left = None
		i.right = None
		i.isRoot = isRoot
		i.level = 0
		i.rowCnt = 0
		i.tbl = None
		i.childType = ""
		i.clusterData = []

	def printTree(i, pTree):
		# if not i.isRoot:
			# for _ in range(i.level):
				#print ("|. ", end =" ")
		#print (pTree.rowCnt)
		if pTree.left:
			pTree.printTree(pTree.left)

		if pTree.right:
			pTree.printTree(pTree.right)

		if not pTree.right and not pTree.left:
			# for _ in range(i.level):
				#print ("|. ", end =" ")
			# print("CHECK: ", len(pTree.clusterData))
			centroidRows.append({
				"clusterData": pTree.clusterData,
				"centroid": pTree.tbl.cols.nums
			})
			# print(centroidRows[0])
			# for col in pTree.tbl.cols.nums:
			# 	print(col.txt, end =" ")
				# if (isinstance(col, Num)):
					#print ("{0:.2f} ({1:.2f})".format(col.mu, col.sd()), end =" ")
				# else:
					#print ("{0:.2f} ({1:.2f})".format(col.mode, col.entropy), end =" ")
			#print()

class Centroids:
	def getCentroids(i):
		main()
		return centroidRows

def main():
	centroidRows = []
	# main_csv = "xomo10000.csv"
	main_csv = "auto.csv"
	node = PTree(True)
	data1 = file(main_csv, main_csv, 100000, node)
	node.printTree(node)


def file(fname, main_csv, min_length, pTree):
	"read lines from a file"
	with open(fname) as fs:
		t = Tbl()
		t.read(fs)
		pTree.tbl = t
		pTree.rowCnt = len(t.rows)
		if fname == main_csv:
			min_length = len(t.rows) ** (1/2)
		
		if len(t.rows)-1 > min_length:
			fastMap(t, pTree)
			levelAppender =  str(pTree.level + 1) + ".csv"
			data3 = file("left" + levelAppender, main_csv, min_length, pTree.left)
			data4 = file("right" + levelAppender, main_csv, min_length, pTree.right)


def fastMap(t, pTree):
	table_header = t.header
	best_delta = len(t.rows)
	best_left = None
	best_right = None
	for index in range(num_times):
		r_index = random.randint(0, len(t.rows)-1)
		selected_row = t.rows[r_index]
		pivot1 = findPivots(t, selected_row)
		pivot2 = findPivots(t, pivot1[1])

		new_dist_list = []
		for new_row in t.rows:
			cos_distance = t.cos(pivot1[1], pivot2[1], new_row, pivot2[0], t.cols)
			# print("cost dist: ", cos_distance)
			new_dist_list.append((cos_distance, new_row))
		new_dist_list.sort(key=lambda x: x[0])
		median = get_median(new_dist_list)
		# print("med: ", median)
		left = []
		right = []
		left.append(table_header)
		# print("value ", table_header)
		right.append(table_header)
		for cos_dist in new_dist_list:
			if cos_dist[0] <= median:
				left.append(cos_dist[1].cells)
			else:
				right.append(cos_dist[1].cells)
		iter_delta = abs(len(right) - len(left))
		
		if iter_delta < best_delta:
			best_delta = iter_delta
			best_left = left
			best_right = right

	levelAppender =  str(pTree.level + 1) + ".csv"

	pTree.left = PTree()
	pTree.left.level = pTree.level + 1
	pTree.left.childType = "left"
	pTree.left.clusterData = best_left
	# print("check: ", best_left)
	get_csv("left" + levelAppender, best_left)

	pTree.right = PTree()
	pTree.right.level = pTree.level + 1
	pTree.right.childType = "right"
	pTree.right.clusterData = best_right
	get_csv("right" + levelAppender, best_right)




def get_csv(csv_text_name, data):
	out = csv.writer(open(csv_text_name,"w"), delimiter=',')
	out.writerows(data)

def findPivots(t, selected_row):
	new_row = None
	dist_list = []
	for new_row in t.rows:
		cal_dist = t.dist(selected_row, new_row, t.cols)
		dist_list.append((cal_dist, new_row))
	dist_list.sort(key=lambda x: x[0])
	new_row = dist_list[int(0.9 * len(dist_list))]
	return new_row

def get_median(new_dist_list):
	half = len(new_dist_list) // 2
	if not len(new_dist_list) % 2:
		return (new_dist_list[half - 1][0] + new_dist_list[half][0]) / 2.0
	else:
		return new_dist_list[half][0]
	

if __name__ == '__main__':
    main()

