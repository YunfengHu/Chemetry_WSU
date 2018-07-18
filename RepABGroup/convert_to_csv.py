# this is used to convert the data in the csv file 
import argparse
import csv 
import os 


## set path
inputPath = '/san/home/yunfeng.hu/Chemistry/all-64rep-xyz/'
outputPath = '/san/home/yunfeng.hu/Chemistry/all_64rep_csv/'
os.chdir(outputPath)



## load file 
files = os.listdir(inputPath)
for file in files:
	with open(inputPath + file, 'r') as fin:
		with open(outputPath + file.replace('xyz', 'csv'), 'w') as fout:
			csv.writer(fout).writerow(['Index', 'Type', 'x', 'y', 'z', 'Snapshot', 'Order'])
			index = file.split('-')[1]
			index = index.strip('.xyz')
			index = index[1:]
			reader = csv.reader(fin, delimiter = ' ')
			lines = fin.readlines()
			j = 0
			order = 1
			for line in lines:
				line = line.strip('\n')
				line = line.split(' ')
				line = list(filter(None, line))
				if len(line) == 1:
					continue
				elif len(line) == 2:
					snapshot = line[1]
				else:
					tempt = [index]
					tempt.extend(line)
					tempt.append(snapshot)
					tempt.append(order)
					order = (order +1)%64
					if order ==0:
						order = 64
					csv.writer(fout).writerow(tempt)






	# j = 0
	# reader = csv.reader(fin, delimiter = ' ')
	# lines = fin.readlines()
	# for line in lines:

	# 	if len(line) ==0:
	# 		continue

	# 	print (line)
	# 	j = j+1
	# 	if j >=10: break


# def main():
# 	parser = argparse.ArgumentParser()
# 	parser.add_argument('--inputPath')
# 	parser.add_argument('--outputPath')
# 	args = parser.parse_args()

# 	os.chdir(args.outputPath)
# 	files = os.listdir(args.inputPath)
# 	outFiles = [file.replace('xyz', 'csv') for file in files]

# 	for infile, outfile in zip(files, outFiles):
# 		with open(args.inputPath+infile, 'r') as fin:
# 			reader = csv.reader(fin, delimiter = ' ')
# 			with open(args.outputPath + outfile, 'w') as fout:
# 				csv.writer(fout).writerow(['Index', 'Type', 'x', 'y', 'z', 'Snapshot', 'Order'])
# 				# lines = [next(reader) for i in range(50)]
# 				j = 1
# 				# for line in lines:
# 				for line in reader:
# 					tempt = list(filter(None, line))
# 					if len(tempt) == 0:
# 						continue
# 					if (tempt[0] == '32') & (len(tempt) == 1):
# 						continue 
# 					if tempt[0] == '#snapshot':
# 						i = tempt[1]
# 					else:
# 						if j%32!=0:
# 							tempt.extend([i,j%32])
# 						else:
# 							tempt.extend([i, 32])
# 						csv.writer(fout).writerow(tempt)
# 						j = j + 1

# if (__name__ == '__main__'):
# 	main()