# import packages 
import numpy as np 
import os
import pandas as pd 
from operator import *
import matplotlib.pyplot as plt


# =====================
# define functions 


# -----------------------
# barcode
def create_barcode(DataFrame, Cutoff, ax=None):
    if ax is None:
        ax = plt.gca()
    colors = {0:'g', 1:'g'}
    lines = []
    for j in range(len(DataFrame)):
    	lines.append((DataFrame['Birth'].iloc[j], DataFrame['Death'].iloc[j]))
    	lines.append((j,j))
    	lines.append(colors[DataFrame['Dimension'].iloc[j]])
    ax.set_xlim([0,0.4])
    ax.axvline(x=Cutoff)
    ax.set_title('Betti'+str(DataFrame['Dimension'].iloc[0])+' Barcode')
    barcode = ax.plot(*lines)
    return barcode



# -----------------------
# betti sequence
def create_bettiseq(Array, Cutoff, Dimension, ax=None):
	if ax is None:
		ax = plt.gca()
	x = np.linspace(0,0.4,401)
	y = Array
	ax.set_xlim([0,0.4])
	ax.axvline(x=Cutoff)
	ax.set_title('Betti' + str(Dimension) +' Sequence')
	bettiSeq = ax.step(x,y, 'r')
	return bettiSeq 


# ===================
# set path 
inputBarcodePath = '/home/yunfeng/Downloads/2018/Clark_project/Report_20180319_Quardrant/StableAtoms10Snapshots/'
inputBettiSeqPath = '/home/yunfeng/Downloads/2018/Clark_project/Report_20180319_Quardrant/StableAtomsBettiSequence/'
outputPath = '/home/yunfeng/Downloads/2018/Clark_project/Report_20180319_Quardrant/'
os.chdir(outputPath)


# =====================
# load data 

# ------------------
# load barcode
df = pd.read_csv(inputBarcodePath+ 'H22_barcode.csv')
df = df[df['MidSnapshot'] == 175]
dfSnapshots = df['Snapshot'].unique()


# -----------------
# load bette sequence 
bettiArray = np.load(inputBettiSeqPath + 'H22_BettiSeq.npy').item()
bettiSnapshots = ['H22_'+ str(snapshot) for snapshot in dfSnapshots]



# =====================
# plot result 
for dfsnapshot, bettisnapshot in zip(dfSnapshots, bettiSnapshots):
	dfTempt = df[(df['Snapshot']==dfsnapshot) & (df['Dimension']!= 2)]
	cutoff = dfTempt['Cutoff'].iloc[0]
	bettiTempt = bettiArray[bettisnapshot][0]
	fig, axs = plt.subplots(2,2, figsize=(16, 8), dpi=80, sharex = True)
	axs = axs.ravel()
	for dim in range(2):
		dfTemptDim = dfTempt[dfTempt['Dimension']==dim]
		create_barcode(dfTemptDim, cutoff, ax = axs[dim])
		create_bettiseq(bettiTempt[dim], cutoff, dim, ax = axs[2+dim])
	plt.savefig('H22Snapshot'+str(dfsnapshot)+'BettiSeqPlot.png')


