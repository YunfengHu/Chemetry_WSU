# load package
import pandas as pd 
import numpy as np
from plotly import tools
import plotly as py
import plotly.graph_objs as go
import math
import os
os.chdir('/home/yunfeng/Downloads/Clark_project/unwrapped-xyz-PT-event_centers')




# set path 
inputPath = '/home/yunfeng/Downloads/Clark_project/unwrapped-xyz-PT-event_centers/'
inputFile = 'zundel_combined_20180103.csv'


# load data 
df = pd.read_csv(inputPath + inputFile)


# subset O76, O95, H189
dfO76 = df[(df['Type'] == 'O') & (df['Index'] == 76)]
dfO95 = df[(df['Type'] == 'O') & (df['Index'] == 95)]
dfH198 = df[(df['Type'] == 'H') & (df['Index'] == 198)]

# calculate distance in x,y,z and 3D

## x,y,z distance between O76, O95 and H198
dfH198['distanceToX76'] = abs(np.array(dfH198['x']) - np.array(dfO76['x'])) 
dfH198['distanceToX95'] = abs(np.array(dfH198['x']) - np.array(dfO95['x'])) 
dfH198['distanceToY76'] = abs(np.array(dfH198['y']) - np.array(dfO76['y'])) 
dfH198['distanceToY95'] = abs(np.array(dfH198['y']) - np.array(dfO95['y'])) 
dfH198['distanceToZ76'] = abs(np.array(dfH198['z']) - np.array(dfO76['z'])) 
dfH198['distanceToZ95'] = abs(np.array(dfH198['z']) - np.array(dfO95['z'])) 


## total distance between H198 to O76 and O95
O76Array = np.array(dfO76.iloc[:,2:5])
O95Array = np.array(dfO95.iloc[:,2:5])
H198Array = np.array(dfH198.iloc[:,2:5])
totalDistanceToO76 = np.linalg.norm(O76Array - H198Array, axis=1)
totalDistanceToO95 = np.linalg.norm(O95Array - H198Array, axis=1)
dfH198['totalDistanceToO76'] = totalDistanceToO76
dfH198['totalDistanceToO95'] = totalDistanceToO95


# create scatter plot for each index  
orders = dfH198['Order'].unique()
data = []
fig = tools.make_subplots(rows=4, cols=1,  subplot_titles=('distance comparion in x','distance comparison in y', 'distance comparison in z', 'total distance comparison'))
for order in orders:
    for i in range(8, dfH198.shape[1]):
        dfTempt = dfH198[dfH198['Order'] == order]
        trace = go.Scatter(
            visible = True,
            x = dfTempt['Snapshot'],
            y = dfTempt.iloc[:,i], 
            name = list(dfTempt)[i]
            )
        data.append(trace)
        fig.append_trace(trace, math.ceil(float((i-7)/2)),1)


# create slider
# snapshots = dfH198['Snapshot'].unique() 
steps = []
for i in range(len(orders)):
    step =  dict(
        method='restyle',
        args=['visible', [False]*len(data)],
        label = str(i+1))
    for j in range((dfH198.shape[1]-8)*i,(dfH198.shape[1]-8)*(i+1)):
        step['args'][1][j] = True
    steps.append(step)


sliders = [dict(
    active = 0,
    currentvalue = {"prefix": "Beads: "},
    # pad = {"t": 50},
    steps = steps
)]


# initial show


fig['layout'].update(height=600, width=1200, title='Distance Comparison', sliders = sliders)


py.offline.plot(fig, filename='distance_comparison')





