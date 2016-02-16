'''
Created on 2016年2月2日

@author: Darren
'''
from random import random
from math import sqrt

class K_Mean(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.data_file_name = "data/km-data.txt"
        self.accuracy = 0.0000001
        self.k = 0
        self.km_data = []
        self.res_data={}
        self.res=[]
        self.dis_alg=""
        
    def parse_km_content(self, content):
        print("Parsing km data...")
        if not content:
            print("Empty km File!")
            return False
        for line_index, line in enumerate(content):
            line = line.replace("\n", "")
            line = line.strip().split(",")
            data = [float(_) for _ in line]
            self.km_data.append(data)
        print("Finished parsing km data...")
        return True
    
    def load_km_data(self):
        print("Loading km data...")
        try:
            file = open(self.data_file_name, "r")
            content = file.readlines()
        except FileNotFoundError:
            print(self.data_file_name + " File not Found!")
            return False
        except:
            print("Error reading km data")
            return False
        print("Finished loading km data...")
        return self.parse_km_content(content)
     
    def get_l1_distance(self,A,B):
        res=0
        for index in range(len(A)):
            res+=abs(A[index]-B[index])
        return res
    
    def get_l2_distance(self,A,B):
        res=0
        for index in range(len(A)):
            res+=(A[index]-B[index])**2
        return sqrt(res)
    
    def compare_centroid(self, A, B):
        for index in range(len(A)):
            if self.get_l2_distance(A[index], B[index]) > self.accuracy:
                return False
        return True
    
    def get_distance(self,A,B):
        if self.dis_alg=="l1":
            return self.get_l1_distance(A, B)
        elif self.dis_alg=="l2":
            return self.get_l2_distance(A, B)
    
    def km_iteration(self, seeds):
        km_set={}
        for __index in range(len(seeds)):
            km_set[__index]=[]
        for element in self.km_data:
            distance=self.get_distance(element,seeds[0])
            set_index=0
            for seed_index in range(1,len(seeds)):
                new_distance=self.get_distance(element,seeds[seed_index])
                if distance>new_distance:
                    set_index=seed_index
                    distance=new_distance
            km_set[set_index].append(element)
        res=[]
        for centroid_index in sorted(km_set.keys()): 
            if len(km_set[centroid_index])==0:
                res.append(seeds[centroid_index])
                continue
            count=[0]*len(seeds[0])
            for element in km_set[centroid_index]:
                for dimension in range(len(element)):
                    count[dimension]+=element[dimension]
            for dimension in range(len(count)):
                count[dimension]/=len(km_set[centroid_index])
            res.append(count)
        self.res_data=km_set
        return res            
                    
                    
    def run_km(self):
        seeds = []
        seedIndex = 0
        while seedIndex < self.k:
            seed = int(random() * len(self.km_data))
            if self.km_data[seed] not in seeds:
                seeds.append(self.km_data[seed])
                seedIndex += 1
        iteration_count=0
        while True:
            iteration_count+=1
            res = self.km_iteration(seeds)
            if self.compare_centroid(seeds, res):
                print("Got results after "+str(iteration_count)+" iterations!")
                self.res=res
                return res
            seeds = res
        
               
    def run(self, k,dis="l2"):
        self.dis_alg=dis
        self.k = k
        if not self.load_km_data():
            return
        return self.run_km()
        
if __name__ == '__main__':
    k_mean = K_Mean()
    print(k_mean.run(3,"l1"))
