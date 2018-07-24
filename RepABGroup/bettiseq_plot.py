## import packages 
import pandas as pd 
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
from matplotlib.patches import Circle, Wedge, Polygon, Ellipse
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import matplotlib.patches as matpatches
import matplotlib.patheffects as PathEffects
import numpy as np 
import os 


## set path 
outputPath = '/san/home/yunfeng.hu/CareerPathWayCH/Report_20180723_Classification/'
os.chdir(outputPath)

## laod data 
GroupAAVe = np.load('/san/home/yunfeng.hu/CareerPathWayCH/filesAAve.npy')
GroupBAve = np.load('/san/home/yunfeng.hu/CareerPathWayCH/filesBAve.npy')


## draw mat show

fig, axes = plt.subplots(nrows=1, ncols=2)
axes = axes.ravel()

im = axes[0].imshow(GroupAAVe, vmin= 0, vmax = 1)
axes[0].set_title('GroupA_Ave BettiSequence')
im = axes[1].imshow(GroupBAve, vmin = 0, vmax= 1)
axes[1].set_title('GroupB_Ave BettiSequence')


fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
fig.colorbar(im, cax=cbar_ax)

plt.savefig('GroupAB_Ave_BettiSequence.png')