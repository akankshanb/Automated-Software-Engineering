import re

def compiler(x):
  "return something that can compile strings of type x"
  try: int(x); return  int(x)
  except:
    try: float(x); return  float(x)
    except : return str(x)

def string(s):
  "read lines from a string"
  for line in s.splitlines(): yield line

def file(fname):
  "read lines from a file"
  with open(fname) as fs:
    for line in cells(cols(rows(fs))): yield line


def rows(src, 
         sep=     ",",
         doomed = r'([\n\t\r ]|#.*)'):
  "convert lines into lists, killing whitespace and comments"
  for line in src:
    line = line.strip()
    line = re.sub(doomed, '', line)
    if line:
        yield line.split(sep)
      
def cols(src, sep=     ",",doomed = r'([\n\t\r ]|#.*)'):
    new_src = list(src)
    for index, header in enumerate(new_src[0]):
        if "?" in header:
            for row in new_src:
                del row[index]
    for line in new_src:
        yield line

def cells(src):
  "convert strings into their right types"
  for n,cells in enumerate(src):
    if n==0:
       yield cells
    else:
        new_cell = []
        for cell in cells:
            new_cell.append(compiler(cell))
        yield [cell for cell in new_cell]

def fromString(s):
    for lst in cells(cols(rows(string(s)))):
        yield lst

if __name__=="__main__":
    f = "table.csv"
    s="""
    $cloudCover, $temp, ?$humid, $wind,  $playHours
    100,        23,    10,    0,    3  # comments
   
    0,          ?,    90,    10,   0
    60,         83,    86,    0,    4
    100,        70,    96,    0,    3
    100,        65,    70,    20,   0
    70,         64,    65,    15,   5
    0,          72,    95,    0,    0
    0,          69,    70,    0,    4,8
    80,          75,    80,    0,    3  
    0,          75,    70,    18,   4
    60,         72,    90,    10,   4
    40,         81,    75,    0,    2    
    100,        71,    91,    15,   0
    """
    len_first = 0
    for index, lst in enumerate(file(f)):
        if index == 0:
            len_first = len(lst)
        if len(lst) > len_first:
            print("skipping line: ", index)
        else:
            print(lst)
        