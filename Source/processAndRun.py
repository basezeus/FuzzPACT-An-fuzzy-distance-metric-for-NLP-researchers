import re
import numpy as np

from fuzzPact import *


doc1=""

with open("../data/doc1.txt", "r") as f:
	doc1= f.read().lower()


doc1 = re.sub(r'(.)\1{3,}', r'\1\1', doc1)
print(len(doc1[0]) )

sentences1=doc1.split("\n")



print(sentences1 )

words1=[]
for s in sentences1:
	[words1.append(w) for w in s.split(" ") if w not in words1]

print(words1)

charset=[]
for w in words1:
	[charset.append(c) for c in w if c not in charset]

print(charset)


print("-----------------------------------------------------")

doc2=""

with open("../data/doc2.txt", "r") as f:
	doc2= f.read().lower()

doc2 = re.sub(r'(.)\1{3,}', r'\1\1', doc2)

print(doc2)
#print(len(doc2[0]) )

sentences2=doc2.split("\n")
print("sentences")
print(sentences2 )

words2=[]
for s in sentences2:
	[words2.append(w) for w in s.split(" ") if w not in words2]

print(words2)

for w in words2:
	[charset.append(c) for c in w if c not in charset]

print(charset)


print("-----------------------------------------------------")

ff = fuzzyFuncs()

print("----Blended----------------")

b0 = fuzzyBlend([ff.fuzzyLevenshtein,ff.fuzzyJaccard],[.5,.5],[0.5,1]) #reduce threshold for fuzzyLevenshtein by 50%
b1 = fuzzyBlend([ff.fuzzyLevenshtein,ff.fuzzyJaccard],[.5,.5])

#Level0
fm_lev = fuzzyModel(charset)
print(fm_lev.lookupTables[0])

#Level1
fl1_lev = fuzzyLevel(b0.callBlend,.7, words1,words2)

print((fl1_lev.l1, fl1_lev.l2))
print()
#print(fl)
fm_lev.addLevel(fl1_lev)
fl1_lev.compute()
print(fm_lev.lookupTables[1])
print()

nsentences1 = [s.split(" ") for s in sentences1]
nsentences2= [s.split(" ") for s in sentences2]
fl2_lev = fuzzyLevel(b1.callBlend,0.7, nsentences1, nsentences2   )
print((fl1_lev.l1, fl1_lev.l2))

fm_lev.addLevel(fl2_lev)

fl2_lev.compute()
#print(fm.levels[0].l1)


print(fm_lev.lookupTables[2])

smax = np.argmax(fm_lev.lookupTables[2],axis=1) 

#print(smax)

wmax = np.argmax(fm_lev.lookupTables[1],axis=1) 

#print(wmax)

sout=""
for i in range(len(sentences1) ):
 	sout = sout+str(sentences1[i])+","+sentences2[smax[i]]+","+ str(fm_lev.lookupTables[2][i,smax[i]]) + "\n"

#print(sout)

wout=""
for i in range(len(words1) ):
 	wout = wout+str(words1[i])+","+words2[wmax[i]]+","+ str(fm_lev.lookupTables[1][i,wmax[i]]) + "\n"

#print(wout)

with open("../data/wout.csv", "w") as f:
	f.write(str(wout))

with open("../data/sout.csv", "w") as f:
	f.write(str(sout) )