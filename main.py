import imagefileinfo as fi
import vq

if __name__ == '__main__':
    K = 10
    #Category_list = ['building']
    Category_list = ['building', 'donkey', 'monkey', 'mug', 'centaur', 'bag', 'carriage', 'wolf', 'zebra', 'statue', 'jetski', 'goat']
    Codebooks = {}
    Pathbook = {}
    for each_category in Category_list:
         f = open("trainingSamples_"+each_category+".txt", 'w')
         f.write("")
         f.close()
         
    for each_category in Category_list:
        Pathbook[each_category] = fi.filter_by_attrs(fi.images_iter("/Users/minhuigu/Downloads/ayahoo_test_images"))[each_category]
        Codebooks[each_category] = vq.code_book(Pathbook[each_category], each_category, K,save=False, read_from_txt = True)
    print Codebooks
    
    TrainingSamples = {}
    for each_category in Category_list:
        TrainingSamples[each_category] = vq.batch_quantization(Pathbook[each_category], Codebooks[each_category], soft=False)
    
    for each_category in Category_list:
        print "Category: ",each_category
        f = open("trainingSamples_"+each_category+".txt", 'a')
        for each_sample in TrainingSamples[each_category]:
           
            line = "+1 "
            for k,v in each_sample.items():
                line = line +  "%s:%s "%(k,v)
            f.write(line)
            print line  
        f.close()
        print " "
        


