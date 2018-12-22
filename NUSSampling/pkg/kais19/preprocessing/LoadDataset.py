#-*- coding:Utf-8 -*-

__author__ = "DIOP Lamine BSF"

class LoadDataset(object):
    
    def __init__(self, baseSequence,indiceClass):
        self.delimiteurSequence = str('-2 ')
        self.dataset = list()
        self.size = 0
        with open(baseSequence, 'r') as base:
            line=base.readline()
            while line:
                self.dataset.append(line.replace("-2","").replace("\n",""))
                line=base.readline()
        self.dataset = self.dataset
        self.size=self.dataset.__len__()
    
    def dataset(self):
        return self.dataset