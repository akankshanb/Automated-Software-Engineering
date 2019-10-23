class Abcd():
    known = None
    a = b = c = d = None
    rx = ""
    data = ""
    # output_types = {}
    yes = no = None
    learn = wait = train = classify = None
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
        self.goal_index = None
        self.train = None
        self.classify = None
        self.learn = {
            "Train": "",
            "Classify": ""
        }
        self.wait = 4

    def Abcd1(self, want, got):

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

    def Abcds(self, learn, wait, classifier_class):
        # self.train = train
        self.train = self.learn["Train"] if classifier_class == None else classifier_class.train
        self.classify = self.learn["Classify"] if classifier_class == None else classifier_class.classify
        self.wait = 4 if wait == None else wait
        self.goal_index = classifier_class.tbl.my["goals"][0]

    def Abcds1(self, row_index, lst):
        # if row_index%self.wait == 0:
        if row_index > self.wait:
            got = self.classify(row_index, lst, "")
            want = lst[self.goal_index]
            self.Abcd1(want, got)
        self.train(row_index, lst)

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
