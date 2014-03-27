"""
Module for getting image file from ayahoo_test_images folder.

Use images_iter function to get info on all files in the directory.
Use filter_by_attrs function to categorize image by their attribute.
"""

import os, sys, re
from collections import defaultdict
from itertools import groupby

def __jpg_file_info(*args):
    """
    Function for storing jpeg file infos.
    """
    attrs = ["name", "location", "attribute"]
    return dict(zip(attrs, args))

def images_iter(directory):
    """
    Get a interator that contains instances of file info dict
    created by all of files inside the input directory.

    Parameters
    ----------
    directory: full path of a directory

    Returns
    -------
    A iterator of a list of file info dict.
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

def filter_by_attrs(images_iter, iterable=False):
    """
    Filter image file by attribute name and store them into a dictionary

    Parameters
    ----------
    images_iter: image list iterator
    iterable: flag for the result format. return iterator if it's true.

    Returns
    -------
    A iterator or dictionary contains all of images categorized by attribute name.

    The format of dictionary looks like below:

        {'attribute1': ['filepath1', 'filepath2', 'filepath3']
         'attribute2': ['filepath4', 'filepath5']
         'attribute3': ['filepath6', 'filepath7', 'filepath8']}

    The format of iterator looks like below:

        ('attribute1', iterator-1),
        ('attribute2', iterator-2),
        ('attribute3', iterator-3), ...

        where:

        iterator-1 =>
          ('attribute1', 'filepath1'), ('attribute1', 'filepath2'), ('attribute1', 'filepath3')
        iterator-2 =>
          ('attribute2', 'filepath4'), ('attribute2', 'filepath5')
        iterator-3 =>
          ('attribute3', 'filepath6'), ('attribute3', 'filepath7'), ('attribute3', 'filepath8')
    """
    def image_generator(iter):
        "Create tuple iterator contains attribute and location infos"
        for image in iter:
            yield (image["attribute"], image["location"])
    def get_attr((attr, loc)):
        "Return attribute for itertool.groupby() to group files."
        return attr

    if iterable:
        return groupby(image_generator(images_iter), get_attr)

    d = defaultdict(list)
    for (k, v) in image_generator(images_iter):
        d[k].append(v)
    return d






