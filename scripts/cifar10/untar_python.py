import PIL.Image as Image

file1 = 'data/cifar-10-batches-py/data_batch_1'
def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='iso-8859-1')
    return dict

dict_train_batch1 = unpickle(file1)
data_train_batch1 = dict_train_batch1.get('data')
labels = dict_train_batch1.get('labels')
img1 = dict_train_batch1['data'][10]   #只解压第10张
a = img1.reshape(3, 32, 32)

# 得到RGB通道
r = Image.fromarray(a[0]).convert('L')
g = Image.fromarray(a[1]).convert('L')
b = Image.fromarray(a[2]).convert('L')
image = Image.merge("RGB", (r, g, b))
# 显示图片
image.save("lambda.png", 'png')
