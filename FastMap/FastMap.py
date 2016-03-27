'''
Created on 2016年3月20日

@author: Darren
'''
from math import sqrt
from Util import Matrix

class FastMap(object):
    
    def __init__(self):
        self.data=[]
        self.results=[]
        self.distances=[]
        
    def run(self,file_name,k):
        self.load_data(file_name)
        self.set_distances()
        self.iteration(k)
        return Matrix.transpose(self.results);
    
    def cal_distance(self,a,b):
        res=0
        for i in range(len(a)):
            res+=(a[i]-b[i])**2
        return sqrt(res)
    
    def set_distances(self):
        for i in range(len(self.data)):
            for j in range(i+1,len(self.data)):
                dis=self.cal_distance(self.data[i], self.data[j])
                self.distances[i][j]=dis
                self.distances[j][i]=dis
      
    def get_max_distance(self):
        max_dis=0
        a,b=-1,-1
        for i in range(len(self.data)):
            for j in range(i+1,len(self.data)):
                if self.distances[i][j]>max_dis:
                    a=i
                    b=j
                    max_dis=self.distances[i][j]
        return a,b
      
    def iteration(self,k):
        if k==0:
            return
        a,b=self.get_max_distance()
        res=[]
        for i in range(len(self.data)):
            if i==a:
                res.append(0.0)
            elif i==b:
                res.append(self.distances[a][b])
            elif self.distances[a][b]!=0:
                res.append((self.distances[a][i]**2+self.distances[a][b]**2-self.distances[b][i]**2)/(2*self.distances[a][b]))
            else:
                res.append(0.0)
        self.results.append(res)
        #map to new distance
        new_distance=[[0]*len(self.data) for _ in range(len(self.data))]
        for i in range(len(self.data)):
            for j in range(i+1,len(self.data)):
                new_dis=0
                if abs(self.distances[i][j]**2-(res[i]-res[j])**2)>1e-10:
                    new_dis=sqrt(self.distances[i][j]**2-(res[i]-res[j])**2)
                new_distance[i][j]=new_dis
                new_distance[j][i]=new_dis
        self.distances=new_distance
        self.iteration(k-1)
        
    def load_data(self,file_name):
        try:
            with open(file_name,"r") as file:
                data=file.readlines()
                for line in data:
                    line=line.strip("\n")
                    line=line.split(",")
                    line=list(map(float,line))
                    self.data.append(line)
                    self.distances=[[0]*len(self.data) for _ in range(len(self.data))]
        except:
            print("Error reading data!") 
        
file_name="data/dims.txt"  
fastMap=FastMap()
result=fastMap.run(file_name,2)
for item in result:
    print(item)