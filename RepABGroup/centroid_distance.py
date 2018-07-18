## import packages 
import pandas as pd 
import os
import math
import numpy as np 
import argparse
from scipy.spatial.distance import pdist
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt 
# import math
# from scipy.stats import ttest_ind

## functions 
def r3_distance(x1,x2,x3,y1,y2,y3):
	return math.sqrt(math.pow(x1-y1,2) + math.pow(x2-y2,2) + math.pow(x3-y3,2))


def centroid_distance(DataFrame, Snap):
	DataFrame = DataFrame[DataFrame['Snapshot'] == Snap]
	DataFrame.loc[:,'xMean'] = DataFrame['x'].groupby(DataFrame['Snapshot']).transform('mean')
	DataFrame.loc[:,'yMean'] = DataFrame['y'].groupby(DataFrame['Snapshot']).transform('mean')
	DataFrame.loc[:,'zMean'] = DataFrame['z'].groupby(DataFrame['Snapshot']).transform('mean')
	# calculate the distance from points to centers
	DataFrame.loc[:,'distanceToCenters'] = DataFrame.apply(lambda x: r3_distance(x['x'], x['y'], x['z'], x['xMean'], x['yMean'], x['zMean']), axis = 1)
	# DataFrame = DataFrame[['Index', 'Type', 'x', 'y', 'z', 'Snapshot', 'Order', 'distanceToCenters']]
	return list(DataFrame['distanceToCenters'])


# ## set path 
# inputPath = '/san/home/yunfeng.hu/Chemistry/all_64rep_csv/'
# outputPath = '/san/home/yunfeng.hu/Chemistry/all_64rep_centroid_20170714/centroid_distance/'
# os.chdir(outputPath)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputPath')
	parser.add_argument('--outputPath')
	parser.add_argument('--inputFile')
	args = parser.parse_args()


	os.chdir(args.outputPath)

	df = pd.read_csv(args.inputPath + args.inputFile)
	snaps = df['Snapshot'].unique()


	dfCD = []
	for snap in snaps:
		dftemp = centroid_distance(df, snap)
		dfCD.append(dftemp)


	dfCD = np.array(dfCD)
	np.save(args.file.replace('csv', 'npy'))


if __name__ == '__main__':
	main()