## import packages 
import numpy as np 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
from scipy.stats import ttest_ind
from operator import *
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os


## constants
step = 0.01


## function
def dist(files):
	PD = []
	for file in files:
		df = np.load(inputPath + file)
		PD.append(df)
	PD = np.array(PD)
	PD = PD.flatten()
	return PD


def betti_ave(files, dim):
	tempdim = np.zeros((5000, 601))
	for file in files:
		temp  = np.load(inputPath + file).item()
		tempkeys = list(temp.keys())
		tempkeys = sorted(tempkeys, key = lambda x: int(x.split('_')[1]))
		tempArray = itemgetter(*tempkeys)(temp)
		tempdist = np.empty((0,601), int)
		for temparray in tempArray:
			temparray = temparray[0][dim]
			temparray[0] = 0
			temparray = np.reshape(temparray, (1, len(temparray)))
			tempdist = np.append(tempdist, temparray, axis = 0)
		tempdim = tempdim + tempdist
	# tempdim = tempdim/len(files)
	return tempdim

# def create_subplot(data, bins, group ,ax=None):
#     if ax is None:
#         ax = plt.gca()
#     ave = np.mean(data)  
#     plot = ax.hist(data, bins, edgecolor = 'k', color = 'y', alpha = 0.5)
#     ax.set_title('Group ' + group + ' pairwise distance')
#     ax.set_xlabel('Bins')
#     ax.set_ylabel('Frequency')
#     ax.axvline(x = ave)
#     ax.text(0.9, 0.9, 'Group ' + group + ' AVe: ' + str(round(ave,4)),
#         horizontalalignment='center',
#         verticalalignment='center',
#         transform=ax.transAxes, bbox={'facecolor':'red', 'alpha':0.5, 'pad':5})
#     return plot


def create_subplot(data, group ,ax=None):
    if ax is None:
        ax = plt.gca()
    plot = ax.matshow(data)
    # ax.colorbar()
    # divider = make_axes_locatable(ax)
    # cax = divider.append_axes("right", size="5%", pad=0.05)
    # ax.colorbar(ax, cax = cax)
    ax.set_title('Group ' + group + ' bettiseq')
    ax.set_xlabel('radius')
    ax.set_ylabel('snapshots')
    return plot



def ttest(data1, data2):
	t, p  = ttest_ind(data1, data2, equal_var = False)
	with open('ttest_report.txt', 'w') as fout:
		fout.write('n1 = ' + str(len(data1)) + '\n')
		fout.write('n2 = ' + str(len(data2)) + '\n')
		fout.write('mean1 = ' + str(np.mean(data1)) + '\n')
		fout.write('mean2 = ' + str(np.mean(data2)) + '\n')
		fout.write('std1 = ' + str(np.std(data1)) + '\n')
		fout.write('std2 = ' + str(np.std(data2)) + '\n')
		fout.write('t = ' + str(t) + '\n')
		fout.write('p = ' + str(p) + '\n')
		if p < 0.01:
			fout.write('Reject the hypothesis that the mean are the same!')
		else:
			fout.write('Fail to reject the hypothesis that the mean are the same!')




## set path 
inputPath = '/san/home/yunfeng.hu/Chemistry/all_64rep_bettiseq_20170714/'
outputPath = '/san/home/yunfeng.hu/Chemistry/'
os.chdir(outputPath)


## load files 
files = os.listdir(inputPath)


## AB Group
filesA = [file for file in files if file.startswith('A')]
filesB = [file for file in files if file.startswith('B')]


PDA = betti_ave(filesA,1)
PDB = betti_ave(filesB,1)

PDAAve = PDA/len(filesA)
PDBAve = PDB/len(filesB)


## plot results
fig, axs = plt.subplots(2,1,figsize = (16,8), dpi=80)
axs = axs.ravel()

create_subplot(PDAAve, 1, axs[0])
create_subplot(PDBAve, 1, axs[1])


plt.tight_layout()
plt.savefig('BettiSeqence' +'.png')



# ===================================================
# PDA = dist(filesA)
# PDB = dist(filesB)

# ## plot graph 
# minbin = min(np.min(PDA), np.min(PDB))
# minbin = np.floor(minbin)
# maxbin = max(np.max(PDA), np.max(PDB))
# maxbin = np.ceil(maxbin)


# bins = np.arange(minbin, maxbin + step, step)

# # plot 
# fig, axs = plt.subplots(2,1,figsize = (16,8), dpi=80)
# axs = axs.ravel()

# create_subplot(PDA, bins, 'A', ax = axs[0])
# axs[1] = create_subplot(PDB, bins, 'B', ax=axs[1])


# plt.tight_layout()
# plt.savefig('PairwiseDistanceHistogram'+'.png')


# ## print result 
# ttest(PDA, PDB)