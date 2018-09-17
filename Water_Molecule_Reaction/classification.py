## import packages 
import numpy as np 
import os 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import datetime

## constants
date = datetime.datetime.today().strftime('%Y%m%d')

x = 15
y = 25
cut = 0.119
amplify = 10
shrink = 1/amplify


## functions 
def amplify_arr(Array,Amplify, Cut):
	arr = np.zeros(np.shape(Array))
	arr[Array>=Cut] = Amplify
	arr[Array<=Cut] = 1/Amplify
	arr = np.multiply(arr, Array)
	return arr

## set path 
inputPath  = '/home/yunfeng/Desktop/test/'
outputPath = '/home/yunfeng/Desktop/test/'
os.chdir(outputPath)


## load data 
PT = np.load(inputPath + 'PT_Wasserstein_20180909.npy')
Inactive = np.load(inputPath + 'Inactive_Wasserstein_20180909.npy')


## amplify cut 
PT = amplify_arr(PT, amplify, cut)
Inactive = amplify_arr(Inactive, amplify, cut)
 

## divide into 3 parts 
# PT
PT_x = PT[:,0:x]
PT_y = PT[:,x:y]
PT_z = PT[:,y:]

# Inactive 
Inactive_x = Inactive[:, 0:x]
Inactive_y = Inactive[:, x:y]
Inactive_z = Inactive[:, y:]


## Average 
PT_x = np.mean(PT_x,1)
PT_y = np.mean(PT_y,1)
PT_z = np.mean(PT_z,1)
PT_cor = np.array([PT_x, PT_y, PT_z]).T


Inactive_x = np.mean(Inactive_x,1)
Inactive_y = np.mean(Inactive_y,1)
Inactive_z = np.mean(Inactive_z,1)
Inactive_cor = np.array([Inactive_x, Inactive_y, Inactive_z]).T


## plot 3d scatter 
fig = plt.figure(figsize = (16,8), dpi = 80)
ax = fig.add_subplot(111, projection='3d')

ax.scatter(PT_x, PT_y, PT_z, c='r', marker='o',label = 'PT')
ax.scatter(Inactive_x, Inactive_y, Inactive_z, c='b', marker='x', label = 'Inactive')

ax.set_title('3D Scatter Plot')
ax.set_xlabel('0-14 Diff Mean')
ax.set_ylabel('15-25 Diff Mean')
ax.set_ylabel('25-40 Diff Mean')
plt.legend()
plt.show()
# plt.savefig('3D_Scatter_Plot_Origin_Diff_' + date+'.png')