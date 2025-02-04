import math

class Tree:
    def __init__(self, universe):
        self.u = universe
        print("u = ", self.u)
        if(self.u == 2):
            self.cluster = [0,0]
            self.summary = None
            print("cluster = ", 0, 0)
        else: 
            block = int(math.sqrt(self.u)) 
            self.cluster = [None] * block
            
            for i in range(0, block):
                self.cluster[i] = Tree(block)
            print("summary: ")
            self.summary = Tree(block)
            
    def insert(self, x):
        if(self.u == 2):
            print("inserting")
            self.cluster[x] = 1
        else: 
            high = self.high(x)
            low = self.low(x)
            print("high: ", high)
            print("low: ", low)
            self.cluster[high].insert(low)
            if self.summary is not None: self.summary.insert(high)
    
    def membership(self, x):
        if self.u == 2: 
            return self.cluster[x] == 1
        else: 
            high = self.high(x)
            low = self.low(x)
            if self.summary.membership(high) is False: 
                return False
            else: 
                return self.cluster[high].membership(low)
    
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
            
    def high(self, x):
        block = int(math.sqrt(self.u))
        return int(math.floor(x/block))
    
    def low(self, x):
        block = int(math.sqrt(self.u))
        return (x % block)
    
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
            
t = Tree(16)
print("----")
t.show()
t.insert(2)
print("----")
t.show()
print("MEMBERSHIP:", t.membership(2))