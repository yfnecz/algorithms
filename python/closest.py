from timings import Timer
from mergesort import sortArray2d
import math
import pprint

pp = pprint.PrettyPrinter()

def distance(p1, p2):
    return math.sqrt( pow(p1[0]-p2[0], 2) + pow(p1[1]-p2[1], 2) )

def validateQuadraticClosestPair(a):
    size = len(a)
    dist = -1
    pair = [a[0], a[0]]
    for i in xrange(size):
        for j in xrange(size-i-1):
            newdist = distance(a[i], a[j+i+1])
            if dist == -1 or newdist < dist:
                dist = newdist
                pair = [a[i], a[j+i+1]]
    return sortArray2d(pair,0)

def sortLinear(q, py):
    j = 0
    a = [[0 for i in xrange(2)] for k in xrange(len(q))]
    for i in xrange(len(py)):
        try:
            num = q.index(py[i])
            a[j] = q[num]
            j = j+1
        except:
            pass
    return a

def baseCase(px):
    dist = -1
    p1 = -1
    p2 = -1
    size = len(px)
    for i in xrange(size-1):
        newdist = distance(px[i], px[i+1])
        if dist == -1 or newdist < dist:
            p1 = i
            p2 = i+1
            dist = newdist
    return [px[p1], px[p2]]

def baseCasePair(pairs):
    dist = -1
    pair = pairs[0]
    for i in xrange(len(pairs)):
        newdist = distance(pairs[i][0], pairs[i][1])
        if dist == -1 or newdist < dist:
            dist = newdist
            pair = pairs[i]
    return pair


def closestSplitPair(px, py, delta):
    n = len(px)
    x = px[n/2-1][0]
    sy = []
    j = 0
    for i in xrange(n):
        if py[i][0] <= x+delta and py[i][0] >= x-delta:
            sy.append([])
            sy[j] = py[i]
            j = j+1

    size = len(sy)
    if size == 1: # no closest split pair may exist
        return [px[0], px[0]]
    
    best = delta
    p1 = -1
    p2 = -1

    for i in xrange(size-1):
        for j in xrange( min(7, size-i-1) ):
            newdist = distance(sy[i], sy[i+j+1])
            if newdist < best:
                best = newdist
                p1 = sy[i]
                p2 = sy[i+j+1]

    if p1 == -1: # no closest pair by y coord found
        return [px[0], px[0]]
    return sortArray2d([p1, p2],0)

def closestPair(px, py):
    size = len(px)

    # base case
    if size == 2 or size == 3:
        return baseCase(px)
    
    q = px[:size/2]
    r = px[size/2:]
    qx = q
    qy = sortLinear(q, py)
    rx = r
    ry = sortLinear(r, py)

    pair1 = closestPair(qx, qy)
    pair2 = closestPair(rx, ry)

    delta = min(distance(pair1[0], pair1[1]), distance(pair2[0], pair2[1]))
    pair3 = closestSplitPair(px, py, delta)

    # not yet tested
    if pair3[0] == pair3[1]:
        return baseCasePair([pair1, pair2])
    else:
        return baseCasePair([pair1, pair2, pair3])
    
import random

# generate source data
#size = 30000
size = 100
t = Timer()
a = [[random.randint(0,size) for r in xrange(2)] for x in xrange(size)]
time0 = t.stop()
print "Time elapsed for building array: %f" % time0
for k in xrange(2):
    for i in xrange(size):
        for j in xrange(size-i):
            if i != j:
                if a[i][k] == a[i+j][k]:
                    a[i][k] += size
print "Time elapsed for randomizing array: %f" % (t.stop() - time0)
                    
#a=[[19,30], [52,57], [50,56],[29,49],[115,671],[309,818]]

logFile=open('input.txt', 'w')
#pp.pprint(a, logFile)
#logFile.write(pp.pformat(a))
logFile.close()

# algorithm
time1 = t.stop()
px = sortArray2d(a,0)
py = sortArray2d(a,1)
pp.pprint(closestPair(px, py))
time2 = t.stop()
print "Total time elapsed: %f" % (time2 - time1)


pp.pprint(validateQuadraticClosestPair(a))
print "Total time for quadratic validation: %f" % (t.stop() - time2)



