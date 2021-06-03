## CervicAI 

### Who do we address?
* Patitents: uploading your cervical images and know the prodiction in few minutes. ![image](https://user-images.githubusercontent.com/75286/120696241-2cf41e80-c461-11eb-9bd6-3633df2bcd66.png)
* Doctors: screening cervical images to save you a lot of time. ![image](https://user-images.githubusercontent.com/75286/120696959-008cd200-c462-11eb-85a8-bdf35047aa16.png)
* Labeling expert:  Automatically label unlabeled data for you.![image](https://user-images.githubusercontent.com/75286/120697215-4cd81200-c462-11eb-89bd-fbdfa2bad19e.png)
* Machine learning enginers / Data scientists:  for unlabeled training data,  1) finding important data; 2) findind features; 3) fiding bias data

### What techinologies we integrated?
* Semi-Self supervised learning: [*SimCLR(Google)*](https://github.com/google-research/simclr),  [*SwAV(Facebook)*](https://github.com/facebookresearch/swav),    [*Dino(Facebook)*](https://github.com/facebookresearch/dino)
* Active learning: [*Detectron2(Facebook)*](https://github.com/facebookresearch/detectron2)


### Usage

#### 1) Patients:

- Dataset A: [*Google Drive*](https://drive.google.com/file/d/10h1cJBiLcc9oGyWWea_2d0gefRo_GXfJ/view?usp=sharing)
- Dataset B: [*Google Drive*](https://drive.google.com/file/d/1kYik0ByDPiK94Xt4mvoV3lOah2Zfx3dH/view?usp=sharing)
- (original images: [*Google Drive*](https://drive.google.com/drive/folders/1GmFM8TEGMVdh17_F_rXxR6dR8ha20y8w?usp=sharing))

#### 2) Doctors:

The default path should be *./experiemnt/data*. 
You can make new directory */experiment* under the root, extract the data, then rename the directory name to *data*.
You can also open *nu_gan.py* to change the default path.

#### 3) Labeling expert:

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
