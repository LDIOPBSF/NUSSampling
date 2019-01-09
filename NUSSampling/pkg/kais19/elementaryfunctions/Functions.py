#-*- coding:Utf-8 -*-

__author__ = "DIOP Lamine BSF"

import os
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

def creatArffFile(contenuBaseSequence, EnsSousSequence, indiceClass, relation,N,tailleMax,nbRep):
    EnsSousSequence = list(set(EnsSousSequence))
    os.makedirs("Arff/"+relation+"/M"+str(tailleMax)+"-"+relation+"/N"+str(N), exist_ok=True)
    tmps21=time.process_time()
    arffData, indiceClass, classAtt = "",0,set()
    arffFic = toArff(contenuBaseSequence, EnsSousSequence, arffData, indiceClass, classAtt)
    arffData, classAtt = arffFic[0], arffFic[1]
    ficArff = "@relation "+str(tailleMax)+'_'+relation+'_'+str(N)+relation+"\n"
    for i in range(len(EnsSousSequence)):
        ficArff=ficArff+"@attribute att"+str(i+1)+" {0, 1}\n"
    
    ficArff=ficArff+"@attribute Class {'"+"', '".join(classAtt)+"'}\n\n\n@data\n"+arffData
    
    with open("Arff/"+relation+"/M"+str(tailleMax)+"-"+relation+"/N"+str(N)+"/"+relation+'M'+str(tailleMax)+"N"+str(N)+"R"+str(nbRep)+'.arff', 'w') as fic:
        fic.write(ficArff)
    tmps22=time.process_time()-tmps21
    print ("Arff file building time = ",tmps22)


def recordSample(EnsSousSequence, N, tailleMax, utility, relation,alpha):
    tmps21=time.process_time()
    ficSample=""
    for s in EnsSousSequence:
        ficSample=ficSample+s+"-2\n"
    alphaStr=""
    if(utility=="alpha"):
        alphaStr=str(alpha)
    with open('Samples/'+utility+alphaStr+"_M"+str(tailleMax)+'_'+relation+'_N'+str(N)+'.txt', 'w') as fic:
        fic.write(ficSample)
    tmps22=time.process_time()-tmps21
    print ("Recording time = ",tmps22)


def recordSampleWithFrequecy(contenuBaseSequence, EnsSousSequence, N, tailleMax, utility, relation,alpha):
    tmps21=time.process_time()
    subSeq = {}
    for s in EnsSousSequence:
        if s in subSeq.keys():
            subSeq[s]+=1
        else:
            subSeq[s]=1
    ficSample="#subsequece (s \in Sample : s ~ D)\tfreq(s,D)\tfreq(s,Sample)\n\n"
    for s in subSeq.keys():
        freq = frequence(contenuBaseSequence, s)
        ficSample=ficSample+s+"-2"+"\t"+str(freq)+"\t"+str(subSeq[s])+"\n"
    alphaStr=""
    if(utility=="alpha"):
        alphaStr=str(alpha)
    with open('Samples/'+utility+alphaStr+"_M"+str(tailleMax)+'_'+relation+'_N'+str(N)+'.txt', 'w') as fic:
        fic.write(ficSample)
    tmps22=time.process_time()-tmps21
    print ("Recording time = ",tmps22)
    
    
def nussamplingLicence():
    print("\n**********************************************************************************\n* NUSSampling : Norm-based Utility Subsequence Sampling.\t\t\t *\n* It's a generalisation of the CSSampling algorithm of Diop & al. (ICDM2018).\t *\n* NUSSampling takes into account several utilities that base on the norm of \t *\n* the patterns. This version is under consideration for publication in Knowledge *\n* and Information Systems (KAIS2019).\t\t\t\t\t\t *\n* version : 1.0\t\t\t\t\t\t\t\t\t *\n* Date : 09/01/2019\t\t\t\t\t\t\t\t *\n**********************************************************************************\n")
