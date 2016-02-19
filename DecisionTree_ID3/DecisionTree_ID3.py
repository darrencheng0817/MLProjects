'''
Created on 2016年2月1日
Implementation of decision tree algorithm.
@author: Darren
'''
from math import log
class TreeNode(object):
    def __init__(self,name):
        self.name=name  #Attribute name
        self.children={}    #key:value of current attribute, value:child node
        self.isEnd=False    #Flag to indicate the leaf
        self.decision={}    #key:value of current attribute, value:label 
        
class DecisionTree_ID3(object):
    def __init__(self):
        self.root=None
        self.attr_file_name="data/attr-data.txt"
        self.dt_file_name="data/dt-data.txt"
        self.query_file_name="data/query.txt"
        self.output_file_name="output.txt"
        self.attr_values={} #key:attribute value:list of the values
        self.index_attr={}  #key:index of attribute in the training data value:attribute
        self.attr_index={}  #key:attribute value:index of attribute in the training data
        self.dt_data=[] #list of training data
        self.query_data={} #key: attribute value:value of attribute
        
    def buildDT(self):
        print("Building decision tree...")
        res=self.buildDTUtil(self.dt_data, set(self.attr_values.keys()))
        print("Finished building decision tree...")
        return res
    
    def get_max_entropy_gain(self,dt_data,attrs):
        if not dt_data:
            return
        statistic={}
        for line in dt_data:
            for index,value in enumerate(line[:-1]):
                attr=self.index_attr[index]
                if attr not in attrs:
                    continue
                if attr not in statistic:
                    statistic[attr]={}
                if value not in self.attr_values[attr]:
                    raise Exception("Unknown content!")
                else:
                    if value not in statistic[attr]:
                        statistic[attr][value]={}
                        statistic[attr][value]["total"]=0
                    label=line[-1]
                    if label not in statistic[attr][value]:
                        statistic[attr][value][label]=0
                    statistic[attr][value][label]+=1
                    statistic[attr][value]["total"]+=1
        total_data_count=len(dt_data)
        res_attr=""
        min_entropy=1
        for attr in statistic.keys():
            sum_entropy=0
            for value in self.attr_values[attr]:
                local_sum=0
                if value not in statistic[attr]:
                    continue
                for label in statistic[attr][value].keys():
                    if label=="total":
                        continue
                    local_sum+=(-statistic[attr][value][label]/statistic[attr][value]["total"]*log(statistic[attr][value][label]/statistic[attr][value]["total"])/log(2))
                sum_entropy+=(local_sum)*statistic[attr][value]["total"]/total_data_count
            if sum_entropy<min_entropy:
                min_entropy=sum_entropy
                res_attr=attr
        if min_entropy==1:
            min_entropy=0.0
        return (res_attr,min_entropy) 
    
    def buildDTUtil(self,dt_data,attrs):
        candidate,entropy=self.get_max_entropy_gain(dt_data,attrs)
        res_node=TreeNode(candidate)
        if entropy==0:
            res_node.isEnd=True
            for data in dt_data:
                res_node.decision[data[self.attr_index[candidate]]]=data[-1]
        else:
            data_set={}
            attr_index=self.attr_index[candidate]
            for data in dt_data:
                if data[attr_index] not in data_set:
                    data_set[data[attr_index]]=[]
                data_set[data[attr_index]].append(data)
            new_attrs=set(attrs)
            new_attrs.remove(candidate)
            for key in data_set.keys():
                res_node.children[key]=self.buildDTUtil(data_set[key], new_attrs)
        return res_node
    
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
        print("Finished parsing attributes data...")
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
        print("Finished loading attributes data...")
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
                    self.attr_index[attr]=attr_index
            else:
                if not line:
                    continue
                line=line.strip().split(":")[1][1:-1]
                line=line.strip().split(", ")     
                self.dt_data.append(line) 
        print("Finished parsing training data...")
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
        print("Finished loading training data...")
        return self.parse_dt_content(content)
    
    def query(self):
        if not self.load_query():
            return
        print("Making query...")
        res=self.query_util(self.root)
        if not res:
            print("Can't make prediction!")
        else:
            print("Prediction: "+res)
        
    def query_util(self,root):
        if root.isEnd:
            if self.query_data[root.name] not in root.decision:
                return ""
            return root.decision[self.query_data[root.name]]
        if self.query_data[root.name] not in root.children:
            return ""
        return self.query_util(root.children[self.query_data[root.name]])
    
    def parse_query_content(self,content):
        print("Parsing query data...")
        if not content:
            print("Empty dt File!")
            return False
        for line_index,line in enumerate(content):
            line=line.replace("\n","")
            line=line.strip().split(";")
            for item in line:
                item=item.strip().split("=")
                self.query_data[item[0].strip()]=item[1].strip()
        print("Finished parsing query data...")
        return True
        
    def load_query(self):
        print("Loading query data...")
        try:
            file=open(self.query_file_name, "r")
            content=file.readlines()
        except FileNotFoundError:
            print(self.query_file_name+" File not Found!")
            return False
        except:
            print("Error load dt data")
            return False
        print("Finished loading query data...")
        return self.parse_query_content(content)
    
        
    def out_put_tree_util(self,root,res,path):
        if root.isEnd:
            for key in root.decision.keys():
                res.append('if '+path+root.name+'=="'+key+'" then '+root.decision[key])
            return
        for key in root.children.keys():
            self.out_put_tree_util(root.children[key], res,path+root.name+'=="'+key+'" and ')
                
    def out_put_tree_to_file(self):
        res=[]
        self.out_put_tree_util(self.root,res,"")
        try:
            file=open(self.output_file_name, "w")
            for line in res:
                file.write(line+"\n")
        except FileNotFoundError:
            print(self.attr_file_name+" File not Found!")
        except:
            print("Error")
                
    def out_put_tree(self):
        print("Outputing Decision tree...")
        res=[]
        self.out_put_tree_util(self.root,res,"")
        for line in res:
            print(line)

if __name__ == '__main__':
    decisionTree_ID3=DecisionTree_ID3()
    decisionTree_ID3.pre_process()
    decisionTree_ID3.out_put_tree_to_file()
    decisionTree_ID3.out_put_tree()
    decisionTree_ID3.query()