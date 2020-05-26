import os, shutil, csv, time
import filter_end.test_cell_seg2 as mala2
import filter_end.concat as concat
import filter_end.predict as predict
import numpy as np

def clean_path(dst,sign):
    if sign == '1':
        for n in dst:
            if os.path.exists(n):
                shutil.rmtree(n)
        for m in dst:
            os.makedirs(m)
    else:
        for n in dst:
            if os.path.exists(n):
                shutil.rmtree(n)

def get_cells_csv(cells_82_P, cells_90_P, out_cells_info):
    _list1 = os.listdir(cells_82_P)
    _list2 = os.listdir(cells_90_P)
    for n in _list1:
        _path = os.path.join(cells_82_P, n)
        if n in _list2:
            _cell_info = [_path, 'P']
        else:
            _cell_info = [_path, 'N']
        f = open(out_cells_info, 'a',newline='')
        writer = csv.writer(f)
        writer.writerow(_cell_info)
        f.close()

def make_82_P_by_df(df):
    clean_path(['cells_82_P'], '1')
    _path = np.array(df["cellpath"])
    _predict_label = np.array(df["predict_label"])
    P_sign = 51

    for path,predict_label in zip(_path,_predict_label):
        if int(predict_label) == P_sign:
            newpath = os.path.join('cells_82_P', path.split('/')[-1])
            shutil.copy(path, newpath)

def make_82():
    clean_path(['cells_82'], '1')
    dst1 = 'cells_82_P'
    dst2 = 'cells_82_N'
    dst_list1 = os.listdir(dst1)
    dst_list2 = os.listdir(dst2)
    for n in dst_list1:
        path_1 = os.path.join(dst1, n)
        newpath_1 = os.path.join('cells_82', path_1.split('/')[-1])
        shutil.copy(path_1, newpath_1)
    for m in dst_list2:
        path_2 = os.path.join(dst2, m)
        newpath_2 = os.path.join('cells_82', path_2.split('/')[-1])
        shutil.copy(path_2, newpath_2)
            
def make_82_P_by_df_2(df):
    clean_path(['cells_82_P'], '1')
    clean_path(['cells_82_N'], '1')
    _path = np.array(df["cellpath"])
    _predict_label = np.array(df["predict_label"])
    _score = np.array(df["score"])
    P_sign = 51
    N_sign = 50

    N_cells_set = []
    for path,predict_label,score in zip(_path,_predict_label,_score):
        if int(predict_label) == P_sign:
            newpath = os.path.join('cells_82_P', path.split('/')[-1])
            shutil.copy(path, newpath)
        elif int(predict_label) == N_sign:
            temp_cell_info = {'path':path, 'score':score}
            N_cells_set.append(temp_cell_info)
    N_cells_set_sort = sorted(N_cells_set, key = lambda i: i['score'])
    cnt = 0
    for n in N_cells_set_sort:
        path_n = n['path']
        newpath = os.path.join('cells_82_N', path_n.split('/')[-1])
        shutil.copy(path_n, newpath)
        cnt = cnt + 1
        if cnt > 100:
            break
    make_82()
            
def get_P_N_path(): #将P改为N
    _list_82 = os.listdir('cells_82_P')
    _list_90 = os.listdir('cells_90_P')
    temp = []
    for n in _list_82:
        if n in _list_90:
            pass
        else:
            temp.append(n)
    return temp

def get_N_P_path(): #将N改为P
    _list_82 = os.listdir('cells_82_N')
    _list_90 = os.listdir('cells_90_P')
    temp = []
    for n in _list_82:
        if n in _list_90:
            temp.append(n)
        else:
            pass
    return temp

def get_final_df(df, temp1, temp2):
    _path = list(np.array(df["cellpath"]))
    __path = []
    for m in _path:
        _m = m.split('/')[-1]
        __path.append(_m)
    N_sign = 50
    for n in temp1:
        _index = __path.index(n)
        df.loc[_index,["true_label","predict_label"]] = [N_sign, N_sign]
    P_sign = 51
    for n in temp2:
        _index = __path.index(n)
        df.loc[_index,["true_label","predict_label"]] = [P_sign, P_sign]
    return df

# if __name__ == "__main__":
def main_filter_end(df, md90, _net, _meta):
    make_82_P_by_df_2(df)
    if os.path.exists('out_cells.csv'):
        os.remove('out_cells.csv')
    path_list = ['temp_con','cells_1400/temp','cells_90_P','out_dict','output2']
    clean_path(path_list,'1')
    # yolo 输入目录'cells_82_P'，输出目录'cells_1400'
    _list = os.listdir('cells_82')
    if len(_list) == 0:
        #get_cells_csv('cells_82_P', 'cells_90_P', 'out_cells.csv')
        _temp = get_P_N_path()
        _temp2 = get_N_P_path()
        df_out = get_final_df(df, _temp,_temp2)
        #clean_path(path_list,0)
        return df_out
    concat_info = concat.main1()
    predict.main1(_net, _meta, concat_info)
    # mala2 输入目录‘cellls_1400/temp/***.png’，输出目录'cells_90_P'存放阳性细胞
    _list = os.listdir('cells_1400/temp')
    if len(_list) == 0:
        #get_cells_csv('cells_82_P', 'cells_90_P', 'out_cells.csv')
        _temp = get_P_N_path()
        _temp2 = get_N_P_path()
        df_out = get_final_df(df, _temp,_temp2)
        #clean_path(path_list,0)
        return df_out
    mala2.main1(md90)
    # 生成csv
    #get_cells_csv('cells_82_P', 'cells_90_P', 'out_cells.csv')
    # 生成新的df
    _temp = get_P_N_path()
    _temp2 = get_N_P_path()
    df_out = get_final_df(df, _temp,_temp2)
    # 删除中间文件
    clean_path(path_list,'0')
    clean_path(['cells_82_P','cells_82_N','cells_82','cells_1400'],'0')
    return df_out
