## import packages 
import pandas as pd 
import os
import numpy as np 
from scipy.spatial.distance import pdist
import argparse
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt 
# from scipy.stats import ttest_ind

## functions 
def pairwise_distance(DataFrame, Snap):
	DataFrameTemp = DataFrame[DataFrame['Snapshot'] == Snap]
	DataFrameTemp = np.array(DataFrameTemp.iloc[:,2:5])
	DataFrameTemp = pdist(DataFrameTemp)
	return DataFrameTemp


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputPath')
	parser.add_argument('--outputPath')
	parser.add_argument('--inputFile')
	args = parser.parse_args()

	## change path
	os.chdir(args.outputPath)

	## laod data
	df = pd.read_csv(args.inputPath + args.inputFile)
	snaps = df['Snapshot'].unique()

	dfPD = []
	for snap in snaps:
		dftemp = pairwise_distance(df, snap)
		dfPD.append(dftemp)


	dfPD = np.array(dfPD)
	np.save(args.inputFile.replace('csv', 'npy'), dfPD)
	


if (__name__ == '__main__'):
	main()
