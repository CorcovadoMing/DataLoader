import glob
import logging
import os
from itertools import count

import datum_pb2
import lmdb
import numpy as np
from datum_utils import *
from PIL import Image


def image_loader(path):
    dirlist = [ item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item)) ]
    logging.info("Create dataset with {0} classes".format(len(dirlist)))
    images = {}
    for subfolder in dirlist:
        images[subfolder] = []
        imagePath = glob.glob(path + '/' + subfolder +'/*')
        im_array = np.array([np.array(Image.open(i).convert('RGB').resize((32, 32), Image.ANTIALIAS), np.uint8) for i in imagePath])
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

def create_db(images, db, batch_size=1024):
    logging.info("Convert dataset into lmdb format")
    env = lmdb.open(db, map_async=True, max_dbs=0)
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

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='[%Y/%m/%d][%I:%M:%S %p] ', level=logging.INFO)
    images = image_loader('test_rawdata')
    create_db(images, 'test')
