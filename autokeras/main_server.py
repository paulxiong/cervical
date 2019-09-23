import pandas as pd
import os

crop='/ai/thumbor/data/loader/scratch/Tzx5x6EK/statistics/55_crop_cells.csv'

#通过裁剪完之后的统计csv里面找出某一类细胞，返回路径数组
def get_cell_lists_for_train(csvpath, cropdir, celltype):
    lists = []
    if not os.path.exists(csvpath):
        return False, lists
    df = pd.read_csv(csvpath)
    df1 = df[df['celltype'] == int(celltype)]
    for index, row in df1.iterrows():
        lists.append(os.path.join(cropdir, row['cell']))
    return False, lists

#出入需要的细胞类型数组，传出一个字典
def get_datasets_for_train(csvpath, celltypes=[1, 7]):
    typetree = {}
    if not os.path.exists(csvpath):
        return False, lists

    for i in celltypes:
        ret, l = get_cell_lists_for_train(csvpath, '', i)
        key = str(i)
        typetree[key] = l
    return True, typetree

get_datasets_for_train(crop, celltypes=[1, 2, 4, 7])
