'''
Created on 2016年3月9日

@author: Darren
'''
from Util import Matrix, Vector

def get_average(data):
    if not data:
        return []
    res=[0]*len(data[0])
    for item in data:
        for index in range(len(item)):
            res[index]+=item[index]
    for index in range(len(item)):
        res[index]/=len(data)    
    return res

def get_variance(data):
    pass

def get_covariance(data,x,y):
    pass

def get_covariance_matrix(data):
    avg=get_average(data)
    centralized_matrix=[0]*len(data)  
    for i,item in enumerate(data):
        centralized_matrix[i]=Vector.minus(item,avg)
    res=Matrix.multiply(Matrix.transpose(centralized_matrix),centralized_matrix)
    N=len(data[0])-1
    return Matrix.multiply_integer(res, 1/N)
    
    