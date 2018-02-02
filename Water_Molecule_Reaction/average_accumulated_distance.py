import numpy as np 
def average_accumulated_distance(DGMS, Selection):
	average_accumulated_distance = []
	for i in Selection:
		dgm = DGMS[i]
		tempt_distances = 0
		for pt in dgm:
			if pt.death == np.inf:
				continue
			else:
				tempt_distances =tempt_distances + pt.death - pt.birth
			# tempt_distances = tempt_distances/len(dgm)
			tempt_distances = tempt_distances/len(dgm)
		average_accumulated_distance.append(tempt_distances)
	return average_accumulated_distance