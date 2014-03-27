import sys
import os
import time
from subprocess import *
from sample_generator import *


if __name__ == '__main__':

    now = time.time()
    
    #Category_list = ['building']
    Category_list = ['building', 'donkey', 'monkey', 'mug', 'centaur', 'bag', 'carriage', 'wolf', 'zebra', 'statue', 'jetski', 'goat']
    K = 25
    
    interval2 = time.time() - now
    print "Used %s seconds."%interval2
    
    images_source = "/Users/minhuigu/Downloads/ayahoo_test_images"
    
    codebook_path = "./codebooks_K%d/"%K
    sample_path = "./samples_K%d/"%K
    pathfile = "./images_K%d/"%K
    log_path = "./logs_K%d/"%K
    
    
    SampleSets = {}
    for each_category in Category_list: 
        SampleSets[each_category] = SampleGenerator(each_category,K,images_source,codebook_path,sample_path,pathfile,log_path)
        SampleSets[each_category].load_paths()
        SampleSets[each_category].load_codebook(K,save=True, read_from_txt=True)
        SampleSets[each_category].generate_positive_samples(soft=False)
        SampleSets[each_category].generate_negative_samples([i for i in Category_list if i!= each_category],soft=False)
   
    print "Program finished."
    interval = time.time() - now
    print "Used %s seconds."%interval

    # The code below edited based on the file easy.py in libsvm library.
    # Used to scale, train, predict the samples.

    if len(sys.argv) <= 1:
    print('Usage: {0} training_file [testing_file]'.format(sys.argv[0]))
    raise SystemExit

    # svm, grid, and gnuplot executable files

    is_win32 = (sys.platform == 'win32')
    if not is_win32:
        svmscale_exe = "libsvm-3.17/svm-scale"
        svmtrain_exe = "libsvm-3.17/svm-train"
        svmpredict_exe = "libsvm-3.17/svm-predict"
        grid_py = "libsvm-3.17/tools/grid.py"
        gnuplot_exe = "/usr/local/Cellar/gnuplot/4.6.5/bin/gnuplot"
    else:
        # example for windows
        svmscale_exe = r"libsvm-3.17\windows\svm-scale.exe"
        svmtrain_exe = r"libsvm-3.17\windows\svm-train.exe"
        svmpredict_exe = r"libsvm-3.17\windows\svm-predict.exe"
        gnuplot_exe = r"c:\tmp\gnuplot\binary\pgnuplot.exe"
        grid_py = r"libsvm-3.17\tools\grid.py"

    assert os.path.exists(svmscale_exe),"svm-scale executable not found"
    assert os.path.exists(svmtrain_exe),"svm-train executable not found"
    assert os.path.exists(svmpredict_exe),"svm-predict executable not found"
    assert os.path.exists(gnuplot_exe),"gnuplot executable not found"
    assert os.path.exists(grid_py),"grid.py not found"

    train_pathname = sys.argv[1]
    assert os.path.exists(train_pathname),"training file not found"
    file_name = os.path.split(train_pathname)[1]
    scaled_file = file_name + ".scale"
    model_file = file_name + ".model"
    range_file = file_name + ".range"

    if len(sys.argv) > 2:
        test_pathname = sys.argv[2]
        file_name = os.path.split(test_pathname)[1]
        assert os.path.exists(test_pathname),"testing file not found"
        scaled_test_file = file_name + ".scale"
        predict_test_file = file_name + ".predict"

    cmd = '{0} -s "{1}" "{2}" > "{3}"'.format(svmscale_exe, range_file, train_pathname, scaled_file)
    print('Scaling training data...')
    Popen(cmd, shell = True, stdout = PIPE).communicate()   

    cmd = '{0} -svmtrain "{1}" -gnuplot "{2}" "{3}"'.format(grid_py, svmtrain_exe, gnuplot_exe, scaled_file)
    print('Cross validation...')
    f = Popen(cmd, shell = True, stdout = PIPE).stdout

    line = ''
    while True:
        last_line = line
        line = f.readline()
        if not line: break
    c,g,rate = map(float,last_line.split())

    print('Best c={0}, g={1} CV rate={2}'.format(c,g,rate))

    cmd = '{0} -c {1} -g {2} "{3}" "{4}"'.format(svmtrain_exe,c,g,scaled_file,model_file)
    print('Training...')
    Popen(cmd, shell = True, stdout = PIPE).communicate()

    print('Output model: {0}'.format(model_file))
    if len(sys.argv) > 2:
        cmd = '{0} -r "{1}" "{2}" > "{3}"'.format(svmscale_exe, range_file, test_pathname, scaled_test_file)
        print('Scaling testing data...')
        Popen(cmd, shell = True, stdout = PIPE).communicate()   

        cmd = '{0} "{1}" "{2}" "{3}"'.format(svmpredict_exe, scaled_test_file, model_file, predict_test_file)
        print('Testing...')
        Popen(cmd, shell = True).communicate()  

        print('Output prediction: {0}'.format(predict_test_file))

