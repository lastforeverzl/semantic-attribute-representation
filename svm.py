import cv2
import numpy as np
import re

class SVM():
	'''wrapper for OpenCV SimpleVectorMachine algorithm'''
	def __init__(self, filename):
		self.model = cv2.SVM()

		input_file = []
		training_Data = []
		label_data = []

		with open(filename) as inputfile:
			for line in inputfile:
				input_file.append(line.strip().split(' '))

		for elem in input_file:
			label_data.append(int(elem.pop(0)))
			temp = []
			for s in elem:
				s = s.split(':')[1]
				temp.append(int(s))
			training_Data.append(temp)

		self._samples = np.array(training_Data, dtype = np.float32)
		self._responses = np.array(label_data, dtype = np.float32)

	def train(self):
		#setting algorithm parameters
		params = dict( kernel_type = cv2.SVM_LINEAR, svm_type = cv2.SVM_C_SVC, C = 1 )
		self.model.train(self._samples, self._responses, None, None, params = params)

	def predict(self):
		return np.float32( [self.model.predict(s) for s in self._samples])



