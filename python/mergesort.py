from timings import Timer
import pprint

# merge already sorted subarrays
def merge(b, c, inv):
    sizeb = len(b)
    sizec = len(c)
    sizea = sizeb + sizec
    a = [0]*sizea
    i = 0
    j = 0
    for k in range(0, sizea):
        if i < sizeb and j < sizec:
            if b[i] <= c[j]:
                a[k] = b[i]
                i+=1
            else:
                a[k] = c[j]
                inv[0]+=(sizeb - i)
                j+=1
        elif i < sizeb:
            a[k] = b[i]
            i+=1
        else:
            a[k] = c[j]
            j+=1
    return a

def merge2d(b, c, index):
    sizeb = len(b)
    sizec = len(c)
    sizea = sizeb + sizec
    a = [[0 for r in xrange(2)] for x in xrange(sizea)]
    i = 0
    j = 0
    for k in range(0, sizea):
        if i < sizeb and j < sizec:
            if b[i][index] <= c[j][index]:
                a[k] = b[i]
                i+=1
            else:
                a[k] = c[j]
                j+=1
        elif i < sizeb:
            a[k] = b[i]
            i+=1
        else:
            a[k] = c[j]
            j+=1
    return a

def sortArray2d(a, index):
    size = len(a)
    if size <= 1:
        return a
    b = a[:size/2]
    c = a[size/2:]
    b = sortArray2d(b, index)
    c = sortArray2d(c, index)
    return merge2d(b, c, index)

# sort array recursively using merge sort
def sortArray(a, inv):
    size = len(a)
    if size <= 1:
        return a
    b = a[:size/2]
    c = a[size/2:]
    b = sortArray(b, inv)
    c = sortArray(c, inv)
    return merge(b, c, inv)

# import random
# pp = pprint.PrettyPrinter()
# a = [random.randint(0,1000000) for r in xrange(400000)]
# inv = [0]
# t = Timer()
# sortArray(a, inv)
# print "Total time elapsed: %f" % t.stop()
# print "Number of inversions = %d" % inv[0]
