# packages
import argparse
import pandas as pd 
import os 
import math




# functions 
def r3_distance(x1,x2,x3,y1,y2,y3):
	return math.sqrt(math.pow(x1-y1,2) + math.pow(x2-y2,2) + math.pow(x3-y3,2))



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--inputPath")
	parser.add_argument("--outputPath")
	args = parser.parse_args()


	os.chdir(args.outputPath)
	files = os.listdir(args.inputPath)
	newfiles = [file.replace('.csv', '_centers.csv') for file in files]

	# centroid and mean 
	for i in range(len(files)):
		print (i)
		df = pd.read_csv(args.inputPath + files[i])
		df['xMean'] = df['x'].groupby(df['Snapshot']).transform('mean')
		df['yMean'] = df['y'].groupby(df['Snapshot']).transform('mean')
		df['zMean'] = df['z'].groupby(df['Snapshot']).transform('mean')
		# calculate the distance from points to centers
		df['distanceToCenters'] = df.apply(lambda x: r3_distance(x['x'], x['y'], x['z'], x['xMean'], x['yMean'], x['zMean']), axis = 1)
		df = df[['Index', 'Type', 'x', 'y', 'z', 'Snapshot', 'Order', 'distanceToCenters']]
		df.to_csv(newfiles[i], index = False)


if (__name__ == '__main__'):
	main()

# # plot histogram 
# x = list(df['distanceToCenters'])
# num_bins = 100
# n, bins, patches = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)
# plt.show()

