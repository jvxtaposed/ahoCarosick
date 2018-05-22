from typing import List
import numpy as np
from collections import deque
import math

'''
MATRIX: where rows: nodes, cols: A/C/G/

pseudocode:
1) start with first position in the db, and the root node
2) if successful transition:
    3) increment current pointer
    4) move to a new node
    5) if terminal node "success"
    
6) else:
    7) retract 'current' pointer
    8) increment 'start' pointer
    9) move to root and repeat
##############
l = 1
c = 1
v = root
repeat
    if((w = A(v,T[c] != 0):
        v = w
        c = c + 1
        if(v has label i):
            print "Pattern i matches starting at position l"
            
    else:
        c = l + 1
        l = c
        v = root
    end
until(c > n) /*n is the db size*/
'''

w = open("output2.txt", "w")
DNA = ""
with open("DNA.txt", "r+") as file:
    line: str
    for line in file:
        line = line.strip()
        if ">" not in line:
            DNA += str(line)
n = len(DNA)
dict = []
node = 1
with open("queries2.txt", "r") as file:
    for line in file:
        line = line.strip()
        dict.append(line)
        node += len(line)
print(dict)
print("number of nodes: " + str(node))

class ACNode:
    id = None
    elem = None
    transitionList = None
    out = None
    fail = None
    def __init__(self, id, elem):
        self.id = id
        self.elem = elem
        self.out = set()
        self.transitionList = []
        self.fail = 0



    def getTrans(self, elem):
        for obj in self.transitionList:
            if obj.elem == elem:
                return obj
        return None

    def tryTrans(self, elem):
        if self.id == 0:
            return True
        else:
            for obj in self.transitionList:
                if obj.elem == elem:
                    return True
            return False

    def addOut(self, add):
        self.out = self.out ^ add



class AC:
    root = None
    newACNode = None
    def __init__(self):
        self.root = ACNode(0, ' ')
        self.newACNode = 0

    def addDict(self, keyword: object) -> object:
        for obj in keyword.split(' '):
            c = 0
            state = 0
            cur = self.root
            obj = obj.upper()
            while c < len(obj):
                l = obj[c]
                c = c + 1
                prev = cur.getTrans(l)
                if prev != None:
                    cur = prev
                else:
                    self.newACNode = self.newACNode +1
                    nxt = ACNode(self.newACNode, l)
                    cur.transitionList.append(nxt)
                    cur = nxt
                    while c < len(obj):
                        self.newACNode = self.newACNode + 1
                        temp = ACNode(self.newACNode, obj[c])
                        cur.transitionList.append(temp)
                        cur = temp
                        c = c + 1
                    break
            cur.out.add(obj)

    def setFailTransitions(self):
        """Sets the fail transitions in tree"""
        queue = deque()
        current = self.root
        child = self.root

        for nd in self.root.transitionList:
            queue.append(nd)
            nd.fail = self.root

        while len(queue) != 0:
            r = queue.popleft()

            for nd in r.transitionList:
                queue.append(nd)
                state = r.fail
                val = nd.elem
                current = state
                while True:
                    if current.tryTrans(val) == False:
                        current = current.fail
                    else:
                        break
                child = current.getTrans(val)
                if child == None:
                    nd.fail = current
                else:
                    nd.fail = child
            nd.addOut(nd.fail.out)

    def findKey(self, findKey):
        for substr in findKey.split(' '):
            c = 0
            cur = self.root
            substr = substr.upper()
            while c < len(substr):
                while True:
                    if cur.tryTrans(substr[c]) == False:
                        cur = cur.fail
                    else:
                        prev = cur.getTrans(substr[c])
                        #print("substring: " + substr[c])
                        break
                if prev != None:
                    cur = prev
                    if len(prev.out) != 0:
                        itr = iter(prev.out)
                        for obj in itr:
                            eval = (n - (len(obj))) * math.pow(0.25, len(obj))
                            print(str(obj) + "\t" + "E:" + str(eval))
                            w.write(str(obj) + "\n")
                c = c + 1


if (__name__ == "__main__"):
    x: AC = AC()


    with open("queries2.txt", "r") as file:
        for line in file:
            line = line.strip()
            x.addDict(line)

    print("DNA length is: " + str(len(DNA)))
    x.setFailTransitions()
    x.findKey(DNA)