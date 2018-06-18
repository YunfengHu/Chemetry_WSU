## ==============
# import packages 
import pandas as pd 
import os 
import numpy as np 
import random
import math

## ==============
# constants 
windowsize = 20
if windowsize == 5:
	sampleNum = int(np.ceil(518/16))
elif windowsize == 20:
	sampleNum = int(np.ceil(2288/16))


## ===============
# functions 
def r3_distance(x1,x2,x3,y1,y2,y3):
	return math.sqrt(math.pow(x1-y1,2) + math.pow(x2-y2,2) + math.pow(x3-y3,2))


def centroid_distance(DataFrame):
		DataFrame['xMean'] = DataFrame['x'].groupby(DataFrame['Snapshot']).transform('mean')
		DataFrame['yMean'] = DataFrame['y'].groupby(DataFrame['Snapshot']).transform('mean')
		DataFrame['zMean'] = DataFrame['z'].groupby(DataFrame['Snapshot']).transform('mean')
		# calculate the distance from points to centers
		DataFrame['distanceToCenters'] = DataFrame.apply(lambda x: r3_distance(x['x'], x['y'], x['z'], x['xMean'], x['yMean'], x['zMean']), axis = 1)
		DataFrame = DataFrame[['Index', 'Type', 'x', 'y', 'z', 'Snapshot', 'Order', 'distanceToCenters']]
		return DataFrame
