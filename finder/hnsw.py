import numpy
import nmslib
import time
import math
import logging
from scipy.sparse import csr_matrix

class Finder:
    #M = , efC = ,
    def __init__(self, persons, M = 30, efC = 200, num_threads = 8):
        self.num_threads = num_threads
        index_time_params = {'M': M, 'indexThreadQty': self.num_threads, 'efConstruction': efC, 'post' : 0}
        self.index = nmslib.init(method='hnsw', space='cosinesimil', data_type=nmslib.DataType.DENSE_VECTOR)
        self.index.addDataPointBatch(persons)
        start = time.time()
        logging.warning('Start indexing')
        self.index.createIndex(index_time_params)
        end = time.time()
        logging.warning('Index-time parameters', index_time_params)
        logging.warning('Indexing time = %f' % (end-start))



    # K = number of neighbors
    def find(self, query, persons_ids =None, treshold = 0.2, efS = 100, K = 5):
        query_time_params = {'efSearch': efS}
        self.index.setQueryTimeParams(query_time_params)
        nbrs = self.index.knnQuery(query, k = K)
        #print ("nbrs[0][0] {} nbrs[1][0] {}".format(nbrs[0][0], nbrs[1][0]))
        #print(nbrs)
        #print("NBRS type is {}".format(type(nbrs[1][0])))
        finded = []
        for i in range(5):
            finded.append({
                    'nbrs_id': nbrs[0][i],
                    'nbrs_dif': nbrs[1][i],
                    'db_id': persons_ids[int(nbrs[0][i])]
            })
        logging.warning("find {}".format(finded))


        if nbrs[1][0] < treshold:
            return nbrs[0][0]
        return None
