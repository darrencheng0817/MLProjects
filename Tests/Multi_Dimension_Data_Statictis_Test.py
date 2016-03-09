'''
Created on 2016年3月9日

@author: Darren
'''
import unittest
from Util import Multi_Dimension_Data_Statictis


class Test(unittest.TestCase):


    def test_get_average(self):
        data=[[1,2,3],[4,5,6],[7,8,9]]
        expected_result=[4,5,6]
        actual_result=Multi_Dimension_Data_Statictis.get_average(data)
        self.assertEqual(expected_result, actual_result)
        
    def test_get_covariance_matrix(self):
        data=[[1,2,3],[4,5,6],[7,8,9]]
        expected_result=[[9,9,9],[9,9,9],[9,9,9]]
        actual_result=Multi_Dimension_Data_Statictis.get_covariance_matrix(data)
        self.assertEqual(expected_result, actual_result)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()