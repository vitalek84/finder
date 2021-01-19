
from scipy.sparse import csr_matrix
from sqlalchemy import create_engine
import numpy

def read_data(filename, max_qty = None):
    row = []
    col = []
    data = []
    read_qty = 0
    with open(filename,'r') as f:
        read_num_ft = 0
        for line in f:
            x = line.replace(':', ' ').strip().split()
            if (len(x) % 2 != 0):
                raise(Exception('Poorly formated line %d in file %s' % (read_qty + 1, filename)))
            if (len(x) == 0): continue
            for i in range(0, len(x), 2):
                row.append(read_qty)
                feat_id = int(x[i])
                read_num_ft = max(read_num_ft, feat_id + 1)
                col.append(feat_id)
                data.append(float(x[i+1]))

            read_qty = read_qty+1
            if max_qty != None and read_qty >= max_qty: break

    print('Read %d rows, # of features %d' %  (read_qty, read_num_ft))
    ft_mat = csr_matrix((numpy.array(data), (numpy.array(row), numpy.array(col))),
                         shape=(read_qty, read_num_ft))
    return (read_qty, ft_mat)


CON_STR ='postgresql://loyalty:loyalty@localhost/loyalty'
engine = create_engine(CON_STR)
result_set = engine.execute("SELECT id, ident FROM loyalty_person")

cols = 256
rows = 0
row=[]
col=[]
data=[]
max_id = engine.execute("SELECT MAX(id) as max_id FROM loyalty_person").fetchone()
print(max_id[0])
allrows =[]

for i in range(max_id[0]+1):
    d = []
    for j in range(256):
        d.append(0)
    allrows.append(d)

for r in result_set:
    allrows[r.id] = r.ident

print(allrows[5][1])    
for r in result_set:

    num_ft =0
    for i in r.ident:
        row.append(r.id)
        col.append(num_ft)
        data.append(i)
        num_ft += 1
    #rows += 1
    rows=r.id+1
#print ("Number of rows {} , colls {}".format(rows, cols))
ft_mat = csr_matrix((numpy.array(data), (numpy.array(row), numpy.array(col))),
                     shape=(rows, cols))

#print(ft_mat[3])
