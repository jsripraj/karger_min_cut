import random
import math

def createGraph(filename):
    with open(filename, 'r') as file:
        G = []
        for line in file:
            G.append([int(x) for x in line.split()])
    return G

def swap(a,b):
    return b,a

def karger(G):
    """
    Create a dictionary to store which nodes have been contracted into other nodes. 
    In a contraction, the lower-valued node will absorb the higher node's
    edges. Thus, after the contraction, the higher node will map to the
    lower node. The higher node's edges are then deleted.
    Key: node's initial value. Value: post-contraction value.
    
    The first element of each row is initialized to a one-element set
    containing the node's initial value. During contractions, the higher-valued
    node's value will be added to the lower-valued node's set to 
    represent the supernode.
    """
    supers = {}
    totalDegree = 0
    for row in G:
        supers[row[0]] = row[0]
        totalDegree += len(row)-1 # exclude node value (1st element)
        row[0] = set(row[:1])
    
    for iteration in range(len(G)-2): # repeat until only 2 nodes left
        # find a random edge. i, j = row, column index
        r = random.randint(1, totalDegree)
        row = 0
        while len(G[row])-1 < r:
            r -= len(G[row])-1
            row += 1
        a = row+1
        b = G[row][r]
        while True:
            if a != supers[a]:
                a = supers[a]
            elif b != supers[b]:
                b = supers[b]
            else:
                break
        if a > b: a,b = swap(a,b)
        aRow, bRow = a-1, b-1

        # contract that edge 
        G[aRow][0] = G[aRow][0].union(G[bRow][0])
        G[aRow] += G[bRow][1:]
        k = 1
        while k < len(G[aRow]): # remove self loops
            if G[aRow][k] in G[aRow][0]:
                del G[aRow][k]
                totalDegree -= 1
            else:
                k += 1
        G[bRow][1:] = []
        for v in G[bRow][0]:
            supers[v] = a
    return totalDegree//2

def minCut(G):
    n = len(G)
    N = pow(n,2) * math.ceil(math.log(n))
    smallestCut = min([len(row)-1 for row in G])
    for trial in range(N):
        GCopy = [[y for y in x] for x in G] 
        cut = karger(GCopy)
        if cut < smallestCut:
            smallestCut = cut
            print('Trial', trial, '/', N, '. Smaller cut found! Min cut:', smallestCut)
        if trial % 1000 == 0:
            print('Trial', trial, '/', N, '. Min cut:', smallestCut)
    return smallestCut


filename = 'kargerMinCut.txt'
G = createGraph(filename)
G1 = [[1,2,3],
     [2,1,3,4],
     [3,1,2,4],
     [4,2,3]]
G2 = [[1,2,6,4],
      [2,1,4,6,3],
      [3,2,5,4],
      [4,1,2,6,3],
      [5,3],
      [6,1,2,4]]
answer = minCut(G)
print('answer:', answer)
