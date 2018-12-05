import sys, random, copy, math, time
from collections import OrderedDict
sys.setrecursionlimit(5000)

connectedFrom = {}
nodes = []
edges = {}


def readFromFile():
    read1 = open("reads_1.fastq", "r")
    lines1 = read1.read().splitlines()
    k = 21
    kmers = []
    counter = 0
    twoPerc = math.floor(len(lines1)/50)
    # Lesa inn file, filtera línur sem hafa ekki dan strengina og lengd kmera er 21
    for x, line in enumerate(lines1):
        if x%twoPerc == 0:
            print("-", end="", flush=True)
        
        # Þar sem að við virðumst ekki geta höndlað alla gagnaskránna, notum við aðeins hluta hennar
        if(counter>=10000): 
           break
        if not(line[0] == '@' or line[0] == '+' or line[0] == '8'):
            for i in range(len(line)-k):                        
                kmers.append(line[i:i+k])
                
                edges[line[i:i+k-1]] = []
                edges[line[i+1:i+k]] = []

                connectedFrom[line[i:i+k-1]] = []
                connectedFrom[line[i+1:i+k]] = []

        counter +=1
    print()
    return kmers  


def coverage(kmers):
    print("--------------------------------------------------")
    return list(OrderedDict.fromkeys(kmers))


def de_Brujin_Graph(kmers):
    allKmers = []
    twoPerc = math.floor(len(kmers)/49)
    for i, kmer in enumerate(kmers):
        if i%twoPerc == 0:
            print("-", end="", flush=True)
        fromNode = kmer[:-1]
        toNode = kmer[1:]
       
        allKmers.append(fromNode)
        allKmers.append(toNode)

        edges[fromNode].append(toNode)
        connectedFrom[toNode].append(fromNode)
    print()
    return list(OrderedDict.fromkeys(allKmers))


def combineNode(n):
    global nodes
    toLen = 0
    fromLen = 0
    
    if n[-20:] in nodes:
        toLen = len(edges[n[-20:]])
        edges[n] = edges[n[-20:]]
        fromLen = len(connectedFrom[n[:20]])
        connectedFrom[n] = connectedFrom[(n[:20])]
        if not(fromLen > 1 or toLen > 1):
            nodes.remove(n[-20:])
    else :
        edges[n] = []
        connectedFrom[n] = []
      
    if fromLen > 1 or toLen != 1 :
        return n
   
    else :
        return combineNode(n+edges[n][0][-1])

def getCheckpoints(nodes):
    checkPoints = []
    twoPerc = math.floor(len(nodes)/49)

    for i, node in enumerate(nodes):
        if i%twoPerc == 0:
            print("-", end="", flush=True)
        toLen = 0
        fromLen = 0
        if node in edges.keys():
            toLen = len(edges[node])
        if node in connectedFrom.keys():
            fromLen = len(connectedFrom[node])
        
        if toLen > 1 or fromLen > 1:
            for n in edges[node]: 
                checkPoints.append(n)

        elif fromLen < 1:
            checkPoints.append(node)
    print()
    return checkPoints


def optimiseGraph(checkPoints):
    optimised = []
    twoPerc = math.floor(len(checkPoints)/49)
    for i, node in enumerate(checkPoints):
        if i%twoPerc == 0:
            print("-", end="", flush=True)
        newNode = combineNode(node)
        optimised.append(newNode)
    print()
    return optimised

def removeTips(nodes):
    filtered = []
    twoPerc = math.floor(len(nodes)/49)
    for i, n in enumerate(nodes):
        if i%twoPerc == 0:
            print("-", end="", flush=True)
        toLen = 0
        fromLen = 0
        if n in edges.keys():
            toLen = len(edges[n])
        if n in connectedFrom.keys():
            fromLen = len(connectedFrom[n])

        if not((toLen == 0 or fromLen == 0) and len(n) <= 2*21):
            filtered.append(n)
    print()
    return filtered

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

def save(f, output):
    print(output)
    f.write(output+'\n')

def main():
    global nodes
    start_time = int(round(time.time()))
    file = open("output.txt", "w")

    save(file, "   _     _ _______ _     _     _ _______ _______ ")
    save(file, "  (_)   (_|_______|_)   (_)   (_|_______|_______)")
    save(file, "   _     _ _____   _     _     _ _____      _    ")
    save(file, "  | |   | |  ___) | |   | |   | |  ___)    | |   ")
    save(file, "   \ \ / /| |_____| |____\ \ / /| |_____   | |   ")
    save(file, "    \___/ |_______)_______)___/ |_______)  |_|   ")
    save(file, "" )      
    save(file, "" )

    save(file, "____________Generating kmers from file____________")
    kmers = readFromFile()
    save(file, str(len(kmers))+ " -> Number of kmers")
    save(file, "" )

    save(file, "____________Filtering kmers by coverage___________")
    kmers = coverage(kmers)
    save(file, str(len(kmers)) +" -> Number of kmers after coverage filter")
    save(file, "" )

    save(file, "_____________Creating de Brujin graph_____________")
    nodes = de_Brujin_Graph(kmers)
    save(file, str(len(nodes))+ " -> Number of nodes in graph")
    save(file, "" )

    save(file, "________________Finding checkpoints_______________")
    checkPoints = getCheckpoints(nodes)
    save(file, str(len(checkPoints))+ " -> Number of checkpoints in graph")
    save(file, "" )

    save(file, "_________________Optimising graph_________________")
    graph = optimiseGraph(checkPoints)
    save(file, str(len(graph))+" -> Number of nodes in graph afer optimisation")
    save(file, "" )

    save(file, "__________________Removing tips___________________")
    graph = removeTips(graph)
    save(file, str(len(graph))+" -> Number of nodes in graph afer tip removal")
    save(file, "" )

    stop_time = int(round(time.time()))
    tot_time = stop_time - start_time
    t = time.strftime("%H:%M:%S", time.gmtime(tot_time))

    save(file, "--------------------------------------------------")    
    save(file, "               Runtime: "+ str(t) )
    save(file, "--------------------------------------------------")

    for k in graph:
        thisknot = str(k) + " -> "+ ",".join(edges[k])
        save(file, thisknot)
    
    file.close()

if __name__== "__main__":
    main()
