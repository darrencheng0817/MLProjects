'''
Created on 2016年3月8日

@author: Darren
'''
from Util import Vector

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
    if not A or len(A)!=len(A[0]):
        raise Exception("Invalid input")
    length=len(A)
    res=append(A,eye(length))
    for i in range(length):
        res[i]=Vector.multiply_integer(res[i], 1/res[i][i])
        for j in range(length):
            if i == j:
                continue
            res[j]=Vector.minus(res[j], Vector.multiply_integer(res[i],res[j][i]))
    for i in range(length):
        res[i]=res[i][length:]
    return res
        

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

def multiply_integer(A,N):
    res=list(A)
    for i in range(len(A)):
        for j in range(len(A[0])):
            res[i][j]*=N
    return res

def transpose(A):
    if not A:
        return A
    res=[[0]*len(A) for _ in range(len(A[0]))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            res[j][i]=A[i][j]
    return res

def append(A,B):
    if not A or not B or len(A)!=len(B):
        raise Exception("Invalid input")
    res=list(A)
    for index in range(len(A)):
        res[index]+=B[index]
    return res

def eye(N):
    res=[[0]* N for _ in range(N)]
    for i in range(N):
        res[i][i]=1
    return res

def determinant(A):
    if not A or len(A)!=len(A[0]):
        raise Exception("Invalid input")
    new_A=list(A)
    for i in range(len(A)):
        for j in range(i+1,len(A)):
            new_A[j]=Vector.minus(new_A[j], Vector.multiply_integer(new_A[i], new_A[j][i]/new_A[i][i]))
    res=1
    for i in range(len(A)):
        res*=new_A[i][i]
    return res
        