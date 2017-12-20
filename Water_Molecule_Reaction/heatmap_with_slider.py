# import packages
import os 
os.chdir('/home/yunfeng/Downloads/Clark_project/Result_20171218/')
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np 
import plotly as py
import plotly.graph_objs as go


# set path
inputPath = '/home/yunfeng/Downloads/Clark_project/Result_20171218/'
inputfiles = '20k-32rep-H7.csv'

# load data 
df = pd.read_csv(inputPath + inputfiles)


# calculate the distance matrix for each snapshot 
data = []
Snapshots = df['Snapshot'].unique()
for snapshot in Snapshots[0:50]:
	dfTempt = df[df['Snapshot'] == snapshot]
	dfTempt = np.array(dfTempt[['x', 'y', 'z']])
	dfTemptDistance = pairwise_distances(dfTempt)
	trace = go.Heatmap(visible = False, z = dfTemptDistance, 
	x = ['H_' + str(i+1) for i in range(len(dfTempt))],
	y = ['H_' + str(i+1) for i in range(len(dfTempt))],
    # colorscale=[[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'],
    # [0.3333333333333333, 'rgb(253,174,97)'], [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'],
    # [0.6666666666666666, 'rgb(171,217,233)'],[0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'],
    # [1.0, 'rgb(49,54,149)']]
	)
	data.append(trace)

data[10]['visible'] = True
snapshots = []
for i in range(len(data)):
    snapshot = dict(
        method = 'restyle',
        args = ['visible', [False] * len(data)],
        label = 'snapshot' + str(i) 
    )
    snapshot['args'][1][i] = True # Toggle i'th trace to "visible"
    snapshots.append(snapshot)

sliders = [dict(
    active = 10,
    currentvalue = {"prefix": "Snapshot: "},
    # pad = {"t": 50},
    steps = snapshots
)]

layout = dict(sliders=sliders)

fig = dict(data=data, layout=layout)

py.offline.plot(fig, filename='snapshot-heatmap.html')
