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
import plotly as py
import plotly.graph_objs as go
from plotly import tools

# constants 
windowsize = 5

# set path
inputPath = '/home/yunfeng/Downloads/2018/Clark_project/raw_data_csv/'
outputPath = '/home/yunfeng/Downloads/2018/Clark_project/Report_20180212/Barcode_Generator_Plot/'
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


# generate barcode 

for targetsnapshots in targetSnapshots:
	targetwindow = [targetsnapshots + i for i in range(-windowsize, windowsize)]
	data = []
	for targetsnapshot in targetwindow:
		dfTempt = df[df['Snapshot']==targetsnapshot]
		points = np.array(dfTempt.iloc[:,2:5])
		Cutoff = cutoff(points)
		rips,m,dgms = generate_rv_complex(points,3)
		count = 0
		for i in range(3):
			x = []
			y = []
			Text = []
			for s in dgms[i]:
				birth = s.birth
				death = s.death
				if death!=np.inf:
					x.append(birth)
					y.append(count)
					Text.append(str(list(rips.__getitem__(s.data))))
					x.append(death)
					y.append(count)
					Text.append(str(list(rips.__getitem__(m.pair(s.data)))))
					x.append(None)
					y.append(None)
					Text.append(None)
				else:
					x.append(birth)
					y.append(count)
					Text.append(str(list(rips.__getitem__(s.data))))
					x.append(1)
					y.append(count)
					Text.append(str(1))
					x.append(None)
					y.append(None)
					Text.append(None)
				count = count + 1
			trace = go.Scatter(
				x=x,
				y=y,
				name = 'Betti' + str(i),
				mode = 'lines + markers',
				text = Text
				)
			data.append(trace)
	for j in range(len(targetwindow)):
		for i in range(3):
			data[j*3+i]['visible'] = False

	data[0]['visible'] = True
	data[1]['visible'] = True
	data[2]['visible'] = True

	steps = []
	for k in range(len(targetwindow)):
		step = dict(
			method = 'restyle',
			args = ['visible', [False]*len(data)],
			label = 'snapshot' + str(targetwindow[k]), 
			)
		step['args'][1][3*k+0] = True
		step['args'][1][3*k+1] = True
		step['args'][1][3*k+2] = True
		steps.append(step)


	sliders = [dict(
	    active = 0,
	    currentvalue = {"prefix": "Snapshot: "},
	    pad = {"t": 50},
	    steps = steps
	)]


	layout = dict(title= 'Barcode_for_snapshot_' + str(targetsnapshots) + 'windowsize5',sliders=sliders)
	fig = dict(data=data, layout=layout)
	py.offline.plot(fig, filename='Barcode_for_snapshot_' + str(targetsnapshots) + 'windowsize5.html', auto_open=False)








