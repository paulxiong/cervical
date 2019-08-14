import numpy as np
import sklearn
from sklearn.manifold import TSNE
import cv2
# Random state.
RS = 20150101
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import matplotlib
from numpy import *

# We import seaborn to make nice plots.
import seaborn as sns
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5,
                rc={"lines.linewidth": 2.5})

P_dataset = []
P_lable = []
N_dataset = []
N_lable = []
# this function is for read image,the input is directory name
def read_N_directory(directory_name):
    # this loop is for read each image in this foder,directory_name is the foder name with images.
    for filename in os.listdir(r"./"+directory_name):
        #print(filename) #just for test
        #img is used to store the image data 
        image = cv2.imread(directory_name + "/" + filename)
      #  print("image=",image)
        image = cv2.resize(image,(100,100),interpolation=cv2.INTER_CUBIC)
        img = image.flatten()
    #    print(img.shape)
        N_dataset.append(img)
        N_img_dataset = np.matrix(N_dataset)
        lable0 = 0
        N_lable.append(lable0)
        N_number = np.matrix(N_lable)
    #print("N_img=",N_img_dataset)    
   # print("N_lable=",N_lable)    
    print("N",N_number.shape) 
  #  print("N=",N_img_dataset)
    return N_img_dataset,N_lable

     
def read_P_directory(directory_name):
    # this loop is for read each image in this foder,directory_name is the foder name with images.
    for filename in os.listdir(r"./"+directory_name ):
        #print(filename) #just for test
        #img is used to store the image data 
        image = cv2.imread(directory_name + "/" + filename)
     #   ResizeImage(image,img,46,46,type)
        #image = image.resize((46, 46),Image.ANTIALIAS)
        image = cv2.resize(image,(100,100),interpolation=cv2.INTER_CUBIC)
       # print(image.shape)
    #    np.savetxt("./datasets1.tsv",image,delimiter=',')
        img = image.flatten()
       # print(img.shape)
        P_dataset.append(img)   
       # print("dataset",dataset)       
        P_img_dataset = np.matrix(P_dataset)
        lable1 = 1
        P_lable.append(lable1)    
        P_number = np.matrix(P_lable)
   # print("P_lable=",P_lable) 
    print("P",P_number.shape)
    #print("P=",P_img_dataset)
    return P_img_dataset,P_lable

def scatter(x, colors):
    # We choose a color palette with seaborn.
    palette = np.array(sns.color_palette("hls", 10))

    # We create a scatter plot.
    f = plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    sc = ax.scatter(x[:,0], x[:,1], lw=0, s=40,
                    c=palette[colors.astype(np.int)])
    plt.xlim(-25, 25)
    plt.ylim(-25, 25)
    ax.axis('off')
    ax.axis('tight')
    # We add the labels for each digit.
    txts = []
    for i in range(10):
        # Position of each label.
        xtext, ytext = np.median(x[colors == i, :], axis=0)
        txt = ax.text(xtext, ytext, str(i), fontsize=24)
        txt.set_path_effects([
            PathEffects.Stroke(linewidth=5, foreground="w"),
            PathEffects.Normal()])
        txts.append(txt)

    return f, ax, sc, txts

if __name__=="__main__":
  N_img_dataset,N_lable = read_N_directory("cell_N1") 
  P_img_dataset,P_lable = read_P_directory("cell_P2") 
  dataset = np.vstack((N_img_dataset,P_img_dataset))
  lable = np.hstack((N_lable,P_lable))
  print("datasets=",dataset)
#  print("lable=",lable)
#  np.savetxt("./datasets.tsv",dataset,delimiter=',')
#  return dataset,lable
 # dataset,lable = main()
  digits_proj = TSNE(random_state=RS).fit_transform(dataset)
#print("digits_proj",digits_proj)
  scatter(digits_proj, lable)
  plt.savefig('tsne_result.png', dpi=120)
  plt.show()
