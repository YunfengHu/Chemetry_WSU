import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt 
import numpy as np 
import os
import datetime


## constants
date = datetime.datetime.today().strftime('%Y%m%d')

amplify = 10
cut = 0.119



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



## plot 
fig, axs = plt.subplots(2,1,figsize = (16,8), dpi = 80, sharex = True)
axs = axs.ravel()

x_axis = range(40) 
for pt in range(len(PT)):
	axs[0].plot(x_axis, PT[pt], 'b-')


for inactive in range(len(Inactive)):
	axs[1].plot(x_axis, Inactive[inactive], 'r-')


# axs[2].plot(x_axis, np.mean(PT, 0), 'b-', label = 'PT')
# axs[2].plot(x_axis, np.mean(Inactive,0), 'r-', label = 'Inactive')
# axs[2].plot(x_axis, [0.119]*len(x_axis), 'y-', label = 'seperation' )
# axs[2].set_title('Ave_Wasserstein')
# axs[2].legend()
plt.savefig('Adjacent_Wasserstein_new_' + date+'.png')



# # ===============================
# import matplotlib
# matplotlib.use("Agg")
# from matplotlib.pyplot as plt 


# plt.figure()
# plt.imshow(PT.T)
# plt.axes().set_aspect('equal')
# plt.savefig('Adjacent_PT_Wasserstein_20180909.png')


# plt.figure()
# plt.imshow(Inactive.T)
# plt.autoscale()
# plt.savefig('Adjacent_Inactive_Wasserstein_20180909.png')



