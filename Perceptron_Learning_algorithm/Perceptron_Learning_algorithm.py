'''
Created on 2016年3月21日

@author: Darren
'''

class Perceptron_Learning(object):
    
    def __init__(self):
        self.data=[]
        self.weights=[]
        self.threshold = 0
        self.learning_rate = 0
        
    def run(self,file_name,threshold = 0,learning_rate = 0.01):
        self.threshold = threshold
        self.learning_rate = learning_rate
        self.load_data(file_name)
        self.weights=[1] * (len(self.data[0])-1)
        while True:
            res=self.iteration()
            if res:
                return self.weights
        
        
     
    def dot_product(self,values, weights):
            return sum(value * weight for value, weight in zip(values, weights))  
        
    def iteration(self):
        error_count = 0
        for item in self.data:
            input_vector=item[:-1]
            desired_output=item[-1]
            result = self.dot_product(input_vector, self.weights) - self.threshold
            error = desired_output*result<=0
            if error:
                error_count += 1
                for index, value in enumerate(input_vector):
                    self.weights[index] += self.learning_rate * desired_output * value
        if error_count == 0:
            return True
        return False
        
    def load_data(self,file_name):
        try:
            with open(file_name,"r") as file:
                data=file.readlines()
                for line in data:
                    line=line.strip("\n")
                    line=line.split(",")
                    line=list(map(float,line))
                    self.data.append([1]+line[:-1]) #ignore the last col
        except:
            print("Error reading data!") 
        
file_name="data/linear.txt"  
perceptron_Learning=Perceptron_Learning()
result=perceptron_Learning.run(file_name)
print(result)