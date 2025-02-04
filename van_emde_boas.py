import math

class Tree:
    # create an empty van Emde Boas tree given the universe size
    def __init__(self, universe):
        self.u = universe
        
        # the smallest cluster size is 2
        # TODO: modify so that the size of each partition is dynamic
        if(self.u == 2):
            self.cluster = [0,0]
            self.summary = None
            
        else: 
            # the size of the block = sqrt(u)
            block = int(math.sqrt(self.u)) 
            self.cluster = [None] * block
            
            # recursively build sqrt(u) clusters each of size sqrt(u)
            for i in range(0, block):
                self.cluster[i] = Tree(block)
            
            # recursively build one summary for each sqrt(u) structures when u > 2
            self.summary = Tree(block)
    
    # insert an element x into the tree
    def insert(self, x):
        # handle erroneous input
        if x >= self.u or x < 0: 
            print("Element not in universe.")
            return 
        
        # insert directly in base case
        if(self.u == 2):
            self.cluster[x] = 1
            
        else: 
            high = self.high(x)
            low = self.low(x)
            
            # recurse to insert
            self.cluster[high].insert(low)
            
            # recursively insert in summary, too
            if self.summary is not None: self.summary.insert(high)
    
    # given an element x, check if it is the tree
    def membership(self, x):
        # handle erroneous input
        if x >= self.u or x < 0: 
            print("Element not in universe.")
            return 
        
        # check drectly in base case
        if self.u == 2: 
            return self.cluster[x] == 1
        
        else: 
            high = self.high(x)
            low = self.low(x)
            
            # check if summary is 0 before bothering to check cluster
            if self.summary.membership(high) is False: 
                return False
            else: 
                return self.cluster[high].membership(low)
    
    # TODO: under construction
    def successor(self, x):
        if self.u == 2: 
            return self.cluster[x] == 1
        else: 
            high = self.high(x)
            low = self.low(x)
            if self.summary.membership(high) is False: 
                return False
            else: 
                return self.cluster[high].membership(low)
    
    # the index of the cluster in which x would be located
    def high(self, x):
        block = int(math.sqrt(self.u))
        return int(math.floor(x/block))
    
    # the index of x's cluster (or x itself) within that cluster
    def low(self, x):
        block = int(math.sqrt(self.u))
        return (x % block)
    
    # rudimentary display of tree
    # TODO: make prettier
    def show(self):
        print("u = ", self.u)
        if(self.u == 2):
            print("cluster = ", self.cluster[0], self.cluster[1])
        else: 
            block = int(math.sqrt(self.u)) 
            
            for i in range(0, block):
                self.cluster[i].show()
                
            print("summary: ")
            self.summary.show()
            
# some test code       
t = Tree(16)
print("----")
t.show()
t.insert(2)
print("----")
t.show()
print("MEMBERSHIP:", t.membership(2))