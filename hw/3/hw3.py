import math
import random
import csv
import cleanData

class Tbl:
    header = [] 
    row_list = []
    col_list = []
    my = {
        "goals": [],
        "xs": [],
        "nums": [],
        "syms": [],
        "weights": []
    }
    def __init__(self,header):
        self.header = header
        for index, header_val in enumerate(header):
            self.CheckHeader(index, header_val)
            col_obj = Col(index, header_val)
            self.col_list.append(col_obj)
            
    def AddRowAndCol(self,row_list):
        row = Row(row_list)
        self.row_list.append(row)
        self.UpdateCol(row_list)
            
    def UpdateCol(self,row_list):
        for index,num in enumerate(row_list):
            try:
                numToAdd = float(self.col_list[index])
                n = Num(self.col_list[index])
                n.NumAdd(numToAdd)
            except:
                sym = Sym(self.col_list[index])
    
    def PrintCols(self):
        for index, column in enumerate(self.col_list):
            print("t.cols")
            print("|   ", index+1)
            column.PrintCol()

    def CheckHeader(self, col_index, header_val):
        print("VAL: ", header_val)
        if any(x in header_val for x in ["<", ">", "$"]):
            if "<" in header_val:
                self.my["weights"].append({ col_index: -1})
            self.my["nums"].append(col_index + 1)
        else:
            self.my["syms"].append(col_index + 1)
        if any(x in header_val for x in ["<", ">", "!"]):
            self.my["goals"].append(col_index + 1)
        else:
            self.my["xs"].append(col_index + 1)
        
    def PrintMy(self):
        print(self.my)
    def PrintRows(self):
        for index, row in enumerate(self.row_list):
            print("|   ", index+1)
            row.PrintRow()

class Abcd():
    known = None
    a = b = c = d = None
    rx = ""
    data = ""
    yes = no = None
    def __init__():
        self.known = {}
        self.a = self.b = self.c = self.d = {}
        self.rx = self.rx if self.rx else "rx"
        self.data = self.data if self.data else "data"
        self.yes = self.no = 0

    def Abcd1(want, got, x):
        # want
        self.known[want] += 1 if want in self.known else 1
        if self.known[want] == 1:
            self.a[want] = self.yes + self.no
            
        # got
        self.known[got] += 1 if got in self.known else 1
        if self.known[got] == 1:
            self.a[got] = self.yes + self.no
        if want == got:
            self.yes += 1
        else:
            self.no += 1

        # check for abcd values
        for x in known:
            if want == x:
                if want == got:
                    self.d += 1
                else:
                    self.b += 1
            else:
                if want == got:
                    self.c += 1
                else:
                    self.a += 1


    def AbcdReport():
        pass

class Col():
    cnt = 0
    txt = None
    mu = m2 = sd = 0
    lo = math.pow(10, 32)
    hi = -1 * lo
    add = None
    # col_type = None
    # goal = None
    weight = 1
    col = 1
    oid = 0
    
    mode = ""
    most = 0
    
    def __init__(self, col_index, txt):
        self.txt = txt
        self.col = col_index + 1


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
        self.add = "Num1"
        
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
    sym_cnt = {}
    def __init__(self, col):
        self.col = col
        self.add = "Sym1"
    
    def SymAdd(self, input_symbol):
        self.col.cnt = self.col.cnt + 1
        if input_symbol in self.sym_cnt:
            self.sym_cnt[input_symbol] = self.sym_cnt[input_symbol] + 1
        else:
            self.sym_cnt[input_symbol] = 1
        tmp = self.sym_cnt[input_symbol]
        if tmp > self.col.most:
            self.col.most = tmp 
            self.col.mode = input_symbol
        return input_symbol

    def SymEnt(self):
        e = p = 0
        for k in self.sym_cnt:
            p = self.sym_cnt[k]/self.col.cnt
            e -= p * math.log10(p)/math.log10(2)
        return e

class Some(Col):
    pass
    
def main():
    """s=
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
    t.PrintMy()
    # c = Col(0, "hello")
    # s = Sym(c)
    # for l in "aaaabbc":
    #     s.SymAdd(l)
    # print("CHECKING: ", s.SymEnt())
if __name__ == '__main__':
    main()
