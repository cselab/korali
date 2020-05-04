
import numpy as np


def extr(line, toint=True, tofloat=False):
    result =  line.strip("\n ").split(" ")
    if tofloat:
        result = [float(r) for r in result]
    elif toint:
        result = [int(r) for r in result]
    return result

class SimplePopulationData():
   def __init__(self):

       self.nIndividuals = None
       self.sigma = None
       self.omega = None
       self.nSamplesEach = 1
       self.data = []

       print("Loading data from data_925.in ... \n")
       with open("model/data_925.in", "r") as fd:
           firstline = fd.readline().strip("\n ").split(" ")
           self.nIndividuals, self.nSamplesEach = map(int, firstline[:2])
           self.sigma, self.omega = map(float, firstline[2:])
           for i in range(self.nIndividuals):
               values = extr(fd.readline(), tofloat=True)
               self.data.append(values)

       self.data = np.array(self.data)



