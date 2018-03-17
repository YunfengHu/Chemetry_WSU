# import packages 

import sys
sys.path.append('/home/yunfeng/Downloads/2018/Clark_project/Python_Code/')
import pandas as pd 
import os
import numpy as np 
import collections
from operator import *


# set path 
inputPath = '/home/yunfeng/Downloads/2018/Clark_project/Report_20180319_Quardrant/StableAtoms10Snapshots/'
outputPath = '/home/yunfeng/Downloads/2018/Clark_project/Report_20180319_Quardrant/StableAtomsBettiSequence/'
os.chdir(outputPath)

# laod files 

## stable files 
files = os.listdir(inputPath)
bettiSeq = np.linspace(0,0.4,401)

## convert barcode to betti sequence

for file in files:	
	bettiSeqDict = collections.defaultdict(list)
	df = pd.read_csv(inputPath + file)
	snapshots = df['Snapshot'].unique()
	for snapshot in snapshots:
		dictname = file.split('_')[0] + '_' + str(snapshot)
		dfSnapshot = df[df['Snapshot']==snapshot]
		bettiSeqDim = []
		for dim in range(2):
			dfSnapshotDim = dfSnapshot[dfSnapshot['Dimension'] == dim]
			dfSnapshotDim = np.array(dfSnapshotDim[['Birth', 'Death']])
			bettiSeqTempt = np.zeros(401)
			for dimlen in range(len(dfSnapshotDim)):
				bettiSeqDimTempt = np.heaviside(bettiSeq - dfSnapshotDim[dimlen,0], 0) - np.heaviside(bettiSeq - dfSnapshotDim[dimlen,1], 0)
				bettiSeqTempt += bettiSeqDimTempt
			bettiSeqDim.append(bettiSeqTempt)
		bettiSeqDim = np.array(bettiSeqDim)
		bettiSeqDict[dictname].append(bettiSeqDim)
	savename = file.replace('barcode.csv', 'BettiSeq.npy')
	np.save(savename, bettiSeqDict)


			
