# -*- coding: utf-8 -*-
import os, cv2, struct
import numpy as np

inputdir="cifar-10-batches-bin"
outputdir="binary_untar"

def open_file_with_full_name(full_path, open_type):
    try:
        file_object = open(full_path, open_type)
        return file_object
    except Exception as e:
        print(e)
        return None

def _read_a_image(file_object):
    raw_img = file_object.read(32 * 32)
    red_img = struct.unpack(">1024B", raw_img)

    raw_img = file_object.read(32 * 32)
    green_img = struct.unpack(">1024B", raw_img)

    raw_img = file_object.read(32 * 32)
    blue_img = struct.unpack(">1024B", raw_img)

    img = np.zeros(shape=(1024, 3))
    for i in range(1024):
        l = [red_img[i], green_img[i], blue_img[i]]
        img[i] = l
    img = img.reshape(32, 32, 3)
    return img

def _read_a_label(file_object):
    raw_label = file_object.read(1)
    if len(raw_label) < 1:
        return None
    label = struct.unpack(">B", raw_label)
    return label

def save_image(image, full_path_name):
    _image = image.astype(np.uint8)
    cv2.imwrite(full_path_name, _image)
    return

def untar_batches_meta(filepath):
    labels = {}
    count = 0
    f = open(filepath, "r")
    for line in f.readlines():
        if line.strip('\n') == '':
            continue
        labels[str(count)] = line.strip('\n')
        count = count + 1
    return labels

def untar_data_batch(index, filepath, outpath, labels):
    if not os.path.exists(filepath):
        return
    train_file = open_file_with_full_name(filepath, 'rb')
    count = 0
    while True:
        label = _read_a_label(train_file)
        if label is None:
            break
        image = _read_a_image(train_file)
        label = label[0]
        if str(label) not in labels.keys():
            print("label not found %s" % str(label))
            continue
        label = labels[str(label)]
        savepath = os.path.join(outpath, str(index), label)
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        savepath = os.path.join(savepath, str(count) + '.png')
        save_image(image, savepath)
        count = count + 1

if __name__ == "__main__":
    labels_index = untar_batches_meta(os.path.join(inputdir, 'batches.meta.txt'))
    print(labels_index)

    for i in range(1, 6):
        data_batch = 'data_batch_%d.bin' % i
        path1 = os.path.join(inputdir, data_batch)
        print(path1)
        untar_data_batch(i, path1, outputdir, labels_index)

    path1 = os.path.join(inputdir, 'test_batch.bin')
    print(path1)
    untar_data_batch('test', path1, outputdir, labels_index)
