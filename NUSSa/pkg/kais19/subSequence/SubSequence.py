
#-*- coding:Utf-8 -*-

__author__ = "Lamine DIOP BSF"

import random

class SubSequence(object):	
	def __init__(self,EnsSequence, EnsSousSequence,nombreDeRejet,contenuBaseSequence,basePonderee, c_accept, c_rejet,tabSigma,indiceClass,utility,alpha):
		self.alpha = alpha
		self.utility=utility
		self.delimiteurItemset = '-1 '
		self.delimiteurSequence = '-2 '
		i,nbSeq=0,len(contenuBaseSequence)
		somme=tabSigma[nbSeq-1]
		alea=somme*random.random()
		self.m=self.trouver(tabSigma,i,nbSeq,alea)
		self.maSequence=self.tableauItemset(contenuBaseSequence[self.m])
		self.M=basePonderee[self.m]
		self.result=self.sousSequence(self.maSequence,nombreDeRejet,self.M[1:],indiceClass)
		self.maSousSequence=self.result[0]
		self.nombreDeRejet=self.result[1]
		c_accept+=self.result[2]
		c_rejet+=self.result[3]
		self.sousSeq=""
		for itemset in self.maSousSequence:
			if itemset!=' ':
				self.sousSeq+=itemset+self.delimiteurItemset+" "
		self.nombreDeRejet = nombreDeRejet
		self.c_accept = c_accept
		self.c_rejet = c_rejet
		EnsSousSequence.append(self.sousSeq)
	
		self.delimiteurI=self.delimiteurItemset+' '
		maSequence= self.delimiteurI.join(self.maSequence)+self.delimiteurItemset+' '+self.delimiteurSequence
		if maSequence in EnsSequence.keys():
			EnsSequence[maSequence]+=1
		else:
			EnsSequence[maSequence]=1
		
	
	
	#pile ou face
	def pile(self):
		return (random.randint(0,1)==1)
	
	#itemset1 privé de l'itemset2
	def prive(self, itemset1,itemset2,indiceClass):
		p,k=0,1
		if indiceClass>0:
			k+=1
		else:
			p=1
		itemset1=itemset1.split(' ')[:-1]
		itemset2=itemset2.split(' ')[p:-k]
		itemset=[]
		for item in itemset1:
			if item not in itemset2:
				itemset.append(item)
		return ' '.join(itemset)+' '
	
	
	def k_norme(self, tabNorme):
		tab=[]
		som=0
		if self.utility=="freq":
			for val in tabNorme:
				som+=val
				tab.append(som)
		elif self.utility=="area":
			for l in range(len(tabNorme)):
				som+=tabNorme[l]*(l+1)
				tab.append(som)
		elif self.utility=="weight":
			for l in range(len(tabNorme)):
				som+=tabNorme[l]*pow(self.alpha,l+1)
				tab.append(som)
				
		i,j=0,len(tab)-1
		alea=random.random()*tab[j]
		k=self.trouver(tab,i,j+1,alea)
		return k+1
		
	
	
	#Tirage aléatoire d'une sous-séquence
	def sousSequence(self, sequence2, nombreDeRejet,tabNorme,indiceClass):
		self.sousSequence=[]
		tailleItemRej=0
		rejet=True
		self.maSeq,Tab=[],[]
		maSeq='-1 '.join(sequence2).split(' ')[:-1]
		if indiceClass==len(sequence2)-1:
			indiceClass=len(maSeq)-1
		Tab[:]=[i for i in range(len(maSeq)) if str(maSeq[i])!='-1' and i!=indiceClass]
		x=self.k_norme(tabNorme)
		T,L=[],[]
		while rejet==True:
			T[:]=list(Tab)
			X=[]
			for i in range(x):			
				m=random.randint(0,len(T)-1)
				X.append(T[m])
				T.remove(T[m])
			L=[]
			f=0
			while f< len(maSeq):
				if f in X or maSeq[f]=='-1':
					L.append(maSeq[f]+' ')
				else:
					L.append('')
				f+=1
			L=''.join(L).split('-1 ')
			n=len(L)-1
			rejet=False
			while n>0 and rejet==False:
				if len(L[n]) != 0:
					k=n-1
					while k>=0 and rejet==False and L[k] in ' ':
						if self.prive(L[n],sequence2[k],indiceClass) not in ' ':
							#sys.exit()
							k-=1
						else:
							L=[]
							rejet=True
							nombreDeRejet+=1
							tailleItemRej+=x
				n-=1
		accep=x
		sousSequence=[b for b in L if b !='']
		return [sousSequence,nombreDeRejet,accep,tailleItemRej]
	
	def tableauItemset(self, sequence):
		self.delimiteurItemset='-1'
		return sequence.split(self.delimiteurItemset+' ')[:-1]
	
	
	#somme des pondérations des séquences de la base
	def tirageSequence(self):
		return self.seq,self.mat
		
	
	
	def trouver(self, tab,i,j,x):
		m=int((i+j)/2)
		if m==0 or (tab[m-1]<x and x<=tab[m]):
			return m
		if tab[m]<x:
			return self.trouver(tab,m+1,j,x)
		return self.trouver(tab,i,m,x)
	
	
	def nbItemset(self, seq):
		nbitemset=0
		if seq!=[]:
			for f in seq:
				if f not in '  ':
					nbitemset+=1
		return nbitemset
	
	def ensembleItems(self, sequence2):
		ens,t=set(),[]
		for i in range(0,len(sequence2)):
			a=sequence2[i].split(' ')[:-1]
			if len(a)>0:
				ens=ens.union(a)
		t[:] = [i for i in ens if len(i)!=0]
		return t
			
	
	
	def priveXdansT(self, X,T):
		return [e for e in T if e not in X]
	
	
		
	
	
	#Norme d'une séquence à partir de sa forme brute, ex : 12 2 -1 3 5 -1 
	def norme(self, sequence):
		sequence=sequence.replace('-1 ', '').split(' ')[:-1]
		som=0
		for f in sequence:
			if f not in '  ':
				som+=1
		return som
	
	#Norme d'une séquence à partir de son tableau d'itemsets correspondant 
	def normeTabItemset(self, tabItemset):
		sequence='-1 '.join(tabItemset).replace('-1 ', '').split(' ')[:-1]
		som=0
		for f in sequence:
			if f not in '  ':
				som+=1
		return som
	
	
	def sommeComb(self, contenuBaseSequence,i,k1,k2):
		val,n=0,self.norme(contenuBaseSequence[i])
		for i in range(k1,k2+1):
			val+=self.combin(n,i)
		return val

