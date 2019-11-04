from enum import Enum

# models type
class mt(Enum):
    UNKNOWN   = 0 #0未知
    UNET      = 1 #1UNET
    GAN       = 2 #2GAN
    SVM       = 3 #3SVM
    MASKRCNN  = 4 #4MASKRCNN
    AUTOKERAS = 5 #5AUTOKERAS
    MALA      = 6 #MALA

# worker type
class wt(Enum):
    UNKNOWN  = 0 #0未知
    DATA     = 1 #1数据处理
    TRAIN    = 2 #2训练
    PREDICT  = 3 #3预测

# datasets status
class ds(Enum):
    INIT            = 0  #0初始化
    READY4PROCESS   = 1  #1用户要求开始处理
    PROCESSING      = 2  #2开始处理
    PROCESSING_ERR  = 3  #3处理出错
    PROCESSING_DONE = 4  #4处理完成
    PATH_ERR        = 5  #5目录不存在
    READY4TRAIN     = 6  #6用户要求开始训练
    TRAINNING       = 7  #7开始训练
    TRAINNING_ERR   = 8  #8训练出错
    TRAINNING_DONE  = 9  #9训练完成
    READY4PREDICT   = 10 #送去做预测
    PREDICTING      = 11 #开始预测
    PREDICTING_ERR  = 12 #预测出错
    PREDICTING_DONE = 13 #预测完成

# datasets type
class dt(Enum):
    UNKNOWN  = 0 #0未知
    TRAIN    = 1 #1训练
    PREDICT  = 2 #2预测
