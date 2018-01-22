import dionysus as d 
import numpy as np
from numpy.linalg import norm
import pandas as pd 
import random
import csv
import math
import itertools 
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, ward, set_link_color_palette
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import pdist
from numpy import inf
import os
outputPath = '/home/yunfeng/Downloads/2018/Clark_project/persistent_bar_code/'
os.chdir(outputPath)

# constant 
startSnapshot = 0
sampleRatio = 0.001


# function 
def convert_to_vertex(Vertex):
	vertex = Vertex.strip('<>')
	vertex = vertex.split(',')
	vertex = [int(item) for item in vertex]
	return vertex


import numpy as np 
from numpy import inf
def change_inf_to_2nd_largest(List, ReplaceValue):
	listcopy = List.copy()
	listcopy = list(set(listcopy))
	listcopy.sort()
	List = np.array(List)
	# List[List == inf] = listcopy[-2]
	List[List == inf] = ReplaceValue
	return List


from scipy.spatial.distance import pdist
import dionysus as d 
def generate_rv_complex(PointsArray):
	dists = pdist(PointsArray)
	# adjacentDist = [norm(PointsArray[i,:] - PointsArray[i+1,:]) for i in range(len(PointsArray)-1)]
	Alpha = 0.5*max(dists)
	rips = d.fill_rips(dists, 2, Alpha)
	m = d.homology_persistence(rips)
	dgms = d.init_diagrams(m, rips)
	return dgms



def persistent_barcode(Diagrams, cutoff, Savefile):
	for i in range(2):
		j = 0
		x=[]
		y=[]
		plt.figure()
		for pt in Diagrams[i]:
			x.append(pt.birth)
			y.append(j)
			x.append(pt.death)
			y.append(j)
			j = j +1
		x = change_inf_to_2nd_largest(x,1)
		pair_x_array = np.reshape(x, (-1, 2))
		pair_y_array = np.reshape(y, (-1, 2))
		for k, pair_x in enumerate(pair_x_array):
			pair_y = pair_y_array[k]
			plt.plot(pair_x, pair_y,linewidth = 3, color = 'g')
		plt.axvline(x=cutoff)
		plt.title('H' + str() + ' ' + Savefile)
		plt.savefig('H' + str(i) + ' ' + Savefile)



def wasserstein_distance(Dgm1, Dgm2, Q=2):
	return d.wasserstein_distance(Dgm1, Dgm2, q=Q)


# set path 
inputPath = '/home/yunfeng/Downloads/2018/Clark_project/raw_data_csv/'
files = ['32rep-H4.csv']
file = files[0]


# load data 
dfTempt = pd.read_csv(inputPath + file)
snapshots = list(dfTempt['Snapshot'].unique())
snapshotsSample = [snapshots[59+i] for i in range(61)]

for snapshot in snapshotsSample:
	dfTemptSubset = dfTempt[dfTempt['Snapshot'] == snapshot]
	points = np.array(dfTemptSubset.iloc[:,2:5])
	adjacentDist = [norm(points[i%len(points),:] - points[(i+1)%len(points),:]) for i in range(len(points))]
	# cutoff = max(adjacentDist)
	dgms = generate_rv_complex(points)
	# Dgms.append(dgms[1])
	cutoff = [pt.death for pt in dgms[0]]
	cutoff = sorted(cutoff)[-2]
	savefile = 'snapshot ' + str(snapshot) + ' in ' + file.replace('csv', 'png')
	persistent_barcode(dgms, cutoff, savefile)
