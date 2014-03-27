from sample_generator import *

if __name__ == '__main__':

    #Category_list = ['building']
    Category_list = ['building', 'donkey', 'monkey', 'mug', 'centaur', 'bag', 'carriage', 'wolf', 'zebra', 'statue', 'jetski', 'goat']
    K = 25
    
    images_source = "/Users/minhuigu/Downloads/ayahoo_test_images"
    
    codebook_path = "./codebook_K%d/"%K
    sample_path = "./samples_K%d/"%K
    pathfile = "./image_path_K%d/"%K
    log_path = "./log_path_K%d/"%K
    
    
    SampleSets = {}
    for each_category in Category_list: 
        SampleSets[each_category] = SampleGenerator(each_category,K,images_source,codebook_path,sample_path,pathfile,log_path)
        SampleSets[each_category].load_paths()
        SampleSets[each_category].load_codebook(K,save=True, read_from_txt=False)
        SampleSets[each_category].generate_positive_samples(num=10,soft=False)
        SampleSets[each_category].generate_negative_samples([i for i in Category_list if i!= each_category],num=10,soft=False)
   
    print "Program finished."


