import string
import heapq
import sys
import argparse

class directedWeightedGraph:

	# Use adjacenecy list representation for the graph. The list is stored using python dictionary
    def __init__(self,gdict=None):
        if gdict is None:
            gdict = {}
        self.gdict = gdict

    def getVertices(self):
        return list(self.gdict.keys())

    def addVertex(self, vrtx):
       if vrtx not in self.gdict:
            self.gdict[vrtx] = []

    def addEdge(self, edge):
        (vrtx1, vrtx2, weight) = edge
        if vrtx1 in self.gdict:
            if (vrtx2, weight) not in self.gdict[vrtx1]:
                self.gdict[vrtx1].append((vrtx2, weight))
        
        else:
            self.gdict[vrtx1] = [(vrtx2, weight)]

    def getEdges(self):
        edgeList = []
        for vrtx in self.gdict:
            for edgeVrtx in self.gdict[vrtx]:
                if (vrtx, edgeVrtx) not in edgeList:
                    edgeList.append((vrtx, edgeVrtx))

        return edgeList

    def getNeighbours(self, vertex):
    	return self.gdict[vertex]

class wordsDictionary:

	def __init__(self):
		wdict = {}

	def constructDictFromFile(self):
		myWordsDict = {}
		with open("dict.txt", "r") as fd:
		    for line in fd:
		    	line = line.rstrip('\n')
		    	if line not in myWordsDict:
		    		myWordsDict[line] = True

	   	self.wdict = myWordsDict

	def isInDictionary(self, word):
		if word in self.wdict:
			return True
		else:
			return False

	def returnKeys(self):
		return self.wdict.keys()

# Create global graph and words dictionary objs
myGraph = directedWeightedGraph()
wordsDict = wordsDictionary()

def insertPermutations(word):
	alphabetsStr = string.ascii_lowercase
	for i in range(len(word) + 1):
		for letter in alphabetsStr:
			newWord = word[:i] + letter + word[i:]

			if wordsDict.isInDictionary(newWord) is True:
				myGraph.addEdge((word, newWord, 1))

def deletePermutations(word):
	for idx in range(len(word)):
		newWord = word[:idx] + word[idx+1:]

		if wordsDict.isInDictionary(newWord) is True:
				myGraph.addEdge((word, newWord, 3))

def swap(string, i, j):
	string = list(string)
	string[i], string[j] = string[j], string[i]
	return ''.join(string)

def twiddlePermutations(word):
	for i in range(len(word) - 1):
		newWord = swap(word, i, i+1)

		if newWord != word:
			if wordsDict.isInDictionary(newWord) is True:
				myGraph.addEdge((word, newWord, 2))

def reversePermutation(word):
	newWord = word[::-1]

	if newWord != word:
		if wordsDict.isInDictionary(newWord) is True:
					myGraph.addEdge((word, newWord, len(word)))

def createGraphFromFile():
	wordsList = wordsDict.returnKeys()

	for word in wordsList:
		myGraph.addVertex(word)

		insertPermutations(word)
		deletePermutations(word)
		twiddlePermutations(word)
		reversePermutation(word)

def performDijkstra(startWord, endWord):

	if not myGraph.getNeighbours(startWord) or not myGraph.getNeighbours(endWord): # If either startWord or endWord is a disconnected vertex
		return {}, {}

	distVertices = {node: float('infinity') for node in myGraph.getVertices()}
	distVertices[startWord] = 0

	entry_lookup = {} # Stores the dist,vertex pairs as mutable objs to be passed to the priorityQ 
	priorityQ = []
	parents = {} # Stores the parent of each vertex in the shortest path tree

	for vertex, dist in distVertices.items(): # Fill up the priority queue
		item = [dist, vertex]
		entry_lookup[vertex] = item
		heapq.heappush(priorityQ, item)

	while len(priorityQ) > 0:
		cur_dist, cur_vertex = heapq.heappop(priorityQ)
		#print cur_dist, cur_vertex

		for neighbour in myGraph.getNeighbours(cur_vertex):
			neighbourVertex, neighbourDist = neighbour
			
			new_distance = distVertices[cur_vertex] + neighbourDist

			if new_distance < distVertices[neighbourVertex]:
				distVertices[neighbourVertex] = new_distance
				parents[neighbourVertex] = cur_vertex 
				
				if neighbourVertex in entry_lookup: # Routine to update the priority queue once a shorter distance is found
					del entry_lookup[neighbourVertex]
					item_new = [new_distance, neighbourVertex]
					entry_lookup[neighbourVertex] = item_new
					heapq.heappush(priorityQ, item_new)


	return distVertices, parents

def getShortestPath(startWord, endWord):
    
    if not wordsDict.isInDictionary(startWord) or not wordsDict.isInDictionary(endWord):
        print str(-1)
        return

    distVertices, parents = performDijkstra(startWord, endWord)

    if not distVertices or not parents: # If the dicts are returned empty due to either word being disconnected
        print str(-1)
        return 

    if distVertices[endWord] == float('infinity'):
        print str(-1)
        return

    parent = endWord
    path = [parent]
    while parent != startWord:
        parent = parents[parent]
        path.insert(0, parent)

    print str(distVertices[endWord]) + ' ' + " ".join(path)


def getShortestLongestPath(startWord):
	
    distVertices, parents = performDijkstra(startWord, 'spam')

    keys = list(distVertices.keys())
    vals = list(distVertices.values())

    maxVal = -1
    for elm in vals:
        if elm != float('infinity') and elm > maxVal:
            maxVal = elm

    if maxVal == -1:
        return -1, []

    maxkey = keys[vals.index(maxVal)] 

    parent = maxkey
    path = [parent]
    while parent != startWord:
        parent = parents[parent]
        path.insert(0, parent)

    return maxVal, path

def getInputPrintOutput():

    wordPairList = sys.stdin.readlines()

    wordsDict.constructDictFromFile()
    createGraphFromFile()

    for entry in wordPairList:
        entry = entry.rstrip('\n')
        words = entry.split(' ')

        getShortestPath(words[0], words[1])

    return 0

def largestShortestDist():
    maxDist = 0
    maxPath = []

    wordsDict.constructDictFromFile()
    createGraphFromFile()

    wordsList = wordsDict.returnKeys()

    print "Executing dictionary traversal: "

    for wordStart in wordsList:
        print wordStart
        dist, path = getShortestLongestPath(wordStart)

        if dist > maxDist:
            maxDist = dist
            maxPath = path[:]
            print maxDist
            print maxPath

    print 'Final: '
    print maxDist
    print 'Final: '
    print maxPath


parser = argparse.ArgumentParser(description= '''This programs reads a dictionary file \'dict.txt\' and then performs two possible operations: 
                                               1) Given a start and end word output the shortest chain path 2) Output the longest shortest path chain in the dictionary file.
                                               By default operation '1' is performed unless the -l flag is provided''')

parser.add_argument('-l', action='store_true')
args = parser.parse_args()

if (args.l):
    largestShortestDist()
else:
    getInputPrintOutput()