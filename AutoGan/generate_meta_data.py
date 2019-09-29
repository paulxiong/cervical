import PIL.Image as Image
import os, pickle

def make_baches_meta():
    dic = {}
    dic['num_cases_per_batch'] = 50
    dic['label_names'] = ['1', '7']
    dic['num_vis'] = 3072
    print(dic)
    with open('./data/cifar-10-batches-py/batches.meta_1', 'wb') as f:
        pickle.dump(dic, f)

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='iso-8859-1')
    return dict

make_baches_meta()    
file1 = 'data/cifar-10-batches-py/batches.meta_1'
dict_train_batch1 = unpickle(file1)
#print(dict_train_batch1)
for key in dict_train_batch1.keys():
    print(key)

