'''
Created on 2016年3月8日

@author: Darren
'''

def multiply(A,B):
    if not A or not B or len(A[0])!=len(B):
        raise Exception("Invalid input")
    res=[[0]*len(B[0]) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(A[0])):
                res[i][j]+=A[i][k]*B[k][j]
    return res

def inverse(A):
    pass

def minus(A,B):
    if not A or not B or len(A)!=len(B) or len(A[0])!=len(B[0]):
        raise Exception("Invalid input")
    res=list(A)
    for i in range(len(A)):
        for j in range(len(A[0])):
            res[i][j]-=B[i][j]
    return res

def plus(A,B):
    if not A or not B or len(A)!=len(B) or len(A[0])!=len(B[0]):
        raise Exception("Invalid input")
    res=list(A)
    for i in range(len(A)):
        for j in range(len(A[0])):
            res[i][j]+=B[i][j]
    return res

def transpose(A):
    if not A:
        return A
    res=[[0]*len(A) for _ in range(len(A[0]))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            res[j][i]=A[i][j]
    return res