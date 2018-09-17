## import packages 
import pandas as pd
import numpy as np  
import os 
from scipy.fftpack import rfft, fft, fftfreq
import datetime
import matplotlib.pyplot as plt
plt.style.use('ggplot')

## constants
date = datetime.datetime.today().strftime('%Y%m%d')
maxNum = 3


## functions 
def fft_abs(Array, NumberofSnaps = 40, Step =1, MaxNum = maxNum):
	snaps = np.linspace(0, NumberofSnaps*Step -Step, NumberofSnaps)
	snaps_f = np.linspace(0.0, 1.0/(2.0*Step), NumberofSnaps/2)
	wassersteinDist = fft(Array)
	amplitude = 2/NumberofSnaps*np.abs(wassersteinDist[:NumberofSnaps//2])
	amplitudeSorted = sorted(amplitude)
	amplitudeSelected = amplitudeSorted[-MaxNum]
	frequencySelected =  snaps_f[amplitude.argsort()[-MaxNum:][::-1]][MaxNum-1]
	return np.array([amplitudeSelected, frequencySelected])



## set path
inputPath = '/home/yunfeng/Desktop/test/'
outputPath = '/home/yunfeng/Desktop/test/Fourier_Analysis/'
os.chdir(outputPath)


## load files 
PT = np.load(inputPath + 'PT_Wasserstein_20180909.npy')
Inactive = np.load(inputPath + 'Inactive_Wasserstein_20180909.npy')


## Fourier Transform Coefficient
# Number of snapshots 
N = 40

# sample spacing 
T = 1

## create Fourier Coordinates 2nd (Amplitute, Frequency)
for maxNum in range(np.shape(PT)[1]):
	PTFourier = np.apply_along_axis(fft_abs, 1, PT, MaxNum = maxNum)
	InactiveFourier = np.apply_along_axis(fft_abs, 1, Inactive, MaxNum = maxNum)


	# np.save('PTFourier_%s.npy' % date, PTFourier)
	# np.save('InactiveFourier_%s.npy' % date, InactiveFourier)


	## plot result
	fig, ax = plt.subplots(figsize = (16,8), dpi = 80)
	ax.plot(PTFourier[:,0], PTFourier[:,1],'ro', label = 'PTFourier')
	ax.plot(InactiveFourier[:,0], InactiveFourier[:,1], 'bx', label = 'InactiveFourier')
	ax.set_xlabel('%s Largest Amplitude' % maxNum)
	ax.set_ylabel('Corresponding Frequency')
	ax.set_title('Fourier Transform MaxNum = %s' % maxNum)
	ax.legend()

	plt.tight_layout()
	plt.savefig('Fourier_maxnum_%s_%s.png' % (maxNum, date))



# # bins end points and wasserstein distance
# snaps = np.linspace(0, N*T-T, N)
# wasserstein1 = PT[0]
# wasserstein2 = Inactive[0]

# ## Fourier Series fit 
# snaps_f = np.linspace(0.0, 1.0/(2.0*T), N/2)
# wasserstein1_f = fft(wasserstein1)
# wasserstein2_f = fft(wasserstein2)

# # plot result
# fig, ax = plt.subplots(2,1,figsize = (16,8), dpi = 80)
# ax = ax.ravel()


# ax[0].plot(snaps, wasserstein1, label = 'PT')
# ax[0].plot(snaps, wasserstein2, label = 'Inactive')
# ax[0].set_xlabel('Adjacent Snaps Index')
# ax[0].set_ylabel('Wasserstein Distance')
# ax[0].set_title('Adjacent Wasserstein Distance')
# ax[0].legend()

# ax[1].plot(snaps_f, 2.0/N * np.abs(wasserstein1_f[:N//2]), label = 'PT')
# ax[1].plot(snaps_f, 2.0/N * np.abs(wasserstein2_f[:N//2]), label = 'Inactive')
# ax[1].legend()
# ax[1].set_xlabel('Frequency')
# ax[1].set_ylabel('Amplitude')
# ax[1].set_title('Fourier Transform')
# plt.tight_layout()
# plt.show()

# a1 = 2/N*np.abs(wasserstein1_f[:N//2])
# b1 = sorted(a1)
# a2 = 2/N*np.abs(wasserstein2_f[:N//2])
# b2 = sorted(a2)
# print ('Second maximum amplitude: %.2f. The corresponding frequency is %f' % (b1[-2],snaps_f[a1.argsort()[-2:][::-1]][1]))
# print ('Second maximum amplitude: %.2f. The corresponding frequency is %f' % (b2[-2],snaps_f[a2.argsort()[-2:][::-1]][1]))



