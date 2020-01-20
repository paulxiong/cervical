import numpy as np

def make_rand_matrix(side=20): # 制作随机矩阵，用于测试
    a = np.random.random((side,side))
    for i in range(0,side):
        for j in range(0,side):
            if a[i,j]>0.3:
                a[i,j] = 1
            else:
                a[i,j] = 0
    return a

def get_min_std_matrix(A): # 制作最分布均匀矩阵
    sum_ = sum(sum(A))
    [x_side, y_side] = A.shape
    B = np.zeros((x_side,y_side))
    long_ = int(x_side*y_side/sum_)
    cnt = 0
    for i in range(0,x_side):
        for j in range(0,y_side):
            cnt = cnt + 1
            if cnt%long_ == 0:
                B[i,j] = 1
    return B

def get_max_std_matrix(A): # 制作分布最不均匀矩阵
    sum_ = sum(sum(A))
    [x_side, y_side] = A.shape
    B = np.zeros((x_side,y_side))
    cnt = 0
    for i in range(0,x_side):
        for j in range(0,y_side):
            B[i,j] = 1
            cnt = cnt + 1
            if cnt >= sum_:
                break
    return B

def get_rand_std(rand_matrix): # 输入矩阵为0,1矩阵，计算矩阵分布均匀程度
    sum_ = sum(sum(rand_matrix))
    [x_side, y_side] = rand_matrix.shape
    fit_x_side = int(x_side/10)
    fit_y_side = int(y_side/10)
    location_p = []
    for i in range(0, x_side-10, int(fit_x_side/2)): # 让每个元素被扫描两次（规则自己随便定，保证元素都被扫描到就行）
        for j in range(0,y_side-10, int(fit_y_side/2)):
            temp_matrix = rand_matrix[i:i+10,j:j+10]
            cnt_p = sum(sum(temp_matrix))
            location_p.append(cnt_p)
    std = np.std(location_p)
    return std

def get_stand_std(A): # 将均匀程度分布在0,1之间，1表示分布最均匀
    if sum(sum(A)) == 0:
        print('不得传入全0矩阵')
        exit()
    A_max = get_max_std_matrix(A)
    A_min = get_min_std_matrix(A)
    A_std = get_rand_std(A)
    A_max_std = get_rand_std(A_max)
    A_min_std = get_rand_std(A_min)
    if A_std < A_min_std:
        return 1
    else:
        return max(0,(A_max_std-A_std)/(A_max_std-A_min_std))

if __name__ == "__main__":
    # 当矩阵为0或者1元素过少，计算分布没有意义
    A = make_rand_matrix(100) # numpy产生随机0,1矩阵均匀程度在0.9~1之间
    print(get_stand_std(A))
