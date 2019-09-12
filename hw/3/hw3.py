import math
import random
import csv
import cleanData
from prettytable import PrettyTable 
ptable = PrettyTable()

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
                numToAdd = float(num)
                n = Num(self.col_list[index])
                n.NumAdd(numToAdd)
            except:
                symToAdd = num
                s = Sym(self.col_list[index])
                s.SymAdd(symToAdd)
    
    def PrintCols(self):
        for index, column in enumerate(self.col_list):
            print("t.cols")
            print("|   ", index+1)
            column.PrintCol()

    def CheckHeader(self, col_index, header_val):
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
        print("t.my")
        for my_val in self.my:
            print("|   ")
            print(my_val)
            print("|   ", self.my[my_val])
            
    def PrintRows(self):
        for index, row in enumerate(self.row_list):
            print("|   ", index+1)
            row.PrintRow()

class Abcd():
    known = None
    a = b = c = d = None
    rx = ""
    data = ""
    # output_types = {}
    yes = no = None

    def __init__(self):
        self.known = {}
        self.a = {}
        self.b = {}
        self.c = {}
        self.d = {}
        self.rx = self.rx if self.rx else "rx"
        self.data = self.data if self.data else "data"
        # self.output_types.yes = 0
        # self.output_types.no = 0
        self.yes = self.no = 0

    def Abcd1(self, want, got):
        # if not want in self.output_types:
        #     self.output_types[want] = 1
        # if not got in self.output_types:
        #     self.output_types[got] = 1

        if not want in self.a:
            self.a[want] = 0
        if not want in self.b:
            self.b[want] = 0
        if not want in self.c:
            self.c[want] = 0
        if not want in self.d:
            self.d[want] = 0
        if not got in self.a:
            self.a[got] = 0
        if not got in self.b:
            self.b[got] = 0
        if not got in self.c:
            self.c[got] = 0
        if not got in self.d:
            self.d[got] = 0

        # want
        if want in self.known:
            self.known[want] += 1
        else:
            self.known[want] = 1

        if self.known[want] == 1:
            self.a[want] = self.yes + self.no
            
        # got
        if got in self.known:
            self.known[got] += 1
        else:
            self.known[got] = 1

        if self.known[got] == 1:
            self.a[got] = self.yes + self.no
        if want == got:
            self.yes += 1
        else:
            self.no += 1

        # check for abcd values
        for x in self.known:
            if want == x:
                if want == got:
                    self.d[x]+=1
                else:
                    self.b[x]+=1
            else:
                if x == got:
                    self.c[x]+=1
                else:
                    self.a[x]+=1

    def AbcdReport(self):
        ptable.field_names = ["db", "rx", "num", "a", "b", "c", "d", "acc", "pre", "pd", "pf", "f", "g", "class"]

        for x in self.known:
            pd = pf = pn = prec = g = f = acc = 0
            a = self.a[x]
            b = self.b[x]
            c = self.c[x]
            d = self.d[x]
            
            if b+d > 0:
                pd = d/(b+d)
            if a+c > 0:
                pf = c/(a+c)
                pn = (b+d)/(a+c)
            if c+d > 0:
                prec = d/(c+d)
            if 1-pf+pd>0:
                g = (2*(1-pf)*pd)/(1-pf+pd)
            if prec+pd > 0:
                f = 2*(prec*pd)/(prec+pd)
            if self.yes + self.no > 0:
                acc = self.yes/(self.yes+self.no)
            ptable.add_row([self.data, self.rx, (self.yes+self.no), a, b, c, d, round(acc, 2), round(prec, 2), round(pd, 2), round(pf, 2), round(f, 2), round(g, 2), x])
        print(ptable)

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
    oid = 1
    
    sym_cnt = None
    mode = ""
    most = 0
    
    def __init__(self, col_index, txt):
        self.txt = txt
        self.sym_cnt = {}
        self.oid = col_index + 1
        self.col = col_index + 1


    def PrintCol(self):
        print("|    |   add: ", self.add)
        print("|    |   col: ", self.col)
        if self.add is "Num1":
            print("|    |   hi: ", self.hi)
            print("|    |   lo: ", self.lo)
            print("|    |   m2: ", self.m2)
            print("|    |   mu: ", self.mu)
            print("|    |   sd: ", self.sd)
            
        if self.add is "Sym1":
            print("|    |   cnt: ", self.sym_cnt)
            print("|    |   mode: ", self.mode)
            print("|    |   most: ", self.most)

        print("|    |   n: ", self.cnt)
        print("|    |   oid: ", self.oid+1)
        print("|    |   txt: ", self.txt)

class Row():
    def __init__(self, row):
        self.row = row
    def PrintRow(self):
        print()

class Num(Col):
    def __init__(self, col):
        self.col = col
        self.col.add = "Num1"
        
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
    def __init__(self, col):
        self.col = col
        self.col.add = "Sym1"
    
    def SymAdd(self, input_symbol):
        self.col.cnt = self.col.cnt + 1
        if input_symbol in self.col.sym_cnt:
            self.col.sym_cnt[input_symbol] = self.col.sym_cnt[input_symbol] + 1
        else:
            self.col.sym_cnt[input_symbol] = 1
        tmp = self.col.sym_cnt[input_symbol]
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
    # Running My for symbols in Col (output 1)
    f = "table.csv"
    index_flag = True
    for row in cleanData.file(f):
        if(index_flag==True):
            t = Tbl(row)
            index_flag = False
        else:
            t.AddRowAndCol(row)
    t.PrintCols()
    print("\n")
    t.PrintMy()

    # Running Abcd for prediction (output 2)
    abcd = Abcd()
    for i in range(1, 7):
        abcd.Abcd1("yes", "yes")
    for i in range(1, 3):
        abcd.Abcd1("no", "no")
    for i in range(1, 6):
        abcd.Abcd1("maybe", "maybe")
    abcd.Abcd1("maybe", "no")
    abcd.AbcdReport()
if __name__ == '__main__':
    main()
