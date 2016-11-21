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
        	myCounterDebug = 0
        	allSet = False
        	childList = {}
        	#First step, giving T/F for roots. They do not have parents so we can assign probability for them.
        	for nodes in nodeList:
        		childList[nodes] = True #adding to the list as true - we add them just to to tell they are visited already
        		if (random.random() <= self.varMap[nodes].getProbability(nodes.getName(), True)): #generate random & assign probability
        			mySample.setAssignment(nodes.getName(), True)
        		else:
        			mySample.setAssignment(nodes.getName(), False)
        		for children in self.varMap[nodes].getChildren(): # add the childs in list as false. It means childs are not visited
        			if children.getVariable() not in childList: #make sure we have no duplicates
        				childList[children.getVariable()] = False


        	while (allSet is False): #keep doing until childList's elements are all true
        		listAdd = [] # hold variables to add to childlist
        		for c in childList: # for each children of childList
        			if (childList[c]): # if this child is done... skip
						continue
        			isValid = True # boolean to check if parents are defined
        			for parents in self.varMap[c].getParents(): # check if all parents is defined
        				if (parents.getVariable() not in childList): #if parent is not in list.. skip
        					isValid = False
        				else: # if in list... but not defined... also skip
        					if (childList[parents.getVariable()]):
        						isValid = True
        					else:
        						isValid = False

        			if (isValid): # if all parents is defined
        				childList[c] = True # set child 'c' is done
        				assigns = {} # hold assignments
        				for parents in self.varMap[c].getParents(): #filling up assignments
        					assigns[parents.getVariable().getName()] = mySample.getValue(parents.getVariable().getName())
        				myRan = random.random() #generate random
        				if (myRan <= self.varMap[c].getProbability(assigns, True)): #applying sampling
        					mySample.setAssignment(c.getName(), True) 
        				else:
        					mySample.setAssignment(c.getName(), False)

        				for children in self.varMap[c].getChildren(): #keep track of children to be added
        					listAdd += [children.getVariable()]
        		#add children of children to list. Avoiding duplicates			
        		for e in listAdd:
        			if (e not in childList):
        				childList[e] = False

        		isAllChecked = True # boolean to check if all variables are visited		
        		for ch in childList: #check if all members are defined
        			if (childList[ch] is False):
        				isAllChecked = False
        		allSet = isAllChecked

        counter = [0.0, 0.0]
        
        for i in range(numSamples):
        	priorSample()
        	isValid = True
        	for g in givenVars:
        		if mySample.getValue(g.getName()) != givenVars[g]:
        			isValid = False
        	if (isValid):

        		if (mySample.getValue(queryVar.getName())):
        			counter[0] += 1.0
        		else:
        			counter[1] += 1.0

        if (counter[0] + counter[1] == 0):
        	return 0

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

        def weightedSample(givenNodes):
        	w = 1.0 #weight
        	for n in self.rootNodes:
        		myList[n.getVariable()] = False
        	allSet = False # boolean to check if all childList is visited
        	childList = {}
        	#First step, giving T/F for roots.
        	for node in myList:
        		childList[node] = True #adding to the list
        		#check if current node has evidence... if not, do like rejected sample by generating random number
        		if node in givenNodes: # has evidence
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
        			if children.getVariable() not in childList: # avoid duplicate
        				childList[children.getVariable()] = False
        	
        	#NEXT STEP...
        	while (allSet is False): #keep doing until childList's elements are all true
        		listAdd = [] # hold variables to add to childlist
        		for c in childList: # for each child of childList
        			if (childList[c]): # if this child is done... skip
						continue
        			isValid = True # boolean to check if parents are defined
        			for parents in self.varMap[c].getParents(): # check if all parents is defined
        				if (parents.getVariable() not in childList): #if parent is not in list.. skip
        					isValid = False
        				else: # if in list... but not defined... also skip
        					if (childList[parents.getVariable()]):
        						isValid = True
        					else:
        						isValid = False

        			if (isValid): # if all parents is defined
        				childList[c] = True # child 'c' is done
        				assigns = {} # variable for assignments
        				for parents in self.varMap[c].getParents(): #filling assignments
        					assigns[parents.getVariable().getName()] = mySample.getValue(parents.getVariable().getName())
        				myRan = random.random() #random for rejected if needed

        				if c in givenNodes: #if c has evidence
        					if givenNodes[c]:
        						mySample.setAssignment(c.getName(), True)
        						w *= self.varMap[c].getProbability(assigns,True)
        					else:
        						mySample.setAssignment(c.getName(), False)
        						w *= self.varMap[c].getProbability(assigns,False)
        				else: #if no evidence...
        					if (myRan <= self.varMap[c].getProbability(assigns, True)): #applying sampling
        						mySample.setAssignment(c.getName(), True) 
        					else:
        						mySample.setAssignment(c.getName(), False)

        				for children in self.varMap[c].getChildren(): #keep track of children of child to be added
        					listAdd += [children.getVariable()] 

        		for e in listAdd: #adding children of child. Avoiding duplicates
        			if (e not in childList):
        				childList[e] = False

        		isAllChecked = True	#boolean to check if all variables were visited	
        		for ch in childList: #check if all members are defined
        			if (childList[ch] is False):
        				isAllChecked = False
        		allSet = isAllChecked

        		if (allSet):
        			return w
        weights = [0, 0]
        
        for n in range(numSamples):
        	w = weightedSample(givenVars)
        	if (mySample.getValue(queryVar.getName())):
        		weights[0] += w
        	else:
        		weights[1] += w


        if (weights[0] + weights[1] == 0):
        	return 0
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
        mySample = Sample()
        
        noEvidenceList = []

        #assigning evidences to sample
        for givenNode in givenVars:
        	mySample.setAssignment(givenNode.getName(), givenVars[givenNode])

        #filling up noEvidenceList with non evidence variables
        for node in self.varMap:
        	if node not in givenVars:
        		noEvidenceList += [node]

        #giving a random value for non evidence variables
        for node in noEvidenceList:
        	rand = random.random()
        	if (rand < 0.5):
        		mySample.setAssignment(node.getName(), True)
        	else:
        		mySample.setAssignment(node.getName(), False)


        count = [0,0]
        
        for runs in range(numTrials):	#repeat n times
        	if (mySample.getValue(queryVar.getName())): # count[0] keep track of queryVar = True
        		count[0] += 1.0
        	else:
        		count[1] += 1.0 # count[1] keep track of queryVar = False
        	for noEvidenceNode in noEvidenceList: # for each no-evidence variable...
        		assignList = {} # preparing to add assignments

        		for node in self.varMap: #filling up assignments defined previously
        			assignList[node.getName()] = mySample.getValue(node.getName())

        		ptrue = self.varMap[noEvidenceNode].getProbability(assignList, True)
        		pfalse = self.varMap[noEvidenceNode].getProbability(assignList, False)

        		for child in self.varMap[noEvidenceNode].getChildren(): #for each child of the current no-evidence variable
        			if mySample.getValue(child.getVariable().getName()):
        				assignList[noEvidenceNode.getName()] = True # set current no-evidence variale = True
        				ptrue *= self.varMap[child.getVariable()].getProbability(assignList, True)
        				assignList[noEvidenceNode.getName()] = False# set current no-evidence variale = False
        				pfalse *= self.varMap[child.getVariable()].getProbability(assignList, True)
        			else:
        				assignList[noEvidenceNode.getName()] = True # set current no-evidence variale = True
        				ptrue *= self.varMap[child.getVariable()].getProbability(assignList, False)
        				assignList[noEvidenceNode.getName()] = False# set current no-evidence variale = False
        				pfalse *= self.varMap[child.getVariable()].getProbability(assignList, False)
        		# Normalizing:
        		if ptrue+pfalse == 0:
        			P = 0
        		else:
        			P = ptrue/(ptrue+pfalse)
        		rann = random.random() # Generate random
        		if rann <= P: #assigning new value for the current noEvidenceNode
        			mySample.setAssignment(noEvidenceNode.getName(), True)
        		else:
        			mySample.setAssignment(noEvidenceNode.getName(), False)
        if count[0]+count[1] == 0:
        	return 0
        return count[0]/(count[1]+count[0])
