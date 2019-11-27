from tbl import *
import csv
import random
num_times = 1
after_num = 1
leaf_num_runs = 1
inc_num = 50
inc_num_end = 100

centroidRows = {
	"BEFORE": [],
	"AFTER": [],
	"allTable": [],
	"incTable": []
}

class PTree:
	def __init__(i, tag, isRoot=False):
		i.left = None
		i.right = None
		i.isRoot = isRoot
		i.level = 0
		i.rowCnt = 0
		i.tbl = None
		i.childType = ""
		i.clusterData = []
		i.tag = tag

	def printTree(i, pTree):
		if not i.isRoot:
			for _ in range(i.level):
				print ("|. ", end =" ")
		print (pTree.rowCnt)
		if pTree.left:
			pTree.printTree(pTree.left)

		if pTree.right:
			pTree.printTree(pTree.right)

		if not pTree.right and not pTree.left:
			for _ in range(i.level):
				print ("|. ", end =" ")
			for col in pTree.tbl.cols.nums[-4:]:
				print(col.txt, end =" ")
				if (isinstance(col, Num)):
					print ("{0:.2f} ({1:.2f})".format(col.mu, col.sd()), end =" ")
					centroidRows[i.tag].append(col)
				else:
					print ("{0:.2f} ({1:.2f})".format(col.mode, col.entropy), end =" ")
					centroidRows[i.tag].append(col)
			print()

	def getLeafClusters(i, pTree):
		if pTree.left:
			pTree.getLeafClusters(pTree.left)

		if pTree.right:
			pTree.getLeafClusters(pTree.right)

		if not pTree.right and not pTree.left:
			centroidRows[i.tag].append({
				"clusterData": pTree.clusterData,
				"centroid": pTree.tbl.cols.nums
			})

def main():
	main_csv = "xomo10000.csv"
	# main_csv = "pom310000.csv"

	# Create 1 tree for BEFORE probe
	nodeBefore = PTree("BEFORE", True)
	data1 = file(main_csv, main_csv, 100000, nodeBefore, "BEFORE")
	nodeBefore.getLeafClusters(nodeBefore)
	# print("Cent bef len: ", len(centroidRows["BEFORE"]))

	# ALL: Create 20 AFTER probes
	baseline = 0
	for index in range(after_num):
		centroidRows["AFTER"] = []
		nodeAfter = PTree("AFTER", True)
		data1 = file(main_csv, main_csv, 100000, nodeAfter, "AFTER")
		nodeAfter.getLeafClusters(nodeAfter)
		# print("Cent aft len: ", len(centroidRows["AFTER"]))
		# select leaf cluster of before trees

		trueTotal = 0
		for leafIndex in range(leaf_num_runs): # ideally 100
			beforeLeaf = centroidRows["BEFORE"][random.randint(0, len(centroidRows["BEFORE"]))-1]
			afterLeaf = centroidRows["AFTER"][random.randint(0, len(centroidRows["AFTER"]))-1]
			# print("rand: ", beforeLeaf["centroid"])
			sameValueList = []
			for centIndex, centroidNum in enumerate(beforeLeaf["centroid"]):
				sameValueList += [centroidNum.same(afterLeaf["centroid"][centIndex])]
			trueTotal += sameValueList.count(True)
			# print("truetotal: ", trueTotal)

		trueTotal = trueTotal/leaf_num_runs
		baseline += trueTotal

	baseline = baseline/after_num
	print("All Baseline: ", baseline)





	# INCREMENTAL: Create 20 AFTER probes - TODO

	data500 = 'data-500.csv'
	with open(main_csv, 'r') as r, open(data500, 'w') as w:
		data = r.readlines()
		header, rows = data[0], data[1:5001]
		random.shuffle(rows)
		requiredRows = '\n'.join([rows[rowIndex].strip() for rowIndex in range(inc_num)])
		incRows = '\n'.join([rows[rowIndex].strip() for rowIndex in range(inc_num, inc_num_end)])
		w.write(header + incRows)

	# for index in range(after_num):
	# 	centroidRows["AFTER"] = []
	# 	nodeAfter = PTree("AFTER", True)
	# 	data1 = file(data500, data500, 500, nodeAfter, "AFTER")
	# 	nodeAfter.getLeafClusters(nodeAfter)
	# 	# print("Cent aft len: ", len(centroidRows["AFTER"]))
	# 	# select leaf cluster of before trees

	# 	trueTotal = 0
	# 	for leafIndex in range(leaf_num_runs): # ideally 100
	# 		beforeLeaf = centroidRows["BEFORE"][random.randint(0, len(centroidRows["BEFORE"]))-1]
	# 		afterLeaf = centroidRows["AFTER"][random.randint(0, len(centroidRows["AFTER"]))-1]
	# 		# print("rand: ", beforeLeaf["centroid"])
	# 		sameValueList = []
	# 		for centIndex, centroidNum in enumerate(beforeLeaf["centroid"]):
	# 			sameValueList += [centroidNum.same(afterLeaf["centroid"][centIndex])]
	# 		trueTotal += sameValueList.count(True)
			# print("truetotal: ", trueTotal)

		# trueTotal = trueTotal/leaf_num_runs
	# 	# baseline += trueTotal

	# baseline = baseline/after_num
	# print("Inc Baseline: ", baseline)
	# ^^ TODO ^^



def file(fname, main_csv, min_length, pTree, tag):
	"read lines from a file"
	with open(fname) as fs:
		# print("hw7 print")
		t = Tbl()
		t.read(fs)
		t.tag = tag
		pTree.tbl = t
		pTree.rowCnt = len(t.rows)
		if fname == main_csv:
			min_length = len(t.rows) ** (1/2)
		
		if len(t.rows)-1 > min_length:
			fastMap(t, pTree)
			levelAppender =  str(pTree.level + 1) + ".csv"
			data3 = file("left" + levelAppender, main_csv, min_length, pTree.left, tag)
			data4 = file("right" + levelAppender, main_csv, min_length, pTree.right, tag)


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

	pTree.left = PTree(pTree.tag)
	pTree.left.level = pTree.level + 1
	pTree.left.childType = "left"
	pTree.left.clusterData = best_left
	get_csv("left" + levelAppender, best_left)

	pTree.right = PTree(pTree.tag)
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

