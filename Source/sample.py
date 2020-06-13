import numpy as np

from fuzzPact import *


ff = fuzzyFuncs()

print("----fuzzyJaccard----------------")
#Level0
fm = fuzzyModel(['a','b','c','d', 'e'])
print(fm.lookupTables[0])

#Level1
fl1 = fuzzyLevel(ff.fuzzyJaccard,.7, ['a','ab','ed'],['ab','c', 'abc', 'de'])

print((fl1.l1, fl1.l2))
print()
#print(fl)
fm.addLevel(fl1)
fl1.compute()
print(fm.lookupTables[1])
print()


fl2 = fuzzyLevel(ff.fuzzyJaccard,0.7, [['a','ab'] , ['ab'] , ['a', 'ed']], [['ab','c', 'abc'], ['c'],['de','ab']]   )
print((fl1.l1, fl1.l2))

fm.addLevel(fl2)
fl2.compute()
#print(fm.levels[0].l1)


print(fm.lookupTables[2])
fl2.compute()
print(fm.lookupTables[2])

print("----fuzzyLevenshtein----------------")

#Level0
fm_lev = fuzzyModel(['a','b','c','d', 'e'])
print(fm_lev.lookupTables[0])

#Level1
fl1_lev = fuzzyLevel(ff.fuzzyLevenshtein,.7, ['a','ab','ed'],['ab','c', 'abc', 'de'])

print((fl1_lev.l1, fl1_lev.l2))
print()
#print(fl)
fm_lev.addLevel(fl1_lev)
fl1_lev.compute()
print(fm_lev.lookupTables[1])
print()

fl2_lev = fuzzyLevel(ff.fuzzyLevenshtein,0.7, [['a','ab'] , ['ab'] , ['a', 'ed']], [['ab','c', 'abc'], ['c'],['de','ab']]   )
print((fl1_lev.l1, fl1_lev.l2))

fm_lev.addLevel(fl2_lev)

fl2_lev.compute()
#print(fm.levels[0].l1)


print(fm_lev.lookupTables[2])


print("----Blended----------------")

b0 = fuzzyBlend([ff.fuzzyLevenshtein,ff.fuzzyJaccard],[.5,.5],[0.5,1]) #reduce threshold for fuzzyLevenshtein by 50%
b1 = fuzzyBlend([ff.fuzzyLevenshtein,ff.fuzzyJaccard],[.5,.5])

#Level0
fm_lev = fuzzyModel(['a','b','c','d', 'e'])
print(fm_lev.lookupTables[0])

#Level1
fl1_lev = fuzzyLevel(b0.callBlend,.7, ['a','ab','ed'],['ab','c', 'abc', 'de'])

print((fl1_lev.l1, fl1_lev.l2))
print()
#print(fl)
fm_lev.addLevel(fl1_lev)
fl1_lev.compute()
print(fm_lev.lookupTables[1])
print()

fl2_lev = fuzzyLevel(b1.callBlend,0.7, [['a','ab'] , ['ab'] , ['a', 'ed']], [['ab','c', 'abc'], ['c'],['de','ab']]   )
print((fl1_lev.l1, fl1_lev.l2))

fm_lev.addLevel(fl2_lev)

fl2_lev.compute()
#print(fm.levels[0].l1)


print(fm_lev.lookupTables[2])