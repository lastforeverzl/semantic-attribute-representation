"""
Module for getting image file from ayahoo_test_images folder.

Use images_iter function to get info on all files in the directory.
"""

import os, sys, re

class FileInfo(dict):
    """
    store basic file info
    """
    def __init__(self, filename, location):
        self["name"] = filename
        self["location"] = location

class JPGFileInfo(FileInfo):
    """
    store image file info
    """
    def __init__(self, filename, location):
        self["attribute"] = self.__parse_attribute(filename)
        FileInfo.__init__(self, filename, location)

    def __parse_attribute(self, filename):
        return re.compile(r'(.*)_.*').match(filename).group(1)

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
    def get_class(filename, module=sys.modules[__name__]):
        "get file info class from filename extension"
        subclass = "%sFileInfo" % os.path.splitext(filename)[1].upper()[1:]
        return hasattr(module, subclass) and \
               getattr(module, subclass) or FileInfo
    return (get_class(os.path.basename(f))(os.path.basename(f), f)
            for f in imagefiles)
