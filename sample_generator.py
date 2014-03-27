import os
import imagefileinfo as fi
import vq
import time

class Time_recorder():
    def __init__(self,log_path):
        self.f = open(log_path , 'w')
        
    def logging(self,content):
        self.f.write(content)
        
    def close(self):
        self.f.close()

class SampleGenerator():
    
    def __check_files__(self,*args):
        for afile in args:
            f = open(afile, 'w')
            f.write("")
            f.close()
     
    def __check_output_folders__(self,*args):
        for a in args:
            if not os.path.exists(a): 
                os.makedirs(a)
          
    def __init__(self,category,K,img_folder,codebook_path,sample_path,pathfile,log_path):
        self.__check_output_folders__(codebook_path,sample_path,pathfile,img_folder,log_path)
        self.log_filename = log_path + category + ".log"
        self.timerecorder = Time_recorder(self.log_filename)
        self.category = category
        self.K = K
        self.psampels = []
        self.nsampels = []
        self.positive_sample_number = 0
        self.negative_sample_number = 0
        self.samples_filename = sample_path + category + "_samples.txt"
        self.codebook = []
        self.codebook_filename = codebook_path + category + "_codebook.txt"
        self.pathbook = {}
        self.pathbook_filename = pathfile +category + "_path.txt"
        now = time.time()
        self.image_pool = fi.filter_by_attrs(fi.images_iter(img_folder))
        interval = time.time() - now
        self.timerecorder.logging("%s :Iterated images by attributes: %s seconds.\n"%(time.ctime(),interval))
        #self.__check_files__(self.samples_filename,\
        #                        self.codebook_filename,\
        #                        self.pathbook_filename)
                                
    def load_paths(self):
        self.pathbook = self.image_pool[self.category]
        print self.pathbook
        f = open(self.pathbook_filename , 'w')
        for eachline in self.pathbook:
            f.write(eachline+'\n')
        f.close()
                
    def load_codebook(self, K, save=True, read_from_txt=False ):
        now = time.time()
        self.codebook = vq.code_book(self.pathbook, self.category,self.codebook_filename, K, save, read_from_txt)
        interval = time.time() - now
        self.timerecorder.logging("%s :Calculated codebook with K=%d : %s seconds.\n"%(time.ctime(),K,interval))
           
    def generate_positive_samples(self, num =100000000, soft=False):
        counter = min(num,len(self.pathbook))
        now = time.time()
        self.psampels = vq.batch_quantization(self.pathbook[:counter], self.codebook,soft)
        interval = time.time() - now
        self.timerecorder.logging("%s :Generated %d psamples: %s seconds.\n"%(time.ctime(),num,interval))
        f = open(self.samples_filename, 'w')
        i = 0
        now = time.time()
        for each_sample in self.psampels:
            if i < counter :
                line = "+1 "
                for k,v in each_sample.items():
                    line = line +  "%s:%s "%(k,v)
                f.write(line+'\n')
                print line  
            i += 1
        interval = time.time() - now
        self.timerecorder.logging("%s :Saved %d psamples to file: %s seconds.\n"%(time.ctime(),counter,interval))
        f.close()
        self.positive_sample_number = len(self.psampels)
        
    def generate_negative_samples(self, category_list, num = 10000000, soft=False):
        counter = min(num,self.positive_sample_number)
        categories = len(category_list)
        f = open(self.samples_filename, 'a')
        i = 0
        now = time.time()
        while i < counter:
            for j in range(categories):
                img = self.image_pool[category_list[j]][i/categories]
                hist = vq.quatization(img, self.codebook, soft=False)
                self.nsampels.append(hist)
                line = "-1 "
                for k,v in hist.items():
                    line = line +  "%s:%s "%(k,v)
                f.write(line+'\n')
                print line
                i += 1
        interval = time.time() - now
        self.timerecorder.logging("%s :Generated and saved %d nsamples to file: %s seconds.\n"%(time.ctime(),counter,interval))       
        f.close()         
        self.negative_sample_number = len(self.nsampels)
        self.timerecorder.close()
        
        
        
        
        
     