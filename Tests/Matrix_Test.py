'''
Created on 2016年3月8日

@author: Darren
'''
import unittest
from Util import Matrix

class Test(unittest.TestCase):


    def test_multiply(self):
        A=[[1,2,3],[4,5,6]]
        B=[[6,5],[4,3],[2,1]]
        expected_result=[[20, 14], [56, 41]]
        actual_result=Matrix.multiply(A, B)
        self.assertEqual(expected_result, actual_result)
        
    def test_plus(self):
        A=[[1,2,3],[4,5,6]]
        B=[[6,5,4],[3,2,1]]
        expected_result=[[7,7,7],[7,7,7]]
        actual_result=Matrix.plus(A, B)
        self.assertEqual(expected_result, actual_result)   
     
    def test_minus(self):
        A=[[1,2,3],[4,5,6]]
        B=[[6,5,4],[3,2,1]]
        expected_result=[[-5,-3,-1],[1,3,5]]
        actual_result=Matrix.minus(A, B)
        self.assertEqual(expected_result, actual_result)    
         
    def test_transpose(self):
        A=[[1,2,3],[4,5,6]]
        expected_result=[[1,4],[2,5],[3,6]]
        actual_result=Matrix.transpose(A)
        self.assertEqual(expected_result, actual_result)
    
    def test_multiply_integer(self):
        A=[[1,2,3],[4,5,6]]
        N=2
        expected_result=[[2,4,6],[8,10,12]]
        actual_result=Matrix.multiply_integer(A,N)
        self.assertEqual(expected_result, actual_result)   
        
    def test_inverse(self):
        A=[[1,1,2],[-1,2,0],[1,1,3]]
        expected_result=[[2.0, -0.3333333333333333, -1.3333333333333335], [1.0, 0.3333333333333333, -0.6666666666666666], [-1.0, 0.0, 1.0]]
        actual_result=Matrix.inverse(A)
        self.assertEqual(expected_result, actual_result) 
    
    def test_eye(self):
        N=3
        expected_result=[[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        actual_result=Matrix.eye(N)
        self.assertEqual(expected_result, actual_result)
        
    def test_append(self):
        A=[[1,2,3],[4,5,6]]
        B=[[1,2,3],[4,5,6]]
        expected_result=[[1, 2, 3, 1, 2, 3], [4, 5, 6, 4, 5, 6]]
        actual_result=Matrix.append(A, B)
        self.assertEqual(expected_result, actual_result)    
    
    def test_determinant(self):
        A=[[1,-9,13,7],[-2,5,-1,3],[3,-1,5,-5],[2,8,-7,-10]]
        expected_result=-312
        actual_result=Matrix.determinant(A)
        self.assertEqual(expected_result, actual_result)   
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_multiply']
    unittest.main()