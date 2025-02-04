import math
import networkx as nx
import matplotlib.pyplot as plt

class Tree:
    # create an empty van Emde Boas tree given the universe size
    def __init__(self, universe):
        self.u = universe
        self.stack = [self]
        
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
    def show_fancy(self):
        # Create a graph
        G = nx.Graph()
        G.add_nodes_from(self)
        prev_n = None
        for n in list(G.nodes):
            if prev_n is not None and prev_n.u > n.u:
                G.add_edge(n,prev_n)
            prev_n = n

        # Draw the graph
        nx.draw(G, with_labels=True)
        plt.show()
        
    def __str__(self) -> str:
        return_string = "u: {}".format(self.u)
        if self.u == 2:
            for c in self.cluster:
                return_string += "\n" + str(c)
        return return_string
    
    def __iter__(self):
        return self
    def __next__(self):
        if not self.stack: 
            raise StopIteration
        else: 
            curr = self.stack.pop()
            print(curr)
            if curr.cluster is list: 
                self.stack.append(curr.cluster)
            elif curr.u >= 4 and curr.cluster is not None:
                for c in curr.cluster[::-1]:
                    self.stack.append(c)
            return curr
    def __len__(self):
        return 1 + len(self.cluster)

                
            
# some test code       
t = Tree(16)
t.insert(2)
t.show_fancy()
t.edge_generator()
print("MEMBERSHIP:", t.membership(2))