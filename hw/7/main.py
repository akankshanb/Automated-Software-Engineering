from tbl import *
import csv
import random

def main():
	main_csv = "xomo10000.csv"
	# data2 = file("pom310000.csv")
	data1 = file(main_csv, main_csv, 100000, { "left": "", "right": ""})



def file(fname, main_csv, min_length, tableString):
	"read lines from a file"
	with open(fname) as fs:
		t = Tbl()
		t.read(fs)
		if fname == main_csv:
			min_length = len(list(fs)) ** (1/2)
		# print("Length", len(t.rows))
		
		if len(t.rows)-1 > min_length:
			fastMap(t, tableString)
			# print("check", tableString["left"])
			tableString["left"] += "|. "
			tableString["right"] += "|. "
			data3 = file("left.csv", main_csv, min_length, tableString)
			data4 = file("right.csv", main_csv, min_length, tableString)
		else:
			if fname == "left.csv":
				print("left value: ", tableString["left"])
			else:
				print("right value: ", tableString["right"])

def fastMap(t, tableString):
	table_header = t.header
	best_delta = len(t.rows)
	best_left = None
	best_right = None
	for index in range(10):
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

	# print("left dist: ", len(best_left))
	# print("right dist: ", len(best_left))

	tableString["left"] += "|. " + str(len(best_left)) + "\n"
	tableString["right"] += "|. " + str(len(best_right)) + "\n"
	get_csv("left.csv", best_left)
	get_csv("right.csv", best_right)

def get_csv(csv_text_name, data):
	out = csv.writer(open(csv_text_name,"w"), delimiter=',')
	out.writerows(data)

def findPivots(t, selected_row):
	new_row = None
	dist_list = []
	for new_row in t.rows:
		cal_dist = t.dist(selected_row, new_row, t.cols)
		# print(new_row)
		dist_list.append((cal_dist, new_row))
	dist_list.sort(key=lambda x: x[0])
	new_row = dist_list[int(0.9 * len(dist_list))]
	return new_row

def get_median(new_dist_list):
	half = len(new_dist_list) // 2
	# print("half: ", half)
	if not len(new_dist_list) % 2:
		return (new_dist_list[half - 1][0] + new_dist_list[half][0]) / 2.0
	else:
		return new_dist_list[half][0]
	

if __name__ == '__main__':
    main()

