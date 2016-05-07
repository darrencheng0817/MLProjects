'''
Created on 2016年5月3日

@author: Darren
'''
DICTFILE="supportingData/SentiWordNet_3.0.0_20130122.txt"
ROOTPATH="rawDataTagged"
SPLITINDEX=6000
class Classifier(object):
    def __init__(self):
        self.d={}
    
    def classifier(self):
        oppos=["not","can't","didn't","don't","couldn't","nor","neither","isn't","aren't","wasn't"]
        total_num=12500
#         for NEG data
        neg_count=0
        for i in range(SPLITINDEX,total_num+1):
            file_name="rawData/NEG."+'{0:05d}'.format(i)+".txt"
            data=self.loadData(file_name)
            words=data.split(" ")
            score=0
            for index,item in enumerate(words):
                word=item.split("/")[0]
                if word and not word[-1].isalpha():
                    word=word[:-1]
                if word in oppos:
                    score-=1
                if word in self.d:
                    if index>0 and words[index-1] in oppos:
                        score-=(self.d[word][0]-self.d[word][1])
                    else:
                        score+=(self.d[word][0]-self.d[word][1])
            if score<0:
                neg_count+=1
        print("Negative accuracy:",neg_count/(total_num-SPLITINDEX+1))
#         for POS data
        pos_count=0
        for i in range(SPLITINDEX,total_num+1):
            file_name="rawData/POS."+'{0:05d}'.format(i)+".txt"
            data=self.loadData(file_name)
            words=data.split(" ")
            score=0
            for index,item in enumerate(words):
                word=item.split("/")[0]
                if word and not word[-1].isalpha():
                    word=word[:-1]
                if word in self.d:
                    if index>0 and words[index-1] in oppos:
                        score-=(self.d[word][0]-self.d[word][1])
                    else:
                        score+=(self.d[word][0]-self.d[word][1])
            if score>0:
                pos_count+=1
        print("Positive accuracy:",pos_count/(total_num-SPLITINDEX+1))
        
          
    def loadData(self,file_name):
        try:
            with open(file_name,"r",encoding='utf-8') as file:
                data=file.read()
                return data 
        except Exception as e:
            e
            #do nothing
        return ""
    
    def train(self):
        oppos=["not","can't","didn't","don't","couldn't","nor","neither","isn't","aren't","wasn't"]
        target_tag=["NN","RB"]
#         for NEG data
        for i in range(1,SPLITINDEX):
            file_name=ROOTPATH+"/NEG."+'{0:05d}'.format(i)+".txt"
            data=self.loadData(file_name)
            words=data.split(" ")
            for index,item in enumerate(words):
                item=item.split("/")
                word=""
                tag=""
                if len(item)>1:
                    word=item[0]
                    tag=item[1]
                if tag in target_tag:
                    while word and not word[-1].isalpha():
                        word=word[:-1]
                    if word not in self.d:
                        self.d[word]=[0,0]
                    self.d[word][1]+=1

#         for POS data
        for i in range(1,SPLITINDEX):
            file_name=ROOTPATH+"/POS."+'{0:05d}'.format(i)+".txt"
            data=self.loadData(file_name)
            words=data.split(" ")
            for index,item in enumerate(words):
                item=item.split("/")
                word=""
                tag=""
                if len(item)>1:
                    word=item[0]
                    tag=item[1]
                if tag in target_tag:
                    while word and not word[-1].isalpha():
                        word=word[:-1]
                    if word not in self.d:
                        self.d[word]=[0,0]
                    self.d[word][0]+=1
    
    def run(self):
        self.train()
#         print(self.d)
        for key in list(self.d.keys()):
            total=self.d[key][0]+self.d[key][1]
            self.d[key][0]/=total
            self.d[key][1]/=total

        self.classifier()
#         print(len(self.d))
    
classifier=Classifier()
classifier.run()