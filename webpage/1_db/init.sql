DROP TABLE IF EXISTS c_user;;/*SkipError*/
CREATE TABLE c_user(
    id BIGINT NOT NULL AUTO_INCREMENT  COMMENT '用户ID' ,
    mobile VARCHAR(128) NOT NULL   COMMENT '手机号' ,
    email VARCHAR(1024)    COMMENT '邮箱' ,
    name VARCHAR(128)    COMMENT '用户名' ,
    image VARCHAR(1024)    COMMENT '用户头像' ,
    introduction VARCHAR(1024)   DEFAULT "" COMMENT '用户文字的介绍' ,
    type_id INT NOT NULL   COMMENT '用户类型 1 超级管理员 1000 普通用户' ,
    password VARCHAR(1024) NOT NULL   COMMENT '密码 加过密' ,
    created_at DATETIME NOT NULL   COMMENT '创建时间' ,
    updated_at DATETIME NOT NULL   COMMENT '更新时间' ,
    revision INT    COMMENT '乐观锁' ,
    PRIMARY KEY (id)
) COMMENT = 'user 地区+年级+课程+章节';;
ALTER TABLE c_user COMMENT 'user';;
DROP TABLE IF EXISTS c_user_type;;/*SkipError*/
CREATE TABLE c_user_type(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '用户类型ID' ,
    name VARCHAR(64)    COMMENT '类型名称' ,
    role VARCHAR(32)    COMMENT '角色英文缩写 前端判断权限使用' ,
    description VARCHAR(1024) NOT NULL   COMMENT '描述' ,
    image VARCHAR(32)    COMMENT '类型图片' ,
    created_at DATETIME NOT NULL   COMMENT '创建时间' ,
    updated_at DATETIME NOT NULL   COMMENT '更新时间' ,
    revision INT    COMMENT '乐观锁' ,
    PRIMARY KEY (id)
) COMMENT = 'user_type 用户类型1--admin，1000---普通用户';;
ALTER TABLE c_user_type COMMENT 'user_type';;
DROP TABLE IF EXISTS c_operationlog;;/*SkipError*/
CREATE TABLE c_operationlog(
    id BIGINT NOT NULL AUTO_INCREMENT  COMMENT 'id' ,
    user_id BIGINT NOT NULL  DEFAULT 0 COMMENT '用户id' ,
    path VARCHAR(1024) NOT NULL  DEFAULT "" COMMENT '访问的路径' ,
    query VARCHAR(1024)   DEFAULT "" COMMENT 'query' ,
    method VARCHAR(32) NOT NULL  DEFAULT "" COMMENT '请求方式' ,
    ip VARCHAR(15) NOT NULL  DEFAULT "" COMMENT '客户端ip地址' ,
    region_id VARCHAR(32) NOT NULL  DEFAULT "" COMMENT 'ip所在的地区的编号' ,
    isp VARCHAR(128) NOT NULL  DEFAULT "" COMMENT '运营商' ,
    input TEXT    COMMENT '输入的参数' ,
    ua VARCHAR(1024) NOT NULL  DEFAULT "" COMMENT 'UserAgent' ,
    code INT NOT NULL  DEFAULT 0 COMMENT '返回码' ,
    bodysize INT NOT NULL  DEFAULT 0 COMMENT 'bodySize' ,
    cost INT NOT NULL  DEFAULT 0 COMMENT '当前请求耗时多少微秒' ,
    referer VARCHAR(1024) NOT NULL  DEFAULT "" COMMENT 'Referer' ,
    created_at DATETIME NOT NULL   COMMENT '创建时间' ,
    PRIMARY KEY (id)
) COMMENT = 'operationlog API访问记录';;
ALTER TABLE c_operationlog COMMENT 'operationlog';;
DROP TABLE IF EXISTS c_region;;/*SkipError*/
CREATE TABLE c_region(
    id VARCHAR(32) NOT NULL  DEFAULT "" COMMENT 'id 是字符串的MD5，32的长度' ,
    cityid BIGINT NOT NULL  DEFAULT 0 COMMENT '城市的id' ,
    country VARCHAR(128) NOT NULL  DEFAULT "" COMMENT '国家' ,
    region VARCHAR(128) NOT NULL  DEFAULT "" COMMENT '地区' ,
    province VARCHAR(128) NOT NULL  DEFAULT "" COMMENT '省份 美国是州' ,
    city VARCHAR(128) NOT NULL  DEFAULT "" COMMENT '城市名字' ,
    isp VARCHAR(128) NOT NULL  DEFAULT "" COMMENT '运营商' ,
    created_at DATETIME    COMMENT '创建时间' ,
    PRIMARY KEY (id)
) COMMENT = '城市 城市编号，方便归属地查询';;
ALTER TABLE c_region COMMENT '城市';;
DROP TABLE IF EXISTS c_email;;/*SkipError*/
CREATE TABLE c_email(
    id BIGINT NOT NULL AUTO_INCREMENT  COMMENT 'ID' ,
    toaddr varchar(254) NOT NULL   COMMENT '接收邮箱地址' ,
    fromaddr varchar(254)    COMMENT '用哪个邮箱发送的' ,
    mailtype INT NOT NULL   COMMENT '类型 0未知1注册2忘记密码' ,
    status INT NOT NULL   COMMENT '发送状态 0未发送1已发送2发送失败' ,
    exire DATETIME NOT NULL   COMMENT '失效时间 超过这个时间邮件失效' ,
    valid VARCHAR(1) NOT NULL   COMMENT '是否有效 0失效1有效2永久有效' ,
    code VARCHAR(32)    COMMENT '邮件发送的验证码' ,
    content TEXT    COMMENT '邮件文本内容 邮件的正文部分' ,
    created_at DATETIME NOT NULL   COMMENT '创建时间' ,
    updated_at DATETIME    COMMENT '更新时间' ,
    revision INT    COMMENT '乐观锁' ,
    PRIMARY KEY (id)
) COMMENT = 'email 发送邮件的记录，包括注册邮件、忘记密码邮件';;
ALTER TABLE c_email COMMENT 'email';;
DROP TABLE IF EXISTS c_token;;/*SkipError*/
CREATE TABLE c_token(
    id INT NOT NULL AUTO_INCREMENT  COMMENT 'ID' ,
    uid BIGINT    COMMENT '用户ID' ,
    token VARCHAR(1024)    COMMENT 'token' ,
    exire DATETIME    COMMENT 'token过期时间' ,
    created_at DATETIME    COMMENT '创建时间' ,
    updated_at DATETIME    COMMENT '更新时间' ,
    revision INT    COMMENT '乐观锁' ,
    PRIMARY KEY (id)
) COMMENT = 'token ';;
ALTER TABLE c_token COMMENT 'token';;
DROP TABLE IF EXISTS c_dataset;;/*SkipError*/
CREATE TABLE c_dataset(
    id BIGINT NOT NULL AUTO_INCREMENT  COMMENT 'ID' ,
    description VARCHAR(1024)   DEFAULT "" COMMENT '描述' ,
    status INT NOT NULL  DEFAULT 0 COMMENT '状态 0初始化 1送去处理 2开始处理 3处理出错 4处理完成' ,
    dir VARCHAR(128) NOT NULL  DEFAULT "" COMMENT '文件夹名称 文件夹名称' ,
    process_time DATETIME    COMMENT '开始处理(裁剪)时间' ,
    process_end DATETIME    COMMENT '处理(裁剪)结束时间' ,
    process_percent INT   DEFAULT 0 COMMENT '处理数据的进度 100表示完成' ,
    ETA INT   DEFAULT 0 COMMENT '预估还要多长时间结束 单位是秒' ,
    parameter_gray INT NOT NULL  DEFAULT 1 COMMENT '数据处理时候颜色 默认1使用灰色，0使用彩色' ,
    parameter_size INT NOT NULL  DEFAULT 100 COMMENT '切割的正方形边长 默认100像素' ,
    parameter_type INT NOT NULL  DEFAULT 0 COMMENT '切割类型 0--图片直接检测并切割出细胞 1--按照标注csv切割细胞 2--mask-rcnn检测细胞和csv交集的切割' ,
    parameter_mid INT    COMMENT '切割使用的模型' ,
    parameter_cache INT    COMMENT '是否使用裁剪过的cache 0--不使用1--使用' ,
    types VARCHAR(1024)   DEFAULT "[]" COMMENT '当前数据集的所有细胞类型 数组，被转成字符串存储' ,
    batchids VARCHAR(3072)   DEFAULT "[]" COMMENT '批次ID数组 数组，被转成字符串存储' ,
    medicalids VARCHAR(3072)   DEFAULT "[]" COMMENT '病例ID数组 数组，被转成字符串存储' ,
    created_by BIGINT NOT NULL  DEFAULT 0 COMMENT '创建者' ,
    created_at DATETIME NOT NULL   COMMENT '创建时间' ,
    updated_at DATETIME NOT NULL   COMMENT '更新时间' ,
    PRIMARY KEY (id)
) COMMENT = 'dataset 数据集合';;
ALTER TABLE c_dataset COMMENT 'dataset';;
DROP TABLE IF EXISTS c_image;;/*SkipError*/
CREATE TABLE c_image(
    ID BIGINT NOT NULL AUTO_INCREMENT  COMMENT 'ID' ,
    CSVPATH VARCHAR(3072) NOT NULL   COMMENT 'CSV路径' ,
    IMGPATH VARCHAR(3072) NOT NULL   COMMENT '图片路径' ,
    W INT NOT NULL   COMMENT '图片分辨率宽' ,
    H INT NOT NULL   COMMENT '图片分辨率高' ,
    BATCHID VARCHAR(128)    COMMENT '批次ID' ,
    MEDICALID VARCHAR(128)    COMMENT '病历号' ,
    created_by BIGINT NOT NULL  DEFAULT 0 COMMENT '创建者' ,
    status INT NOT NULL  DEFAULT 1 COMMENT '状态 0删除1正常' ,
    type INT NOT NULL  DEFAULT 0 COMMENT '类型 0系统默认自带1用户上传' ,
    CREATED_TIME DATETIME    COMMENT '创建时间' ,
    UPDATED_TIME DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (ID)
) COMMENT = 'image 图片';;
ALTER TABLE c_image COMMENT 'image';;
DROP TABLE IF EXISTS c_label;;/*SkipError*/
CREATE TABLE c_label(
    ID BIGINT NOT NULL AUTO_INCREMENT  COMMENT '标注信息ID' ,
    IMGID BIGINT NOT NULL   COMMENT '所属图片的ID' ,
    TYPE INT NOT NULL   COMMENT '类新' ,
    x1 INT NOT NULL  DEFAULT 0 COMMENT '左上角X坐标 单位是像素' ,
    y1 INT NOT NULL  DEFAULT 0 COMMENT '左上角Y坐标 单位是像素' ,
    x2 INT NOT NULL  DEFAULT 0 COMMENT '右下角X坐标 单位是像素' ,
    y2 INT NOT NULL  DEFAULT 0 COMMENT '右下角Y坐标 单位是像素' ,
    status INT   DEFAULT 0 COMMENT '状态 0 未审核 1 已审核 2 移除 10 审核+未审核的' ,
    created_by BIGINT   DEFAULT 0 COMMENT '创建者' ,
    CREATED_TIME DATETIME    COMMENT '创建时间' ,
    UPDATED_TIME DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (ID)
) COMMENT = 'label 标注信息';;
ALTER TABLE c_label COMMENT 'label';;
DROP TABLE IF EXISTS c_category;;/*SkipError*/
CREATE TABLE c_category(
    ID INT NOT NULL   COMMENT '分类ID' ,
    NAME VARCHAR(128) NOT NULL   COMMENT '名字' ,
    P1N0 INT NOT NULL   COMMENT '是阴性还是阳性' ,
    OTHER VARCHAR(3072) NOT NULL   COMMENT '描述' ,
    CREATED_TIME DATETIME    COMMENT '创建时间' ,
    UPDATED_TIME DATETIME    COMMENT '更新时间' 
) COMMENT = 'category 病的分类';;
ALTER TABLE c_category COMMENT 'category';;
DROP TABLE IF EXISTS c_model;;/*SkipError*/
CREATE TABLE c_model(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '模型ID' ,
    type INT NOT NULL   COMMENT '类型 0未知 1UNET 2GAN 3SVM 4MASKRCNN 5AUTOKERAS 6MALA 50全部的裁剪模型 51全部的分类模型 52全部模型' ,
    pid BIGINT NOT NULL   COMMENT '从哪个项目训练出来的' ,
    description VARCHAR(1024)    COMMENT '描述' ,
    path VARCHAR(1024) NOT NULL   COMMENT '模型路径' ,
    recall DECIMAL(32,10)    COMMENT '召回率' ,
    precision1 DECIMAL(32,10)    COMMENT '准确率' ,
    n_train INT    COMMENT '训练用了多少张图片' ,
    n_classes INT    COMMENT '训练有几个分类' ,
    types VARCHAR(1024)    COMMENT '训练的标签 数组，被转成字符串存储' ,
    input_shape VARCHAR(128)    COMMENT '训练输入的尺寸' ,
    model_count INT    COMMENT '产生的模型个数' ,
    best_model INT    COMMENT 'best_modelID 本次训练出的所有模型里面最优模型是第几个' ,
    loss DECIMAL(32,10)    COMMENT '损失' ,
    metric_value DECIMAL(32,10)    COMMENT '训练的准确度' ,
    evaluate_value DECIMAL(32,10)    COMMENT '评估准确度' ,
    created_by BIGINT    COMMENT '创建人' ,
    created_at DATETIME NOT NULL   COMMENT '创建时间' ,
    updated_at DATETIME NOT NULL   COMMENT '更新时间' ,
    PRIMARY KEY (id)
) COMMENT = 'model 模型文件的信息';;
ALTER TABLE c_model COMMENT 'model';;
DROP TABLE IF EXISTS c_project;;/*SkipError*/
CREATE TABLE c_project(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '项目的id' ,
    did BIGINT NOT NULL  DEFAULT 0 COMMENT '数据集的id' ,
    description VARCHAR(1024)   DEFAULT "" COMMENT '项目描述' ,
    dir VARCHAR(32)   DEFAULT "" COMMENT '项目目录' ,
    status INT   DEFAULT 0 COMMENT '项目状态 0初始化 1送去处理 2开始处理 3处理出错 4处理完成 5 送去审核预测结果 6 预测结果审核完成' ,
    start_time DATETIME    COMMENT '开始训练/预测时间' ,
    end_time DATETIME    COMMENT '训练/预结束时间' ,
    percent INT   DEFAULT 0 COMMENT '训练/预的进度' ,
    ETA INT   DEFAULT 0 COMMENT '预估还要多长时间结束' ,
    type INT NOT NULL  DEFAULT 0 COMMENT '项目类型 0 未知 1 保留 2 训练 3 预测' ,
    parameter_time INT   DEFAULT 1800 COMMENT '训练多长时间autokeras参数 只有训练时候需要' ,
    parameter_resize INT   DEFAULT 100 COMMENT '训练之前统一的尺寸' ,
    parameter_mid INT   DEFAULT 0 COMMENT '预测使用的模型的id 只有预测时候需要' ,
    parameter_mtype INT   DEFAULT 0 COMMENT '预测使用的模型的类型 只有预测时候需要,不是前端传递,后端计算得到' ,
    parameter_type INT   DEFAULT 0 COMMENT '预测方式 0没标注的图1有标注的图' ,
    cellstype VARCHAR(1024)   DEFAULT "[]" COMMENT '预测完之后的细胞类型统计 数组，被转成字符串存储' ,
    created_by BIGINT NOT NULL  DEFAULT 0 COMMENT '创建人' ,
    vid BIGINT   DEFAULT 0 COMMENT '谁去做审核(verify)的用户ID' ,
    created_at DATETIME    COMMENT '创建时间' ,
    updated_at DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id)
) COMMENT = 'project 训练/预测的项目';;
ALTER TABLE c_project COMMENT 'project';;
DROP TABLE IF EXISTS c_predict;;/*SkipError*/
CREATE TABLE c_predict(
    id BIGINT NOT NULL AUTO_INCREMENT  COMMENT '预测信息ID' ,
    imgid BIGINT NOT NULL   COMMENT '所属图片的ID' ,
    pid BIGINT NOT NULL   COMMENT '所属项目的ID' ,
    x1 INT NOT NULL  DEFAULT 0 COMMENT '左上角X坐标 单位是像素' ,
    y1 INT NOT NULL  DEFAULT 0 COMMENT '左上角Y坐标 单位是像素' ,
    x2 INT NOT NULL  DEFAULT 0 COMMENT '右下角X坐标 单位是像素' ,
    y2 INT NOT NULL  DEFAULT 0 COMMENT '右下角Y坐标 单位是像素' ,
    cellpath VARCHAR(1024) NOT NULL  DEFAULT "" COMMENT '上述坐标切割出来的细胞' ,
    predict_score INT NOT NULL  DEFAULT 0 COMMENT '预测得分 50表示50%' ,
    predict_type INT NOT NULL  DEFAULT 0 COMMENT '预测的细胞类型' ,
    predict_p1n0 INT NOT NULL  DEFAULT 0 COMMENT '预测阴/阳性' ,
    true_type INT NOT NULL  DEFAULT 0 COMMENT '医生标注的细胞类型 默认等于predict_type' ,
    true_p1n0 INT NOT NULL  DEFAULT 0 COMMENT '医生标注的阴/阳性 默认等于predict_p1n0' ,
    vid BIGINT   DEFAULT 0 COMMENT '谁去做审核(verify)的用户ID' ,
    status INT   DEFAULT 0 COMMENT '状态 0 未审核 1 已审核 2 移除 3 管理员确认' ,
    created_by BIGINT   DEFAULT 0 COMMENT '创建者' ,
    created_at DATETIME    COMMENT '创建时间' ,
    updated_at DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id)
) COMMENT = 'predict 预测完之后的信息';;
ALTER TABLE c_predict ADD INDEX pid_imgid_status(pid,imgid,status);;
ALTER TABLE c_predict ADD INDEX verify_id(vid,status);;
ALTER TABLE c_predict COMMENT 'predict';;
DROP TABLE IF EXISTS c_review;;/*SkipError*/
CREATE TABLE c_review(
    id BIGINT NOT NULL AUTO_INCREMENT  COMMENT 'ID' ,
    predictid BIGINT NOT NULL  DEFAULT 0 COMMENT '预测信息ID' ,
    imgid BIGINT NOT NULL   COMMENT '所属图片的ID' ,
    pid BIGINT NOT NULL   COMMENT '所属项目的ID' ,
    x1 INT NOT NULL  DEFAULT 0 COMMENT '左上角X坐标 单位是像素' ,
    y1 INT NOT NULL  DEFAULT 0 COMMENT '左上角Y坐标 单位是像素' ,
    x2 INT NOT NULL  DEFAULT 0 COMMENT '右下角X坐标 单位是像素' ,
    y2 INT NOT NULL  DEFAULT 0 COMMENT '右下角Y坐标 单位是像素' ,
    cellpath VARCHAR(1024) NOT NULL  DEFAULT "" COMMENT '上述坐标切割出来的细胞' ,
    imgpath VARCHAR(1024) NOT NULL  DEFAULT "" COMMENT '原图路径' ,
    w INT NOT NULL  DEFAULT 0 COMMENT '原图的宽 单位是像素' ,
    h INT NOT NULL  DEFAULT 0 COMMENT '原图的高 单位是像素' ,
    predict_score INT NOT NULL  DEFAULT 0 COMMENT '预测得分 50表示50%' ,
    predict_type INT NOT NULL  DEFAULT 0 COMMENT '预测的细胞类型' ,
    predict_p1n0 INT NOT NULL  DEFAULT 0 COMMENT '预测阴/阳性' ,
    true_type INT NOT NULL  DEFAULT 0 COMMENT '医生标注的细胞类型 默认等于predict_type' ,
    true_p1n0 INT NOT NULL  DEFAULT 0 COMMENT '医生标注的阴/阳性 默认等于predict_p1n0' ,
    vid BIGINT   DEFAULT 0 COMMENT '谁去做审核(verify)的用户ID' ,
    status INT   DEFAULT 0 COMMENT '状态 0 未审核 1 已审核 2 移除 3 管理员确认' ,
    created_by BIGINT   DEFAULT 0 COMMENT '创建者' ,
    created_at DATETIME    COMMENT '创建时间' ,
    updated_at DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id)
) COMMENT = 'review 医生审核细胞的信息';;
ALTER TABLE c_review ADD INDEX predictid(predictid);;
ALTER TABLE c_review COMMENT 'review';;
DROP TABLE IF EXISTS c_result;;/*SkipError*/
CREATE TABLE c_result(
    id BIGINT NOT NULL AUTO_INCREMENT  COMMENT 'ID' ,
    did BIGINT NOT NULL  DEFAULT 0 COMMENT '数据集ID' ,
    pid BIGINT NOT NULL  DEFAULT 0 COMMENT '所属项目的ID' ,
    description VARCHAR(1024) NOT NULL  DEFAULT "" COMMENT '项目描述' ,
    pcnt INT   DEFAULT 0 COMMENT '阳性细胞个数' ,
    ncnt INT   DEFAULT 0 COMMENT '阴性细胞个数' ,
    ucnt INT   DEFAULT 0 COMMENT '不是细胞个数' ,
    fovcnt INT NOT NULL  DEFAULT 0 COMMENT 'FOV的个数' ,
    p1n0 INT NOT NULL   COMMENT '病例预测的阴阳性 50阴性51阳性100未知' ,
    truep1n0 INT    COMMENT '病例实际的阴阳性 50阴性51阳性100未知' ,
    remark VARCHAR(1024)   DEFAULT "" COMMENT '备注' ,
    created_by BIGINT   DEFAULT 0 COMMENT '创建者' ,
    created_at DATETIME    COMMENT '创建时间' ,
    updated_at DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id)
) COMMENT = 'result 项目预测结果统计';;
ALTER TABLE c_result COMMENT 'result';;
DROP TABLE IF EXISTS c_label2;;/*SkipError*/
CREATE TABLE c_label2(
    id VARCHAR(128) NOT NULL   COMMENT '标注信息 时间辍+项目ID+数据集ID+用户ID+随机字符串' ,
    preid BIGINT NOT NULL  DEFAULT 0 COMMENT '预测的ID 人工标注的默认是0' ,
    pid BIGINT NOT NULL  DEFAULT 0 COMMENT '项目ID' ,
    did BIGINT NOT NULL  DEFAULT 0 COMMENT '数据集ID' ,
    typeid INT NOT NULL  DEFAULT 100 COMMENT '类型的ID' ,
    x1 INT NOT NULL  DEFAULT 0 COMMENT '整图左上角X坐标 单位是像素' ,
    y1 INT NOT NULL  DEFAULT 0 COMMENT '整图左上角Y坐标 单位是像素' ,
    x2 INT NOT NULL  DEFAULT 0 COMMENT '整图右下角X坐标 单位是像素' ,
    y2 INT NOT NULL  DEFAULT 0 COMMENT '整图右下角Y坐标 单位是像素' ,
    status INT NOT NULL  DEFAULT 0 COMMENT '状态 0 未审核 1 已审核 2 移除 10 审核+未审核的' ,
    created_by BIGINT   DEFAULT 0 COMMENT '创建者' ,
    created_at DATETIME    COMMENT '创建时间' ,
    updated_at DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id)
) COMMENT = 'label2 标注信息,新版本';;
ALTER TABLE c_label2 COMMENT 'label2';;
DROP TABLE IF EXISTS c_errorlog;;/*SkipError*/
CREATE TABLE c_errorlog(
    id BIGINT NOT NULL AUTO_INCREMENT  COMMENT 'ID' ,
    type INT   DEFAULT 0 COMMENT '类型 0前端' ,
    opid BIGINT   DEFAULT 0 COMMENT 'operationlog的ID' ,
    errlog TEXT    COMMENT '出错内容,字符串' ,
    created_by BIGINT   DEFAULT 0 COMMENT '创建人' ,
    created_at DATETIME NOT NULL   COMMENT '创建时间' ,
    updated_at DATETIME NOT NULL   COMMENT '更新时间' ,
    PRIMARY KEY (id)
) COMMENT = 'errorlog 前端出错的信息';;
ALTER TABLE c_errorlog COMMENT 'errorlog';;
DROP TABLE IF EXISTS c_syscfg;;/*SkipError*/
CREATE TABLE c_syscfg(
    id INT NOT NULL AUTO_INCREMENT  COMMENT 'ID' ,
    host VARCHAR(1024)   DEFAULT "" COMMENT '协议+本服务域名+端口' ,
    email_register_content TEXT    COMMENT '发送注册邮件的格式' ,
    email_forgot_content TEXT    COMMENT '发送忘记密码邮件的格式' ,
    referer_en INT   DEFAULT 0 COMMENT '开启图片防盗链 0未知1关闭２开启' ,
    referers VARCHAR(1024)   DEFAULT "[]" COMMENT '防盗链白名单 http开头的字符串数组' ,
    referer_404_url VARCHAR(1024)   DEFAULT "" COMMENT '图片不存在,默认图片' ,
    referer_401_url VARCHAR(1024)   DEFAULT "" COMMENT '非法请求,默认图片' ,
    imgexpires INT   DEFAULT 72 COMMENT '浏览器上图片缓存过期时间 单位是小时' ,
    avatar_url VARCHAR(1024)   DEFAULT "" COMMENT '用户默认头像 http开头的字符串数组' ,
    created_by BIGINT   DEFAULT 0 COMMENT '创建人' ,
    created_at DATETIME NOT NULL   COMMENT '创建时间' ,
    updated_at DATETIME NOT NULL   COMMENT '更新时间' ,
    PRIMARY KEY (id)
) COMMENT = 'syscfg 系统配置信息';;
ALTER TABLE c_syscfg COMMENT 'syscfg';;


LOCK TABLES `c_user` WRITE;
INSERT INTO `c_user` VALUES (1,'','xundong_km@163.com','xundong_km@163.com','http://workaiossqn.tiegushi.com/xdedu/images/touxiang.jpg','',1,'$2a$10$3KTmT3vqZkPKv9.E4DDpW.KsP.T/FlfPjMuDR9qNyPtRZfrhTW3uW','2019-12-25 09:56:26','2019-12-25 09:56:27',NULL);
UNLOCK TABLES;
