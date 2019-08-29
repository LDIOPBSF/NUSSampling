#-*- coding:Utf-8 -*-

# NUSSampling
# Copyright (c) 2019  Lamine Diop (1;2), Cheikh Talibouya Diop (1), Arnaud Giacometti (2), Dominique Li (2) and Arnaud Soulet (2)
# (1) University of Gaston Berger of Saint-Louis, Senegal, Email: {diop.lamine3, cheikh-talibouya.diop}@ugb.edu.sn
# (2) University of Tours, France, Email: {arnaud.giacometti, dominique.li, arnaud.soulet}@univ-tours.fr

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# ---------------------------------------------------------------------

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
    N=1000 # Sample size
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
                print ("Preprocessing time (s) : ", tmps22)
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
                    print ("Sampling time (s) : ", tmps22)
                #************  Ouput 
                #   creatArffFile(contenuBaseSequence, EnsSousSequence, indiceClass,relation,N,tailleMax,nbRep)
                #   recordSample(EnsSousSequence, N, tailleMax, utility, relation,alpha)
                #   recordSampleWithFrequecy(contenuBaseSequence, EnsSousSequence, N, tailleMax, utility, relation,alpha)
                tmps2=time.process_time()-tmps1
                print ("****************** Total execution time (s) : ",tmps2)
    
if __name__ == "__main__":
    main()

