import sys, random, copy
from collections import OrderedDict
sys.setrecursionlimit(5000)

read1 = open("reads_1.fastq", "r")
lines1 = read1.read().splitlines()
k = 21
dna = []
kmers = []
counter = 0
# Lesa inn file, filtera línur sem hafa ekki dan strengina og lengd kmera er 21
for x, line in enumerate(lines1):
    if(counter>=1000): 
        break
    if not(line[0] == '@' or line[0] == '+' or line[0] == '8'):
        for i in range(len(line)-k):                        
            kmers.append(line[i:i+k])
    counter +=1   

          
'''
def checkio(data):
    for index in range(len(data) -1, -1, -1):
        if data.count(data[index]) == 1:
            del data[index]
    return data
'''

print(len(kmers))
kmers = list(OrderedDict.fromkeys(kmers))
print(len(kmers))


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
'''
for kmer in kmers:
        fromNode = kmer[:-1]
        toNode = kmer[1:]
        if fromNode not in knots:
                knots.append(fromNode)
                connections[fromNode] = []
                connectedFrom[fromNode] = []
                counter[fromNode] = 0 
        if toNode not in knots:
                counter[toNode] = 0
        
        counter[fromNode] += 1
        counter[toNode] += 1
        connections[fromNode].append(toNode)
        totEdges += 1
'''
nodes = []
edges = {}

for kmer in kmers:
    fromNode = kmer[:-1]
    toNode = kmer[1:]

    if fromNode not in nodes:
        nodes.append(fromNode)
        edges[fromNode] = []
    
    edges[fromNode].append(toNode)

data_struct = []
file = open("testfile.txt","w")
for node in nodes:
    temp = node, ' -> ', ','.join(edges[node])
    data_struct.append((str(node),edges[node]))
    file.write(str(temp))
    file.write('\n')
file.close() 

for data in data_struct:
    if(len(data[1]) > 1):
        print(data)



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



def restart():
    global k, currConn, pStart, pEnd
    
    k = graphstart
    currConn = copy.deepcopy(conn)
    pStart = []
    pEnd = []



pathFound = False
k = graphstart
currConn = copy.deepcopy(conn)
pStart = []
pEnd = []

while not pathFound:
        
    smallPath = createPath([k],currConn)
    
    if smallPath[-1] is graphend:
        path = pStart + smallPath
    else:
        path = pStart + smallPath + pEnd


    if (len(path) > totEdges):
        print('->'.join(str(x) for x in path))
        pathFound = True
    else:
        k = random.choice([x for x in path if len(currConn[x]) > 0 and x != graphend])
        i = path.index(k)
        pStart = path[:i]
        pEnd = path[i+1:]
