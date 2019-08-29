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

from math import log
from math import pow

class WeightedDataset(object):
    def __init__(self, dataset,tailleMax,indiceClass,utility,alpha):
        self.utility = utility
        self.alpha = alpha
        self.delimiteurItemset='-1'
        self.basePonderee, self.tabSigma,som,self.ponderation=list(),list(),0.0,{}
        for sequence in dataset:
            sequence=self.tableauItemset(sequence,indiceClass)
            self.M=self.nbSousSeqCSSampling(sequence,tailleMax)
            val=0
            if len(self.M)>0:
                val=self.sumUtility(self.M[1:],utility)
            self.basePonderee.append(self.M)
            som+=val
            self.tabSigma.append(som)
            self.ponderation[" -1 ".join(sequence)+'-2']=val

    #Norme d'une séquence à partir de son tableau d'itemsets correspondant 
    def normeTabItemset(self, tabItemset):
        sequence='-1 '.join(tabItemset).replace('-1 ', '').split()#[:-1]
        return len(sequence)
    
    #Intersection de deux itemsets
    def intersection(self, itemset1,itemset2):
        itemset1=itemset1.split()#[:-1]
        itemset2=itemset2.split()#[:-1]
        itemset=[]
        for item in itemset1:
            if item in itemset2:
                itemset.append(item)
        return ' '.join(itemset)+' '
    
    def intersection1(self, itemset1,itemset2):
        itemset1=itemset1.split()#[:-1]
        itemset2=itemset2.split()#[:-1]
        return ' '.join(list(set(itemset1).intersection(set(itemset2))))+' '
    
    #Position set
    def positionSet(self, sequence, itemset):
        ps,i=[], 0
        x=len(sequence)
        #print "sequence, itemset",sequence, itemset
        while i<x:
            intersec=self.intersection(sequence[i],itemset)
            if intersec !=' ':
                k,chaine=i+1, intersec
                while k < x and chaine not in self.intersection(sequence[k],itemset):
                    k+=1
                if k==x:
                    ps.append(i)
            i+=1
        return ps
    
    
    #l'ensemble des sous-ensembles possible d'un ensemble
    def setOfSubsets(self, ens):
        p = []
        i, imax = 1, 2**len(ens)-1
        while i <= imax:
            s = []
            j, jmax = 0, int(log(i,2))
            while j <= jmax:
                if (i>>j)&1 == 1:
                    s.append(ens[j])
                j += 1
            p.append(s)
            i += 1 
        return p
    
    #séquence formée par les itemsets des indices de 0..k
    def prefixe(self, sequence,k):
        return sequence[:-(len(sequence)-1-k)]
    
    
    #Taille d'un itemset
    def tailleItemset(self, itemset):
        return len(itemset.split(' ')[:-1])
    
    
    def unionElem(self, positionSet,sequence):
        result=set()
        for f in positionSet:    
            result=result.union(set(sequence[f].split(' ')[:-1]))
        return result
    
    
    def tableauItems(self, seq):
        tab=[]
        for f in seq:
            tab+=f.split(' ')[:-1]
        return tab
    
    def prefix(self, seq,itemset):
        for f in seq:
            if itemset in f:
                return True
        return False
    

    
    def nbItems(self, itemset):
        return len(itemset.split(' ')[:-1])
    
    #nombre de sous-sequences d'une séquence Crible d'Al'Amine
    def nbSousSeqCSSampling(self,sequence,k):
        if k==0 or sequence==[]:
            return [[1]]
        else:
            nt=self.normeTabItemset(sequence)
            k=min(k,nt)
            T=[[1],[1]]
            R=[[0],[0]]
            for i in range(1,k+1):
                T[0].append(1)
                T[1].append(T[1][i-1]+self.combin(self.nbItems(sequence[0]),i))
                R[0].append(0)
                R[1].append(0)
            for i in range(2,len(sequence)+1):
                R.append([0])
                T.append([1])
                ps=self.positionSet(sequence[:i-1], sequence[i-1])
                sousEnsPS=self.setOfSubsets(ps)
                for j in range(1,k+1):
                    T[i].append(int(0))
                    R[i].append(int(0))
                    for u in range(len(sousEnsPS)):
                        intersecMulti=sequence[:i-1][sousEnsPS[u][0]]
                        v=1
                        while v<len(sousEnsPS[u]):
                            intersecMulti=self.intersection(intersecMulti,sequence[:i-1][sousEnsPS[u][v]])
                            v+=1
                        intersecMulti=self.intersection(sequence[i-1],intersecMulti)
                        if intersecMulti==' ':
                            intersecMulti=''
                        m = min(sousEnsPS[u])
                        kmax = self.tailleItemset(intersecMulti)
                        for v in range(1,j+1):
                            R[i][j] += pow(-1,len(sousEnsPS[u])+1)*T[m][j-v]*self.combin(kmax,v)
                    for v in range(min([self.tailleItemset(sequence[i-1]),j])+1):
                        T[i][j] += T[i-1][j-v]*self.combin(self.tailleItemset(sequence[i-1]),v)
                    T[i][j] -= R[i][j]
            return T[-1][0:1]+[T[-1][i]-T[-1][i-1] for i in range(1,len(T[-1]))]
    
    def combin(self, n, k):
        if k>n or n==0: return 0 #LDIOPBSF
        if k > n//2:
            k = n-k
        x = 1
        y = 1
        i = n-k+1
        while i <= n:
            x = (x*i)//y
            y += 1
            i += 1
        return x
        
    
    def sumUtility(self, M,utility):
        self.som = 0.0
        if utility == "area":
            for i in range(len(M)):
                self.som+=M[i]*(i+1)
        elif utility == "freq":
            self.som = sum(M)
        elif utility == "alpha":
            for i in range(len(M)):
                self.som+=M[i]*pow(self.alpha,i+1)
        return self.som
    
    #Transformer la séquence en un tableau d'itemsets
    def tableauItemset(self,sequence,indiceClass):
        if indiceClass>=0:
            if indiceClass>0:
                return sequence.split(self.delimiteurItemset+' ')[:-2] # fin de sequence
            elif indiceClass==0:
                return sequence.split(self.delimiteurItemset+' ')[1:-1]  #debut de sequence
        else:
            return sequence.split(self.delimiteurItemset+' ')[:-1]
