import numpy as np 
from numpy import inf
import matplotlib.pyplot as plt 

def change_inf_to_2nd_largest(List, ReplaceValue):
	listcopy = List.copy()
	listcopy = list(set(listcopy))
	listcopy.sort()
	List = np.array(List)
	# List[List == inf] = listcopy[-2]
	List[List == inf] = ReplaceValue
	return List


def plot_persistent_barcode(Diagrams, cutoff, Savefile, H = 'H1'):
	color = ['r', 'g', 'b']
	if H == 'H1':
		Range = range(1,2)
	elif H == 'Both':
		Range = range(2)
	elif H == 'All':
		Range = range(3)
	plt.figure()
	j = 0
	for i in Range:
		x=[]
		y=[]
		for pt in Diagrams[i]:
			x.append(pt.birth)
			y.append(j)
			x.append(pt.death)
			y.append(j)
			j = j +1
		x = change_inf_to_2nd_largest(x,1)
		pair_x_array = np.reshape(x, (-1, 2))
		pair_y_array = np.reshape(y, (-1, 2))
		for k, pair_x in enumerate(pair_x_array):
			pair_y = pair_y_array[k]
			plt.plot(pair_x, pair_y,linewidth = 3, color = color[i])
	plt.axvline(x=cutoff)
	plt.title('Persistant Barcode')
	plt.savefig(Savefile)
