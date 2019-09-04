import math
import random

# class Tbl:
#     list_row = []
#     def addLine(data):
#         row = Row(data)
#         list_row.append(row)
class Col():
    cnt = 0

class Num(Col):
    Col() 
    mu = m2 = sd = 0
    lo = math.pow(10, 32)
    hi = -1 * lo
        
    def NumAdd(self, input_number):
        self.cnt = self.cnt + 1
        if input_number < self.lo:
            self.lo = input_number
        if input_number > self.hi:
            self.hi = input_number
        d = input_number - self.mu
        # For Mean
        self.mu += d/self.cnt
        self.m2 += d * (input_number - self.mu)
        # For Standard deviation
        if self.m2 < 0 or self.cnt < 2:
            self.sd = 0
        else :   
            self.sd = math.pow(self.m2/(self.cnt-1), 0.5)
        return self.mu, self.sd

    def NumRemove(self, input_number):
        if self.cnt < 2:
            self.sd = 0
            return self.mu, self.sd
        self.cnt = self.cnt - 1
        d = input_number - self.mu
        # For Mean
        self.mu -= d/self.cnt
        self.m2 -= d * (input_number - self.mu)
        # For Standard deviation
        if self.m2 < 0 or self.cnt < 2:
            self.sd = 0
        else:   
            self.sd = math.pow(self.m2/(self.cnt - 1), 0.5)
        return self.mu, self.sd

class Sym(Col):
    pass
class Some(Col):
    pass

def main():
    cnt = 100
    N = Num()
    input_numbers = []

    mu_list = []
    sd_list = []
    
    # with open('example.csv') as csvfile:
    #     readCSV = csv.reader(csvfile, delimiter=',')

    sample_string = "1,2,3,4,5"
    sample_list = sample_string.split(",")
    print(sample_list)

    for i in range(cnt):
        input_numbers.append(random.randint(10, 1000))

    for index, input_number in enumerate(input_numbers):
        mu, sd = N.NumAdd(input_number)
        if (index + 1)%10 == 0:
            mu_list.append(mu)
            sd_list.append(sd)
    
    for index in range(cnt - 1, 8, -1):
        if (index + 1)%10 == 0:
            
            mu_compare = mu_list.pop()
            if round(mu_compare, 4) == round(mu, 4):
                print("MU match at index: ", index, "for: ", mu, " and cached: ", mu_compare)
            else:
                print("MU mismatch at index: ", index, "for: ", mu, " and cached: ", mu_compare)

            sd_compare = sd_list.pop()
            if round(sd_compare, 4) == round(sd, 4):
                print("SD match at index: ", index, "for: ", mu, " and cached: ", mu_compare)
            else:
                print("SD mismatch at index: ", index, "for: ", sd, " and cached: ", sd_compare)

        mu, sd = N.NumRemove(input_numbers[index])
if __name__ == '__main__':
    main()
