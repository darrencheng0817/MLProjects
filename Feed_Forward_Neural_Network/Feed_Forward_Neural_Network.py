'''
Created on 2016年4月12日

@author: Darren
'''
import matplotlib.pyplot as plt
from random import random
from math import exp

class Feed_Forward_Neural_Network():
    def __init__(self):
        self.data=[]
        self.weight=[[0]*3 for _ in range(3)]
        self.output_weight=[0]*3
    
    def load_data(self,file_name):
        try:
            with open(file_name,"r") as file:
                data=file.readlines()
                for line in data:
                    line=line.strip("\n")
                    x,y,z=line.split(" ")
                    self.data.append([float(x),float(y),int(z)])
        except:
            print("Error reading data!")  
    
    def run(self):
        self.init_weight()
        print(self.get_sign(self.data[4][:-1]+[1]))
    
    def get_sign(self,data):
        perceptron_res=[]
        for i in range(3):
            perceptron_res.append(self.perceptron(self.weight[i], data))
        return self.cal_output_sign(self.output_weight, perceptron_res)
        
    
    def perceptron(self,weight,data):
        res=0
        for i in range(len(weight)):
            res+=weight[i]*data[i]
        print(res,self.theta(res))
        return self.theta(res)
          
    def cal_output_sign(self,weight,data):
        res=0
        for i in range(len(weight)):
            res+=weight[i]*data[i]
        return res 
    
    def init_weight(self):
        for i in range(len(self.weight)):
            for j in range(len(self.weight[i])):
                self.weight[i][j]=random()*2-1
        for i in range(len(self.output_weight)):
            self.output_weight[i]=random()*2-1
    
    
    def theta(self,s):
        return (exp(s)-exp(-s))/(exp(s)+exp(-s))
    
    def draw_points(self):
        '''
        Draw original data in blue and red
        '''
        x1=[]
        y1=[]
        x2=[]
        y2=[]
        for element in self.data:
            if element[2]==1:
                x1.append(element[0])
                y1.append(element[1])
            else:
                x2.append(element[0])
                y2.append(element[1])
        area = 10
        plt.scatter(x1, y1, s=area, c="blue", alpha=0.5)
        plt.scatter(x2, y2, s=area, c="red", alpha=0.5)
        plt.show()    
        
feed_Forward_Neural_Network=Feed_Forward_Neural_Network()
feed_Forward_Neural_Network.load_data("data/nnsvm-data.txt")
feed_Forward_Neural_Network.draw_points()
feed_Forward_Neural_Network.run()
print(feed_Forward_Neural_Network.data)