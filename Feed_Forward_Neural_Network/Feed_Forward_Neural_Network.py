'''
Created on 2016年4月12日

@author: Darren
'''

class Feed_Forward_Neural_Netword():
    def __init__(self):
        self.data=[]
    
    def load_data(self,file_name):
        try:
            with open(file_name,"r") as file:
                data=file.readlines()
                for line in data:
                    line=line.strip("\n")
                    x,y,z=line.split(" ")
                    self.data.append([float(x),float(y),int(z)])
        except:
            print("Error reading data!")  
        
        
feed_Forward_Neural_Netword=Feed_Forward_Neural_Netword()
feed_Forward_Neural_Netword.load_data("data/nnsvm-data.txt")
print(feed_Forward_Neural_Netword.data)