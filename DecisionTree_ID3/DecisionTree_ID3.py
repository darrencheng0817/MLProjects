'''
Created on 2016年2月1日

@author: Darren
'''
class TreeNode(object):
    def __init__(self):
        self.value=""
        self.children={}
        self.isEnd=False
        
        
class DecisionTree_ID3(object):
    def __init__(self):
        self.root=None
        self.attr_file_name="data/attr-data.txt"
        self.dt_file_name="data/dt-data.txt"
        self.attr_values={}
        self.index_attr={}
        self.dt_data=[]
    
    def buildDT(self):
        return
         
    def pre_process(self):
        print("PreProcessing...")
        if not self.load_attr_data() or not self.load_dt_data():
            return False
        self.root=self.buildDT()
        
    def parse_attr_content(self,content):
        print("Parsing attributes data...")
        if not content:
            print("Empty attr File")
            return False
        for line in content:
            line=line.replace("\n","")
            if not line:
                continue
            line=line.strip().split(":")
            attr_name=line[0]
            attr_values=line[1].strip()[1:-1]
            attr_values=attr_values.split(", ")
            if attr_name in self.attr_values:
                print("Duplicate attr!")
                return False
            self.attr_values[attr_name]=attr_values
        print("Finish parsing attributes data...")
        return True 
    
    def load_attr_data(self):
        print("Loading attributes data...")
        try:
            file=open(self.attr_file_name, "r")
            content=file.readlines()
        except FileNotFoundError:
            print(self.attr_file_name+" File not Found!")
            return False
        except:
            print("Error")
            return False
        print("Finish loading attributes data...")
        return self.parse_attr_content(content)
        
    def parse_dt_content(self,content):
        print("Parsing training data...")
        if not content:
            print("Empty dt File!")
            return False
        for line_index,line in enumerate(content):
            line=line.replace("\n","")
            if line_index==0:
                line=line[1:-1]
                line=line.strip().split(", ")
                for attr_index,attr in enumerate(line):
                    self.index_attr[attr_index]=attr
            else:
                if not line:
                    continue
                line=line.strip().split(":")[1][1:-1]
                line=line.strip().split(", ")     
                self.dt_data.append(line) 
        print("Finish parsing training data...")
        return True
        
    def load_dt_data(self):
        print("Loading training data...")
        try:
            file=open(self.dt_file_name, "r")
            content=file.readlines()
        except FileNotFoundError:
            print(self.dt_file_name+" File not Found!")
            return False
        except:
            print("Error load dt data")
            return False
        print("Finish loading training data...")
        return self.parse_dt_content(content)

if __name__ == '__main__':
    decisionTree_ID3=DecisionTree_ID3()
    decisionTree_ID3.pre_process()