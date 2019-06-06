import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import cv2
import glob
import ntpath
import os

import torchvision.utils as vutils
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
import random
from PIL import Image
import torch
import torch.utils.data as data
import torch.nn as nn
from torchvision import datasets, models, transforms
from torch.autograd import Variable

#data_dir = 
#data_dir = '../input'

def load_img(img_path):
    with open(img_path, 'rb') as f:
        with Image.open(f) as img_f:
            return img_f.convert('RGB').resize((320,320))
# define custom dataset
class MyDataSet(data.Dataset):
    def __init__(self, filename, training=True, validating=False, train_percent=0.85, transforms=None, data_dir='datasets_train'):
        df = pd.read_csv(filename)
        if training:
            print("Dataset #1")
            split_index = (int)(df.values.shape[0]*train_percent)
            if validating:
                split_data = df.values[split_index:]
            else:
                split_data = df.values[:split_index]
            imgs = [None]*split_data.shape[0]
            labels = [None]*split_data.shape[0]
            for i, row in enumerate(split_data):
                fn, labels[i] = row
                print(fn)
                img_path = data_dir + '/train/' + str(fn) 
                imgs[i] = load_img(img_path)
        else:
            imgs = [None]*df.values.shape[0]
            for i, row in enumerate(df.values):
                fn, _ = row
                img_path = data_dir + '/' + str(fn) 
                imgs[i] = load_img(img_path)
        self.imgs = imgs
        self.training = training
        self.transforms = transforms
        self.num = len(imgs)
        if self.training:
            self.labels = np.array(labels, dtype=np.float32)
    def __getitem__(self, index):
        if not self.transforms is None:
            img = self.transforms(self.imgs[index])
        if self.training:
            return img, self.labels[index]
        else:
            return img
    def __len__(self):
        return self.num

# define data augumentation

def randomRotate(img):
    angel = random.randint(0,4) * 90
    return img.rotate(angel)
 
data_transforms = {
    'train': transforms.Compose([
        transforms.RandomSizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.Lambda(lambda x: randomRotate(x)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'test': transforms.Compose([
        transforms.Scale(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
}

def get_data_loader(filename='train_labels1.csv', training=True, validating=False, shuffle=True, data_dir='datasets_train'):
    if training and not validating:
        transkey = 'train'
    else:
        transkey = 'test'
    dset = MyDataSet(filename, training=training, validating=validating, transforms=data_transforms[transkey], data_dir=data_dir)
    loader = torch.utils.data.DataLoader(dset, batch_size=16, shuffle=shuffle, num_workers=4)
    loader.num = dset.num
    return loader

def lr_scheduler(optimizer, epoch, init_lr=0.001, lr_decay_epoch=8):
    lr = 0
    for param_group in optimizer.param_groups:
        lr = param_group['lr']
    if epoch % lr_decay_epoch == 0 and epoch >= lr_decay_epoch:
        lr = lr * 0.6
    if epoch % lr_decay_epoch == 0 and epoch >= lr_decay_epoch:
        print('LR is set to {}'.format(lr))
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr
    return optimizer    

weight_file = 'best_model.pth'

def do_train(net, criterion, optimizer, lr_scheduler, epochs=100):
    print("Dataset ##1")
    data_loaders = {'train': get_data_loader(), 'valid': get_data_loader(validating=True)}
    best_model = net
    best_acc = 0
    for epoch in range(epochs):
        print('Epoch {}/{}'.format(epoch, epochs))
        for phase in ['train', 'valid']:
            if phase == 'train':
                optimizer = lr_scheduler(optimizer, epoch)
                net.train(True)
            else:
                net.train(False)
            running_loss = 0.
            running_corrects = 0
            for imgs, labels in data_loaders[phase]:
                imgs, labels = Variable(imgs.cuda()), Variable(labels.cuda())
                optimizer.zero_grad()
                outputs = net(imgs)
                preds = torch.ge(outputs.data, 0.5).resize_(labels.data.size())
                loss = criterion(outputs, labels)
                if phase == 'train':
                    loss.backward()
                    optimizer.step()
                running_loss += loss.item()
                
                running_corrects += torch.sum(preds.int() == labels.data.int())
                
            #print("running_corrects", running_corrects.item(), data_loaders[phase].num)
                
            epoch_loss = running_loss / data_loaders[phase].num
            epoch_acc = running_corrects.item() / data_loaders[phase].num * 1.0
            print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))
            if phase == 'valid' and epoch_acc > best_acc:
                best_acc = epoch_acc
                torch.save(net.state_dict(), weight_file)
                best_model = net
    print('Best validation accuracy: {:4f}'.format(best_acc))
    return best_model
                


def get_dense201():
    net = models.densenet201(pretrained=True)
    net.classifier = nn.Sequential(nn.Linear(net.classifier.in_features, 1), nn.Sigmoid())
    return net.cuda()

def train_net():
    print("get net")
    net = get_dense201()
    print("get net ok")
    
    criterion = nn.BCELoss()
    optimizer = torch.optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    do_train(net, criterion, optimizer, lr_scheduler)


def predict(net, sample_submission, data_dir):
    loader = get_data_loader(filename=sample_submission, training=False, shuffle=False, data_dir=data_dir)
    preds = []
    net.eval()
    for i, img in enumerate(loader, 0):
        inputs = Variable(img.cuda())
        outputs = net(inputs)
        pred = outputs.data.cpu().tolist()
        for p in pred:
            preds.append(p)
    return np.array(preds)

def submit(preds, sample_submission, filename, data_dir, npy_outdir, preview_outdir, base_filename):
    df = pd.read_csv(sample_submission) 
    df['positive'] = preds 
    #print(df.head())
    df.to_csv(filename, index=False)
    
    image_dict = None
    
    for index, row in df.iterrows():
        # access data using column names
        print(index, row['name'], row['positive'])
        
        if row['positive'] < 0.3:
            filename = os.path.join('{}/{}'.format(data_dir, row['name']))
        
            original = cv2.imread(filename)
            original = original[:,:,::-1]
            resize_image = cv2.resize(original, (32, 32))
            
            m = np.array([resize_image])
            if image_dict is not None:
                image_dict = np.append(image_dict, m,  axis=0)
            else:
                image_dict = m
        
        
    preview_npy = os.path.join(npy_outdir, '%s_predicted.npy'%base_filename)    
    image = image_dict #np.array(image_dict)
    
    if image is None:
        return
    np.save(preview_npy, image)
    
    print(image.shape)
    image = np.transpose(image, (0,3,1,2))
    print(image.shape)
    
    preview_segpng = os.path.join(preview_outdir, '%s_seg_predicted.png'%base_filename)   
    vutils.save_image(torch.FloatTensor(image), preview_segpng ,nrow=10,padding=2, normalize=True)
    

if False:
    train_net()

if False:
    net = get_dense201()
    net.load_state_dict(torch.load(weight_file))
    preds = predict(net)
    submit(preds, 'submission.csv')
    

def process_origin_image(net):

    # Split train set
    total_images = np.sort(glob.glob(os.path.join(ORIGIN_DIR, FILE_PATTERN)))
    print(total_images)
    print('Num of total images: {}'.format(len(total_images)))

    for source in total_images:
        filename = ntpath.basename(source)
        base_filename = os.path.splitext(filename)[0]
        print("item", base_filename)

        
        filename = os.path.join('{}/{}.png_output'.format(ROOT_FOLDER, ntpath.basename(base_filename)))
    
        data_dir = os.path.join('{}/crops'.format(filename))
        preview_outdir = os.path.join('{}/preview'.format(filename))
        npy_outdir = os.path.join('{}/npy/'.format(ROOT_FOLDER))
        
        sample_submission = os.path.join(preview_outdir, 'sample_submission.csv')
        submission = os.path.join(preview_outdir, 'submission.csv')
        
        if os.path.exists(sample_submission):
            preds = predict(net, sample_submission, data_dir)
            submit(preds, sample_submission, submission, data_dir, npy_outdir, preview_outdir, base_filename)
        


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Cervix Cancer Detection Step 3: Crop FOV into cells')
    parser.add_argument('--origindir', required=True,
                        metavar="/path/to/origin/FOV/images/*/*...",
                        help='Directory to FOV images, for images in subdir, use */*/')
    
    parser.add_argument('--filepattern',
                        default='*.png',
                        help='select the files with the suffix pattern,e.g. *.png,*.jpg ')
    
    parser.add_argument('--datasets', required=True,
                        metavar="/path/to/datasets",
                        help='Directory to cell images for classfication ')
    
    args = parser.parse_args()
    ORIGIN_DIR = args.origindir
    FILE_PATTERN = args.filepattern
    ROOT_FOLDER = args.datasets 
    
    net = get_dense201()
    net.load_state_dict(torch.load(weight_file))
    process_origin_image(net)