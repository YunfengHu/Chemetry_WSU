import pandas as pd 
import os 
import numpy as np
import csv 


inputPath = '/home/yunfeng/Downloads/2018/Clark_project/Report_20180212/Zundel-to-Eigen-PTs/'
outputPath = '/home/yunfeng/Downloads/2018/Clark_project/Report_20180212/Zundel-to-Eigen-PT/'
os.chdir(outputPath)

excelFiles = pd.ExcelFile('/home/yunfeng/Downloads/2018/Clark_project/Report_20180212/' + 'H106_20_succ_PTs_150_timewindow.xlsx')

sheetNames = excelFiles.sheet_names
sheetNames = [sheetname for sheetname in sheetNames if sheetname.startswith('PT')]
targetSnapshots = [sheetname.split('_')[0] for sheetname in sheetNames]
targetSnapshots = [int(targetsnapshot.split('-')[1]) for targetsnapshot in targetSnapshots]

dfAllBeads = pd.DataFrame()
dfSomeBeads = pd.DataFrame()
for sheetname, targetsnapshot in zip(sheetNames, targetSnapshots):
	df = excelFiles.parse(sheetname)
	indices = list(df['Unnamed: 1'])
	indexNaN = indices.index(np.nan)
	indexType = indices.index('Type')
	dfFull =  df.iloc[0:indexNaN, :]
	headerFull = dfFull.iloc[0]
	dfFull = dfFull[1:]
	dfFull.columns = headerFull
	dfFull = dfFull.dropna(axis=1, how='all')
	dfFull['target_snapshot'] = [targetsnapshot for i in range(len(dfFull))]
	dfAllBeads = dfAllBeads.append(dfFull, ignore_index = True)
	dfBeads = df.iloc[indexType:, :]
	headerBeads = dfBeads.iloc[0]
	dfBeads = dfBeads[1:]
	dfBeads.columns = headerBeads
	dfBeads = dfBeads.dropna(axis=0, how='any')
	dfBeads['target_snapshot'] = [targetsnapshot for i in range(len(dfBeads))]
	dfSomeBeads = dfSomeBeads.append(dfBeads, ignore_index = True)
