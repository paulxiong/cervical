import os
import numpy as np
from scipy.misc import imsave, imread, imresize
from sklearn.model_selection import train_test_split

class_map = {
    0: 'Norm',
    1: 'LSIL',
    2: 'HSIL',
    3: 'HPV',
    4: 'NILM',
    5: 'SCC',
    6: 'ASCUS',
    7: 'ASCH',
    8: 'AGC',
    9: 'AIS',
    10:'ADC',
    11:'T',
    12:'M',
    13:'HSV'
}
class_map_reverse = {}
for i in class_map.keys():
    class_map_reverse[class_map[i]] = i

NILM_TYPE = [0, 4, 11, 12, 13]

org_dir = './segmentation/datasets/classify/train_datasets/default/dataset'
#dirs=['train_datasets/Norm', 'train_datasets/LSIL', 'train_datasets/HSIL', 'train_datasets/HPV', 'train_datasets/SCC']
#dirs=['train_datasets/Norm', 'train_datasets/LSIL', 'train_datasets/HSIL', 'train_datasets/HPV', 'train_datasets/SCC']

M = None
Y = None
M_test = None
Y_test = None

random_labels = 5
proportion=0.5  #0.7 train 0.3 test
abnorm_cnt = 0
norm_vs_abnorm = 0.75


norm_cells = []
abnorm_cells = []
abnorm_y = []
abnorm_retype = 0
cell_types = []

for i in class_map.keys():
    train_dir = os.path.join(org_dir, 'train', class_map[i])
    trainfile = [os.path.join(train_dir, file) for file in os.listdir(train_dir)]
    test_dir = os.path.join(org_dir, 'test', class_map[i])
    testfile = [os.path.join(test_dir, file) for file in os.listdir(test_dir)]
    files = trainfile + testfile
    if len(files)>0:
        cell_types += [i]
        if i in NILM_TYPE:
            norm_cells += files
        else:
            abnorm_retype += 1
            abnorm_y += [abnorm_retype] * len(files)
            abnorm_cells += files
        
        
print('Norm cells cnt: %s' % len(norm_cells))
print('Abnorm cells cnt: %s' % len(abnorm_cells))
        
abnorm_cnt = len(abnorm_cells)
norm_cnt = int(np.ceil(0.75 * abnorm_cnt))

if norm_cnt < len(norm_cells):
    norm_cells = list(np.random.choice(norm_cells, size=norm_cnt))
print('Norm cells cnt after random choice: %s ' % len(norm_cells))

cells = abnorm_cells + norm_cells
y = abnorm_y + [0]*len(norm_cells)

train_cells, test_cells, train_y, test_y = train_test_split(cells,y, test_size=proportion, stratify=y)

for file, i in zip(train_cells, train_y):
    #cell_type = file.split('/')[-2]
    #i = class_map_reverse[cell_type]
    image = imread(file)
    resize_image = imresize(image, [32, 32], interp='nearest')
    m = np.array([resize_image])
    if M is not None:
        M = np.append(M, m,  axis=0)
        Y = np.append(Y, np.array([i]), axis=0)
    else:
        M = m
        Y = np.array([i])

for file, i in zip(test_cells,test_y):
    #cell_type = file.split('/')[-2]
    #i = class_map_reverse[cell_type]
    image = imread(file)
    resize_image = imresize(image, [32, 32], interp='nearest')
    m = np.array([resize_image])
    if M_test is not None:
        M_test = np.append(M_test, m,  axis=0)
        Y_test = np.append(Y_test, [i], axis=0)
    else:
        M_test = m
        Y_test = np.array([i])
    



#/dataset_A/cell_level_label/
#X_test.npy  X_train.npy  y_test.npy  y_train.npy

if not os.path.exists('dataset_act'):
    os.mkdir("dataset_act")
if not os.path.exists('dataset_act/cell_level_label'):
    os.mkdir("dataset_act/cell_level_label")
    
print(cell_types)
print(len(Y))
print(len(Y_test))
print("total abnorm cnt:%s" % abnorm_cnt)

np.save('dataset_act/cell_level_label/X_train.npy', M)
np.save('dataset_act/cell_level_label/y_train.npy', Y)
np.save('dataset_act/cell_level_label/X_test.npy', M_test)
np.save('dataset_act/cell_level_label/y_test.npy', Y_test)
