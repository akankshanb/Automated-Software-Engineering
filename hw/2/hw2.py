import math
import random
import csv
import cleanData

class Tbl:
    header = [] 
    row_list = []
    col_list = []
    invalid_cols = []
    def __init__(self,header):
        self.header = header
        for index, header_val in enumerate(header):
            col_obj = Col(index, header_val)
            self.col_list.append(col_obj)
            

    def AddRowAndCol(self,row_list):
        row = Row(row_list)
        self.row_list.append(row)
        self.UpdateCol(row_list)
            

    def UpdateCol(self,num_list):
        for index,num in enumerate(num_list):
            n = Num(self.col_list[index])
            try:
                n.NumAdd(float(num))
            except:
                print("You dont want to add strings now.. do you??")
    
    def PrintCols(self):
        for index, column in enumerate(self.col_list):
            print("|   ", index+1)
            column.PrintCol()

    def PrintRows(self):
        for index, row in enumerate(self.row_list):
            print("|   ", index+1)
            row.PrintRow()

class Col():
    cnt = 0
    txt = None
    mu = m2 = sd = 0
    lo = math.pow(10, 32)
    hi = -1 * lo
    add = "Num1"
    col = 1
    oid = 0

    def __init__(self, col_index, txt):
        self.txt = txt
        self.col = col_index + 1

    # def addNum(self, input_num):
        # self.cnt += 1
    #     self.col_list.append(input_num)

    def PrintCol(self):
        print("|    |   add: ", self.add)
        print("|    |   col: ", self.col)
        print("|    |   hi: ", self.hi)
        print("|    |   lo: ", self.lo)
        print("|    |   m2: ", self.m2)
        print("|    |   mu: ", self.mu)
        print("|    |   n: ", self.cnt)
        print("|    |   oid: ", self.oid)
        print("|    |   sd: ", self.sd)
        print("|    |   txt: ", self.txt)

class Row():
    def __init__(self, row):
        self.row = row
    def PrintRow(self):
        print()

class Num(Col):
    def __init__(self, col):
        self.col = col
    # mu = m2 = sd = 0
    # lo = math.pow(10, 32)
    # hi = -1 * lo
        
    def NumAdd(self, input_number):
        self.col.cnt = self.col.cnt + 1
        if input_number < self.col.lo:
            self.col.lo = input_number
        if input_number > self.col.hi:
            self.col.hi = input_number
        d = input_number - self.col.mu
        # For Mean
        self.col.mu += d/self.col.cnt
        self.col.m2 += d * (input_number - self.col.mu)
        # For Standard deviation
        if self.col.m2 < 0 or self.col.cnt < 2:
            self.col.sd = 0
        else :   
            self.col.sd = math.pow(self.col.m2/(self.col.cnt-1), 0.5)
        # self.PrintCol()
        return self.col.mu, self.col.sd

    def NumRemove(self, input_number):
        if self.col.cnt < 2:
            self.col.sd = 0
            return self.col.mu, self.col.sd
        self.col.cnt = self.col.cnt - 1
        d = input_number - self.col.mu
        # For Mean
        self.col.mu -= d/self.col.cnt
        self.col.m2 -= d * (input_number - self.col.mu)
        # For Standard deviation
        if self.col.m2 < 0 or self.col.cnt < 2:
            self.col.sd = 0
        else:   
            self.col.sd = math.pow(self.col.m2/(self.col.cnt - 1), 0.5)
        return self.col.mu, self.col.sd

class Sym(Col):
    pass
class Some(Col):
    pass

def main():
    
    # with open('table.csv','r') as csvfile:
    #     readCSV = csv.reader(csvfile, delimiter=',')
    #     index_flag = True
    #     for row in readCSV:
    #         if(index_flag==True):
    #             t = Tbl(row)
    #             index_flag = False
    #         else:
    #             t.AddRowAndCol(row)
    #     t.PrintCols()
    s="""
        $cloudCover, $temp, ?$humid, $wind,  $playHours
        100,        68,    80,    0,    3   # comments
        0,          85,    85,    0,    0
        0,          80,    90,    10,   0
        60,         83,    86,    0,    4
        100,        70,    96,    0,    3
        100,        65,    70,    20,   0
        70,         64,    65,    15,   5
        0,          72,    95,    0,    0
        0,          69,    70,    0,    4
        80,          75,    80,    0,    3  
        0,          75,    70,    18,   4
        60,         72,    90,    10,   4
        40,         81,    75,    0,    2    
        100,        71,    91,    15,   0
        """
    f = "table.csv"
    index_flag = True
    for row in cleanData.file(f):
        if(index_flag==True):
            t = Tbl(row)
            index_flag = False
        else:
            t.AddRowAndCol(row)
    t.PrintCols()
if __name__ == '__main__':
    main()
