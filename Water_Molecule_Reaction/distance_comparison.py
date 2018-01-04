# load package
import pandas as pd 
import numpy as np
from plotly import tools
import plotly as py
import plotly.graph_objs as go
import math
import os
os.chdir('/home/yunfeng/Downloads/Clark_project/unwrapped-xyz-PT-event_centers')


# functions 
def create_subplot(DataFrame, StepFactor, ShowFactor, IndexName):
    Factors = DataFrame[StepFactor].unique()
    data = []
    fig = tools.make_subplots(rows=4, cols=1,  subplot_titles=('distance comparion in x','distance comparison in y', 'distance comparison in z', 'total distance comparison'))
    for factor in Factors:
        for i in range(8, DataFrame.shape[1]):
            dfTempt = DataFrame[DataFrame[StepFactor] == factor]
            trace = go.Scatter(
                visible = True,
                x = dfTempt[ShowFactor],
                y = dfTempt.iloc[:,i], 
                name = list(dfTempt)[i]
                )
            data.append(trace)
            fig.append_trace(trace, math.ceil(float((i-7)/2)),1)
    steps = []
    for i in range(len(Factors)):
        step =  dict(
            method='restyle',
            args=['visible', [False]*len(data)],
            label = str(Factors[i]))
        for j in range((DataFrame.shape[1]-8)*i,(DataFrame.shape[1]-8)*(i+1)):
            step['args'][1][j] = True
        steps.append(step)

    sliders = [dict(
        active = 0,
        currentvalue = {"prefix": str(StepFactor) + ": "},
        # pad = {"t": 50},
        steps = steps
    )]
    fig['layout'].update(height=600, width=1200, title='Distance Comparison ' + IndexName + ' v.s. O76 and ' + IndexName + ' v.s. O95 per ' + str(StepFactor), sliders = sliders)

    py.offline.plot(fig, filename='distance_comparison_per_'+ str(StepFactor) + '_' + IndexName)



# set path 
inputPath = '/home/yunfeng/Downloads/Clark_project/unwrapped-xyz-PT-event_centers/'
inputFile = 'zundel_combined_20180103.csv'


# load data 
df = pd.read_csv(inputPath + inputFile)


# subset O76, O95, H189
dfO76 = df[(df['Type'] == 'O') & (df['Index'] == 76)]
dfO95 = df[(df['Type'] == 'O') & (df['Index'] == 95)]
df189 = df[(df['Type'] == 'H') & (df['Index'] == 189)]

# calculate distance in x,y,z and 3D

## x,y,z distance between O76, O95 and H189
df189['distanceToX76'] = abs(np.array(df189['x']) - np.array(dfO76['x'])) 
df189['distanceToX95'] = abs(np.array(df189['x']) - np.array(dfO95['x'])) 
df189['distanceToY76'] = abs(np.array(df189['y']) - np.array(dfO76['y'])) 
df189['distanceToY95'] = abs(np.array(df189['y']) - np.array(dfO95['y'])) 
df189['distanceToZ76'] = abs(np.array(df189['z']) - np.array(dfO76['z'])) 
df189['distanceToZ95'] = abs(np.array(df189['z']) - np.array(dfO95['z'])) 


## total distance between H189 to O76 and O95
O76Array = np.array(dfO76.iloc[:,2:5])
O95Array = np.array(dfO95.iloc[:,2:5])
H189Array = np.array(df189.iloc[:,2:5])
totalDistanceToO76 = np.linalg.norm(O76Array - H189Array, axis=1)
totalDistanceToO95 = np.linalg.norm(O95Array - H189Array, axis=1)
df189['totalDistanceToO76'] = totalDistanceToO76
df189['totalDistanceToO95'] = totalDistanceToO95



create_subplot(df189, 'Bead', 'Snapshot', 'H189')
create_subplot(df189, 'Snapshot', 'Bead', 'H189')

