"""
Module for getting image file from ayahoo_test_images folder.

Use images_iter function to get info on all files in the directory.
Use filter_by_attrs function to categorize image by their attribute.
"""

import os, sys, re
from collections import defaultdict

def __jpg_file_info(*args):
    """
    Function for storing jpeg file infos.
    """
    attrs = ["name", "location", "attribute"]
    return dict(zip(attrs, args))

def images_iter(directory):
    """
    Get a iterable object that contains instances of JPGFileInfo
    class created by all of files inside the input directory.

    Parameters
    ----------
    directory: full path of a directory

    Returns
    -------
    A iterator of JPGFileInfo instances.
    """
    imagefiles = (os.path.join(os.path.abspath(directory), f)
                  for f in os.listdir(directory))
    def _parse_attribute(filename):
        "Get image attribute from filename"
        return re.compile(r'(.*)_.*').match(filename).group(1)
    def _get_func(filename, module=sys.modules[__name__]):
        "Get file info func from filename extension"
        func = "__%s_file_info" % os.path.splitext(filename)[1].lower()[1:]
        return getattr(module, func)
    return (_get_func(os.path.basename(f))(os.path.basename(f), f,
            _parse_attribute(os.path.basename(f))) for f in imagefiles)

def filter_by_attrs(image_iter):
    """
    Filter image file by attribute name and store them into a dictionary

    Parameters
    ----------
    image_iter: image list iterator

    Returns
    -------
    A dictionary contains all of images categorized by attribute name.
    """
    def image_generator(iter):
        for image in iter:
            yield (image["attribute"], image["location"])
    d = defaultdict(list)
    for (k, v) in image_generator(image_iter):
        d[k].append(v)
    return d








