import sys 
sys.path.append('/home/yunfeng/Downloads/2018/Clark_project/Python_Code/')

import pandas as pd 
import os
import numpy as np 
from generate_rv_complex import *
from numpy.linalg import norm
from numpy import inf
import matplotlib.pyplot as plt 
from generate_rv_complex import *
from cutoff import *
import csv
import random
import plotly as py
import plotly.graph_objs as go
from plotly import tools


# constants 
sampleSize = 0.01

# set path
inputPath = '/home/yunfeng/Downloads/2018/Clark_project/raw_data_csv/'
outputPath = '/home/yunfeng/Downloads/2018/Clark_project/Report_20180319_Quardrant/StableAtoms10Snapshots/'
os.chdir(outputPath)

# load data 
dfH = pd.read_csv('/home/yunfeng/Downloads/2018/Clark_project/H2OIndex.csv', encoding = "ISO-8859-1")
HydroList = list(dfH['H index'])
HydroList.extend(list(dfH['H index.1']))
HydroList = [H-102 for H in HydroList]
targetSnapshots = random.sample(range(0,60000), int(sampleSize*60000))
targetSnapshots.sort()

for Hindex in HydroList:
	df = pd.read_csv(inputPath + '32rep-H' + str(Hindex) +'.csv')
	with open(outputPath + 'H' + str(Hindex) + '_barcode.csv','w') as fout:
		csv.writer(fout).writerow(['Hindex','Snapshot', 'Dimension', 'Filtration', 'Birth', 'Death', 'Generator', 'Terminator', 'Cutoff', 'MidSnapshot'])
		for targetsnapshot in targetSnapshots:
			targetsnapshotSeq = [targetsnapshot+i for i in range(-5,6)]
			for snapshot in targetsnapshotSeq:
				dfTempt = df[df['Snapshot']==snapshot]
				points = np.array(dfTempt.iloc[:,2:5])
				rips,m,dgms = generate_rv_complex(points,3)
				Cutoff = [pt.death for pt in dgms[0]]
				Cutoff = sorted(Cutoff)[-2]
				for i,dgm in enumerate(dgms):
					if i<=2:
						for s in dgm:
							if s.death != np.inf:
								birthGen = list(rips.__getitem__(s.data))
								deathGen = list(rips.__getitem__(m.pair(s.data)))
								# if set(birthGen).intersection(set(deathGen)) == set(birthGen):
								# 	flag = 1
								# else:
								# 	flag = 0
								csv.writer(fout).writerow([Hindex, snapshot, i, s.data, s.birth, s.death, birthGen, deathGen, Cutoff, targetsnapshot])
							else:
								csv.writer(fout).writerow([Hindex, snapshot, i, s.data, s.birth, 0.5, list(rips.__getitem__(s.data)), 1, Cutoff, targetsnapshot])
					else: continue
	fout.close()


