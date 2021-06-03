## CervicAI 

This repository contains the Python (ML)/Go (GUI) implementation for our  
            <B>Cervical Cancer AI System for Individual End User</B>


Specially thanks for the open source codes shared by [*caogang/wgan-gp*](https://github.com/caogang/wgan-gp) and [*DigitalSlideArchive/HistomicsTK*](https://github.com/DigitalSlideArchive/HistomicsTK)

### Requirements

* [*Pytorch*](https://github.com/pytorch/pytorch)
* [*HistomicsTK*](https://github.com/DigitalSlideArchive/HistomicsTK)
* [*An Unofficial Compiled Version of HistomicsTK (Python 3.5.6, GCC 7.3.0, Ubuntu 16.04.3 LTS)*](https://drive.google.com/file/d/10jisjIPYJrYxhDTyQaNTZFmwx9QaXhZr/view?usp=sharing)


### Usage

#### 1) Download Data

- Dataset A: [*Google Drive*](https://drive.google.com/file/d/10h1cJBiLcc9oGyWWea_2d0gefRo_GXfJ/view?usp=sharing)
- Dataset B: [*Google Drive*](https://drive.google.com/file/d/1kYik0ByDPiK94Xt4mvoV3lOah2Zfx3dH/view?usp=sharing)
- (original images: [*Google Drive*](https://drive.google.com/drive/folders/1GmFM8TEGMVdh17_F_rXxR6dR8ha20y8w?usp=sharing))

#### 2) Extract

The default path should be *./experiemnt/data*. 
You can make new directory */experiment* under the root, extract the data, then rename the directory name to *data*.
You can also open *nu_gan.py* to change the default path.

#### 3) Usage

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
