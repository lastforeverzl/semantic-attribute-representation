import sys
import os
import time
from subprocess import *
from lib.sample_generator import *

if __name__ == '__main__':

    option = 1
    if len(sys.argv) <= 2 :
        option = input("Generate Samples or do classsification test?\n "\
                     "1-->Generate Samples, 2-->Classification:  ")

    if option == 1:
        now = time.time()

        Category_list = ['building', 'donkey', 'monkey', 'mug', 'centaur', 'bag', 'carriage', 'wolf', 'zebra', 'statue', 'jetski', 'goat']
        #K = 20
        K = input("Input cluster centers K: ")
        K = int(K)

        multi = input("Binary classfication for one category, or multi-categories classification?\n"\
                    "1-->Binary, 2-->multi-categories: ")
        Multi_category = False if int(multi) == 1 else True

        quanti = input("Do hard of soft quantizaiont?\n"\
                    "1-->hard, 2-->soft: ")

        soft_quantization = False if int(quanti) == 1 else True

        images_source = "/Users/minhuigu/Downloads/ayahoo_test_images"
        codebook_path = "./codebook_K%d/"%K
        sample_path = "./samples_K%d/"%K
        pathfile = "./image_path_K%d/"%K
        log_path = "./log_path_K%d/"%K

        from_txt = False
        if Multi_category:
            from_txt = False

        SampleSets = {}
        for each_category in Category_list:
            SampleSets[each_category] = SampleGenerator(each_category,K,images_source,codebook_path,\
                                    sample_path,pathfile,log_path,multi_categories=Multi_category,index=Category_list.index(each_category))
            SampleSets[each_category].load_paths()
            SampleSets[each_category].load_codebook(K,save=True, read_from_txt=from_txt)
            SampleSets[each_category].generate_positive_samples(soft=soft_quantization)
            if not Multi_category:
                SampleSets[each_category].generate_negative_samples([i for i in Category_list if i!= each_category],soft=soft_quantization)

        print "Program finished."

        interval = time.time() - now
        print "Used %s seconds."%interval

    elif option == 2:

        #The code below edited based on the file easy.py in libsvm library.
        #Used to scale, train, predict the samples.

        print('Usage: {0} training_file [testing_file]'.format(sys.argv[0]))

        # svm, grid, and gnuplot executable files

        is_win32 = (sys.platform == 'win32')
        if not is_win32:
            svmscale_exe = "libsvm-3.17/svm-scale"
            svmtrain_exe = "libsvm-3.17/svm-train"
            svmpredict_exe = "libsvm-3.17/svm-predict"
            grid_py = "libsvm-3.17/tools/grid.py"
            gnuplot_exe = "/usr/local/bin/gnuplot"
            #gnuplot_exe = "/usr/local/Cellar/gnuplot/4.6.5/bin/gnuplot"
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


        train_pathname = raw_input("input train file: ")
        assert os.path.exists(train_pathname),"training file not found"
        file_name = os.path.split(train_pathname)[1]
        scaled_file = file_name + ".scale"
        model_file = file_name + ".model"
        range_file = file_name + ".range"

        dotest = input("add test file? 1-->yes, 2-->no: ")

        if int(dotest) == 1:
            test_pathname = raw_input("input test file: ")
            file_name = os.path.split(test_pathname)[1]
            assert os.path.exists(test_pathname),"testing file not found"
            scaled_test_file = file_name + ".scale"
            predict_test_file = file_name + ".predict"

        cmd = '{0} -s "{1}" "{2}" > "{3}"'.format(svmscale_exe, range_file, train_pathname, scaled_file)
        print('****************************')
        print('* Scaling training data... *')
        print('****************************')
        Popen(cmd, shell = True, stdout = PIPE).communicate()

        cmd = '{0} -svmtrain "{1}" -gnuplot "{2}" "{3}"'.format(grid_py, svmtrain_exe, gnuplot_exe, scaled_file)
        print('***********************')
        print('* Cross validation... *')
        print('***********************')
        f = Popen(cmd, shell = True, stdout = PIPE).stdout

        line = ''
        while True:
            last_line = line
            line = f.readline()
            if not line: break
        c,g,rate = map(float,last_line.split())

        print('Best c={0}, g={1} CV rate={2}'.format(c,g,rate))

        cmd = '{0} -c {1} -g {2} "{3}" "{4}"'.format(svmtrain_exe,c,g,scaled_file,model_file)
        print('***************')
        print('* Training... *')
        print('***************')
        Popen(cmd, shell = True, stdout = PIPE).communicate()

        print('Output model: {0}'.format(model_file))
        if len(sys.argv) > 2:
            cmd = '{0} -r "{1}" "{2}" > "{3}"'.format(svmscale_exe, range_file, test_pathname, scaled_test_file)
            print('Scaling testing data...')
            Popen(cmd, shell = True, stdout = PIPE).communicate()

            cmd = '{0} "{1}" "{2}" "{3}"'.format(svmpredict_exe, scaled_test_file, model_file, predict_test_file)
            print('**************')
            print('* Testing... *')
            print('**************')
            Popen(cmd, shell = True).communicate()

            print('Output prediction: {0}'.format(predict_test_file))
    else:
        raise SystemExit
