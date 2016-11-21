#!/usr/bin/env python
""" generated source for module BayesianNetwork """
from Assignment4 import *
import random
# 
#  * A bayesian network
#  * @author Panqu
#  
class BayesianNetwork(object):
    """ generated source for class BayesianNetwork """
    # 
    #     * Mapping of random variables to nodes in the network
    #     
    varMap = None

    # 
    #     * Edges in this network
    #     
    edges = None

    # 
    #     * Nodes in the network with no parents
    #     
    rootNodes = None

    # 
    #     * Default constructor initializes empty network
    #     
    def __init__(self):
        """ generated source for method __init__ """
        self.varMap = {}
        self.edges = []
        self.rootNodes = []

    # 
    #     * Add a random variable to this network
    #     * @param variable Variable to add
    #     
    def addVariable(self, variable):
        """ generated source for method addVariable """
        node = Node(variable)
        self.varMap[variable]=node
        self.rootNodes.append(node)

    # 
    #     * Add a new edge between two random variables already in this network
    #     * @param cause Parent/source node
    #     * @param effect Child/destination node
    #     
    def addEdge(self, cause, effect):
        """ generated source for method addEdge """
        source = self.varMap.get(cause)
        dest = self.varMap.get(effect)
        self.edges.append(Edge(source, dest))
        source.addChild(dest)
        dest.addParent(source)
        if dest in self.rootNodes:
            self.rootNodes.remove(dest)

    # 
    #     * Sets the CPT variable in the bayesian network (probability of
    #     * this variable given its parents)
    #     * @param variable Variable whose CPT we are setting
    #     * @param probabilities List of probabilities P(V=true|P1,P2...), that must be ordered as follows.
    #       Write out the cpt by hand, with each column representing one of the parents (in alphabetical order).
    #       Then assign these parent variables true/false based on the following order: ...tt, ...tf, ...ft, ...ff.
    #       The assignments in the right most column, P(V=true|P1,P2,...), will be the values you should pass in as probabilities here.
    #     
    def setProbabilities(self, variable, probabilities):
        """ generated source for method setProbabilities """
        probList = []
        for probability in probabilities:
            probList.append(probability)
        self.varMap.get(variable).setProbabilities(probList)

    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using rejection sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numSamples Number of rejection samples to perform
    #     
    def performRejectionSampling(self, queryVar, givenVars, numSamples):
        """ generated source for method performRejectionSampling """
        #  TODO

        mySample = Sample()
        myList = {}

        def priorSample():
        	for n in self.rootNodes:
        		myList[n.getVariable()] = False
        	sampleNode(myList)

        def sampleNode(nodeList):
        	#print self.varMap[node].getVariable().getName() #working
        	#print "current node: ", node.getName()
        	#assignment = {}
        	#assignment["Cloudy"] = True
        	#assignment["Rain"] = True
        	#assignment["wetGrass"] = True
        	#print self.varMap[node].getProbability(assignment, True)
        	#print "Look: "
        	#print self.rootNodes[0].getProbability(assignment, True)
        	#print self.rootNodes[0].getVariable().getName()
        	myCounterDebug = 0
        	allSet = False
        	childList = {}
        	#First step, giving T/F for roots. They do not have parents.
        	for nodes in nodeList:
        		childList[nodes] = True #adding to the list
        		#print "asdadsasdasd: ", nodes.getName()
        		if (random.random() <= self.varMap[nodes].getProbability(nodes.getName(), True)):
        			mySample.setAssignment(nodes.getName(), True)
        		else:
        			mySample.setAssignment(nodes.getName(), False)
        		for children in self.varMap[nodes].getChildren():
        			#print children.getVariable().getName()
        			childList[children.getVariable()] = False

        	#print "The value is: ", mySample.getValue("Cloudy")

        	while (allSet is False): #keep doing until childList's elements are all true
        		myCounterDebug += 1 # for debug, used when infinite loop happens
        		listAdd = [] # hold variables to add to childlist
        		for c in childList: # for each children of childList
        			if (childList[c]): # if this child is done... skip
						continue
        			isValid = True # boolean to check if parents are defined
        			for parents in self.varMap[c].getParents(): # check if all parents is defined
        				#print "MY PARENT IS.... = ", parents.getVariable().getName() #--- YES! REMOVE LATER
        				if (parents.getVariable() not in childList): #if not i list.. skip
        					isValid = False
        				else: # if in list... but not defined... also skip
        					if (childList[parents.getVariable()]):
        						isValid = True
        					else:
        						isValid = False

        			if (isValid): # if all parents is defined
        				#print "IS VALID OK?!?!?!"
        				childList[c] = True # child 'c' is done
        				#print c.getName()
        				assigns = {} # adding assignments
        				for parents in self.varMap[c].getParents():
        					assigns[parents.getVariable().getName()] = mySample.getValue(parents.getVariable().getName())
        					#print "THIS: ", parents.getVariable().getName()
        				myRan = random.random()
        				#print "Random is: ", myRan
        				#for pp in assigns:
        				#	print "Name: ", pp, "Value: ", assigns[pp]
        				#print "c = ", c.getName()
        				#print "self.varMap[c].getProbability(assigns, True) = ", self.varMap[c].getProbability(assigns, True)
        				if (myRan <= self.varMap[c].getProbability(assigns, True)): #applying sampling
        					mySample.setAssignment(c.getName(), True) 
        					#print "SETTING TRUE"
        				else:
        					#print "SETTING FALSE"
        					mySample.setAssignment(c.getName(), False)

        				for children in self.varMap[c].getChildren(): #keep track of children to be added
        					#print "IM ADDING THIS: ", children.getVariable().getName()
        					#childList[children.getVariable()] = False
        					listAdd += [children.getVariable()] 
        				isValid = True #reset isValid
        		for e in listAdd:
        			if (e not in childList):
        				childList[e] = False

        		isAllChecked = True		
        		for ch in childList: #check if all members are defined
        			if (childList[ch] is False):
        				isAllChecked = False
        		allSet = isAllChecked

        		#if (allSet):
        		#	print "THIS HAS FINISHED... CHECKING VALUES...."
        		#	for ch in childList:
        		#		print "AAAA: ", ch.getName(), "BBBB: ", childList[ch]




        		if (myCounterDebug > 10):
        			print "BROKEN....."
        			for c in childList:
        				print c.getName()
        			break
        #print "FINISH...."





        #givenVars is a array that contains objects of type RandomVariable located at Assignment4.py
        #Thus... can use their methods.
        #for objs in givenVars:
        #	print objs.getName()
        
        #this prints all nodes in the graph
        #for objs in self.varMap:
        #	print objs.getName()
        
        
        counter = [0.0, 0.0]
        #priorSample()

        #for n in self.varMap:
        #	
        
        for i in range(numSamples):
        	priorSample()
        	#for n in self.varMap:
        	#	print "Name: ", n.getName(), "value: ", mySample.getValue(n.getName())
        	isValid = True
        	for g in givenVars:

        		if mySample.getValue(g.getName()) != givenVars[g]:
        			isValid = False
        	if (isValid):

        		if (mySample.getValue(queryVar.getName())):
        			counter[0] += 1.0
        		else:
        			counter[1] += 1.0

        	
        

        #print "c1 = ", counter[0], "c2 = ", counter[1]

        if (counter[0] + counter[1] == 0):
        	return 0

        #if (mySample.getValue(queryVar.getName())):
      #  	return counter[0]/(counter[0] + counter[1])
      #  else:
       # 	return counter[1]/(counter[0] + counter[1])
        return counter[0]/(counter[0] + counter[1])
   
        
    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using weighted sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numSamples Number of weighted samples to perform
    #     
    def performWeightedSampling(self, queryVar, givenVars, numSamples):
        """ generated source for method performWeightedSampling """
        #  TODO

        mySample = Sample()
        myList = {}

        def weightedSample(givenNodes): #givenNodes has its name&value! asd[Sprinker ] = Ture
        	#weight
        	mySample.setWeight(1.0) # For weight
        	w = 1.0
        	for n in self.rootNodes:
        		myList[n.getVariable()] = False
        	
        	myCounterDebug = 0 #For debug only -- can be removed later
        	allSet = False # boolean to check if all childList is visited
        	childList = {}
        	#First step, giving T/F for roots.
        	for node in myList:
        		childList[node] = True #adding to the list
        		#check if current node has evidence... if not, do like rejected sample by generating random number
        		if node in givenNodes: # has evidence
        			#print "this is in evidence: ", node.getName()
        			if (givenNodes[node]):
        				mySample.setAssignment(node.getName(), True)
        				
        				w *= self.varMap[node].getProbability(node.getName(),True)
        			else:
        				mySample.setAssignment(node.getName(), False)
        				w *= self.varMap[node].getProbability(node.getName(),False)
        		else: # do not have evidence
        			if (random.random() <= self.varMap[node].getProbability(node.getName(), True)): 
        				mySample.setAssignment(node.getName(), True)
        			else:
        				mySample.setAssignment(node.getName(), False)
        		for children in self.varMap[node].getChildren(): #add childs to childlist
        			#print children.getVariable().getName()
        			childList[children.getVariable()] = False
        	#NEXT STEP

        	while (allSet is False): #keep doing until childList's elements are all true
        		myCounterDebug += 1 # for debug, used when infinite loop happens
        		listAdd = [] # hold variables to add to childlist
        		for c in childList: # for each children of childList
        			if (childList[c]): # if this child is done... skip
						continue
        			isValid = True # boolean to check if parents are defined
        			for parents in self.varMap[c].getParents(): # check if all parents is defined
        				#print "MY PARENT IS.... = ", parents.getVariable().getName() #--- YES! REMOVE LATER
        				if (parents.getVariable() not in childList): #if not in list.. skip
        					isValid = False
        				else: # if in list... but not defined... also skip
        					if (childList[parents.getVariable()]):
        						isValid = True
        					else:
        						isValid = False

        			if (isValid): # if all parents is defined
        				#print "IS VALID OK?!?!?!"
        				childList[c] = True # child 'c' is done
        				#print c.getName()
        				assigns = {} # adding assignments
        				for parents in self.varMap[c].getParents():
        					assigns[parents.getVariable().getName()] = mySample.getValue(parents.getVariable().getName())
        					#print "THIS: ", parents.getVariable().getName()
        				myRan = random.random() #random for rejected if needed
        				#print "Random is: ", myRan
        				#print "BELOW IS ASSIGNMENTS"
        				#for pp in assigns:
        				#	print "Name: ", pp, "Value: ", assigns[pp]
        				#print "ASSIGNMENTS DONE...."
        				#print "c = ", c.getName()
        				#print "self.varMap[c].getProbability(assigns, True) = ", self.varMap[c].getProbability(assigns, True)

        				if c in givenNodes: #if has evidence
        				#	print "HAS EVIDENCE: ", c.getName()
        					if givenNodes[c]:
        						mySample.setAssignment(c.getName(), True)
        						w *= self.varMap[c].getProbability(assigns,True)
        				#		print "SETTING TRUE... weight = ", self.varMap[c].getProbability(assigns,True)
        					else:
        						mySample.setAssignment(c.getName(), False)
        						w *= self.varMap[c].getProbability(assigns,False)
        				#		print "SETTING FALSE... weight = ", self.varMap[c].getProbability(assigns,False)
        				else: #if no evidence...
        				#	print "NO EVIDENCE...."
        					if (myRan <= self.varMap[c].getProbability(assigns, True)): #applying sampling
        						mySample.setAssignment(c.getName(), True) 
        				#		print "SET true...."
        					else:
        						mySample.setAssignment(c.getName(), False)
        				#		print "SET FALSE...."

        				for children in self.varMap[c].getChildren(): #keep track of children to be added
        					#print "IM ADDING THIS: ", children.getVariable().getName()
        					#childList[children.getVariable()] = False
        					listAdd += [children.getVariable()] 
        				isValid = True #reset isValid -- maybe not necessary

        		for e in listAdd:
        			if (e not in childList):
        				childList[e] = False

        		isAllChecked = True		
        		for ch in childList: #check if all members are defined
        			if (childList[ch] is False):
        				isAllChecked = False
        		allSet = isAllChecked

        		"""if (allSet):
        			print "THIS HAS FINISHED... CHECKING VALUES...."
        			for ch in childList:
        				print "AAAA: ", ch.getName(), "BBBB: ", childList[ch]"""
        		if (allSet):
        			return w



        #print weightedSample(givenVars)
        #return 0
        weights = [0, 0]
        

        for n in range(numSamples):
        	w = weightedSample(givenVars)
        	if (mySample.getValue(queryVar.getName())):
        		weights[0] += w
        	else:
        		weights[1] += w


        if (weights[0] + weights[1] == 0):
        	return 0

        #print "weight[0] = ", weights[0], " weight[1] = ", weights[1]
        #if (mySample.getValue(queryVar.getName())):
        	#return weights[0] / (weights[0] + weights[1])
       # else:
        #	return weights[1] / (weights[0] + weights[1])
        return weights[0] / (weights[0] + weights[1])
    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using Gibbs sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numTrials Number of Gibbs trials to perform, where a single trial consists of assignments to ALL
    #       non-evidence variables (ie. not a single state change, but a state change of all non-evidence variables)
    #     
    def performGibbsSampling(self, queryVar, givenVars, numTrials):
        """ generated source for method performGibbsSampling """
        #  TODO


        #queryNode, queryValue = queryVar[0]

        #print "Q: ", queryNode.getName(), " V: ", queryValue
        mySample = Sample()
        
        noEvidenceList = []

        #assigning evidences to sample
        for givenNode in givenVars:
        	mySample.setAssignment(givenNode.getName(), givenVars[givenNode])
        	#print "Setting ", givenNode.getName(), " to be ", givenVars[givenNode]

        for node in self.varMap:
        	if node not in givenVars:
        		noEvidenceList += [node]
        		#print "added: ", node.getName(), "to non-evidence list"

        for node in noEvidenceList:
        	rand = random.random()
        	if (rand < 0.5):
        		#print "assigning randomly", node.getName(), " to be True"
        		mySample.setAssignment(node.getName(), True)
        	else:
        		#print "assigning randomly", node.getName(), " to be False"
        		mySample.setAssignment(node.getName(), False)


        count = [0,0]

        #print "queryNode is: ", queryVar.getName()

        #print "This is the list of Sample: "
        #for dd in self.varMap:
        	#print dd.getName(), " = ", mySample.getValue(dd.getName())
        #print "Sample list done."
        
        for runs in range(numTrials):	#repeat n times
        	if (mySample.getValue(queryVar.getName())):
        		count[0] += 1.0
        	else:
        		count[1] += 1.0
        	for noEvidenceNode in noEvidenceList:
        		assignList = {}
        		#print "Getting list of Assignments: "

        		for node in self.varMap: #filling up assignments
        			assignList[node.getName()] = mySample.getValue(node.getName())
        			#print node.getName(), " = ", mySample.getValue(node.getName())
        		#print len(assignList)
        		#print noEvidenceNode.getName()
        		ptrue = self.varMap[noEvidenceNode].getProbability(assignList, True)
        		pfalse = self.varMap[noEvidenceNode].getProbability(assignList, False)
        		for child in self.varMap[noEvidenceNode].getChildren():
        			#print child.getVariable().getName()
        			assignList[noEvidenceNode.getName()] = True
        			pt = self.varMap[child.getVariable()].getProbability(assignList, True)
        			assignList[noEvidenceNode.getName()] = False
        			pf = self.varMap[child.getVariable()].getProbability(assignList, True)

        			if mySample.getValue(child.getVariable().getName()):
        				ptrue *= pt
        				pfalse *= pf
        			else:
        				ptrue *= (1.0-pt)
        				pfalse *= (1.0-pf)
        		P = ptrue/(ptrue+pfalse)
        		rann = random.random()
        		if rann <= P:
        			mySample.setAssignment(noEvidenceNode.getName(), True)
        		else:
        			mySample.setAssignment(noEvidenceNode.getName(), False)
        #print "count[0] = ", count[0], " count[1] = ", count[1]
        return count[0]/(count[1]+count[0])
        #return 0
