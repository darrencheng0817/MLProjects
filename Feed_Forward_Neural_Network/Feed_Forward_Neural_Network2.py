'''
Created on 2016年4月12日

@author: Darren
'''
import math
import random

random.seed(0)

# get a random num in (a,b)
def rand(a, b):
    return (b - a) * random.random() + a

def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill] * J)
    return m


def randomizeMatrix(matrix, a, b):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = random.uniform(a, b)


def sigmoid(x):
    return math.tanh(x)



def dsigmoid(y):
    return 1.0 - y ** 2



class Neural_Network:
    def __init__(self, ni, nh, no):
        # number of input, hidden, and output nodes
        self.ni = ni + 1
        self.nh = nh
        self.no = no

        # output
        self.ai = [1.0] * self.ni
        self.ah = [1.0] * self.nh
        self.ao = [1.0] * self.no

        # weight
        self.wi = makeMatrix(self.ni, self.nh)  
        self.wo = makeMatrix(self.nh, self.no)  
       
        randomizeMatrix(self.wi, -0.2, 0.2)
        randomizeMatrix(self.wo, -2.0, 2.0)
        
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def runNN(self, inputs):
        if len(inputs) != self.ni - 1:
            print('incorrect number of inputs')

        for i in range(self.ni - 1):
            self.ai[i] = inputs[i]

        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum += ( self.ai[i] * self.wi[i][j] )
            self.ah[j] = sigmoid(sum)

        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum += ( self.ah[j] * self.wo[j][k] )
            self.ao[k] = sigmoid(sum)

        return self.ao


    def backPropagate(self, targets, N, M):
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k] - self.ao[k]
            output_deltas[k] = error * dsigmoid(self.ao[k])

        # update output weight
        for j in range(self.nh):
            for k in range(self.no):
                # output_deltas[k] * self.ah[j] 才是 dError/dweight[j][k]
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] += N * change + M * self.co[j][k]
                self.co[j][k] = change

        
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error += output_deltas[k] * self.wo[j][k]
            hidden_deltas[j] = error * dsigmoid(self.ah[j])

        # update hidden weight
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j] * self.ai[i]
                # print 'activation',self.ai[i],'synapse',i,j,'change',change
                self.wi[i][j] += N * change + M * self.ci[i][j]
                self.ci[i][j] = change

        error = 0.0
        for k in range(len(targets)):
            error = 0.5 * (targets[k] - self.ao[k]) ** 2
        return error


    def weights(self):
        print('Input weights:')
        for i in range(self.ni):
            print (self.wi[i])
        print ('Output weights:')
        for j in range(self.nh):
            print (self.wo[j])
        print('')

    def test(self, patterns):
        error_count=0
        for p in patterns:
            inputs = p[0]
            res=self.runNN(inputs)
            if res[0]*p[1][0]<0:
                error_count+=1
        print("Error rate:",error_count/len(patterns))

    def train(self, patterns, max_iterations=1000, N=0.5, M=0.1):
        for i in range(max_iterations):
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.runNN(inputs)
                error = self.backPropagate(targets, N, M)
        self.test(patterns)

def load_data(file_name):
    res=[]
    try:
        with open(file_name,"r") as file:
            data=file.readlines()
            for line in data:
                line=line.strip("\n")
                x,y,z=line.split(" ")
                res.append([[float(x),float(y)],[int(z)]])
    except:
        print("Error reading data!")  
    return res
            
def main():
    data=load_data("data/nnsvm-data.txt")
    train_set=data[45:70]
    test_set=data[:45]+data[70:]
    neural_Network = Neural_Network(2, 3, 1)
    neural_Network.train(train_set)
    neural_Network.test(test_set)

if __name__ == "__main__":
    main()
