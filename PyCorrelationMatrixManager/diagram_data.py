import os
import numpy as np
from functools import reduce

# DT and T data in a dictionary CAN become quite slow!
# If updating storage of dt/t data to a np.array - need a different merge method
class DiagramData:
    def __init__(self, filenames):
        self.diagram_data = {}
        for filename in filenames: 
            new_data = DiagramFileLoader(filename).data
            merge(self.diagram_data, new_data)

class DiagramFileLoader:
    def __init__(self, filename):
        if not os.path.exists(filename):
            raise SystemError("File does not exist!  Tried loading {}".format(filename))
        else:
            self.data = self.load_diagram_file(filename)

    def load_diagram_file(self,filename):
        self.diagram_data={}

        with open(filename, "r") as file:
            current_diagram=None
            for line in file:
                if line[0]=="B":
                    current_diagram=line
                    self.diagram_data[current_diagram]={}
                else:
                    data=line.split(' ')
                    dt=int(data[0])
                    t=int(data[1])
                    value=complex(float(data[2]),float(data[3]))
                    
                    if dt in self.diagram_data[current_diagram]:
                        self.diagram_data[current_diagram][dt][t]=value
                    else:
                        self.diagram_data[current_diagram][dt]={t: value}

        return self.diagram_data

# from https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries
def merge(a, b, path=None):
    #"merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

# works
#print(merge({1:{"a":"A"},2:{"b":"B"}}, {2:{"c":"C"},3:{"d":"D"}}))
# has conflict
#merge({1:{"a":"A"},2:{"b":"B"}}, {1:{"a":"A"},2:{"b":"C"}})