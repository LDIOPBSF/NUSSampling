#-*- coding:Utf-8 -*-

__author__ = "DIOP Lamine BSF"

import os
#import sys
import time

#Inclusion 
def inclus(itemset1, itemset2):
    itemset1=itemset1.split(' ')
    itemset2=itemset2.split(' ')
    for f in itemset1:
        if f not in itemset2:
            return False
    return True
    
#Check if a sequence is a subsequence of another sequence
def isSubSequence(sousSeq, sequence):
    tab1=sousSeq.split(' -1 ')[:-1]
    tab2=sequence.split(' -1 ')
    if len(tab1)>len(tab2):
        return False
    i,j,ok, taille1,taille2=0,0,True,len(tab1),len(tab2)
    while i<taille1 and ok:
        while j<taille2 and not inclus(tab1[i], tab2[j]): 
            j+=1
        if j==taille2:
            ok=False    
        else:
            j+=1
        i+=1
    return ok==True
    

#Frequency
def frequence(contenuBaseSequence,sousSequence):
    som=0
    for sequence in contenuBaseSequence:
        if isSubSequence(sousSequence,sequence)==True:
            som+=1
    return som

def toArff(contenuBaseSequence, mesAttributs, arffData, indiceClass, classAtt):
    for sequence in contenuBaseSequence:
        seq=sequence.split(' -1 ')
        for s in mesAttributs:
            if isSubSequence(s,sequence)==True:
                arffData=arffData+"1,"
            else:
                arffData=arffData+"0,"
        arffData=arffData+"'"+seq[indiceClass]+"'"+'\n'
        classAtt.add(seq[indiceClass])           
    return [arffData, classAtt]

def creatArffFile(contenuBaseSequence, EnsSousSequence, indiceClass, relation,N,tailleMax,nbRep, utility):
    EnsSousSequence = list(set(EnsSousSequence))
    arffPathDir = "Arff."+utility
    os.makedirs(arffPathDir+"/"+relation+"/M"+str(tailleMax)+"-"+relation+"/N"+str(N), exist_ok=True)
    tmps21=time.process_time()
    arffData, indiceClass, classAtt = "",0,set()
    arffFic = toArff(contenuBaseSequence, EnsSousSequence, arffData, indiceClass, classAtt)
    arffData, classAtt = arffFic[0], arffFic[1]
    ficArff = "@relation "+str(tailleMax)+'_'+relation+'_'+str(N)+"_"+utility+"\n"
    for i in range(len(EnsSousSequence)):
        ficArff=ficArff+"@attribute att"+str(i+1)+" {0, 1}\n"
    
    ficArff=ficArff+"@attribute Class {'"+"', '".join(classAtt)+"'}\n\n\n@data\n"+arffData
    
    with open(arffPathDir+"/"+relation+"/M"+str(tailleMax)+"-"+relation+"/N"+str(N)+"/"+relation+'M'+str(tailleMax)+"N"+str(N)+"R"+str(nbRep)+'.arff', 'w') as fic:
        fic.write(ficArff)
    tmps22=time.process_time()-tmps21
    print ("Arff file building time = ",tmps22)


def recordSample(EnsSousSequence, N, tailleMax, utility, relation):
    samplePathDir = "Samples."+utility
    tmps21=time.process_time()
    ficSample=""
    for s in EnsSousSequence:
        ficSample=ficSample+s+"-2\n"
      
    with open(samplePathDir+'/'+utility+"_M"+str(tailleMax)+'_'+relation+'_N'+str(N)+'.txt', 'w') as fic:
        fic.write(ficSample)
    tmps22=time.process_time()-tmps21
    print ("Recording time = ",tmps22)


def recordSampleWithFrequecy(contenuBaseSequence, EnsSousSequence, N, tailleMax, utility, relation,alpha):
    samplePathDir = "Samples."+utility
    tmps21=time.process_time()
    subSeq = {}
    for s in EnsSousSequence:
        if s in subSeq.keys():
            subSeq[s]+=1
        else:
            subSeq[s]=1
    ficSample="#subsequence (s \in Sample : s ~ D)\tfreq(s,D)\tfreq(s,Sample)\n\n"
    for s in subSeq.keys():
        freq = frequence(contenuBaseSequence, s)
        ficSample=ficSample+s+"-2"+"\t"+str(freq)+"\t"+str(subSeq[s])+"\n"
    with open(samplePathDir+'/'+utility+"_M"+str(tailleMax)+'_'+relation+'_N'+str(N)+"_alpha"+str(alpha).replace(".", "")+'.txt', 'w') as fic:
        fic.write(ficSample)
    tmps22=time.process_time()-tmps21
    print ("Recording time = ",tmps22)
