import csv 
import os 

files = os.listdir('/home/yunfeng/Downloads/20k-data-for-YF')
outFiles = [file.replace('xyz', 'csv') for file in files]

for infile, outfile in zip(files, outFiles):
	with open('/home/yunfeng/Downloads/20k-data-for-YF/'+infile, 'r') as fin:
		reader = csv.reader(fin, delimiter = ' ')
		with open('/home/yunfeng/Downloads/Chemistry_Data/' + outfile, 'w') as fout:
			csv.writer(fout).writerow(['Index', 'Type', 'x', 'y', 'z', 'Snapshot', 'Order'])
			# lines = [next(reader) for i in range(50)]
			j = 1
			# for line in lines:
			for line in reader:
				tempt = list(filter(None, line))
				if len(tempt) == 0:
					continue
				if tempt[0] == '32':
					continue 
				if tempt[0] == '#snapshot':
					i = tempt[1]
				else:
					if j%32!=0:
						tempt.extend([i,j%32])
					else:
						tempt.extend([i, 32])
					csv.writer(fout).writerow(tempt)
					j = j + 1
