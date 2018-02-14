import pandas as pd 
import os
import matplotlib.pyplot as plt 


# constants 
width = 0.25

inputPath = '/home/yunfeng/Downloads/2018/Clark_project/Report_20180212/Barcode_Generator/'
outputPath = '/home/yunfeng/Downloads/2018/Clark_project/Report_20180212/Barcode_Cyclelength/'
os.chdir(outputPath)

files = os.listdir(inputPath)

for file in files:
	print (file)
	dfTempt = pd.read_csv(inputPath + file)
	snapshots = dfTempt['Snapshot'].unique()
	for snapshot in snapshots:
		fig, axs = plt.subplots(2,1, figsize=(16, 8), dpi=80)
		axs = axs.ravel()
		# generate barcode 
		colors = {0:'g', 1:'r', 2: 'b'}
		dfSnapshotTempt = dfTempt[dfTempt['Snapshot'] == snapshot]
		dimensions = [0,1,2]
		cutoff = dfSnapshotTempt['Cutoff'].iloc[0]
		dfCyclesLength = dfSnapshotTempt.groupby(['Dimension','Flag']).size().reset_index(name = 'counts')
		FullList = [[0, 0], [0, 1], [1, 0], [1, 1], [2,0], [2, 1]]
		dfCyclesLengthList = [[dim,flag] for dim, flag in zip(dfCyclesLength['Dimension'], dfCyclesLength['Flag'])]
		MissingList = [item for item in FullList if item not in dfCyclesLengthList]
		for missing in MissingList:
			dfCyclesLength=dfCyclesLength.append({'Dimension':missing[0], 'Flag':missing[1], 'counts':0}, ignore_index=True)
		lines = []
		for i in range(len(dfSnapshotTempt)):
			lines.append((dfSnapshotTempt['Birth'].iloc[i],dfSnapshotTempt['Death'].iloc[i]))
			lines.append((i,i)) 
			if dfSnapshotTempt['Flag'].iloc[i] == 1:
				lines.append(colors[dfSnapshotTempt['Dimension'].iloc[i]])
			else:
				lines.append('k')
		axs[0].set_title('Persistent Barcode for '+ str(snapshot))
		axs[0].plot(*lines)
		axs[0].axvline(x=cutoff)
		pos = dimensions
		for i in range(2):
			axs[1].bar([p + i*width for p in pos], 
		    #using df['pre_score'] data,
		    dfCyclesLength[dfCyclesLength['Flag']==i]['counts'], 
		    # of width
		    width, 
		    # with alpha 0.5
		    alpha=0.5, 
		    # with color
		    color=colors[i], 
		    # with label the first value in first_name
		    label='H' + str(i))
		axs[1].set_ylabel('Counts')
		axs[1].set_title('Long v.s. Short Cyles in Each Group')
		axs[1].set_xticks([p+width*0.5 for p in pos])
		axs[1].set_xticklabels(['H'+ str(i) for i in range(len(pos))])
		axs[1].legend(['Long', 'Short'], loc='upper left')
		plt.savefig('Persistent Barcode for '+ str(snapshot))
		plt.close(fig)




