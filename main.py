import argparse
import logging

from create_dataset import *

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='[%Y/%m/%d][%I:%M:%S %p] ', level=logging.INFO)
    parser = argparse.ArgumentParser(description='Data Loader')
    parser.add_argument('--train', help='training dir')
    parser.add_argument('--resize', help='resize image')
    parser.add_argument('--output', help='output dataset dir')

    args = parser.parse_args()

    if not args.train or not args.output:
        parser.print_help()
    else:
        db_name = args.train.split('/')[-1]
        if not db_name:
            db_name = args.train.split('/')[-2]
        if not db_name:
            db_name = args.train
        images = image_loader(args.train, int(args.resize))
        create_lmdb(images, args.output + '/' + db_name)
