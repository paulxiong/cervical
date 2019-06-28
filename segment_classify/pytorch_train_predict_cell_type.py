import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import cv2
import glob
import ntpath
import os
import shutil

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
import cv2

#data_dir = 
#data_dir = '../input'

# def load_img(img_path):
#     with open(img_path, 'rb') as f:
#         with Image.open(f) as img_f:
#             img = img_f.convert('RGB').resize((320,320))
#             print(img.shape)
#             return img

def load_img(img_path):
    r = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE).astype("uint8")
    g = r
    b = r
    img = np.dstack((r, g, b))
    
    image = Image.fromarray(img).resize((320,320))
        
    return image

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

def get_data_loader(filename='datasets_train/train_labels1.csv', training=True, validating=False, shuffle=True, data_dir='datasets_train'):
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

weight_file = 'best_model_2.pth'

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

def submit(preds, sample_submission, filename, data_dir, outdir):
    df = pd.read_csv(sample_submission) 
    df['positive'] = preds 
    #print(df.head())
    df.to_csv(filename, index=False)
    
    image_dict = None
    
    for index, row in df.iterrows():
        # access data using column names
        
        
        if row['positive'] < 0.5:
            filename = os.path.join('{}'.format(row['name']))
        
            src_file = os.path.join(data_dir, filename)
            dst_file = os.path.join(outdir, filename)
            shutil.copy(src_file, dst_file)
        else:
            filename = os.path.join('{}'.format(row['name']))
            filename2 = ntpath.basename(filename)
            
            src_file = os.path.join(data_dir, filename)
            dst_file = os.path.join(outdir, 'ABNormal', filename2)
            shutil.copy(src_file, dst_file)

            print(index, row['name'], row['positive'])
            
if False:
    train_net()
    exit()

if False:
    net = get_dense201()
    net.load_state_dict(torch.load(weight_file))
    preds = predict(net)
    submit(preds, 'submission.csv')
    

def process_origin_image(net):

    sample_submission = os.path.join('/opt/yunhai/GAN/github/cervical/Nu_Gan/CellLevel/2019-05-23+2019-01FJ+RedHouse/', 'sample_submission.csv')
    submission = os.path.join('/opt/yunhai/GAN/github/cervical/Nu_Gan/CellLevel/2019-05-23+2019-01FJ+RedHouse/', 'submission.csv')
        
    if os.path.exists(sample_submission):
        preds = predict(net, sample_submission, '/opt/yunhai/GAN/github/cervical/Nu_Gan/CellLevel/2019-05-23+2019-01FJ+RedHouse/dataset/train/')
        submit(preds, sample_submission, submission, '/opt/yunhai/GAN/github/cervical/Nu_Gan/CellLevel/2019-05-23+2019-01FJ+RedHouse/dataset/train/', '/opt/yunhai/GAN/github/cervical/Nu_Gan/CellLevel/2019-05-23+2019-01FJ+RedHouse/dataset/filtered/')
        


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Cervix Cancer Detection Step 3: Crop FOV into cells')

    parser.add_argument('--filepattern',
                        default='*.png',
                        help='select the files with the suffix pattern,e.g. *.png,*.jpg ')
    
    args = parser.parse_args()
    FILE_PATTERN = args.filepattern

    
    net = get_dense201()
    net.load_state_dict(torch.load(weight_file))
    process_origin_image(net)