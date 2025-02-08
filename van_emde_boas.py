import math
import networkx as nx
import matplotlib.pyplot as plt

class Tree:
    # create an empty van Emde Boas tree given the universe size
    def __init__(self, universe):
        self.u = universe
        self.stack = [self]
        self.min = -1
        self.max = -1
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
            if self.summary is not None: 
                self.summary.insert(high)

        if x < self.min or self.min == -1:
            self.min = x
        if x > self.max: 
            self.max = x
            
    
    # given an element x, check if it is the tree
    def membership(self, x):
        # handle erroneous input
        if self.min == -1 or x > self.max or x < self.min: 
            return False
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
    
    def successor(self, x):
        if x < self.min: 
            return self.min
        elif x >= self.max: 
            return math.inf
        
        if self.u == 2: 
            if x == 0 and self.cluster[1] == 1: 
                return 1
            else: 
                return math.inf
        else: 
            high = self.high(x)
            low = self.low(x)
            if low < self.cluster[high].max:
                j = self.cluster[high].successor(low)
                return high*(math.sqrt(self.u)) + j
            else: 
                i = self.summary.successor(high)
                return i*(math.sqrt(self.u)) + self.cluster[i].min

    
    # the index of the cluster in which x would be located
    def high(self, x):
        if(x == math.inf or x == -math.inf):
            return math.inf
        block = int(math.sqrt(self.u))
        return int(math.floor(x/block))
    
    # the index of x's cluster (or x itself) within that cluster
    def low(self, x):
        block = int(math.sqrt(self.u))
        return (x % block)
    
    
    # rudimentary display of tree
    def print(self):
        print("u = ", self.u)
        if(self.u == 2):
            print("cluster = ", self.cluster[0], self.cluster[1])
        else: 
            block = int(math.sqrt(self.u)) 
            
            for i in range(0, block):
                self.cluster[i].show()
                
            print("summary: ")
            self.summary.show()


    #TODO: display summary
    def show(self):
        G = nx.DiGraph()
        G.add_nodes_from(self)
                
        special_stack = []
        for curr in G.nodes: 
            s_len = len(special_stack)
            if s_len != 0:
                parent = special_stack[s_len-1]
                if parent[1] != 0:
                    G.add_edge(parent[0], curr)
                    parent[1] -= 1
                if parent[1] == 0:
                    special_stack.pop(s_len-1)
            if curr.u != 2: 
                special_stack.append([curr, math.sqrt(curr.u)])
            
        pos = nx.bfs_layout(G, self)
        nx.draw(G, pos, arrows=True, with_labels=True, node_size=3000, node_color='#fff2fc', font_size=8,
            font_weight='bold')
        plt.show()
        
    def __str__(self) -> str:
        return_string = "u: {}".format(self.u)
        if self.u == 2:
            for c in self.cluster:
                return_string += "\n" + str(c)
        return_string += "\nmin = {}\n".format(self.min)
        return_string += "max = {}\n".format(self.max)
        return return_string
    def __iter__(self):
        return self
    def __next__(self):
        if not self.stack: 
            raise StopIteration
        else: 
            curr = self.stack.pop()
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
t.insert(15)
t.insert(12)

t.insert(13)

# t.edge_generator()
print("successor: ", t.successor(10))
print("MEMBERSHIP:", t.membership(2))
print("MEMBERSHIP:", t.membership(13))
t.show()

# print(t.min)