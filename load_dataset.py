import datum_pb2
import lmdb
from datum_utils import *

def load_dataset_from_lmdb(db):
    lmdb_cursor = lmdb.open(db + '.lmdb', readonly=True).begin().cursor()
    datum = datum_pb2.Datum()
    dataset = {}
    for key, value in lmdb_cursor:
        datum.ParseFromString(value)
        label = datum.label
        data = datum_to_array(datum)
        dataset.setdefault(label, [])
        dataset[label].append(data)
    return dataset

if __name__ == '__main__':
    data_name = 'caltech101'
    dataset = load_dataset_from_lmdb(data_name)
    print dataset.keys()
