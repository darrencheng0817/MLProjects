'''
Created on 2016年3月7日

@author: Darren
'''
from Util import Matrix, Multi_Dimension_Data_Statictis, Gaussian
import copy
from math import log
import matplotlib.pyplot as plt
class Gaussian_Mixture_Model(object):
    '''
    Gaussian Mixture Model
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.data=[]
        self.accurate=0.0000000001
        self.res_data=[]
        self.k=0
        
    def load_data(self,file_name):
        try:
            with open(file_name,"r") as file:
                data=file.readlines()
                for line in data:
                    line=line.strip("\n")
                    x,y=line.split(",")
                    self.data.append([float(x),float(y)])
        except:
            print("Error reading data!")  
    
    def iteration(self,data_sets):
        covs=[]
        avgs=[]
        new_data_sets=[[] for _ in range(len(data_sets))]
        #get the expectation and covariance matrix
        for data_set in data_sets:
            cov=Multi_Dimension_Data_Statictis.get_covariance_matrix(data_set)
            avg=Multi_Dimension_Data_Statictis.get_average(data_set)
            covs.append(cov)
            avgs.append(avg)
        # assign data to cluster
        for data in self.data:
            max_p=0
            max_p_index=0
            for index in range(len(data_sets)):
                gauss_value=Gaussian.gaussian([[_n] for _n in data], avgs[index], covs[index])
                if gauss_value>max_p:
                    max_p=gauss_value
                    max_p_index=index
            new_data_sets[max_p_index].append(data)
        covs=[]
        avgs=[]
        #calculate the new expectation and covariance matrix
        for data_set in data_sets:
            cov=Multi_Dimension_Data_Statictis.get_covariance_matrix(data_set)
            avg=Multi_Dimension_Data_Statictis.get_average(data_set)
            covs.append(cov)
            avgs.append(avg)
        likehood=0
        # calculate the likelihood
        for index in range(len(data_sets)):
            temp=0
            for data in data_sets[index]:
                gauss_value=Gaussian.gaussian([[_n] for _n in data], avgs[index], covs[index])
                temp+=gauss_value
            likehood+=log(temp)
        return likehood,new_data_sets
                    
    def run(self,k,file_name):
        self.k=k
        self.load_data(file_name)
        data_sets=[]
        pre_likehood=0
        l=len(self.data)//k
        data=copy.deepcopy(self.data)
        for i in range(k):
            data_sets.append(data[:l])
            data=data[l:]
        count=0
        while True:
            count+=1
            new_likehood,data_sets=self.iteration(data_sets)
            if abs(new_likehood-pre_likehood)<self.accurate:
                print("Get result in "+str(count)+" iterations!")
                print(new_likehood)
                self.res_data=data_sets
                break
            pre_likehood=new_likehood
            
    def draw_results(self):
        '''
        Draw results data in different color
        '''
        colors=["blue","yellow","green","black","cyan","gray","pink"]
        if self.k>len(colors):
            print("Don't have that much colors to show the results!")
            return
        if not self.res_data:
            print("No results to show!")
            return
        if len(self.res_data[0][0])!=2:
            print("Only support Two-Dimension!")  
            return
        for cluster_index in range(len(self.res_data)):
            x=[]
            y=[]
            for element in self.res_data[cluster_index]:
                x.append(element[0])
                y.append(element[1])
            area = 20
            plt.scatter(x, y, s=area, c=colors[cluster_index], alpha=0.5)
        plt.show()       
         
file_name="data/clusters.txt"                
gaussian_mixture_model=Gaussian_Mixture_Model()
gaussian_mixture_model.run(3,file_name)
gaussian_mixture_model.draw_results()