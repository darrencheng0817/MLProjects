'''
Created on 2016年4月12日

@author: Darren
'''
import matplotlib.pyplot as plt
from sklearn import svm

class Support_Vector_Machine():
    def __init__(self):
        self.x=[]
        self.y=[]
    
    def load_data(self,file_name):
        try:
            with open(file_name,"r") as file:
                data=file.readlines()
                for line in data:
                    line=line.strip("\n")
                    x,y,z=line.split(" ")
                    self.x.append([float(x)**2,float(y)**2])
                    self.y.append(int(z))
        except:
            print("Error reading data!")  
     
    def run(self):
        clf = svm.SVC()
        clf.fit(self.x, self.y)  
        error_count=0
        prediction=clf.predict(self.x).tolist()
        for i in range(len(self.y)):
            if prediction[i]!=self.y[i]:
                error_count+=1
        print("error prediction:",error_count)

         
    def draw_points(self):
        '''
        Draw original data in blue and red
        '''
        x1=[]
        y1=[]
        x2=[]
        y2=[]
        for element in self.data:
            if element[2]==1:
                x1.append(element[0])
                y1.append(element[1])
            else:
                x2.append(element[0])
                y2.append(element[1])
        area = 10
        plt.scatter(x1, y1, s=area, c="blue", alpha=0.5)
        plt.scatter(x2, y2, s=area, c="red", alpha=0.5)
        plt.show()    
        
support_Vector_Machine=Support_Vector_Machine()
support_Vector_Machine.load_data("data/nnsvm-data.txt")
# support_Vector_Machine.draw_points()
support_Vector_Machine.run()

