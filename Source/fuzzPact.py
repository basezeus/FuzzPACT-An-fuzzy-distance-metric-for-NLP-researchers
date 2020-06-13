import numpy as np
'''
Assumption: The character set MUST be common!
* There is no legitimate way of having a fuzzy matching between characters that we know of.
* Either 2 characters are same or they're different.
* To compare documents from languages that have a difference of only few characters, the user is adviced to provide the union of the 2 alphabet as the "charset".
'''

class fuzzyModel:
	def __init__(self,charset):
		self.levels=[]
		self.charset = charset

		self.levels.append(fuzzyLevel(None,1,self.charset,self.charset))
		
		self.lookupTables=[]
		self.lookupTables.append(np.identity(len(charset),dtype=float))

	def addLevel(self, level):
		self.levels.append(level)
		level.id = len(self.levels)-1
		level.model = self

class fuzzyLevel:
	def __init__(self,scoringFunction,threshold, l1,l2):
		self.score= scoringFunction
		self.threshold = threshold
		#The swap seems inelegant. We would like to remove it if our scoring functions are not dependent on which list is longer
		#We  keep a track of all swaps that are performed using level[i].listsSwapped = True/False
		#if(len(l1)<=len(l2)):
		self.l1=l1
		self.l2=l2
		self.listsSwapped=False
		#else:
			# self.l2=l1
			# self.l1=l2
			# self.listsSwapped=True
			# print("swap performed!!")

		self.opTable = np.zeros((len(self.l1),len(self.l2)))
		self.id=-1
		self.model= None
		self.lookupGenerated = False;

	def compute(self):
		if self.id == -1:
			print("level not appended to any model. Add the level using: model.addLevel(level)")
			return
		if self.lookupGenerated:
			#TODO: Handle modifications to existing lookups
			print("A lookup table has been computed for this level once.")
			return

		for i in range(len(self.l1)):
			for j in range(len(self.l2)):
				self.opTable[i,j] = self.score(self.l1[i],self.l2[j], self.model, self.id,self.threshold)
		self.model.lookupTables.append(self.opTable)
		self.lookupGenerated = True
		#return opTable


#Score functions

class fuzzyBlend:
	'''
	Blends scoring mechanisms by taking the weighted averages of their return values
	'''
	def __init__(self,scoringFunctionList,weightList,fractionOfThresh=None):
		'''
		Sets up a blend.
		'''
		if not len(scoringFunctionList) == len(weightList):
			print("lengths of function list and weights do not agree")
			return

		self.scoringFunctionList = scoringFunctionList
		self.weightList= weightList

		if fractionOfThresh is None:
			self.fractionOfThresh  = [1 for f in scoringFunctionList]
		else:
			self.fractionOfThresh = fractionOfThresh

	def callBlend(self,l1,l2, model, id, thresh):
		blendedScore=0.0;
		totalWt=0.0
		for i in range( len(self.scoringFunctionList) ):
			func = self.scoringFunctionList[i]
			wt = self.weightList[i]
			totalWt+=wt
			fthr = self.fractionOfThresh[i]
			blendedScore += float(wt) * func(l1,l2, model, id, fthr*thresh)

		if totalWt ==0.0:
			print("total of weights for this blend is currently 0")
			return

		return blendedScore/totalWt

class fuzzyFuncs:
	"""implement your fuzzy functions here."""
	def __init__(self):
		pass

	def fuzzyJaccard(self, l1,l2, model, id, thresh):
		#TODO: condsider non greedy approach
		intersection = 0
		#TODO: Vectorize the following loops part
		#print(("thresh: ", thresh))
		for e1 in l1:
			#TODO: add swap check
			e1_idx = model.levels[id-1].l1.index(e1)
			temp=0
			for e2 in l2:
				e2_idx = model.levels[id-1].l2.index(e2)
				if model.lookupTables[id-1][e1_idx,e2_idx]>thresh:
					temp = max(temp , model.lookupTables[id-1][e1_idx,e2_idx])
			intersection += temp
		#print((len(l1),len(l2) , " intersection :", intersection))	
		union = len(l1)+len(l2) - intersection
		return intersection/union


	def fuzzyLevenshtein(self,l1,l2,model,id,thresh):
		numRows=len(l1)+1
		numCols=len(l2)+1
		dist = [[0 for x in range(numCols)] for x in range(numRows)]
		# source prefixes can be transformed into empty strings 
		# by deletions:
		for i in range(1, numRows):
			dist[i][0] = i

		# target prefixes can be created from an empty source string
		# by inserting the characters
		for i in range(1, numCols):
			dist[0][i] = i

		for col in range(1, numCols):
			e2_idx = model.levels[id-1].l2.index(l2[col-1])
			for row in range(1, numRows):
				e1_idx = model.levels[id-1].l1.index(l1[row-1])
	            # if l1[row-1] == l2[col-1]:
	            #     cost = 0
	            # else:
	            #     cost = 1
				cost=1
				#fetch score from lookup to get substitution cost
				#print(("e1 e2 idxes :" , (e1_idx,e2_idx) ))
				score = model.lookupTables[id-1][e1_idx,e2_idx]
				#if score<=threshold, we consider a 0 match. (The user is adviced to set threhold to 0 to negate this check!)
				if score>thresh:
					cost = 1- score

				dist[row][col] = min(dist[row-1][col] + 1,      # deletion
	                                 dist[row][col-1] + 1,      # insertion
	                                 dist[row-1][col-1] + cost) # substitution


		return 1.0 - (dist[numRows-1][numCols-1] / float(max(numRows-1,numCols-1))  )
