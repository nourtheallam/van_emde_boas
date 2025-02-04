import math

class Tree:
    cluster =[]
    u = 0
    summary = []
    def __init__(self, cluster):
        if cluster == None:
            self.u = 0
            self.summary = None
            self.cluster = None
            return
        self.u = len(cluster)
        if len(cluster) == 2:
            self.cluster = cluster
            
            ### debugging
            print("cluster:")
            for i in self.cluster:
                print(i)
            ####
            
        else:
            block_size = int(math.sqrt(self.u)) 
            block_num = int(self.u / block_size)
            self.cluster = [None] * block_num
            
            print("Size: " , self.u, "Cluster: ")
            j = 0
            k = 0
            for i in range(0, block_num, 1):
                self.cluster[i] = Tree(cluster[j: j + block_size])
                if ((i+1) % 2 == 0 and block_num > 2):
                    self.summary.cluster[i] = Tree()
                    
                j += block_size

            # if(block_num == 2):
            #     self.summary = self.summary_builder()
            #     print("Summary: ", self.summary.cluster[0], self.summary.cluster[1])
            # elif(block_num == 4):
            #     self.summary = Tree(None)
            #     cluster_1 = Tree([self.cluster[0].summary.cluster[0] or self.cluster[0].summary.cluster[1], self.cluster[1].summary.cluster[0] or self.cluster[1].summary.cluster[0]])     
            #     cluster_2 = Tree([self.cluster[2].summary.cluster[0] or self.cluster[2].summary.cluster[1], self.cluster[3].summary.cluster[0] or self.cluster[3].summary.cluster[0]])   
            #     self.summary.cluster = [cluster_1, cluster_2]     
            #     self.summary.summary = Tree([int(self.summary.cluster[0].cluster[0] or self.summary.cluster[0].cluster[1]), int(self.summary.cluster[1].cluster[0] or self.summary.cluster[1].cluster[1])])
                
    def summary_builder(self):
        return Tree([int(self.cluster[0].cluster[0] or self.cluster[0].cluster[1]), int(self.cluster[1].cluster[0] or self.cluster[1].cluster[1])])

Tree([0,0,1,1,1,1,0,1,0,0,0,0,0,0,1,1])



