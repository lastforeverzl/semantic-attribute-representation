import cv2
import os
import numpy as np
from scipy import cluster, stats, spatial
from math import sqrt, pi, exp


def __dist(u, v):
    """
    Get euclidean distance of two ndarray.

    Parameters
    ----------
    u, v : numpy ndarray

    Returns
    -------
    The distance calculated by scipy.
    """
    return spatial.distance.euclidean(u, v)
    
    
def __guassian_kernel(x, sigma=200):
    """
    Gaussian kernel density estimation

    Parameters
    ----------
    x: the distance
    sigma: given sigma value

    Returns
    -------
    Estimation value of the give x and sigma
    """
    return (1 / (sqrt(2.*pi) * sigma)) * exp(-x ** 2 / (2.*sigma**2))
    
    
def __sift_dect_and_compute(image):
    """
    Extract features and computes their descriptors using SIFT algorithm.
    

    Parameters
    ----------
    image: the absolute path of image file
    

    Returns
    -------
    kp: Keypoints detected by SIFT.
    des: descriptors computed by SIFT.
    """
    img = cv2.imread(image, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kp, des = cv2.SIFT().detectAndCompute(gray, None)
    return kp, des

def quatization(image, code_book, soft=False):
    """
    Do hard quatization by assign codes from a code book to target image
    that computes the euclidian distance between image and every frame
    in the code_book.

    Parameters
    ----------
    image: the absolute path of image file
    code_book: numpy ndarray
    soft: the flag for the type of quatization. If true, we will use soft 
          quatization. The default one is hard quatization.

    Returns
    -------
    adict: the frequency histogram of the representation of bag of words
    """
    kp, des = __sift_dect_and_compute(image)
    print image, "--> SIFT feature number: ", len(kp)
    adict = {}
    shortest = []
    for i in range(0, len(code_book)):
        adict[i] = 0
                
    if soft is False:   
        for p in des:
            mini = 0
            for i in range(0, len(code_book)):
                t = __dist(code_book[i], p)
                if mini == 0 or t < mini:
                    mini = t
                    shortest = i
            adict[shortest] += 1

    else:     
        sum_k_ri = {}
        
        for i in range(0, len(code_book)):
            s = 0
            for j in range(0, len(code_book)):
                s += __guassian_kernel(__dist(code_book[i], code_book[j]))
                sum_k_ri[i] = s
            
        for i in range(0, len(code_book)):
            for j in des:
                adict[i] += __guassian_kernel(__dist(j, code_book[i])) / (sum_k_ri[i]) 
                       
    return adict                    
    

def code_book(folder_path, K, save=True, read_from_txt = False):
    """
    Generate the bag of words for a folder of pictures.

    Parameters
    ----------
    folder_path: the absolute path of the folder that contains set of
    images

    k: int or ndarray
       The number of clusters to form as well as the number of
       centroids to generate.

    save: The flag for saving the result code book.

    Returns
    -------
    nd: ndarray
        A 'k' by 'N' array of centroids found at the last iteration of
        k-means.
    """
    des_pool = np.zeros((0, 128))
    kp = []
    if read_from_txt is True:
        nd = np.loadtxt('word.txt')
    else:
        for each_img in os.listdir(folder_path):
            image_path = folder_path + each_img
            kp, des = __sift_dect_and_compute(image_path)
            print image_path, "--> SIFT feature number: ", len(kp)
            des_pool = np.concatenate((des_pool, des))
        print "Pool shape: "
        print des_pool.shape
        print "Clustering... ", "K = ",K
        nd, p = cluster.vq.kmeans2(des_pool, K)

        if save:
            print "saving codebook to word.txt"
            np.savetxt('word.txt', nd)
    return nd
