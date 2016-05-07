'''
Created on 2016年5月3日

@author: Darren
'''
DICTFILE="supportingData/SentiWordNet_3.0.0_20130122.txt"
ROOTPATH="rawData"
class Classifier(object):
    def __init__(self):
        self.d={}
    
    def classifier(self):
        oppos=["not","can't","didn't","don't","couldn't","nor","neither","isn't","aren't","wasn't"]
        total_num=12500
#         for NEG data
        neg_count=0
        for i in range(1,total_num+1):
            file_name=ROOTPATH+"/NEG."+'{0:05d}'.format(i)+".txt"
            data=self.loadData(file_name)
            words=data.split(" ")
            score=0
            for index,item in enumerate(words):
                word=item
#                 word=item.split("/")[0]
                if word and not word[-1].isalpha():
                    word=word[:-1]
                if word in oppos:
                    score-=1
                if word in self.d:
                    if index>0 and words[index-1] in oppos:
                        score-=(self.d[word][0]-self.d[word][1])
                    else:
                        score+=(self.d[word][0]-self.d[word][1])
            if score<=0:
                neg_count+=1
                
        print("Negative accuracy:",neg_count/total_num)
#         for POS data
        pos_count=0
        for i in range(1,total_num+1):
            file_name=ROOTPATH+"/POS."+'{0:05d}'.format(i)+".txt"
            data=self.loadData(file_name)
            words=data.split(" ")
            score=0
            for index,item in enumerate(words):
                word=item
#                 word=item.split("/")[0]
                if word and not word[-1].isalpha():
                    word=word[:-1]
                if word in self.d:
                    if index>0 and words[index-1] in oppos:
                        score-=(self.d[word][0]-self.d[word][1])
                    else:
                        score+=(self.d[word][0]-self.d[word][1])
            if score>=0:
                pos_count+=1
        print("Positive accuracy:",pos_count/total_num)
        
          
    def loadData(self,file_name):
        try:
            with open(file_name,"r",encoding='utf-8') as file:
                data=file.read()
                return data 
        except Exception as e:
            e
            #do nothing
        return ""
    
    def loadDict(self):
#         try:
#             with open(DICTFILE,"r") as file:
#                 data=file.readlines()
#                 for index,line in enumerate(data):
#                     line=line.strip("\n")
#                     if line[0]=="#":
#                         continue
#                     line=line.split("-|-")
#                     if float(line[2])>0 or float(line[3])>0:
#                         words=line[4].split(" ")
#                         for word in words:
#                             word=word.split("#")[0]
#                             self.d[word]=[float(line[2]),float(line[3])]               
#         except Exception as e:
#             print(e)
        try:
            with open("supportingData/negativeWord.txt","r",encoding='utf-8') as file:
                data=file.readlines()
                for index,line in enumerate(data):
                    line=line.strip("\n")
                    if line==";":
                        continue
                    self.d[line]=[0,1]             
        except Exception as e:
            print(e)
        try:
            with open("supportingData/positiveWord.txt","r",encoding='utf-8') as file:
                data=file.readlines()
                for index,line in enumerate(data):
                    line=line.strip("\n")
                    if line==";":
                        continue
                    self.d[line]=[1,0]             
        except Exception as e:
            print(e)
            
    
    def run(self):
        self.loadDict()
        self.classifier()
#         print(len(self.d))
    
classifier=Classifier()
classifier.run()