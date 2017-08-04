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
from random import shuffle

def image_loader(path, size=32, channel=3):
    dirlist = [ item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item)) ]
    logging.info("Create dataset with {0} classes from {1}".format(len(dirlist), path))
    images = {}
    for subfolder in dirlist:
        imagePath = glob.glob(path + '/' + subfolder +'/*')
        if channel == 3:
            im_array = np.array([np.array(Image.open(i).convert('RGB').resize((size, size), Image.ANTIALIAS), np.uint8) for i in imagePath])
        elif channel == 1:
            im_array = np.array([np.array(Image.open(i).convert('L').resize((size, size), Image.ANTIALIAS), np.uint8) for i in imagePath])[:,:,:,None]
        images[subfolder] = im_array
    return images

def split_testing(images, ratio=0.20):
    train_images = {}
    test_images = {}
    for key in images:
        t = len(images[key])
        sp = int(t * ratio) + 1
        shuffle(images[key])
        test_images[key] = images[key][:sp]
        train_images[key] = images[key][sp:]
    return train_images, test_images

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
        for data in images[label]:
            datum = array_to_datum(data, label_no)
            batch.append((str(i.next()), datum))
            if len(batch) >= batch_size:
                write_batch_lmdb(env, batch)
                batch = []
    write_batch_lmdb(env, batch)
    batch = []
    env.close()

def create_pickle(train_images, test_images, db):
    output = db + '.pkl'
    logging.info("Convert dataset into pkl format to {0}".format(output))
    x, xt = [], []
    y, yt = [], []
    for label in train_images:
        for train in train_images[label]:
            x.append(train)
            y.append(label)
        for test in test_images[label]:
            xt.append(test)
            yt.append(label)
    x = np.array(x)
    y = np.array(y)
    xt = np.array(xt)
    yt = np.array(yt)
    pickle.dump((x, y, xt, yt), open(output, 'wb'))


if __name__ == '__main__':
    test_dataset = '/datasets/caltech101'
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='[%Y/%m/%d][%I:%M:%S %p] ', level=logging.INFO)
    images = image_loader(test_dataset)
    train_images, test_images = split_testing(images)
    create_pickle(train_images, test_images, test_dataset)
    #create_lmdb(images, test_dataset)
