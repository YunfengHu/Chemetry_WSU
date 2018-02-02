# Successful Proton Transfer
# O2 and O38 – snapshot 230 – 530 (PT at snap. 380 in centroid data)
# O2 and O38 – snapshot 3310 – 3610 (PT  at snap. 3460  in centroid data)
# O38 and O16 – snapshot 20515 – 20815 (PT  at snap. 20665  in centroid data)
# O38 and O16 – snapshot 24140– 24440 (PT  at snap. 24290  in centroid data)
# O16 and O21 – snapshot 36018 – 36318 (PT  at snap. 36168  in centroid data)
# O16 and O21 – snapshot 37009 – 37309 (PT  at snap. 37159  in centroid data)
# O21 and O5 – snapshot 41271 – 41571 (PT at snap. 41421 in centroid data)
# O21 and O5 – snapshot 43563 – 43863 (PT at snap. 43713 in centroid data)


# input package
import sys
sys.path.append('/home/yunfeng/Downloads/2018/Clark_project/Python_Code/')
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from plot_persistent_barcode import *
from numpy.linalg import norm
from generate_rv_complex import *
from average_accumulated_distance import *
import os

# constant
windowsize = 10


# set path 
inputPath = '/home/yunfeng/Downloads/2018/Clark_project/raw_data_csv/'
outputPath = '/home/yunfeng/Downloads/2018/Clark_project/Report_20180205/'
os.chdir(outputPath)

# load data 
df = pd.read_csv(inputPath + '32rep-H4.csv')
targetSnapshots = [380, 3460, 20665, 24290, 36168, 37159, 41421, 43713]


# calculate AAD

for targetsnapshot in targetSnapshots:
	average_accumulated_distances = []
	windowSnapshots = [i for i in range(targetsnapshot-windowsize, targetsnapshot + windowsize)]
	for snapshot in windowSnapshots:
		dfTempt = df[df['Snapshot'] == snapshot]
		points = np.array(dfTempt.iloc[:,2:5])

		rips, m, dgms = generate_rv_complex(points, 3)
		snapshotDistance = average_accumulated_distance(dgms, [0,1,2])
		average_accumulated_distances.append(snapshotDistance)
	# plot result
	fig, axs = plt.subplots(4,1, sharex = True, figsize=(16, 8), dpi=80)
	axs = axs.ravel()
	for i in range(4):
		if i == 3:
			AAD = [average_accumulated_distances[j][0] + average_accumulated_distances[j][1] for j in range(len(average_accumulated_distances))]
		else:
			AAD = [average_accumulated_distances[j][i] for j in range(len(average_accumulated_distances))]
		axs[0].set_title('Snapshot ' +str(targetsnapshot) +'_Average Accumulated Distance for H0, H1, H2 and H0,H1 & H2')
		axs[i].plot(windowSnapshots, AAD, 'g-')
		axs[i].axvline(x=targetsnapshot)
	plt.savefig('snapshot_' +str(targetsnapshot)+' average_accumulated_distances_' + 'step' + str(windowsize)+'.png')

