from __future__ import print_function   # if you are using Python 2
import dionysus as d
from numpy import *

simplices = [([2], 3), ([1,2], 2), ([0,2], 2),
             ([0], 0),   ([1], 1), ([0,1], 2), ([4], 2), ([0,1,2], 3)]
f = d.Filtration()
for vertices, time in simplices:
    f.append(d.Simplex(vertices, time))
f.sort()
for i,s in enumerate(f):
   print(i,s)


m = d.homology_persistence(f)
# for i,c in enumerate(m):
# 	print(i, c)



for i in range(len(m)):
	# boundary = f[i].boundary()
	# print (list(boundary))
	# print (i, str(f[i]).split()[0])
	if m.pair(i) < i: continue      # skip negative simplices
	dim = f[i].dimension()
	if m.pair(i) != m.unpaired:
		# print(dim, i, m.pair(i), list(f[i])) # for generator
		print(dim, i, m.pair(i), list(f[m.pair(i)].boundary()))
	else:
		print(dim, i, list(f.__getitem__(i).boundary()))

