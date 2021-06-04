# CervicAI 

## Who do we address?
* Patitents: uploading your cervical images and know the prodiction in few minutes: ![image](https://user-images.githubusercontent.com/75286/120696241-2cf41e80-c461-11eb-9bd6-3633df2bcd66.png)


* Doctors: screening cervical images to save you a lot of time: ![image](https://user-images.githubusercontent.com/75286/120696959-008cd200-c462-11eb-85a8-bdf35047aa16.png)


* Labeling expert:  Automatically label unlabeled data for you: ![image](https://user-images.githubusercontent.com/75286/120697215-4cd81200-c462-11eb-89bd-fbdfa2bad19e.png)


* Machine learning enginers / Data scientists:  
![image](https://user-images.githubusercontent.com/75286/120869922-6e152d00-c54c-11eb-9a91-4374cb82666d.png)
  We do
  - How to find the dupicated images
  - How to find the similar images
  - How to find the bias images
  - How to pick the important images
  - How to train the imbalanced images
  
  We don't
  - address bias by adjusting layers, hyper-parameters
  - get high score by fine turn anyting 
  - have any INNOVATION but leveraging existed/proved technologies such as PCA, SimCLR, etc.  

## What technologies we integrated?
* Semi-Self supervised learning: [*SimCLR(Google)*](https://github.com/google-research/simclr),  [*SwAV(Facebook)*](https://github.com/facebookresearch/swav),    [*Dino(Facebook)*](https://github.com/facebookresearch/dino)
  - Why Semi-Self supervised learning: domain expert (doctor) is expensive, labling time is very long.
* Active learning: [*Detectron2(Facebook)*](https://github.com/facebookresearch/detectron2)
  - Why active learning: Pixies to machine is diffrent to human beings, machine can do better to choose what they need. 

## Usage

### 1) Patients:

- Dataset A: [*Google Drive*](https://drive.google.com/file/d/10h1cJBiLcc9oGyWWea_2d0gefRo_GXfJ/view?usp=sharing)
- Dataset B: [*Google Drive*](https://drive.google.com/file/d/1kYik0ByDPiK94Xt4mvoV3lOah2Zfx3dH/view?usp=sharing)
- (original images: [*Google Drive*](https://drive.google.com/drive/folders/1GmFM8TEGMVdh17_F_rXxR6dR8ha20y8w?usp=sharing))

### 2) Doctors:

The default path should be *./experiemnt/data*. 
You can make new directory */experiment* under the root, extract the data, then rename the directory name to *data*.
You can also open *nu_gan.py* to change the default path.

### 3) Labeling expert:

Three tasks can be chosen using flags as follows.

* Unsupervised Cell-level Classification:
```shell
python nu_gan.py --task 'cell_representation'
```

* Unsupervised Image-level Classification:
```shell
python nu_gan.py --task 'image_classification'
```

* Neuclei Segmentation:
```shell
python nu_gan.py --task 'cell_segmentation'
```

For convenience, the parameters for training is stored in *nu_gan.py*, which can be changed easily.
