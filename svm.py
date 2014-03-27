import cv2
import numpy as np

class SVM():
    """SVM algorithm based on opencv CvSVM

    Wrapper for OpenCV SimpleVectorMachine algorithm

    Attributes:
        directory: the path of one category folder.
        model: SVM implementation based on OpenCV
        _samples: training data.
        _responses: label data.
    """gi

    def __init__(self, directory):
        """Inits SVM class according to given directory"""
        self.model = cv2.SVM()

        input_file = []
        training_Data = []
        label_data = []

        with open(directory) as inputfile:
            for line in inputfile:
                input_file.append(line.strip().split(' '))

        for elem in input_file:
            label_data.append(int(elem.pop(0)))
            temp = []
            for s in elem:
                temp.append(int(s.split(':')[1]))
            training_Data.append(temp)

        self._samples = np.array(training_Data, dtype = np.float32)
        self._responses = np.array(label_data, dtype = np.float32)

    def train(self):
        """
        Trains an SVM

        SVM params:
            params.svm_type    = CvSVM::C_SVC
            params.kernel_type = CvSVM::RBF
            params.C: regulates to optimal value according to the samples and the result, 
                        (0.00001， 0.001， 0.01， 0.1， 1， 10， 100， 1000， 5000)
        """
        params = dict( kernel_type = cv2.SVM_RBF, svm_type = cv2.SVM_C_SVC, C = 0.125 )
        self.model.train(self._samples, self._responses, None, None, params = params)

    def predict(self):
        """Predicts the response for input samples"""
        return np.float32( [self.model.predict(s) for s in self._samples])



