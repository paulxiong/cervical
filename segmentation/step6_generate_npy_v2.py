import os
import numpy as np
import pandas as pd
from scipy.misc import imread, imresize
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
NILM_TYPE = [0, 4, 11, 12, 13]

def step6_generate_npy_v2(train_datasets, train_test_datasets):
    batch_id = 'default'
    output_dir = os.path.join(train_datasets, batch_id)
    dataset_dir = os.path.join(output_dir, 'dataset')
    cell_level_label = os.path.join(train_test_datasets, "data")

    org_dir = dataset_dir
    M = None
    Y = None
    M_test = None
    Y_test = None
    proportion=0.5  #0.7 train 0.3 test
    abnorm_cnt = 0
    abnorm_retype = 0
    #cell_types = []
    df = pd.DataFrame()
    for i in class_map.keys():
        train_dir = os.path.join(org_dir, 'train', class_map[i])
        trainfile = [os.path.join(train_dir, file) for file in os.listdir(train_dir)]
        test_dir = os.path.join(org_dir, 'test', class_map[i])
        testfile = [os.path.join(test_dir, file) for file in os.listdir(test_dir)]
        files = trainfile + testfile
        if len(files)>0:
            if i in NILM_TYPE:
                retype = 0
            else:
                abnorm_retype += 1
                retype = abnorm_retype

            type_df = pd.DataFrame({'FilePath':files,
                                    'CellTypes': [i]*len(files),
                                    "ReTypes":[retype]*len(files)})
            df = df.append(type_df, ignore_index=True)

    norm_cells = df.loc[df['ReTypes']==0]
    abnorm_cells = df.loc[df['ReTypes']!=0].copy()

    print('Norm cells cnt: %s' % len(norm_cells))
    print('Abnorm cells cnt: %s' % len(abnorm_cells))

    abnorm_cnt = len(abnorm_cells)
    norm_cnt = int(np.ceil(0.75 * abnorm_cnt))

    if norm_cnt < len(norm_cells):
        indexes = np.random.choice(list(range(len(norm_cells))), size=norm_cnt)
        norm_cells = norm_cells.iloc[indexes]
    print('Norm cells cnt after random choice: %s ' % len(norm_cells))

    cells = abnorm_cells.append(norm_cells, ignore_index=True)
    y = cells['ReTypes']

    train_cells, test_cells = train_test_split(cells, test_size=proportion, stratify=y)

    for _, row in train_cells.iterrows():
        #cell_type = file.split('/')[-2]
        file = row['FilePath']
        i = row['ReTypes']
        image = imread(file)
        resize_image = imresize(image, [32, 32], interp='nearest')
        m = np.array([resize_image])
        if M is not None:
            M = np.append(M, m,  axis=0)
            Y = np.append(Y, np.array([i]), axis=0)
        else:
            M = m
            Y = np.array([i])

    for _, row in test_cells.iterrows():
        #cell_type = file.split('/')[-2]
        file = row['FilePath']
        i = row['ReTypes']
        image = imread(file)
        resize_image = imresize(image, [32, 32], interp='nearest')
        m = np.array([resize_image])
        if M_test is not None:
            M_test = np.append(M_test, m,  axis=0)
            Y_test = np.append(Y_test, [i], axis=0)
        else:
            M_test = m
            Y_test = np.array([i])

    if not os.path.exists(cell_level_label):
        os.mkdir(cell_level_label)

    print('Cell Types: {}'.format(df['CellTypes'].unique()))
    print('Training samples: %s' % len(Y))
    print('Testing sampels: %s' % len(Y_test))
    print("total abnorm cnt:%s" % abnorm_cnt)

    print(cells.groupby(['CellTypes','ReTypes']).count())

    np.save(cell_level_label + '/X_train.npy', M)
    np.save(cell_level_label + '/y_train.npy', Y)
    np.save(cell_level_label + '/X_test.npy', M_test)
    np.save(cell_level_label + '/y_test.npy', Y_test)
