## import packages
import pandas as pd 
import numpy as np 
from scipy.spatial.distance import pdist
import os


## constants 
windowsize = 5

## set path 
inputPathRaw = '/home/yunfeng/Downloads/2018/Clark_project/raw_data_csv/'
outputPath = '/home/yunfeng/Downloads/2018/Clark_project/Report_20180509_OriginalSnaps_Centroid_Check/AllBarcode/AllPairwiseDistance' + str(windowsize) +'/'
os.chdir(outputPath)

## load data 
if windowsize == 20:
	df = pd.ExcelFile('/home/yunfeng/Downloads/2018/Clark_project/Dataset/successfulPTs-unreactiveH-04-22-18.xlsx')
	df = df.parse(df.sheet_names[0])
	df = df[df['H index']!= 154]
elif windowsize == 5:	
	df = pd.read_csv('/home/yunfeng/Downloads/2018/Clark_project/Dataset/all-Successful-PTs-5snap-redo.csv')
	df = df[df['H index']!=154]



## create pairwise distance 
for hindex, snap in zip(df['H index'], df['snap of PT']):
	hindex = hindex - 102
	dfRaw = pd.read_csv(inputPathRaw + '32rep-H' + str(hindex)+'.csv')
	snaps = [snap + i for i in range(-windowsize, windowsize + 1)]
	dfRawTempt = dfRaw[dfRaw['Snapshot'].isin(snaps)]
	pairwiseDist = []
	for snaptempt in snaps:
		dfRawTemptDist = dfRawTempt[dfRawTempt['Snapshot']==snaptempt]
		pairwiseDist.append(pdist(np.array(dfRawTemptDist.iloc[:,2:5])))
	np.save('H' + str(hindex) + '_Snapshot'+str(snap) + '_Windowsize' + str(windowsize) +'_PairwiseDistance.npy', pairwiseDist)


