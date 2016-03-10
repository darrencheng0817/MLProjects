'''
Created on 2016年3月9日

@author: Darren
'''
def minus(A,B):
    if not A or not B or len(A)!=len(B):
        raise Exception("Invalid input")
    res=list(A)
    for i in range(len(A)):
        res[i]-=B[i]
    return res

def plus(A,B):
    if not A or not B or len(A)!=len(B):
        raise Exception("Invalid input")
    res=list(A)
    for i in range(len(A)):
        res[i]+=B[i]
    return res

def multiply_integer(A,N):
    res=list(A)
    for i in range(len(A)):
        res[i]*=N
    return res