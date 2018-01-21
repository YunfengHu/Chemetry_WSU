import dionysus as d 
import numpy as np
from numpy.linalg import norm
import pandas as pd 
import random
import csv
import math
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from numpy import inf
import os
outputPath = '/home/yunfeng/Downloads/2018/Clark_project/raw_data_edge_face/'
os.chdir(outputPath)

# constant 
sampleRatio = 0.001


# function 
def convert_to_vertex(Vertex):
	vertex = Vertex.strip('<>')
	vertex = vertex.split(',')
	vertex = [int(item) for item in vertex]
	return vertex


import numpy as np 
from numpy import inf
def change_inf_to_2nd_largest(List):
	listcopy = List.copy()
	listcopy = list(set(listcopy))
	listcopy.sort()
	List = np.array(List)
	List[List == inf] = listcopy[-2]
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
	for i in range(3):
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
		x = change_inf_to_2nd_largest(x)
		pair_x_array = np.reshape(x, (-1, 2))
		pair_y_array = np.reshape(y, (-1, 2))
		for k, pair_x in enumerate(pair_x_array):
			pair_y = pair_y_array[k]
			plt.plot(pair_x, pair_y,linewidth = 3, color = 'r')
		plt.axvline(x=cutoff)
		plt.title('H' + str(i) + ' ' + Savefile)
		plt.savefig('H' + str(i) + ' ' + Savefile)




# set path 
inputPath = '/home/yunfeng/Downloads/2018/Clark_project/raw_data_csv/'
files = ['32rep-H4.csv']
file = files[0]


# load data 
dfTempt = pd.read_csv(inputPath + file)
snapshots = list(dfTempt['Snapshot'].unique())
startSnapshot = 0
snapshotsSample = snapshots[startSnapshot:math.ceil(sampleRatio*len(snapshots))]


# create barcode for each sample 
for snapshot in snapshotsSample:
	dfTemptSubset = dfTempt[dfTempt['Snapshot'] == snapshot]
	points = np.array(dfTemptSubset.iloc[:,2:5])
	adjacentDist = [norm(points[i,:] - points[i+1,:]) for i in range(len(points)-1)]
	cutoff = 0.5*max(adjacentDist)
	dgms = generate_rv_complex(points)
	savefile = 'snapshot ' + str(snapshot) + ' in ' + file.replace('csv', 'png')
	persistent_barcode(dgms, cutoff, savefile)

	
