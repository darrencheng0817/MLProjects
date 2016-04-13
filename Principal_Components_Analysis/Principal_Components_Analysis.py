'''
Created on 2016年3月18日

@author: Darren
'''
from Util import Multi_Dimension_Data_Statictis, Matrix
import numpy as np


class Principal_Components_Analysis(object):
    
    def __init__(self):
        self.data=[]
    
    def run(self,file_name,k):
        self.load_data(file_name)
        return self.analysis(k)
        
        
    def analysis(self,k):
#         Calculate the empirical mean
        means=Multi_Dimension_Data_Statictis.get_average(self.data)
#         Calculate the deviations from the mean
        deviations=Multi_Dimension_Data_Statictis.get_deviations(self.data) #unused
        mean_subtracted_data=Matrix.minus(self.data, Matrix.multiply([[1] for _ in range(len(self.data))], Matrix.transpose(means)))
#         Find the covariance matrix
        covariance_matrix=Multi_Dimension_Data_Statictis.get_covariance_matrix(mean_subtracted_data)
#         Find the eigenvectors and eigenvalues of the covariance matrix
        x= np.mat(covariance_matrix)
        eigenvalues,eigenvectors=np.linalg.eigh(x)
        eigenvalues=eigenvalues.tolist()
        eigenvectors=Matrix.transpose(eigenvectors.tolist())
#         Rearrange the eigenvectors and eigenvalues
        eigenvalue_and_eigenvector=[]
        for i in range(len(eigenvalues)):
            eigenvalue_and_eigenvector.append((eigenvalues[i],eigenvectors[i]))
        
        eigenvalue_and_eigenvector=sorted(eigenvalue_and_eigenvector, reverse=True)
#         Choosing k eigenvectors with the largest eigenvalues
        transform_matrix=[]
        for i in range(k):
            transform_matrix.append(eigenvalue_and_eigenvector[i][1])
        return Matrix.transpose(Matrix.multiply(transform_matrix,Matrix.transpose(self.data)))
        
        
        
        
    def load_data(self,file_name):
        try:
            with open(file_name,"r") as file:
                data=file.readlines()
                for line in data:
                    line=line.strip("\n")
                    line=line.split(",")
                    line=list(map(float,line))
                    self.data.append(line)
        except:
            print("Error reading data!") 
        
file_name="data/dims.txt"  
principal_Components_Analysis=Principal_Components_Analysis()
result=principal_Components_Analysis.run(file_name,2)
for index,item in enumerate(result):
    print(index,item)
      