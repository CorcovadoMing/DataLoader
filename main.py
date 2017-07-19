import argparse
import logging

from create_dataset import *

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='[%Y/%m/%d][%I:%M:%S %p] ', level=logging.INFO)
    parser = argparse.ArgumentParser(description='Data Loader')
    parser.add_argument('-type', help='pickle or lmdb')
    parser.add_argument('-train', help='training dir')
    parser.add_argument('-test', help='testing dir')
    parser.add_argument('-resize', help='resize image')
    parser.add_argument('-output', help='output dataset dir')
    parser.add_argument('-split', help='split train/test ratio')
    args = parser.parse_args()

    if not args.train or not args.output or not args.type:
        parser.print_help()

    elif not args.test and not args.split:
        print 'Error: Need to specify the test dir or split ratio'

    else:
        train, test = None, None

        db_name = args.train.split('/')[-1]
        if not db_name:
            db_name = args.train.split('/')[-2]
        if not db_name:
            db_name = args.train

        train = image_loader(args.train, int(args.resize))

        if not args.test:
            # split from training data
            train, test = split_testing(train, args.split)
        elif not args.split:
            # load from testing folder
            test = image_loader(args.test, int(args.resize))

        # Make sure the train and test are holded
        if not train or not test:
            print 'Error: training data and testing data are not holded'

        # Save to different formats
        if args.type == 'lmdb':
            create_lmdb(train, test, args.output + '/' + db_name)
        elif args.type == 'pickle':
            create_pickle(train, test, args.output + '/' + db_name)



