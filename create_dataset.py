from PIL import Image
import numpy
import os
import glob
import datum_utils
import lmdb

def readimage(path):
    dirlist = [ item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item)) ]
    images = []

    for subfolder in dirlist:
        imagePath = glob.glob(path + '/' + subfolder +'/*')
        im_array = numpy.array([numpy.array(Image.open(i), 'f') for i in imagePath])
        images.append(im_array)
    return images

if __name__ == '__main__':
    readimage('test_rawdata')
