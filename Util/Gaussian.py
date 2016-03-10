'''
Created on 2016年3月9日

@author: Darren
'''
import math
from math import sqrt,exp
from Util import Matrix

def gaussian(x,u,C):
    res=(1/sqrt(2*math.pi*Matrix.determinant(C)))
    temp=Matrix.transpose(Matrix.minus(x, u))
    temp=Matrix.multiply(temp, Matrix.inverse(C))
    temp=Matrix.multiply(temp,Matrix.minus(x, u))
    res*=exp(-0.5*temp[0][0])
    return res


print(gaussian([[4]],[[4]],[[1]]))
print(1/sqrt(2*math.pi))