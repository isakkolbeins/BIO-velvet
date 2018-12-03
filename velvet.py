import sys, random, copy
sys.setrecursionlimit(5000)

read1 = open("reads_1.fastq", "r")
lines1 = read1.read().splitlines()
k = 21
coverage = 100
dna = []
kmers = []


# Lesa inn file, filtera línur sem hafa ekki dan strengina
for x, line in enumerate(lines1):
        if(x>1000): break
        if not(line[0] == '@' or line[0] == '+' or line[0] == '8'):
                for i in range(len(line)-k):
                        
                        kmers.append(line[i:i+k])


# for read in dna:
#     for i in range(len(read)-k):
#         kmers.append(dna[0][i:i+k])

connections = {}
counter = {}
knots = []
totEdges = 0
nostart = []
graphend = -1
graphstart = -1
connectedFrom = {}

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

print(len(knots))

for k in knots:
        if (counter[k] < coverage):
                knots.remove(k)

print(len(knots))


for k in knots:
        for c in connections[k]:
                if c not in knots:
                        connections[k].remove(c)  

print(len(knots))


#for k in knots:
    #print(k, ' -> ', ','.join(connections[k]))

def createPath(path, currConn):
        currKnot = path[-1]
        if currKnot not in currConn.keys():
                return path
        elif len(currConn[currKnot]) > 0:
                c = random.choice(currConn[currKnot])
                currConn[currKnot].remove(c)
                path.append(c)
                return createPath(path, currConn)
        else :
                return path



def restart():
        global k, currConn, pStart, pEnd
        
        k = graphstart
        currConn = copy.deepcopy(conn)
        pStart = []
        pEnd = []



cycleFound = False
k = graphstart
currConn = copy.deepcopy(conn)
pStart = []
pEnd = []

while not cycleFound:
        
        smallPath = createPath([k],currConn)
        
        if smallPath[-1] is graphend:
                path = pStart + smallPath
        else :
                path = pStart + smallPath + pEnd


        if (len(path) > totEdges):
                out = ''
                for i, curr in enumerate(path):
                        if i == 0: out = curr
                        else: out += curr[-1]
                print(out)
                cycleFound = True
        else :
                k = random.choice([x for x in path if len(currConn[x]) > 0 and x != graphend])

                i = path.index(k)
                pStart = path[:i]
                pEnd = path[i+1:]
