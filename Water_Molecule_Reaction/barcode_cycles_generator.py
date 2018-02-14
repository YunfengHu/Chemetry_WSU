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
import plotly as py
import plotly.graph_objs as go
from plotly import tools

# constants 
windowsize = 5

# set path
inputPath = '/home/yunfeng/Downloads/2018/Clark_project/raw_data_csv/'
outputPath = '/home/yunfeng/Downloads/2018/Clark_project/Report_20180212/Barcode_Generator/'
os.chdir(outputPath)

# load data 
df = pd.read_csv(inputPath + '32rep-H4.csv')
dfTarget = pd.ExcelFile('/home/yunfeng/Downloads/2018/Clark_project/Report_20180212/' + 'all-replicas-succ-PTs-H106_02_08_18.xlsx')
sheetNames = dfTarget.sheet_names
dfTarget = dfTarget.parse(sheetNames[0])
header = dfTarget.iloc[0]
dfTarget = dfTarget[1:]
dfTarget.columns = header 
targetSnapshots = dfTarget['Initial Snap.'].unique()



for targetsnapshots in targetSnapshots:
	targetwindow = [targetsnapshots + i for i in range(-windowsize, windowsize)]
	with open(outputPath + str(targetsnapshots)+'_barcode.csv','w') as fout:
		csv.writer(fout).writerow(['Snapshot', 'Dimension', 'Filtration', 'Birth', 'Death', 'Generator', 'Terminator', 'TargetSnapshot', 'Cutoff', 'Flag'])
		for targetsnapshot in targetwindow:
			dfTempt = df[df['Snapshot']==targetsnapshot]
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
							if set(birthGen).intersection(set(deathGen)) == set(birthGen):
								flag = 1
							else:
								flag = 0
							csv.writer(fout).writerow([targetsnapshot, i, s.data, s.birth, s.death, birthGen, deathGen, targetsnapshots, Cutoff, flag])
						else:
							csv.writer(fout).writerow([targetsnapshot, i, s.data, s.birth, 1, list(rips.__getitem__(s.data)), 1, targetsnapshots, Cutoff, 0])
				else: continue

