import os

inputPath = '/san/home/yunfeng.hu/Chemistry/all_64rep_csv/'
outputPath = '/san/home/yunfeng.hu/Chemistry/PythonCode/'
os.chdir(outputPath)


files = os.listdir(inputPath)



with open('barcode.sub', 'w') as fin:
	fin.write('EXECUTABLE = /usr/bin/python3\n')
	fin.write('UNIVERSE = Vanilla\n')
	fin.write('SHOULD_TRANSFER_FILES = If_needed\n')
	fin.write('WHEN_TO_TRANSFER_OUTPUT = On_Exit\n')
	fin.write('getenv = True\n')
	for file in files:
		fin.write('ARGUMENTS = /san/home/yunfeng.hu/Chemistry/PythonCode/barcode_generator_file.py --inputPath ' + inputPath + ' --outputPath /san/home/yunfeng.hu/Chemistry/all_64rep_barcode_20170714/ --inputFile ' + file +'\n')
		fin.write('OUTPUT = condor_test.out\n')
		fin.write('ERROR = condor_test.err\n')
		fin.write('stream_error = True\n')
		fin.write('request_memory = 50\n')
		fin.write('stream_output = True\n')
		fin.write('Queue\n')
		fin.write('\n')

fin.close()