import imagefileinfo as fi

if __name__ == '__main__':
    print fi.filter_by_attrs(fi.images_iter("/Users/hanyan/Downloads/ayahoo_test_images"))["bag"]
