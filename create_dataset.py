import glob
import logging
import os
from itertools import count

import datum_pb2
import lmdb
import pickle
import numpy as np
from datum_utils import *
from PIL import Image


def image_loader(path, size=32):
    dirlist = [ item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item)) ]
    logging.info("Create dataset with {0} classes from {1}".format(len(dirlist), path))
    images = {}
    for subfolder in dirlist:
        images[subfolder] = []
        imagePath = glob.glob(path + '/' + subfolder +'/*')
        im_array = np.array([np.array(Image.open(i).convert('RGB').resize((size, size), Image.ANTIALIAS), np.uint8) for i in imagePath])
        images[subfolder].append(im_array)
    return images

def write_batch_lmdb(env, batch):
    try:
        with env.begin(write=True) as txn:
            for key, datum in batch:
                txn.put(key, datum.SerializeToString())
    except lmdb.MapFullError:
        txn.abort()
        curr_limit = env.info()['map_size']
        new_limit = curr_limit * 2
        env.set_mapsize(new_limit)
        write_batch_lmdb(env, batch)

def create_lmdb(images, db, batch_size=1024):
    output = db + '.lmdb'
    logging.info("Convert dataset into lmdb format to {0}".format(output))
    env = lmdb.open(output, map_async=True, max_dbs=0)
    i = count(0)
    l = count(0)
    batch = []
    for label in images:
        label_no = l.next()
        for data in images[label][0]:
            datum = array_to_datum(data, label_no)
            batch.append((str(i.next()), datum))
            if len(batch) >= batch_size:
                write_batch_lmdb(env, batch)
                batch = []
    write_batch_lmdb(env, batch)
    batch = []
    env.close()

def create_pickle(images, db):
    output = db + '.pkl'
    logging.info("Convert dataset into pkl format to {0}".format(output))
    x = []
    y = []
    for label in images:
        for data in images[label][0]:
            x.append(data)
            y.append(label)
    x = np.array(x)
    y = np.array(y)
    pickle.dump((x,y), open(output, 'wb'))


if __name__ == '__main__':
    test_dataset = 'caltech101'
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='[%Y/%m/%d][%I:%M:%S %p] ', level=logging.INFO)
    images = image_loader(test_dataset)
    create_lmdb(images, test_dataset)
    create_pickle(images, test_dataset)
