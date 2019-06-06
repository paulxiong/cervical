
# coding: utf-8

# In[1]:

import os
import cv2
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, StratifiedKFold, train_test_split
from sklearn.utils import shuffle
from sklearn import metrics
import keras
from keras.models import Model
from keras.optimizers import Adam
from keras.applications.inception_v3 import InceptionV3
from keras.layers import Dense, Input, Flatten, Dropout, GlobalAveragePooling2D, GlobalMaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from keras import backend as K
import tensorflow as tf

import shutil
import glob


def get_flops(model):
    run_meta = tf.RunMetadata()
    opts = tf.profiler.ProfileOptionBuilder.float_operation()

    # We use the Keras session graph in the call to the profiler.
    flops = tf.profiler.profile(graph=K.get_session().graph,
                                run_meta=run_meta, cmd='op', options=opts)

    return flops.total_float_ops  # Prints the "flops" of the model.

##=====================================
## Image pre preocess and augmnetation
##=====================================
def padding(img, img_size, color):
    shape = img.shape[:-1]
    #print(img.shape,img_size)
    delta_height = img_size[0]-shape[0]
    delta_width = img_size[1]-shape[1]
    top = delta_height//2
    bottom = delta_height-top
    left = delta_width//2
    right = delta_width-left
    new_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return new_img

def double_size_and_padding(img, img_size, color):
    shape = img.shape[:-1]
    shape = tuple([edge*2 for edge in shape])
    img = cv2.resize(img, shape)
    #print(img.shape,img_size)
    assert (shape[0] < img_size[0])&(shape[1] < img_size[1]), \
                        "Input shape:{},Require shape:{}".format(shape, img_size)
    new_img = padding(img, img_size, color)
    return new_img

def oversize_crop(img, img_size, ratio):
    max_height = img_size[0] // ratio
    max_width = img_size[1] // ratio
    height = np.shape(img)[0]
    width = np.shape(img)[1]
    if width > max_width:
        left = (width - max_width) // 2
        right = width - max_width - left
        img = img[:, left:-right, :]
    if height > max_height:
        above = (height - max_height) // 2
        below = height - max_height - above
        img = img[above:-below, :, :]
    return img 

def augment(src, img_size, angle, translation):
    import math
    #Image Rotation
    image_center = tuple(np.array(src.shape[1::-1]) / 2)
    #print("img center is: ", image_center)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(src, rot_mat, src.shape[1::-1], flags=cv2.INTER_LINEAR)

    #Image Translation
    M = np.float32([[1,0,translation],[0,1,translation]])
    result = cv2.warpAffine(result, M, result.shape[1::-1], flags=cv2.INTER_LINEAR)

    #Image Crop
    max_height = img_size[0]
    max_width = img_size[1]

    height = np.shape(result)[0]
    width = np.shape(result)[1]
    
    color = [0, 0, 0]

    if max_width < width:
        left_edge = math.ceil((width - max_width)//2.0)
        right_edge = math.floor((width + max_width)//2.0)
        left_axis, right_axis = 0, 0
    else:
        delta_w = max_width - width
        left_edge, right_edge = 0, width
        left_axis, right_axis = delta_w//2, delta_w-(delta_w//2)

    if max_height < height:
        top_edge = math.ceil((height - max_height)//2.0)
        bottom_edge = math.floor((height + max_height)//2.0)
        top_axis, bottom_axis = 0, 0
    else:
        delta_h = max_height - height
        top_edge, bottom_edge = 0, height
        top_axis, bottom_axis = delta_h//2, delta_h-(delta_h//2)

    patch_img = cv2.copyMakeBorder(result[top_edge:bottom_edge, left_edge:right_edge], \
                                top_axis, bottom_axis, left_axis, right_axis, \
                                cv2.BORDER_CONSTANT, value=color)
    return patch_img

def augment_bkup(src, choice):
    if choice == 0:
        # Rotate 90
        src = np.rot90(src, 1)
    if choice == 1:
        # flip vertically
        src = np.flipud(src)
    if choice == 2:
        # Rotate 180
        src = np.rot90(src, 2)
    if choice == 3:
        # flip horizontally
        src = np.fliplr(src)
    if choice == 4:
        # Rotate 90 counter-clockwise
        src = np.rot90(src, 3)
    if choice == 5:
        # Rotate 180 and flip horizontally
        src = np.rot90(src, 2)
        src = np.fliplr(src)
    return src
##==============================
## histogram equlization
#===============================

def validate_attributes(data, dtypes, attri=[]):
    assert type(data) == np.ndarray, "Need a numpy ndarray as input"
    assert np.sum([data.dtype == dtype for dtype in dtypes]) >= 1, "Data type missmatch"
    if 'positive' in attri:
        assert (data >= 0).all(), "Not positive"
    if 'integer' in attri:
        assert (np.int64(data) == data).all(), "Not integer"
    if 'notempty' in attri:
        assert np.size(data) != 0, "Empty array"
    if 'vector' in attri:
        assert len(np.shape(data)) == 1, "Not a vector"
    if '2d' in attri:
        assert len(np.shape(data)) == 2, "Not a 2d array"
        
def computeCumulativeHistogram(img, nbins):
    nn = np.histogram(img.flatten(), nbins)[0]
    cum = np.cumsum(nn)
    return nn, cum

def createTransformationToIntensityImage(a, hgram, m, n, nn, cum):
    cumd = np.cumsum(hgram * np.size(a) / np.sum(hgram))
    
    # Create transformation to an intensity image by minimizing the error
    # between desired and actual cumulative histogram.
    tol = np.dot(np.ones((m, 1)), 
                 np.min(np.stack([np.append(nn[0:n-1], 0),np.append(0, nn[1:n])]), 
                        axis=0)[np.newaxis,:]/2
                )
    #import ipdb; ipdb.set_trace()
    err = (np.dot(cumd[:,np.newaxis], np.ones((1, n))) - 
           np.dot(np.ones((m, 1)), cum[np.newaxis,:])) + tol
    #here for some calculation error, we set epsilon= 2.2204e-15
    d = np.where(err < (-np.size(a)*np.sqrt(2.2204e-14)))
    if len(d) !=0:
        err[d] = np.size(a)
        
    T = np.argmin(err, axis=0)
    
    return T

def histeq(*param):
    assert len(param) in [2, 3], "Invalid number of input parameters"
    NPTS = 256
    
    if len(param) == 2:
        #HISTEQ(I, HGRAM)
        a = param[0]
        hgram = param[1]
        map_method = 'GML'
        validate_attributes(a, [np.uint8], ['2d'])
        validate_attributes(hgram,[np.float32, np.float64],
                            ['vector','notempty'])
        n = NPTS
    else:
        a = param[0]
        hgram = param[1]
        map_method = param[2]
        validate_attributes(a, [np.uint8], ['2d'])
        validate_attributes(hgram,[np.float32, np.float64],
                            ['vector','notempty'])
        n = NPTS
        
    #ipdb.set_trace()
    if map_method == 'mat':
        #++++++MAT++++++
        hgram = hgram * (np.size(a) / np.sum(hgram))
        m = len(hgram)
    
        nn, cum = computeCumulativeHistogram(a, n)
        tk = createTransformationToIntensityImage(a, hgram, m, n, nn, cum)
        #++++++++++++++++++
    else:
        hist, hist_c = computeCumulativeHistogram(a, n)
        #normalize
        hist = hist / np.sum(hist)
        hist_c = hist_c / hist_c[-1]
        assert len(hist) == len(hgram), "hgram must be as same as image"
        hgram = hgram / np.sum(hgram)
        hgram_c = np.cumsum(hgram)
        
        err = np.abs(np.dot(np.ones((n, 1)), hgram_c[np.newaxis,:]) - 
                 np.dot(hist_c[:,np.newaxis], np.ones((1, n))))
        if map_method == 'SML':
            tk = np.argmin(err, axis=0)
        elif map_method == 'GML':
            # method1
            col_min = np.argmin(err, axis=1)
            tk = np.zeros(256)
            start = 0
            for i, mi in enumerate(col_min):
                if mi != start:
                    if start == 0:
                        tk[range(start, mi + 1)] = i
                    else:
                        tk[range(start + 1, mi + 1)] = i
                    start = mi
            #method 2
            #tk1 = np.zeros(256)
            #lastStartY, lastEndY, startY, endY = [0]*4
            #for x in range(256):
                #minValue = err[x, 0]
                #for y in range(256):
                    #if minValue > err[x, y]:
                        #endY = y
                        #minValue = err[x, y]
                #if (startY != lastStartY) or (endY != lastEndY):
                    #for i in range(startY, endY+1):
                        #tk1[i] = x
                    #lastStartY = startY
                    #lastEndY = endY
                    #startY = lastEndY + 1
            #assert (tk1 == tk).all(), "tk is not the same, \n {}".format(err)
                    
    #print(tk)
    for i, j in enumerate(tk):
        a[a==i] = j
    #max min scale
    limit = [np.min(tk), np.max(tk)]
    
    a = np.floor((a - limit[0])/(limit[1]-limit[0])*255.0)
    
    hist = np.histogram(a.flatten(), bins=n)[0]
    return a.astype(np.uint8), hist    


def contrast_enhance(img_batch, color_mode, clahe):
    L_CHANNEL = 0
    V_CHANNEL = -1
    S_CHANNEL = 1
    channels = []
    hist_batch = None
    
    if color_mode == 'HSV_CLAHE_V':
        for_color = cv2.COLOR_BGR2HSV
        back_color = cv2.COLOR_HSV2BGR
        channels = [V_CHANNEL]
    elif color_mode == 'HSV_CLAHE_S':
        for_color = cv2.COLOR_BGR2HSV
        back_color = cv2.COLOR_HSV2BGR
        channels = [S_CHANNEL]
    elif color_mode == 'HSV_CLAHE_SV':
        for_color = cv2.COLOR_BGR2HSV
        back_color = cv2.COLOR_HSV2BGR
        channels = [S_CHANNEL, V_CHANNEL]
    elif color_mode == 'LAB_CLAHE_L':
        for_color = cv2.COLOR_BGR2LAB
        #for LAB is a Cartesian Coordinate System
        #back_color = cv2.COLOR_LAB2BGR
        channels = [L_CHANNEL]
    elif color_mode == 'HIST_BATCH_EQ':
        for_color = cv2.COLOR_BGR2HSV
        back_color = cv2.COLOR_HSV2BGR
        channels = [V_CHANNEL]
        hist_batch = np.zeros(256)
    elif color_mode == 'HIST_BATCH_EQ_LAB':
        for_color = cv2.COLOR_BGR2LAB
        #for LAB is a Cartesian Coordinate System
        #back_color = cv2.COLOR_LAB2BGR
        channels = [L_CHANNEL]
        hist_batch = np.zeros(256)
    elif color_mode == 'RGB':
        return None
    else:
        return None
    
    for i, img in enumerate(img_batch):
        img = cv2.cvtColor(img, for_color)
        img_batch[i] = img
        # if need to do hist batch equalization, sum the hist in a batch first
        if (hist_batch is not None) and channels:
            channel = img[..., channels[0]]
            hist = np.histogram(channel.flatten(), bins=256)[0]
            hist_batch = hist + hist_batch
        elif channels:
            for ch in channels:
                img[..., ch] = clahe.apply(img[..., ch])
            if 'LAB' not in color_mode:
                img_batch[i] = cv2.cvtColor(img, back_color)
            
    if hist_batch is not None:
        for i, img in enumerate(img_batch):
            img[..., channels[0]], _ = histeq(img[..., channels[0]], hist_batch)
            if 'LAB' not in color_mode:
                img_batch[i] = cv2.cvtColor(img, back_color)

#================================
## Imbalance Data Set Sampling
#================================
def down_sample(df, ratio):
    maj_rand_index = np.random.choice(len(df), int(ratio*len(df)), replace=False)
    df = df.iloc[maj_rand_index]
    return df

#def up_sample(df, choices, translations, tmp_dir, with_origin=False):
def up_sample(df, choices, translations, tmp_dir, img_size, with_origin=False):
    #whether with original data
    if with_origin:
        df_tmp = df.copy()
    else:
        df_tmp = pd.DataFrame()

    for file, gt in df[['name', 'gt']].values:
        aug_path = os.path.join(tmp_dir, *file.split('/')[-3:-1])
        if not os.path.exists(aug_path):
            os.makedirs(aug_path)
        base_name = os.path.basename(file)
        img = cv2.imread(file)
        for choice in choices:
            for translation in translations:
                angle = choice * 360 //len(choices)
                img_aug = augment(img, img_size, angle, translation)
                save_path = os.path.join(aug_path, str(angle)+'_'+str(translation)+'_'+base_name)
                cv2.imwrite(save_path, img_aug)
                series = pd.Series({'name':save_path,
                                    'gt':gt,
                                   })
                df_tmp = df_tmp.append(series, ignore_index=True)
    return df_tmp

def dataset_augment(df, img_size, tmp_dir='./tmp'):
    pos_samples = df.loc[df['gt'] != 0]
    neg_samples = df.loc[df['gt'] == 0]

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    #do data augment on positive cells
    print("Preparing data augment: %s"%AUGMENTATION)
    if AUGMENTATION == 'Minority':
        pass
    elif AUGMENTATION == 'Majority_Down_Minority_Up':
        pass
    elif AUGMENTATION == 'Majority_Down':
        pass
    elif AUGMENTATION == 'Classwise_Minority':
        pass
    elif AUGMENTATION == "Classwise_Majority_Down_Minority_Up":
        pass
    elif AUGMENTATION == "SMOTE":
        pass
    elif AUGMENTATION == "Up_All":
        #normal cells:  Rotation choices = 20, translations = 14
        #normal cells:  Rotation choices = 10, translations = 10
        neg_sample_df = up_sample(neg_samples, range(10), range(10), tmp_dir, img_size)
        pos_sample_df = up_sample(pos_samples, range(15), range(10), tmp_dir, img_size)
        df = df.append(neg_samples_df, ignore_index=True)
        df = df.append(pos_samples_df, ignore_index=True)
        """
        up_sample_df = up_sample(df, range(10), range(10), tmp_dir, img_size)
        df = df.append(up_sample_df, ignore_index=True)
        """
    else:
        print("Augmentation Method:{}".format(AUGMENTATION))
    df = shuffle(df, random_state=0)
    df = df[['name', 'gt']]
    
    return df

##=======================================
## Loading Data Sets
##=======================================
def load_train_from_folder(path):
    CLASS = ['Norm', 'LSIL', 'HSIL', 'HPV', 'SCC']
    GTS = [0, 1, 2, 3, 4]
    train_files = []
    train_set = pd.DataFrame()
    for c, gt in zip(CLASS, GTS):
        files = glob.glob(os.path.join(path, c, '*.BMP'))
        #print(files)
        if len(files) != 0:
            data = list( zip( files, [gt] * len(files) ) )
            train_set = train_set.append(pd.DataFrame(data, columns=['name', 'gt']))
            train_files = train_files + files
    #print(train_set)
    print(np.shape(train_set['gt']))
    train_labels = train_set['gt'].values.copy()
    
    return train_files, train_set, train_labels
    
def load_test_from_folder(path):
    test_files, test_set, _ = load_train_from_folder(path)
    test_set['positive'] = 0.5
    return test_files, test_set

def load_train(path):
    train_set = pd.read_csv('input/train_labels.csv')
    assert len(train_set) == len(train_set['name'].unique()), "Train set has multi labeled sample"
    train_files = []
    for i in range(len(train_set)):
        train_files.append(path + train_set.iloc[i][0])
    train_set['name'] = train_files
    
    train_label = train_set['positive'].values.copy()
    print(np.shape(train_set['positive']))
    #train_files = list(train_set['name'].values)
    train_set.columns = ['name', 'gt']
    
    return train_files, train_set, train_label


def load_test(path):
    test_set = pd.read_csv('input/sample_submission.csv')
    assert len(test_set) == len(test_set['name'].unique()), "Test set has multi labeled sample"
 
    test_files = []
    for i in range(len(test_set)):
        test_files.append(path + test_set.iloc[i][0])
    return test_files, test_set
    
    
##===========================================
# # Define CNN Model Architecture
#============================================
def inceptionv3(img_dim, clf_mode='Binary', dropout=0.5, class_num=1):
    input_tensor = Input(shape=img_dim)
    base_model = InceptionV3(include_top=False,
                             weights='imagenet',
                             input_shape=img_dim)
    bn = BatchNormalization()(input_tensor)
    x = base_model(bn)
    x = GlobalAveragePooling2D()(x)
    #x = GlobalMaxPooling2D()(x)
    x = Dropout(dropout)(x)
    if clf_mode == 'Binary':
        #define last layer
        output = Dense(class_num, activation='sigmoid')(x)
        #define loss mode
        loss_mode = 'binary_crossentropy'
    elif clf_mode == 'MultiClass':
        assert class_num > 1, "Error, Multi class Number %d !> 1"%class_num
        #add a layer 
        #x = Dense(512, activation='elu')(x)
        #x = Dropout(dropout)(x)
        #last layer
        output = Dense(class_num, activation='softmax')(x)
        #loss mode
        loss_mode = 'categorical_crossentropy'
    
    model = Model(input_tensor, output)
    #model.compile(optimizer=Adam(lr=1e-4), loss=loss_mode, 
    #              metrics=['accuracy'])

    return model
    
def weighted_categorical_crossentropy(weights):
    """
    A weighted version of keras.objectives.categorical_crossentropy
    
    Variables:
        weights: numpy array of shape (C,) where C is the number of classes
    
    Usage:
        weights = np.array([0.5,2,10]) # Class one at 0.5, class 2 twice the normal weights, class 3 10x.
        loss = weighted_categorical_crossentropy(weights)
        model.compile(loss=loss,optimizer='adam')
    """
    
    weights = K.variable(weights)
        
    def loss(y_true, y_pred):
        # scale predictions so that the class probas of each sample sum to 1
        y_pred /= K.sum(y_pred, axis=-1, keepdims=True)
        # clip to prevent NaN's and Inf's
        y_pred = K.clip(y_pred, K.epsilon(), 1 - K.epsilon())
        # calc
        loss = y_true * K.log(y_pred) * weights
        loss = -K.sum(loss, -1)
        return loss
    
    return loss


##===============================================================
## Result Analysis 
## Generate train result df and valid result df for error analysis
##===============================================================
def evaluate_scores(preds_train, preds_valid, y_train, y_valid, train_scores, valid_scores, i):
    if CLF_MODE == 'Binary':
        preds_valid = preds_valid[:, 0]
        preds_train = preds_train[:, 0]
        valid_score = metrics.roc_auc_score(y_valid, preds_valid)
        train_score = metrics.roc_auc_score(y_train, preds_train)
        print('Val Score:{} for fold {}'.format(valid_score, i))
        print('Train Score: {} for fold {}'.format(train_score, i))
        valid_scores.append(valid_score)
        train_scores.append(train_score)
        print('Avg Train Score:{0:0.5f}, Val Score:{1:0.5f} after {2:0.5f} folds'.format
              (np.mean(train_scores), np.mean(valid_scores), i))
    elif CLF_MODE == 'MultiClass':
        valid_scores_class = []
        train_scores_class = []
        for col, clazz in enumerate([0, 1, 2, 3, 5]):
            if (y_valid == clazz).any():
                valid_score = metrics.roc_auc_score((y_valid == clazz), preds_valid[:, col])
            else:
                valid_score = 0
            if (y_train == clazz).any():
                train_score = metrics.roc_auc_score((y_train == clazz), preds_train[:, col])
            else:
                train_score = 0
            print('Val Score:{} for fold {},class {}'.format(valid_score, i, clazz))
            print('Train Score: {} for fold {}, class {}'.format(train_score, i, clazz))
            valid_scores_class.append(valid_score)
            train_scores_class.append(train_score)
        valid_scores.append(valid_scores_class)
        train_scores.append(train_scores_class)
        for clazz, scores in enumerate(zip(np.mean(train_scores, axis=0), 
                                           np.mean(valid_scores, axis=0))):
            if clazz == 4:
                clazz = 5
            #print('Class {} Avg Train Score:{0:0.5f}, Val Score:{1:0.5f} after {2:0.5f} folds'.format
            print('Class {} Avg Train Score:{}, Val Score:{} after {} folds'.format
                  (clazz, scores[0], scores[1], i))
    return preds_train, preds_valid

def gen_res_df(y, preds, index, folder, df):
    tmp1_df = pd.DataFrame()
    tmp1_df['gt'] = y
    assert len(np.shape(preds)) <= 2, "Preds dimession missmatch"
    if len(np.shape(preds)) == 2:
        for i in range(np.shape(preds)[1]):
            tmp1_df['preds_'+str(i)] = preds[:, i]
    else:
        tmp1_df['preds'] = preds
    tmp1_df['index'] = index
    tmp1_df['folder'] = folder
    df = df.append(tmp1_df, ignore_index=True)
    print(df.head())
    return df

#==============================
##  Generator
#==============================
def trn_generator(x, batch_size, clf_mode, clahe_param=[5, (2, 2)]):
    #create clahe instance
    clahe = cv2.createCLAHE(clipLimit=clahe_param[0], tileGridSize=clahe_param[1])
    # eye array for one hot 
    one_hot_target = np.eye(class_num)
    
    while True:
        for start in range(0, len(x), batch_size):
            x_batch = []
            y_batch = []
            end = min(start + batch_size, len(x))
            train_batch = x[start:end]
            for _, series in train_batch.iterrows():
                filepath = series['name']
                if clf_mode == 'Binary':
                    tag = series['gt']
                elif clf_mode == 'MultiClass':
                    gt = int(series['gt'])
                    tag = one_hot_target[gt if gt < 5 else 4]
                    #if gt == 5:
                    #    tag = one_hot_target[4]
                    #else:
                        
                #assert type(filepath)=='str',train_batch.info()
                #print(tag)
                assert os.path.exists(filepath), "File did not exists: {}".format(filepath)
                img = cv2.imread(filepath)
                x_batch.append(img)
                y_batch.append(tag)
                
            contrast_enhance(x_batch, COLOR_MODE, clahe)
                
            for i, img in enumerate(x_batch):
                if PADDING_METHOD == 'Double_ZoomOut_Padding':
                    if (np.shape(img)[0] >= 150) or (np.shape(img)[1] >= 150):
                        img = oversize_crop(img, img_size, 2)
                    img = double_size_and_padding(img, img_size, (0, 0, 0))
                elif PADDING_METHOD == 'Padding':
                    img = padding(img, img_size, (0, 0, 0))
                elif PADDING_METHOD == 'Warp':
                    img = cv2.resize(img, img_size)
                else:
                    print("Not supported Padding method.")
                    exit(-1)
                if AUGMENTATION == 'RandomRotate':
                    img = augment(img, np.random.randint(6))
                x_batch[i] = img
                
            
            for i, img in enumerate(x_batch):
                assert img.shape[:-1] == img_size, "img size error: No.{}, Size {}".format(i, img.shape)
                    
            #print(type(x_batch))
            #print(x_batch)
            x_batch = np.array(x_batch, np.float32) / 255.
            y_batch = np.array(y_batch, np.uint8)
            #   print(np.unique(y_batch))
            yield x_batch, y_batch

def pred_generator(x, batch_size, clahe_param=[5, (2, 2)]):
    #create clahe instance
    clahe = cv2.createCLAHE(clipLimit=clahe_param[0], tileGridSize=clahe_param[1])
    while True:
        for start in range(0, len(x), batch_size):
            x_batch = []
            end = min(start + batch_size, len(x))
            test_batch = x[start:end]
            for _, series in test_batch.iterrows():
                filepath = series['name']
                assert os.path.exists(filepath), "File did not exists: {}".format(filepath)
                img = cv2.imread(filepath)
                x_batch.append(img)
            
            #do contrast enhancment for the batch 
            contrast_enhance(x_batch, COLOR_MODE, clahe)
            
            for i, img in enumerate(x_batch):    
                if PADDING_METHOD == 'Double_ZoomOut_Padding':
                    if (np.shape(img)[0] >= 150) or (np.shape(img)[1] >= 150):
                        img = oversize_crop(img, img_size, 2)
                    img = double_size_and_padding(img, img_size, (0, 0, 0))
                elif PADDING_METHOD == 'Padding':
                    img = padding(img, img_size, (0, 0, 0))
                elif PADDING_METHOD == 'Warp':
                    img = cv2.resize(img, img_size)
                else:
                    print("Not supported Padding method.")
                    exit(-1)
                if AUGMENTATION == 'RandomRotate':
                    img = augment(img, np.random.randint(6))
                x_batch[i] = img
                
            x_batch = np.array(x_batch, np.float32) / 255.
            yield x_batch

##==========================================================
# # Hyper-Param Tuning for Train Model, 
# Here we use 5-fold cross-validation to train the model.
# Submission file is saved with the average of all folds. 
# Additionally, prediction arrays are saved for each fold in 
# case we want to hand-pick results from an individual fold.
#============================================================
def train_model_kf(model, batch_size, epochs, img_size, x, y, test, n_fold, skf, clf_mode):
    if clf_mode == 'Binary':
        preds_test = np.zeros(len(test), dtype=np.float)
    elif clf_mode == 'MultiClass':
        preds_test = np.zeros((len(test), 5), dtype=np.float)
    train_scores = []; valid_scores = []

    i = 1
    trn_df = pd.DataFrame()
    val_df = pd.DataFrame()
    
    init_weights = model.get_weights()
    if clf_mode == 'Binary':
        if LOSS_WEIGHTS is not None:
            print("Not support Weighted binary cross entropy loss.")
            exit(-1)
            pass
        else:
            print("LOSS_WEIGHTS is not set, use binary cross entropy loss")
            loss_func = 'binary_crossentropy'
            
    elif clf_mode == 'MultiClass':
        if LOSS_WEIGHTS is not None:
            global class_num
            assert len(LOSS_WEIGHTS) == class_num, "LOSS_WEIGHTS shape is not as same as class_num"
            loss_func = weighted_categorical_crossentropy(LOSS_WEIGHTS)
        else:
            print("LOSS_WEIGHTS is not set, use categorical cross entropy loss")
            loss_func = 'categorical_crossentropy'
        
    

    #for train_index, test_index in kf.split(x):
    for train_index, test_index in skf.split(x, y):
        #to prevent file wirte confilct,use CUDA_DEVICE No. to seperate the tmp files
        tmp_dir = './tmp'+CUDA_DEVICE
        preds_train = np.zeros(len(train_index), dtype=np.float)
        x_train = x.iloc[train_index]; x_valid = x.iloc[test_index]
        #x_train = dataset_augment(x_train, tmp_dir)
        x_train = dataset_augment(x_train, img_size, tmp_dir)

        
        print("Train set shape: {} after k_fold..".format(x_train.shape))
        print("Valid set shape: {} after k_fold..".format(x_valid.shape))
        
        if clf_mode == 'Binary':
            x_train['gt'] = (x_train['gt'] > 0).astype(np.uint8)
            x_valid['gt'] = (x_valid['gt'] > 0).astype(np.uint8)
        #elif clf_mode == 'MultiClass':
        #    one_hot_trn = pd.get_dummies(x_train['gt'])
        #    x_train = pd.concat([x_train, one_hot_trn], axis=1)
        #     one_hot_vld = pd.get_dummies(x_valid['gt'])
        #    x_valid = pd.concat([x_valid, one_hot_vld], axis=1)
        #    for trn, val in zip(x_train.columns, x_valid.columns):
        #        assert trn == val, "Category missmatch, trn:{}, val:{}".\
        #                        format(x_train.columns, x_valid.columns)
        
        y_train = x_train['gt']; y_valid = x_valid['gt']
        
        print(x_train.head())
        print(x_valid.head())

        clahe_param = [5, (2, 2)]
        
        train_generator = trn_generator(x_train, batch_size, clf_mode, clahe_param)
        valid_generator = trn_generator(x_valid, batch_size, clf_mode, clahe_param)
        
        train_generator_p = pred_generator(x_train, batch_size, clahe_param)
        valid_generator_p = pred_generator(x_valid, batch_size, clahe_param)
        test_generator = pred_generator(test, batch_size, clahe_param)
        
        callbacks = [EarlyStopping(monitor='val_loss', patience=5, verbose=1, min_delta=1e-4),
                     ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=1, cooldown=1, 
                                       verbose=1, min_lr=1e-7),
                     ModelCheckpoint(filepath=('./weights/inception.fold_' + str(i) + '_{}'*len(param_list) + '.hdf5').format(*param_list), 
                                     verbose=1, save_best_only=True, save_weights_only=True, mode='auto')]

        train_steps = len(x_train) / batch_size
        valid_steps = len(x_valid) / batch_size
        test_steps = len(test) / batch_size
        
        print(loss_func)
        model.compile(optimizer=Adam(lr=1e-4), loss=loss_func, 
                             metrics = ['accuracy'])

        model.fit_generator(train_generator, train_steps, epochs=epochs, verbose=1, 
                            callbacks=callbacks, validation_data=valid_generator, 
                            validation_steps=valid_steps)

        model.load_weights(filepath=('./weights/inception.fold_' + str(i) + '_{}'*len(param_list) + '.hdf5').format(*param_list))

        print('Running validation predictions on fold {}'.format(i))
        preds_valid = model.predict_generator(generator=valid_generator_p,
                                              steps=valid_steps, verbose=1)
        

        print('Running train predictions on fold {}'.format(i))
        preds_train = model.predict_generator(generator=train_generator_p,
                                              steps=train_steps, verbose=1)
        print(np.shape(preds_valid), np.shape(preds_train))
                
        preds_train, preds_valid = evaluate_scores(preds_train, preds_valid, y_train, y_valid,
                                                   train_scores, valid_scores, i)
            
        trn_df = gen_res_df(y_train, preds_train, 0, i, trn_df)
        val_df = gen_res_df(y_valid, preds_valid, 0, i, val_df)
        
        
        print('Running test predictions with fold {}'.format(i))

        preds_test_fold = model.predict_generator(generator=test_generator,
                                                  steps=test_steps, verbose=1)
        
        if clf_mode == 'Binary':
            preds_test_fold = preds_test_fold[:, -1]

        preds_test += preds_test_fold

        print('\n\n')

        i += 1

        if i <= n_fold:
            print('Now beginning training for fold {}\n\n'.format(i))
            model.set_weights(init_weights)
        else:
            print('Finished training!')

    preds_test /= n_fold
    trn_df.to_csv(('./train_analysis/train_result'+'_{}'*len(param_list)+'.csv').format(*param_list))
    val_df.to_csv(('./train_analysis/valid_result'+'_{}'*len(param_list)+'.csv').format(*param_list))


    return preds_test
#================================
## train single fold
#================================
def train_model_single(model, batch_size, epochs, img_size, train_df, valid_df, clf_mode):
    trn_df = pd.DataFrame()
    val_df = pd.DataFrame()

    tmp_dir = './tmp'+CUDA_DEVICE
    preds_train = np.zeros(len(train_df), dtype=np.float)
    x_train = train_df; x_valid = valid_df
    x_train = dataset_augment(x_train, img_size, tmp_dir)
        
    print("Train set shape: {} ".format(x_train.shape))
    print("Valid set shape: {} ".format(x_valid.shape))
        
        
    if clf_mode == 'Binary':
        loss_func = 'binary_crossentropy'
        x_train['gt'] = (x_train['gt'] > 0).astype(np.uint8)
        x_valid['gt'] = (x_valid['gt'] > 0).astype(np.uint8)
    elif clf_mode == 'MultiClass':
        loss_func = 'categorical_crossentropy'
        one_hot_trn = pd.get_dummies(x_train['gt'])
        x_train = pd.concat([x_train, one_hot_trn], axis=1)
        one_hot_vld = pd.get_dummies(x_valid['gt'])
        x_valid = pd.concat([x_valid, one_hot_vld], axis=1)
        for trn, val in zip(x_train.columns, x_valid.columns):
            assert trn == val, "Category missmatch, trn:{}, val:{}".\
                                format(x_train.columns, x_valid.columns)
        
    y_train = x_train['gt']; y_valid = x_valid['gt']
    
    print(x_train.head())
    print(x_valid.head())
    
    clahe_param = [5, (2, 2)]
    
    train_generator = trn_generator(x_train, batch_size, clf_mode, clahe_param)
    valid_generator = trn_generator(x_valid, batch_size, clf_mode, clahe_param)
    
    train_generator_p = pred_generator(x_train, batch_size, clahe_param)
    valid_generator_p = pred_generator(x_valid, batch_size, clahe_param)
    
    callbacks = [EarlyStopping(monitor='val_loss', patience=5, verbose=1, min_delta=1e-4),
                 ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=1, cooldown=1, 
                                   verbose=1, min_lr=1e-7),
                 ModelCheckpoint(filepath=('inception_single_' + '_{}'*len(param_list) + '.hdf5').format(*param_list), 
                                 verbose=1, save_best_only=True, save_weights_only=True, mode='auto')]
 
    train_steps = len(x_train) / batch_size
    valid_steps = len(x_valid) / batch_size
    
    model = model
    #model.compile(optimizer=Adam(lr=1e-4), loss='binary_crossentropy', 
    #                     metrics = ['accuracy'])
 
    model.compile(optimizer=Adam(lr=1e-4), loss=loss_func, 
                             metrics = ['accuracy'])
    model.fit_generator(train_generator, train_steps, epochs=epochs, verbose=1, 
                        callbacks=callbacks, validation_data=valid_generator, 
                        validation_steps=valid_steps)
 
    model.load_weights(filepath=('inception_single_' + '_{}'*len(param_list) + '.hdf5').format(*param_list))
 
    print('Running validation predictions}')
    preds_valid = model.predict_generator(generator=valid_generator_p,
                                          steps=valid_steps, verbose=1)
    
 
    print('Running train predictions')
    preds_train = model.predict_generator(generator=train_generator_p,
                                          steps=train_steps, verbose=1)
    print(np.shape(preds_valid), np.shape(preds_train))
            
    preds_train, preds_valid = evaluate_scores(preds_train, preds_valid, y_train, y_valid,
                                               [], [], 0)
                                               
    if clf_mode == 'Binary':
        preds_test = preds_valid[:, -1]
    elif clf_mode == 'MultiClass':
        preds_test = preds_valid
        
    trn_df = gen_res_df(y_train, preds_train, 0, 0, trn_df)
    val_df = gen_res_df(y_valid, preds_valid, 0, 0, val_df)
    
    print('\n\n')
 
 
    print('Finished training!')

    trn_df.to_csv(('./train_analysis/train_result'+'_{}'*len(param_list)+'.csv').format(*param_list))
    val_df.to_csv(('./train_analysis/valid_result'+'_{}'*len(param_list)+'.csv').format(*param_list))


    return preds_test
#padding_methods = ["Double_ZoomOut_Padding", "Padding","Warp"]
#cuda_devices = '0,1,2,3,4,5,6,7'
#augmentations = ['Minority', 'RandomRotate', "Majority_Down_Minority_Up",Majority_Down]
#split_method = ["CellBased", "FovBased"]
#clf_modes = ['Binary', 'MultiClass']
#================================================
# Tool functions
#================================================
def copy_data_by_type(df,dst_dir):
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    
    CLASS = ['Norm', 'LSIL', 'HSIL', 'HPV', 'SCC']
    gt = [0, 1, 2, 3, 4]

    for i, t in enumerate(gt):
        try:
            tmp_df = df.loc[df['gt']==t]
        except:
            tmp_df = df.loc[df['positive']==t]
        path = os.path.join(dst_dir, CLASS[i])
        if not os.path.exists(path):
            os.mkdir(path)
        for _, row in tmp_df.iterrows():
            src_path = row['name']
            names = src_path.split('/')[-3] + '_' + src_path.split('/')[-1]
            dst_path = os.path.join(path,names)
            shutil.copy(src_path, dst_path)

def input_statistics(df):
    global CLASS
    gts = df['gt'].unique()
    gts.sort()
    print("================================")
    for gt, c in zip(gts, CLASS):
        num = len(df.loc[df['gt']==gt])
        print("Num of Class {} Cell: {} ".format(c, num))
    print('================================')
        
#====================
# main
#====================
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Cervix Cancer Classifier Training')
    parser.add_argument('--resize_method', required=True,
                        metavar="{Double_ZoomOut_Padding, Padding, Warp}",
                        help='how to resize the image to fit input shape requirement')
    parser.add_argument('--augment',required=True,
                        metavar="{Minority, RandomRotate, Majority_Down_Minority_Up}",
                        help='how to augment data in train set')
    parser.add_argument('--split_method', required=True,
                        metavar="{CellBased, FovBased}",
                        help='Directory to Segment cell images for classfication ')
    parser.add_argument('--dropout',
                        default=0.5,
                        help="dropout value",
                        type=float)
    parser.add_argument('--clf_mode',required=True, 
                        metavar="{Binary,MultiClass}",
                        help='classifier mode, binary classifier or multi-class classifier')
    parser.add_argument('--kfold',
                        default=5,
                        help="Number of kflods use in CV, if kfold=0, only do the train test split",
                        type=int)
    parser.add_argument('--downsample_ratio',
                        default=0.5,
                        help="Majority down sample ratio",
                        type=float)
    parser.add_argument('--cuda_device',
                        default='0',
                        help='use with cuda_device for training')
    parser.add_argument('--color_mode',
                        metavar="{RGB,HSV,HSV_CLAHE_V,HSV_CLAHE_S,HSV_CLAHE_SV,LAB_CLAHE_L}",
                        default='RGB',
                        help='classifier mode, binary classifier or multi-class classifier')
    parser.add_argument('--input_form',
                        metavar="{CSV, FOLDER}",
                        default='CSV',
                        help='input dataset storage format, if stored as FOLDER, need to confirm the dictionary structure')
    parser.add_argument('--input_shape',
                        default=[299, 299],
                        type=int,
                        nargs='+',
                        help='set input shape')
    parser.add_argument('--loss_weights',
                        default=None,
                        type=float,
                        #help='use weighted loss function as loss function')
                        nargs='+',
                        help='set input shape')
    args = parser.parse_args()
    print(args)
    
    #CUDA_DEVICE = "7"
    #PADDING_METHOD = "Double_ZoomOut_Padding"
    #AUGMENTATION = "RandomRotate"
    #SPLIT_METHOD = "CellBased" #train test split method
    #DROPOUT = 0.5
    #CLF_MODE = 'MultiClass'
    #RANDOM_SEED = 15
    #K_FOLD = 5
    #K_FOLD = 5
    #COLOR_MODEL = 'RGB','HSV&CLAHE'
    CUDA_DEVICE = args.cuda_device
    PADDING_METHOD = args.resize_method
    AUGMENTATION = args.augment
    SPLIT_METHOD = args.split_method #train test split method
    DROPOUT = args.dropout
    CLF_MODE = args.clf_mode
    RANDOM_SEED = 15
    #K_FOLD = 5
    K_FOLD = args.kfold
    RATIO = args.downsample_ratio
    INPUT_FORM = args.input_form
    
    COLOR_MODE = args.color_mode
    LOSS_WEIGHTS = args.loss_weights
    
    if LOSS_WEIGHTS is not None:
        WEIGHTED_LOSS = 'WeightedLoss'
    else:
        WEIGHTED_LOSS = 'NormalLoss'
    
    
    
    
    img_height = args.input_shape[0]
    img_width = args.input_shape[1]
    
    print("Color Mode: %s" % COLOR_MODE)
    
    
    CLASS = ['Norm', 'LSIL', 'HSIL', 'HPV', 'SCC']
    param_list = [PADDING_METHOD, AUGMENTATION, SPLIT_METHOD, DROPOUT, CLF_MODE, COLOR_MODE, WEIGHTED_LOSS]
    
    
    os.environ["CUDA_VISIBLE_DEVICES"] = CUDA_DEVICE

    # # Load Datasets
    # Since we will be using a generator we don't need to actually load in any files into memory, all we need is the filepaths :)
    #PATH = '../../../'
    PATH = './'
    train_path = os.path.join(PATH, 'train_datasets') 
    test_path =  os.path.join(PATH, 'test_datasets')
    
    if INPUT_FORM == 'CSV':
        _, train_set, train_label = load_train(PATH)
        #_, train_set, _ = load_train(path)
        print(train_set.head())
    
        copy_data_by_type(train_set, train_path)
    
        #test_files, test_set = load_test(path)
        _, test_set = load_test(PATH)
        print(test_set.head())
    
        copy_data_by_type(test_set, test_path)
    elif INPUT_FORM == 'FOLDER':
        _, train_set, train_label = load_train_from_folder(train_path)
        _, test_set = load_test_from_folder(test_path)
        
    
    input_statistics(train_set)
    input_statistics(test_set)
    print("Train set shape: {} after loading..".format(train_set.shape))
    print("Test set shape: {} after loading..".format(test_set.shape))
    
    if SPLIT_METHOD == "CellBased":
        #Join the train set and test set to data_set
        data_set = train_set.append(test_set[['name', 'gt']], ignore_index=True)
        del train_set, test_set, train_label
        #Cell-based train test splits
        train_set, test_set = train_test_split(data_set, test_size=0.15, 
                                               stratify=data_set['gt'], 
                                               random_state=RANDOM_SEED)
        train_set = train_set.reset_index(drop=True)
        test_set = test_set.reset_index(drop=True)
        #rewrite train label
        train_label = train_set['gt'].values.copy()
        print(train_set.info())
    elif SPLIT_METHOD == "FovBased":
        pass
    else:
        print("Unknow train test split method: %s"%SPLIT_METHOD)
        exit(-1)
    
    
    print("Train set shape: {} after train_test_split..".format(train_set.shape))
    print("Test set shape: {} after train_test_split..".format(test_set.shape))

    #define Keras classifier model
    img_channels = 3
    img_dim = (img_height, img_width, img_channels)
    if CLF_MODE == 'MultiClass':
        class_num = 5
    elif CLF_MODE == 'Binary':
        class_num = 1
    else:
        print("Not support CLF_MODE: %s"%CLF_MODE)
        exit(-1)
        pass
    

    
    model = inceptionv3(img_dim, dropout=DROPOUT, clf_mode=CLF_MODE, class_num=class_num)
    print(get_flops(model))
    model.summary()
    

    batch_size = 50
    epochs = 50
    n_fold = K_FOLD
    img_size = (img_height, img_width)
    #kf = KFold(n_splits=n_fold, shuffle=True)
    
    if n_fold != 0:
        skf = StratifiedKFold(n_splits=n_fold, shuffle=True)
        print("n-Fold: %d"%skf.get_n_splits(train_set, train_label))
        test_pred = train_model_kf(model, batch_size, epochs, img_size, train_set, 
                                   train_label, test_set, n_fold, skf, clf_mode=CLF_MODE)
    else:
        test_pred = train_model_single(model, batch_size, epochs, img_size, train_set, 
                                       test_set, clf_mode=CLF_MODE)
    #test_pred = train_model_kf(model, batch_size, epochs, img_size, train_set, 
    #                        train_label, test_files, n_fold, kf)

    print(len(np.shape(test_pred)))
    assert len(np.shape(test_pred)) <= 2, "Test Preds dimession missmatch"
    if len(np.shape(test_pred)) == 2:
        for i in range(np.shape(test_pred)[1]):
            test_set['positive_'+str(i)] = test_pred[:, i]
    else:
        test_set['positive'] = test_pred
    test_set.to_csv(('./train_analysis/submission'+'_{}'*len(param_list)+'.csv').format(*param_list), index=None)

