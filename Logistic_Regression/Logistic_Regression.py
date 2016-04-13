'''
Created on 2016年3月23日

@author: Darren
'''
from math import exp
from Util import Matrix
import time
import random

class Logistic_Regression(object):
    
    def __init__(self):
        self.data_X=[]
        self.data_Y=[]
        self.weights=[]
        self.learning_rate = 0
        self.max_itr=0
        
    def run(self,file_name,learning_rate=0.001,max_itr=20000):
        self.max_itr=max_itr
        self.learning_rate=learning_rate
        self.load_data(file_name)
        self.weights=[0] *len(self.data_X[0])
        min_error=50
        best_weights=[]
        for _ in range(self.max_itr):
            self.iteration()
            error_count=self.test()
            if min_error>error_count:
                min_error=error_count
                best_weights=self.weights
        print(min_error)
        print(best_weights)
        return self.weights
    
    def test(self):
        res=0
        for i in range(len(self.data_X)):
            result=0
            for j in range(len(self.data_X[0])):
                result+=self.data_X[i][j]*self.weights[j]
            result=self.__sigmoid(result)
            if (result>0.5 and self.data_Y[i]==0) or (result<0.5 and self.data_Y[i]==1):
                res+=1
        return res
        
    def iteration(self):
        for i in range(len(self.data_X)):
            E=0
            for j in range(len(self.data_X[0])):
                E+=self.data_X[i][j]*self.weights[j] 
            h=self.__sigmoid(E)
            error=self.data_Y[i]-h
            for j in range(len(self.data_X[0])):
                self.weights[j]+=self.learning_rate*self.data_X[i][j]*error 
    
    def __sigmoid(self, inX):
        try:
            res=1.0/(1+exp(-inX))
        except OverflowError:
            res=1
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
                    self.data_Y.append(line[4])
        except:
            print("Error reading data!") 
        
file_name="data/linear.txt"  
logistic_Regression=Logistic_Regression()
result=logistic_Regression.run(file_name)
print(result)