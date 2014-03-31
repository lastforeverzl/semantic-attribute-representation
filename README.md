semantic-attribute-representation
=================================

In this repository, based on what we have finished so far, we need to extend it to build semantic and attribute representation for our images. Using aYahoo dataset which has 12 categories, wolf, zebra, goat, donkey, monkey, statue of people, centaur, bag, building, jet ski, carriage, and mug, including 2,237 pictures.

##Dependecies:

[OpenCV-Python](http://docs.opencv.org/trunk/doc/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html#py-table-of-content-setup)

[Scipy Library](http://www.scipy.org/scipylib/index.html)

[Numpy] (http://www.numpy.org)

[LIBSVM_3.17](http://www.csie.ntu.edu.tw/~cjlin/libsvm/)

##File Structure:
```
-root/
  |__K20_samples/  			            	  (Samples for k = 20)
  |__K25_samples/           			      (Samples for k = 25)
  |__Multiclasses_K20samples/     			  (Multiclasses sampels for k = 20)
  |__K20_classification_results   			  (12 Binary classification results for k = 20)
  |__Multicategories_classification_reuslts   (Multi-categories classification result)
  |__lib/                         			  (Directory for holding library files)
  |__libsvm-3.17/                 			  (LibSVM algorithm lib)
  |__main.py                     			  (Runnable file)
```

##Running Code:
1. Generate Samples
```
  python main.py
```
2. Running SVM classification
```
  python main.py
```

