'''
Created on 2016年3月18日

@author: Darren
'''

class Principal_Components_Analysis(object):
    
    def __init__(self):
        self.data=[]
    
    def run(self,file_name):
        self.load_data(file_name)
    
    def load_data(self,file_name):
        try:
            with open(file_name,"r") as file:
                data=file.readlines()
                for line in data:
                    line=line.strip("\n")
                    line=line.split(",")
                    self.data.append(line)
        except:
            print("Error reading data!")  
        print(self.data)
        
file_name="data/dims.txt"  
principal_Components_Analysis=Principal_Components_Analysis()
principal_Components_Analysis.run(file_name)