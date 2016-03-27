'''
Created on 2016年3月23日

@author: Darren
'''
from math import exp
from Util import Matrix
import time
import random
'''
Created on 2016年3月21日

@author: Darren
'''

class Logistic_Regression(object):
    
    def __init__(self):
        self.data_X=[]
        self.data_Y=[]
        self.weights=[]
        self.learning_rate = 0
        self.max_itr=0
        
    def run(self,file_name,learning_rate=0.001,max_itr=1000):
        self.max_itr=max_itr
        self.learning_rate=learning_rate
        self.load_data(file_name)
        self.weights=[[0]  for _ in range(len(self.data_X[0]))]
        min_error=50
        for _ in range(self.max_itr):
            self.iteration()
            print(self.weights)
            error_count=self.test()
            print(error_count)
            min_error=min(min_error,error_count)
#             time.sleep(0.5)
        print(min_error)
        return self.weights
    
    def __sigmoid(self, inX):
        try:
            res=1.0/(1+exp(-inX))
        except OverflowError:
            res=1
        return res
    
    def test(self):
        res=0
        for i in range(len(self.data_X)):
            result=0
            for j in range(len(self.data_X[0])):
                result+=self.data_X[i][j]*self.weights[j][0]
            result=self.__sigmoid(result)
            if (result>0.5 and self.data_Y[i][0]==0) or (result<0.5 and self.data_Y[i][0]==1):
                res+=1
        return res
    
    def iteration(self):
        A=Matrix.multiply(self.data_X, self.weights)
        E=Matrix.minus(self.g_function(A),self.data_Y)
        temp=Matrix.multiply_integer(Matrix.multiply(Matrix.transpose(self.data_X), E), self.learning_rate)
        self.weights=Matrix.minus(self.weights,temp)
        
    def g_function(self,A):
        res=[[0] for _ in range(len(A))]
        for i in range(len(A)):
            try:
                res[i][0]=1.0/(1+exp(A[i][0]))
            except OverflowError:
                res[i][0]=1
        return res
        
        
    def load_data(self,file_name):
        try:
            with open(file_name,"r") as file:
                data=file.readlines()
                for line in data:
                    line=line.strip("\n")
                    line=line.split(",")
                    line=list(map(float,line))
                    self.data_X.append([1]+line[:3]) #ignore the 4th col
                    if line[4]==-1:
                        line[4]=0
                    self.data_Y.append([line[4]])
        except:
            print("Error reading data!") 
        
file_name="data/linear.txt"  
logistic_Regression=Logistic_Regression()
result=logistic_Regression.run(file_name)
print(result)