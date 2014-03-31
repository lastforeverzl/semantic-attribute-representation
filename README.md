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
  |__K20_outputs/                 (Outputs for k = 20)
  |__K25_outputs/                 (Outputs for k = 25)
  |__Multiclasses_output_K20/     (Multiclasses outputs for k = 20)
  |__lib/                         (Directory for holding library files)
  |__libsvm-3.17/                 (LibSVM algorithm lib)
  |__main.py                      (Runnable file)
```

##Running Code:
1. Generate Samples
```
  python main.py
```
2. Running SVM classification
```
  python main.py training_file [testing_file]
```

