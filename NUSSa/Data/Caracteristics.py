#!C:\Python27
#-*- coding:Utf-8 -*-

__author__ = "DIOP Lamine BSF"

import os
import sys

baseSequence=sys.argv[1]

delimiteurSequence='-2 '

mesBases=["BMS.txt","SIGN.txt","D100K6S2T6I.txt","D100K5S2T6I.txt","D10K5S2T6I.txt","D10K6S3T10I.txt",]
def contenuDeMaBase(baseSequence):
    with open(baseSequence, 'r') as base:
        contenu=base.read()
    contenu=contenu.replace('\n',' ') 
    contenu=contenu.replace('\r',' ')
    contenu=contenu[:-2]
    contenu=contenu.split(delimiteurSequence)
    #print "bsf",contenu
    return contenu

for baseSequence in mesBases:
    print("===================="),baseSequence,("==================")
    #Lecture de la base de séquences
    contenu=""
    T=0
    contenu=contenuDeMaBase(baseSequence)
    
    for sequence in contenu:
        sequence=sequence.split(' -1 ')
        for itemset in sequence:
            T= max(T,len(itemset.split(' ')))
    print("T = "),T




