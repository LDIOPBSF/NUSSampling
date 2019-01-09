#-*- coding:Utf-8 -*-

__author__ = "DIOP Lamine BSF"

import os
import time
import sys
import math
import csv
import re
import random
import functools
from pkg.kais19.subSequence.SubSequence import *
from pkg.kais19.preprocessing.LoadDataset import *
from pkg.kais19.preprocessing.WeightedDataset import *
from pkg.kais19.elementaryfunctions.Functions import *
import numpy


def main():
    indiceClass = -1 # negative value if no class
    N=10000 # Sample size
    utility = "area" # "area" or "freq" or alpha "asl-gt-thad.txt", "asl-bu.txt", "seq-auslan", "blocks.txt", "context.txt", "pioneer.txt", "skater.txt"
    alpha = 0.05 # by default
    datasets = ["D10K5S2T6I.txt"] #,"D10K6S3T10I.txt","D100K5S2T6I.txt","D100K6S2T6I.txt"]
    nussamplingLicence()
    print("****************** Number of patterns : ",N," ******************")
    for baseSequence in datasets:
        contenuBaseSequence = LoadDataset("Data\\"+baseSequence, -1).dataset
        relation=baseSequence.split(".")[0]
        print("Dataset : ",relation)
        for tailleMax in [2,3]: # maximal norm, by default minimal norm m=1
            print("Maximum norm : ",tailleMax)
            for utility in ["area"]:
                tmps1=time.process_time()
                print("utility : ",utility)
            #************  Preprocessing
                tmps21=time.process_time()
                wData = WeightedDataset(contenuBaseSequence,tailleMax,indiceClass,utility,alpha)
                basePonderee,tabSigma=wData.basePonderee,wData.tabSigma
                tmps22=time.process_time()-tmps21
                print ("Preprocessing time : ", tmps22)
            #************  Sampling
                for nbRep in range(1):
                    tmps21=time.process_time()
                    EnsSousSequence, EnsSequence=[],{}
                    nombreDeRejet,c_accept, c_rejet=0,0,0
                    tableauPhiSequence,tableauNbApparitionSequence=[],[]
                    i=0
                    while i<N:
                        mesValParam=SubSequence(EnsSequence, EnsSousSequence,nombreDeRejet,contenuBaseSequence,basePonderee, c_accept, c_rejet,tabSigma,indiceClass,utility,alpha)
                        nombreDeRejet,c_accept, c_rejet=mesValParam.nombreDeRejet,mesValParam.c_accept,mesValParam.c_rejet
                        i+=1
                    tmps22=time.process_time()-tmps21
                    print ("Sampling time : ", tmps22)
                #************  Ouput 
                #   creatArffFile(contenuBaseSequence, EnsSousSequence, indiceClass,relation,N,tailleMax,nbRep)
                #   recordSample(EnsSousSequence, N, tailleMax, utility, relation,alpha)
                #   recordSampleWithFrequecy(contenuBaseSequence, EnsSousSequence, N, tailleMax, utility, relation,alpha)
                tmps2=time.process_time()-tmps1
                print ("################## Total execution time : ",tmps2)
    
if __name__ == "__main__":
    main()

