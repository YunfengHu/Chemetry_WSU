## import packages 
from sklearn import svm 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle
import numpy as np 
import os 

## functions 
def split_data(Data, TrainRatio, Shuffle = 'No'):
	if Shuffle == 'No':
		data = Data
	elif Shuffle == 'Yes':
		data = shuffle(Data, random_state = 0)
	trainLength = int(np.ceil(len(data)*TrainRatio))
	testLength = int(np.ceil((len(data) - trainLength)/2))
	train = data[0:trainLength]
	validation = data[trainLength: trainLength+ testLength]
	test = data[trainLength+ testLength:]
	return train, validation, test



def pred_accuracy(Label1, Label2):
	return sum(Label1 == Label2)/len(Label1)




## set path 
inputPath = '/san/home/yunfeng.hu/CareerPathWayCH/'
outputPath = '/san/home/yunfeng.hu/CareerPathWayCH/Classification/'
os.chdir(outputPath)



## load files 
GroupA = np.load('/san/home/yunfeng.hu/CareerPathWayCH/filesAAve.npy')
GroupB = np.load('/san/home/yunfeng.hu/CareerPathWayCH/filesBAve.npy')


## split data into training, cross validation and testing 

# split data
GroupATrain, GroupAVal, GroupATest = split_data(GroupA, 0.6, Shuffle = 'Yes')
GroupBTrain, GroupBVal, GroupBTest = split_data(GroupB, 0.6, Shuffle = 'Yes')

# combine data
Train = np.concatenate((GroupATrain, GroupBTrain), axis = 0)
Validation = np.concatenate((GroupAVal, GroupBVal), axis = 0)
Test = np.concatenate((GroupATest, GroupBTest), axis = 0)


# set labels
TrainLabel = np.array([0]*len(GroupATrain) + [1]*len(GroupBTrain))
ValidationLabel = np.array([0]*len(GroupAVal) + [1]*len(GroupBVal))
TestLabel = np.array([0]*len(GroupATest) + [1]*len(GroupBTest))

## Classification 
# SVM

# fit model
clf = svm.SVC(kernel = 'linear')
model = clf.fit(Train, TrainLabel)
coef = model.coef_[0]
supportVectors = clf.support_vectors_  # vectors determine the margin
intercept = clf.intercept_

# validate
validationLabel = clf.predict(Validation)
validationAccuracy = pred_accuracy(ValidationLabel, validationLabel)

# fun test 
validationSign = np.dot(Validation, coef) + intercept

# test 
testLabel = clf.predict(Test)
testAccuracy = pred_accuracy(TestLabel, testLabel)


# k nearest neighbors 

# fit model
neigh = KNeighborsClassifier(n_neighbors=2)
mdoel = neigh.fit(Train, TrainLabel) 

# validate
validationLabel = neigh.predict(Validation)
validationAccuracy = pred_accuracy(ValidationLabel, validationLabel)


# test 
testLabel = clf.predict(Test)
testAccuracy = pred_accuracy(TestLabel, testLabel)


# Logistic Regression

# fit model
lg = LogisticRegression()
model = lg.fit(Train, TrainLabel)
coef = lg.coef_
intercept = lg.intercept_

# validate
validationLabel = lg.predict(Validation)
validationAccuracy = pred_accuracy(ValidationLabel, validationLabel)


# test 
testLabel = lg.predict(Test)
testAccuracy = pred_accuracy(TestLabel, testLabel)