'''
Created on 2016年3月21日

@author: Darren
'''
from Util import Matrix

class Linear_Regression(object):
    
    def __init__(self):
        self.data_X=[]
        self.data_Y=[]
        
    def run(self,file_name):
        self.load_data(file_name)
        for index in range(len(self.data_X)):
            self.data_X[index]=[1]+self.data_X[index]
        temp=Matrix.multiply(Matrix.transpose(self.data_X),self.data_X)
        temp=Matrix.multiply(Matrix.inverse(temp),Matrix.transpose(self.data_X))
        temp=Matrix.multiply(temp,self.data_Y)
        return temp
        
        
        
    def load_data(self,file_name):
        try:
            with open(file_name,"r") as file:
                data=file.readlines()
                for line in data:
                    line=line.strip("\n")
                    line=line.split(",")
                    line=list(map(float,line))
                    self.data_X.append(line[:2]) #ignore the 4th and 5th cols
                    self.data_Y.append(line[2])
        except:
            print("Error reading data!") 
        temp=[]
        for item in self.data_X:
            temp.append(" ".join(list(map(str,item))))
        print(";".join(temp))
        print(";".join(list(map(str,self.data_Y))))
        
file_name="data/linear.txt"  
linear_Regression=Linear_Regression()
result=linear_Regression.run(file_name)
print(result)