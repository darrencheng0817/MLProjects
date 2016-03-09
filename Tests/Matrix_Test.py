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
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_multiply']
    unittest.main()