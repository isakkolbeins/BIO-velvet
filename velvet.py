import sys, random, copy
from collections import OrderedDict
sys.setrecursionlimit(5000)


def readFromFile():
    read1 = open("reads_2.fastq", "r")
    lines1 = read1.read().splitlines()
    k = 21
    dna = []
    kmers = []
    counter = 0
    # Lesa inn file, filtera línur sem hafa ekki dan strengina og lengd kmera er 21
    for x, line in enumerate(lines1):
        #if(counter>=1000): 
            #break
        if not(line[0] == '@' or line[0] == '+' or line[0] == '8'):
            for i in range(len(line)-k):                        
                kmers.append(line[i:i+k])
        counter +=1
    return kmers  

def coverage(kmers):
    return list(OrderedDict.fromkeys(kmers))



#for read in dna:
#        for i in range(len(read)-k):
#                kmers.append(dna[0][i:i+k])

connections = {}
counter = {}
knots = []
totEdges = 0
nostart = [] 
graphend = -1
graphstart = -1
connectedFrom = {}
nodes = []
edges = {}

def de_Brujin_Graph(kmers):
    print(" -> connecting kmers ")
    for i, kmer in enumerate(kmers):
        if(i%10000 == 0):
            print("Done with ", i)
        fromNode = kmer[:-1]
        toNode = kmer[1:]

        if fromNode not in nodes:
            nodes.append(fromNode)
            edges[fromNode] = []
            connectedFrom[fromNode] = []

        if toNode not in nodes:
            nodes.append(toNode)
            edges[toNode] = []
            connectedFrom[toNode] = []

        edges[fromNode].append(toNode)
        connectedFrom[toNode].append(fromNode)


def combineNode(n):
    toLen = 0
    fromLen = 0
    #print("--- n --- ", n)
    if n[-20:] in edges.keys():
        toLen = len(edges[n[-20:]])
        edges[n] = edges[n[-20:]]

    if n[:20] in connectedFrom.keys():
        fromLen = len(connectedFrom[n[:20]])
        connectedFrom[n] = connectedFrom[(n[:20])]
    
    if fromLen > 1 or toLen > 1:
        #Ekki með, break dont save or delete
        # edges[n] = edges[n[-20:]]
        # connectedFrom[n] = connectedFrom[n[:20]]
        return n
    
    if toLen == 0:
        if n[-20:] in nodes:
            nodes.remove(n[-20:])
        return n
    
    if n[-20:] in nodes:
        nodes.remove(n[-20:])
    #print(edges[n][0][-1])
    return combineNode(n+edges[n][0][-1])

def getCheckpoints(nodes):
    checkPoints = []
    for node in nodes:
            toLen = 0
            fromLen = 0
            if node in edges.keys():
                toLen = len(edges[node])
            if node in connectedFrom.keys():
                fromLen = len(connectedFrom[node])
           
            if toLen > 1 or fromLen > 1:
                for n in edges[node]: 
                    checkPoints.append(n)

            if fromLen < 1:
                checkPoints.append(node)
    return checkPoints


def optimiseGraph(checkPoints):
    for node in checkPoints:
        nodes.append(combineNode(node))
    return nodes

def removeTips(nodes):
    filtered = []
    for n in nodes:
        toLen = 0
        fromLen = 0
        if n in edges.keys():
            toLen = len(edges[n])
        if n in connectedFrom.keys():
            fromLen = len(connectedFrom[n])

        if not((toLen == 0 or fromLen == 0) and len(n) <= 2*21):
            filtered.append(n)

    return filtered
    

#for k in knots:
#        if (counter[k] < coverage):
#                knots.remove(k)



#for k in knots:
 #       for c in connections[k]:
  #              if c not in knots:
   #                     connections[k].remove(c)  


#for k in knots:
    #print(k, ' -> ', ','.join(connections[k]))
# Removing the tips

# for x in kmers[1:]

def createPath(path, currConn):
    currKnot = path[-1]
    if currKnot not in currConn.keys():
        return path
    elif len(currConn[currKnot]) > 0:
        c = random.choice(currConn[currKnot])
        currConn[currKnot].remove(c)
        path.append(c)
        return createPath(path, currConn)
    else:
        return path


def main():
    print(" _     _ _______ _     _     _ _______ _______ ")
    print("(_)   (_|_______|_)   (_)   (_|_______|_______)")
    print(" _     _ _____   _     _     _ _____      _    ")
    print("| |   | |  ___) | |   | |   | |  ___)    | |   ")
    print(" \ \ / /| |_____| |____\ \ / /| |_____   | |   ")
    print("  \___/ |_______)_______)___/ |_______)  |_|   ")
    print()


    kmers = readFromFile()
    print("_________________Kmers generated from file_________________")
    print(len(kmers), " -> Number of kmers")
    print()

    kmers = coverage(kmers)
    print("_____________________Coverage filtered_____________________")
    print(len(kmers)," -> Number of kmers after coverage filter")
    print()

    de_Brujin_Graph(kmers)
    print("__________________De Brujin Graph created__________________")
    print(len(nodes), " -> Number of nodes in graph")
    print()


    checkPoints = getCheckpoints(nodes)
    print("_____________________Checkpoints found_____________________")
    print(len(nodes), " -> Number of checkpoints in graph")
    print()

    graph = optimiseGraph(checkPoints)
    print("______________________Graph optimised______________________")
    print(len(graph)," -> Number of nodes in graph afer optimisation")
    print()

    graph = removeTips(graph)
    print("_______________________Tips removed________________________")
    print(len(graph)," -> Number of nodes in graph afer tip removal: ")
    print()

    for k in graph: 
        print(k, " -> ", ','.join(edges[k]))

if __name__== "__main__":
    main()
