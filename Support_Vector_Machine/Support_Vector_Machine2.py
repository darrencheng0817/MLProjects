'''
Created on 2016年4月29日

@author: Darren
'''

from numpy import *
import matplotlib.pyplot as plt 


# calulate kernel value
def calcKernelValue(matrix_x, sample_x):
    return matrix_x * sample_x.T


# calculate kernel matrix given train
def calcKernelMatrix(train_x):
    numSamples = train_x.shape[0]
    kernelMatrix = mat(zeros((numSamples, numSamples)))
    for i in range(numSamples):
        kernelMatrix[:, i] = calcKernelValue(train_x, train_x[i, :])
    return kernelMatrix


# for storing variables and data
class SVMStruct:
    def __init__(self, dataSet, labels, C, toler):
        self.train_x = dataSet # each row stands for a sample
        self.train_y = labels  # corresponding label
        self.C = C             # slack variable
        self.toler = toler     # termination condition for iteration
        self.numSamples = dataSet.shape[0] # number of samples
        self.alphas = mat(zeros((self.numSamples, 1))) # Lagrange factors for all samples
        self.b = 0
        self.errorCache = mat(zeros((self.numSamples, 2)))
        self.kernelMat = calcKernelMatrix(self.train_x)

def calcError(svm, alpha_k):
    output_k = float(multiply(svm.alphas, svm.train_y).T * svm.kernelMat[:, alpha_k] + svm.b)
    error_k = output_k - float(svm.train_y[alpha_k])
    return error_k


def updateError(svm, alpha_k):
    error = calcError(svm, alpha_k)
    svm.errorCache[alpha_k] = [1, error]

def selectAlpha_j(svm, alpha_i, error_i):
    svm.errorCache[alpha_i] = [1, error_i] 
    candidateAlphaList = nonzero(svm.errorCache[:, 0].A)[0] 
    maxStep = 0; alpha_j = 0; error_j = 0

    if len(candidateAlphaList) > 1:
        for alpha_k in candidateAlphaList:
            if alpha_k == alpha_i: 
                continue
            error_k = calcError(svm, alpha_k)
            if abs(error_k - error_i) > maxStep:
                maxStep = abs(error_k - error_i)
                alpha_j = alpha_k
                error_j = error_k
    else:           
        alpha_j = alpha_i
        while alpha_j == alpha_i:
            alpha_j = int(random.uniform(0, svm.numSamples))
        error_j = calcError(svm, alpha_j)
    
    return alpha_j, error_j


def innerLoop(svm, alpha_i):
    error_i = calcError(svm, alpha_i)
    
    if (svm.train_y[alpha_i] * error_i < -svm.toler) and (svm.alphas[alpha_i] < svm.C) or\
        (svm.train_y[alpha_i] * error_i > svm.toler) and (svm.alphas[alpha_i] > 0):

        # step 1: select alpha j
        alpha_j, error_j = selectAlpha_j(svm, alpha_i, error_i)
        alpha_i_old = svm.alphas[alpha_i].copy()
        alpha_j_old = svm.alphas[alpha_j].copy()

        # step 2: calculate the boundary L and H for alpha j
        if svm.train_y[alpha_i] != svm.train_y[alpha_j]:
            L = max(0, svm.alphas[alpha_j] - svm.alphas[alpha_i])
            H = min(svm.C, svm.C + svm.alphas[alpha_j] - svm.alphas[alpha_i])
        else:
            L = max(0, svm.alphas[alpha_j] + svm.alphas[alpha_i] - svm.C)
            H = min(svm.C, svm.alphas[alpha_j] + svm.alphas[alpha_i])
        if L == H:
            return 0

        # step 3: calculate eta (the similarity of sample i and j)
        eta = 2.0 * svm.kernelMat[alpha_i, alpha_j] - svm.kernelMat[alpha_i, alpha_i] \
                  - svm.kernelMat[alpha_j, alpha_j]
        if eta >= 0:
            return 0

        # step 4: update alpha j
        svm.alphas[alpha_j] -= svm.train_y[alpha_j] * (error_i - error_j) / eta

        # step 5: clip alpha j
        if svm.alphas[alpha_j] > H:
            svm.alphas[alpha_j] = H
        if svm.alphas[alpha_j] < L:
            svm.alphas[alpha_j] = L

        # step 6: if alpha j not moving enough, just return        
        if abs(alpha_j_old - svm.alphas[alpha_j]) < 0.00001:
            updateError(svm, alpha_j)
            return 0

        # step 7: update alpha i after optimizing aipha j
        svm.alphas[alpha_i] += svm.train_y[alpha_i] * svm.train_y[alpha_j] \
                                * (alpha_j_old - svm.alphas[alpha_j])

        # step 8: update threshold b
        b1 = svm.b - error_i - svm.train_y[alpha_i] * (svm.alphas[alpha_i] - alpha_i_old) \
                                                    * svm.kernelMat[alpha_i, alpha_i] \
                             - svm.train_y[alpha_j] * (svm.alphas[alpha_j] - alpha_j_old) \
                                                    * svm.kernelMat[alpha_i, alpha_j]
        b2 = svm.b - error_j - svm.train_y[alpha_i] * (svm.alphas[alpha_i] - alpha_i_old) \
                                                    * svm.kernelMat[alpha_i, alpha_j] \
                             - svm.train_y[alpha_j] * (svm.alphas[alpha_j] - alpha_j_old) \
                                                    * svm.kernelMat[alpha_j, alpha_j]
        if (0 < svm.alphas[alpha_i]) and (svm.alphas[alpha_i] < svm.C):
            svm.b = b1
        elif (0 < svm.alphas[alpha_j]) and (svm.alphas[alpha_j] < svm.C):
            svm.b = b2
        else:
            svm.b = (b1 + b2) / 2.0

        # step 9: update error cache for alpha i, j after optimize alpha i, j and b
        updateError(svm, alpha_j)
        updateError(svm, alpha_i)

        return 1
    else:
        return 0

def trainSVM(train_x, train_y, C, toler, maxIter):
    svm = SVMStruct(mat(train_x), mat(train_y), C, toler)
    
    # start training
    entireSet = True
    alphaPairsChanged = 0
    iterCount = 0
    # Iteration termination condition:
    #     Condition 1: reach max iteration
    #     Condition 2: no alpha changed after going through all samples,
    #                  in other words, all alpha (samples) fit KKT condition
    while (iterCount < maxIter) and ((alphaPairsChanged > 0) or entireSet):
        alphaPairsChanged = 0

        # update alphas over all training examples
        if entireSet:
            for i in range(svm.numSamples):
                alphaPairsChanged += innerLoop(svm, i)
            iterCount += 1
        # update alphas over examples where alpha is not 0 & not C (not on boundary)
        else:
            nonBoundAlphasList = nonzero((svm.alphas.A > 0) * (svm.alphas.A < svm.C))[0]
            for i in nonBoundAlphasList:
                alphaPairsChanged += innerLoop(svm, i)
            iterCount += 1

        # alternate loop over all examples and non-boundary examples
        if entireSet:
            entireSet = False
        elif alphaPairsChanged == 0:
            entireSet = True

    print ('Training complete!')
    return svm

# show your trained svm model only available with 2-D data
def showSVM(svm):
    if svm.train_x.shape[1] != 2:
        print ("Only support 2 dimension data!")
        return 1
    
    for i in range(svm.numSamples):
        if svm.train_y[i] == -1:
            plt.plot(svm.train_x[i, 0], svm.train_x[i, 1], 'or')
        elif svm.train_y[i] == 1:
            plt.plot(svm.train_x[i, 0], svm.train_x[i, 1], 'ob')

    supportVectorsIndex = nonzero(svm.alphas.A > 0)[0]
    for i in supportVectorsIndex:
        plt.plot(svm.train_x[i, 0], svm.train_x[i, 1], 'oy')

    w = zeros((2, 1))
    for i in supportVectorsIndex:
        w += multiply(svm.alphas[i] * svm.train_y[i], svm.train_x[i, :].T) 
    min_x = min(svm.train_x[:, 0])[0, 0]
    max_x = max(svm.train_x[:, 0])[0, 0]
    y_min_x = float(-svm.b - w[0] * min_x) / w[1]
    y_max_x = float(-svm.b - w[0] * max_x) / w[1]
    plt.plot([min_x, max_x], [y_min_x, y_max_x], '-g')
    plt.show()

# testing your trained svm model given test set
def testSVM(svm, test_x, test_y):
    test_x = mat(test_x)
    test_y = mat(test_y)
    numTestSamples = test_x.shape[0]
    supportVectorsIndex = nonzero(svm.alphas.A > 0)[0]
    supportVectors = svm.train_x[supportVectorsIndex]
    supportVectorLabels = svm.train_y[supportVectorsIndex]
    supportVectorAlphas = svm.alphas[supportVectorsIndex]
    matchCount = 0
    for i in range(numTestSamples):
        kernelValue = calcKernelValue(supportVectors, test_x[i, :])
        predict = kernelValue.T * multiply(supportVectorLabels, supportVectorAlphas) + svm.b
        if sign(predict) == sign(test_y[i]):
            matchCount += 1
    accuracy = float(matchCount) / numTestSamples
    return accuracy




def main(): 
    print ("step 1: load data..."  )
    dataSet = []  
    labels = []  
    fileIn = open('data/nnsvm-data.txt')  
    for line in fileIn.readlines():  
        lineArr = line.strip("\n").split(" ") 
        dataSet.append([float(lineArr[0])**2, float(lineArr[1])**2])  
        labels.append(float(lineArr[2]))  
      
    dataSet = mat(dataSet)  
    labels = mat(labels).T  
    train_x = dataSet[0:101, :]  
    train_y = labels[0:101, :]  
    test_x = dataSet[0:101, :]  
    test_y = labels[0:101, :]  
    
    print ("step 2: training..."  )
    C = 0.6  
    toler = 0.001  
    maxIter = 50  
    svmClassifier = trainSVM(train_x, train_y, C, toler, maxIter)  
      
    print ("step 3: testing...")  
    accuracy = testSVM(svmClassifier, test_x, test_y)  
    
    print ("step 4: show the result..."  )  
    print ('Accuracy is: %.3f%%' % (accuracy * 100)  )
    showSVM(svmClassifier)  
    
main()
