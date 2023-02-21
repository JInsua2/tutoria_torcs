import csv

import numpy as np

from entorno import Env

env = Env(5)
qtable = np.random.rand(25, 5).tolist()
""""
with open("prueba.csv", "w+") as my_csv:
    csvWriter = csv.writer(my_csv, delimiter=',')
    csvWriter.writerows(qtable)

"""
import numpy as np

with open("prueba.csv") as file_name:
    array = np.loadtxt(file_name, delimiter=",")
dos=2

class CircularQueue(object):
    MAX_SIZE=2

    def __init__(self,elem):
        self.cola=[]
        self.cola.append(elem)
        self.front=1
    def añadir(self, other):
        if len(self.cola)<3:
            self.cola.append(other)
        else:
            self.cola[self.front]=other
        self.front=(self.front+1)%3
    def getCola(self):
        return self.cola

estados_circulares=CircularQueue([0,1])
estados_circulares.añadir([18,3])
estados_circulares.añadir([7,3])
estados_circulares.añadir([4,5])
estados_circulares.añadir([1,1])
estados_circulares.añadir([2,2])
estados_circulares.añadir([3,3])






with open("qtable.csv") as file_name:
    qtable = np.loadtxt(file_name, delimiter=",").tolist()
print(qtable[4])#4,1 4,4 4,2