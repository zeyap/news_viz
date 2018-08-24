from simhash import Simhash
import random
import math
import copy

def cluster(page_list):
    input_text = [page['text'] for page in page_list]
    k_means = KMeans(4,input_text)
    k_means.run()
    res = []
    for i,group in enumerate(k_means.output):
        res.append([])
        for page_id in group:
            res[i].append(page_list[page_id])
    print(res)
    return res


class KMeans(object):
    def __init__(self,k=4,inputs=[]):
        if len(inputs)>k:
            self.k = k
        else:
            self.k = len(inputs)

        self.input = inputs

        self.output = []
        self.d = []
        for i in range(0,len(inputs)):
            self.d.append([])
            for j in range(0,len(inputs)):
                self.d[i].append(math.inf)
    
    def run(self):
        self.gen_centroids()
        converged = False
        while converged==False:
            self.cluster_inputs()
            curr_centroids = copy.deepcopy([c['centroid'] for c in self.clusters])
            self.regen_centroids()
            next_centroids = copy.deepcopy([c['centroid'] for c in self.clusters])
            converged = self.is_identical(curr_centroids,next_centroids)
        groups = [cluster['group'] for cluster in self.clusters]

        for i,group in enumerate(groups):
            self.output.append([])
            for item in group:
                self.output[i].append(item)

        # self.output = [self.input[item] for item in (group for group in groups)]

    
    #randomly choose seeds
    def gen_centroids(self):
        self.clusters = []
        input_len = len(self.input)
        if input_len==0:
            return

        if input_len ==1:
            self.clusters.append({
                'centroid':0
                })
            return

        random.seed(1)
        for i in range(0,self.k):
            r = random.randint(0,input_len)
            self.clusters.append({
                'centroid':r
                })

    def regen_centroids(self):        
        for cluster in self.clusters:
            min_dist = math.inf
            min_id = -1
            distances = self.d
            for point in cluster['group']:

                if distances[point][cluster['centroid']]!=math.inf:
                    curr_dist = distances[point][cluster['centroid']]
                elif distances[cluster['centroid']][point]!=math.inf:
                    curr_dist = distances[point][cluster['centroid']] = distances[cluster['centroid']][point]
                else:
                    curr_dist = distances[point][cluster['centroid']] = distances[cluster['centroid']][point] =self.dist(point,cluster['centroid'])

                if curr_dist<min_dist:
                    min_dist = curr_dist
                    min_id = point
            cluster['centroid'] = min_id

    
    def is_identical(self,a,b):
        return len(set(a).intersection(b)) == len(a)
    
    def cluster_inputs(self):
        for cluster in self.clusters:
            cluster['group'] = []

        for item in self.input:
            min_dist = math.inf
            min_dist_id = -1
            for cluster in self.clusters:
                c = cluster['centroid']
                curr_dist = self.dist(item,self.input[c])
                if curr_dist<min_dist:
                    min_dist = curr_dist
                    min_dist_id = cluster['centroid']
            cluster['group'].append(min_dist_id)


    def dist(self,a='',b=''):
        return Simhash(a).distance(Simhash(b))