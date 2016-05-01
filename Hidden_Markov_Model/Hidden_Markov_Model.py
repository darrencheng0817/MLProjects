'''
Created on 2016年4月12日

@author: Darren
'''
from math import sqrt, log

class Hidden_Markov_Model():
    def __init__(self):
        self.grid=[]
        self.towers=[]
        self.observations=[]
        self.distances=[]
        self.transform_probability=[]
    
    def load_data(self):
        try:
            with open("data/hmm-data-grid.txt","r") as file:
                data=file.readlines()
                for line in data:
                    line=line.strip("\n").split(" ")
                    self.grid.append(line)
            with open("data/hmm-data-towers.txt","r") as file:
                data=file.readlines()
                for line in data:
                    line=line.strip("\n").split(" ")
                    self.towers.append((int(line[0]),int(line[1])))
            with open("data/hmm-data-observations.txt","r") as file:
                data=file.readlines()
                for line in data:
                    line=line.strip("\n").split(" ")
                    line=list(map(lambda x:round(float(x),1),line))
                    self.observations.append(line)        
        except:
            print("Error reading data!")  
    
    def get_transform_probability(self):
        res=[[0] * len(self.grid[0]) for _ in range(len(self.grid))]
        trans=[(1,0),(0,1),(-1,0),(0,-1)]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j]=="1" and (i,j) in self.towers:
                    continue
                c=0
                for tran_index in range(len(trans)):
                    x=i+trans[tran_index][0]
                    y=j+trans[tran_index][1]
                    if 0<=x<len(self.grid) and 0<=y<len(self.grid[0]) and (x,y) not in self.towers and self.grid[x][y]=="1":
                        c+=1
                res[i][j]=1/c
        return res
    
    def get_Init_probrbality(self): 
        res=[[0] * len(self.grid[0]) for _ in range(len(self.grid))]
        def count_total(grid):
            res=0
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j]=="1":
                        res+=1
            return res
        total=count_total(self.grid)-len(self.towers)
        for i in range(len(res)):
            for j in range(len(res[i])):
                if self.grid[i][j]=="1":
                    res[i][j]=1/total
        for i in range(len(self.towers)):
            x,y=self.towers[i]
            res[x][y]=0
        return res
    
    def get_path(self,p):
        res=[]
        res.append(p[-1][0])
        pre=p[-1][0]
        p=list(reversed(p))
        for item1 in p[1:]:
            for item2 in item1:
                if abs(pre[0]-item2[0]) +abs(pre[1]-item2[1])==1:
                    res.append(item2)
                    pre=item2
                    break
        return list(reversed(res))
                
        
    def viterbi(self):
        res=[]
        emission=self.get_emission_probability_init(self.observations[0])
        res.append(emission)
        for step in range(1,11):
            new_emission=[]
            largest=0
            for x,y in emission:
                temp,value=self.get_emission_probability(self.observations[step], (x,y))
                if abs(value-largest)<0.1:
                    new_emission+=temp
                elif value>largest:
                    new_emission=temp
                    largest=value
            emission=new_emission
            res.append(emission)
        return res
    
    def get_emission_probability_init(self,observation):
        largest=0
        res=[]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j]=="1" and (i,j) in self.towers:
                    continue
                prob=1
                for k in range(len(self.towers)):
                    if 0.7*self.distances[i][j][k]<=observation[k]<=1.3*self.distances[i][j][k]:
                        prob+=-log(1/(6*self.distances[i][j][k]))
                    else:
                        prob+=0
                if abs(prob-largest)<0.1:
                    res.append((i,j))
                elif prob>largest:
                    res=[(i,j)]
                    largest=prob
        return res
    
    def get_emission_probability(self,observation,pre):
        largest=0
        res=[]
        trans=[(1,0),(0,1),(-1,0),(0,-1)]
        for tran_index in range(len(trans)):
            i=pre[0]+trans[tran_index][0]
            j=pre[1]+trans[tran_index][1]
            prob=0
            if 0<=i<len(self.grid) and 0<=j<len(self.grid[0]) and (i,j) not in self.towers and self.grid[i][j]=="1":
                for k in range(len(self.towers)):
                    if 0.7*self.distances[i][j][k]<=observation[k]<=1.3*self.distances[i][j][k]:
                        prob+=-log(1/(6*self.distances[i][j][k]))
                    else:
                        prob+=0
            if abs(prob-largest)<0.1:
                res.append((i,j))
            elif prob>largest:
                res=[(i,j)]
                largest=prob
        return res,largest
    
    def get_distances(self):
        res=[[0]*len(self.grid[0]) for _ in range(len(self.grid))]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j]=="1" and (i,j) in self.towers:
                    continue
                distances=[]
                for k in range(len(self.towers)):
                    x,y= self.towers[k]
                    distances.append(sqrt((x-i)**2+(y-j)**2))
                res[i][j]=distances
        return res
                    
                        
    
    def run(self):
        self.distances=self.get_distances()
        self.transform_probability=self.get_transform_probability()
        p=self.viterbi()
        for index,item in enumerate(p):
            print(index+1,item)
        print(self.get_path(p))
        
        
hidden_Markov_Model=Hidden_Markov_Model()
hidden_Markov_Model.load_data()
hidden_Markov_Model.run()