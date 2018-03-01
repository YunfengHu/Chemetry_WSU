## import packages 
import pandas as pd 
import os 
import matplotlib.pyplot as plt 


## functions 
def create_subplot(data, ax=None):
    if ax is None:
        ax = plt.gca()
    bp = ax.scatter(data[:,0], data[:,1])
    return bp




def create_barcode(DataFrameBD, Cutoff, ax = None):
	if ax is None:
		ax = plt.gca()
	lines = []
	for j in range(len(DataFrameBD)):
		lines.append((DataFrameBD['Birth'].iloc[j],DataFrameBD['Death'].iloc[j]))
		lines.append((j,j)) 
		lines.append('r')
	ax.set_title('H' + str(df['Hindex'].iloc[0]) +'_' + str(df['Snapshot'].iloc[0])  + 'Persistent Barcode')
	ax.plot(*lines)
	barcode = ax.axvline(x=cutoff)
	return barcode


def create_scatter(DataFrameBD, Cutoff, ax = None):
	if ax is None:
		ax = plt.gca()
	DataFrameBD['Persistence'] = DataFrameBD['Death'] - DataFrameBD['Birth']
	ax.set_title('H' + str(df['Hindex'].iloc[0]) +'_' + str(df['Snapshot'].iloc[0])  + 'Birth Persistent Plot')
	ax.scatter(DataFrameBD['Birth'], DataFrameBD['Persistence'])
	scatter = ax.axvline(x=cutoff)
	return scatter



## set path 
inputPath = '/home/yunfeng/Downloads/2018/Clark_project/Report_Statistical_Result_20180226/StableAtomBarcodeFile/'
outputPath = '/home/yunfeng/Downloads/2018/Clark_project/Report_Statistical_Result_20180305/'
os.chdir(outputPath)


## load files 
files = os.listdir(inputPath)
df = pd.read_csv(inputPath + files[0])
df = df[(df['Snapshot'] == 56093) & df['Dimension'] == 1]
cutoff = df['Cutoff'].iloc[0]



## plot result
fig, axs = plt.subplots(1,2, figsize=(16, 8), dpi=80)
axs = axs.ravel()
axs[0] = create_barcode(df, cutoff, axs[0])
axs[1] = create_scatter(df, cutoff, axs[1])
plt.show()

