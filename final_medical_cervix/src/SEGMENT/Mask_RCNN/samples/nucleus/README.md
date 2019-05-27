# Nuclei Counting and Segmentation

This sample implements the [2018 Data Science Bowl challenge](https://www.kaggle.com/c/data-science-bowl-2018).
The goal is to segment individual nuclei in microscopy images.
The `nucleus.py` file contains the main parts of the code, and the two Jupyter notebooks

## Environment setup
1.Download the stage1_train.zip from Kaggle. 
2.Create a 'datasets/nucleus/' dir in ../../
3.In ../../datasets/nucleus , Create 'stage1_train' and 'test' dir
4.Unzip stage1_train.zip in 'stage1_train' dir
5.Copy our pap smears data set into test dir


## Command line Usage
Train a new model starting from ImageNet weights using `train` dataset (which is `stage1_train` minus validation set)

With --backbone arguement, we can change the used backbones for mask rcnn. Now we support mobilenet224v1, resnet50, resnet101
FYI: when use mobilenet224v1 as backbone, we need to add --train_bn=true too
```
python3 nucleus.py train --dataset=/path/to/dataset --subset=train --weights=imagenet --backbone=mobilenet224v1 --train_bn=true
```

Train a new model starting from specific weights file using the full `stage1_train` dataset
```
python3 nucleus.py train --dataset=/path/to/dataset --subset=stage1_train --weights=/path/to/weights.h5
```

Resume training a model that you had trained earlier
```
python3 nucleus.py train --dataset=/path/to/dataset --subset=train --weights=last
```

Generate submission file from `stage1_test` images
```
python3 nucleus.py detect --dataset=/path/to/dataset --subset=stage1_test --weights=<last or /path/to/weights.h5>
```

## Jupyter notebook Environment

1.In this dir, run 
```
jupyter notebook --no-browser --port <your_port>

```
In terminal, there will be a token, and we need to remeber it.

2.On private computer(not our gpu server), run
```
ssh -L <private_local_port>:127.0.0.1:<your_port> user@host_ip -p <ssh_port>
```
Such that we build a ssh tunnel to access jupyter notebook server.

3.On private computer , open
```
http://localhost:<private_local_port> 
```
in web browser 

## Jupyter notebooks
Two Jupyter notebooks are provided as well: `inspect_nucleus_data.ipynb` and `inspect_nucleus_model.ipynb`.
They explore the dataset, run stats on it, and go through the detection process step by step.

`inspect_nucleus_model_pap_smears.ipynb`
is for our time cost analysis.

`inspect_nucleus_model.ipynb` is changed too. We can see the time cost on Sic-Bowl dataset.