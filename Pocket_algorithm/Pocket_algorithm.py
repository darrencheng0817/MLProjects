'''
Created on 2016年3月21日

@author: Darren
'''

class Perceptron_Learning(object):
    
    def __init__(self):
        self.data=[]
        self.weights=[]
        self.result=(float('inf'),[])
        self.threshold = 0
        self.learning_rate = 0
        self.max_iteration_count=0
        
    def run(self,file_name,threshold = 0,learning_rate = 0.01,max_iteration_count=500):
        self.threshold = threshold
        self.learning_rate = learning_rate
        self.max_iteration_count=max_iteration_count
        self.load_data(file_name)
        self.weights=[0] * (len(self.data[0])-1)
        for _ in range(self.max_iteration_count):
            res=self.iteration()
            if res:
                break
        return self.result[1]
        
        
     
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
        if error_count<self.result[0]:
            print(error_count)
            self.result=(error_count,self.weights)
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
                    self.data.append([1]+line[:3]+line[4:]) #ignore the 4th col
        except:
            print("Error reading data!") 
        
file_name="data/linear.txt"  
perceptron_Learning=Perceptron_Learning()
result=perceptron_Learning.run(file_name)
print(result)