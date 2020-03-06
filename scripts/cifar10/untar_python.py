import PIL.Image as Image
import pickle, os

inputdir="cifar-10-batches-py"
outputdir="python_untar"

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='iso-8859-1')
    return dict

def save_image(img, imgpath):
    a = img.reshape(3, 32, 32)
    # 得到RGB通道
    r = Image.fromarray(a[0]).convert('L')
    g = Image.fromarray(a[1]).convert('L')
    b = Image.fromarray(a[2]).convert('L')
    image = Image.merge("RGB", (r, g, b))
    image.save(imgpath, 'png')


def untar_data_batch(batch_index, filepath, _labels_indexes):
    dict_train_batch1 = unpickle(filepath)
    data_train_batch1 = dict_train_batch1.get('data')
    labels = dict_train_batch1.get('labels')
    filenames = dict_train_batch1.get('filenames')
    path1 = os.path.join(outputdir, str(batch_index))
    if not os.path.exists(path1):
        os.makedirs(path1)
    for i in range(len(labels)):
        label = labels[i]
        label_name = _labels_indexes[int(label)]
        path2 = os.path.join(path1, label_name)
        if not os.path.exists(path2):
            os.makedirs(path2)
        imgpath = os.path.join(path2, filenames[i])
        img1 = dict_train_batch1['data'][i]
        save_image(img1, imgpath)

def untar_batches_meta(filepath):
    dict_train_batch1 = unpickle(filepath)
    print(dict_train_batch1)
    labels = dict_train_batch1.get('label_names')
    return labels

labels_index = untar_batches_meta(os.path.join(inputdir, 'batches.meta'))

for i in range(1, 6):
    data_batch = 'data_batch_%d' % i
    path1 = os.path.join(inputdir, data_batch)
    print(path1)
    untar_data_batch(i, path1, labels_index)


test_batch_path = os.path.join(inputdir, 'test_batch')
untar_data_batch('test', test_batch_path, labels_index)
