import cv2
import numpy as np



##==============================
## histogram equlization
#===============================
def validate_attributes(data, dtypes, attri=[]):
    assert type(data) == np.ndarray, "Need a numpy ndarray as input"
    assert np.sum([data.dtype == dtype for dtype in dtypes]) >= 1, "Data type missmatch"
    if 'positive' in attri:
        assert (data >= 0).all(), "Not positive"
    if 'integer' in attri:
        assert (np.int64(data) == data).all(), "Not integer"
    if 'notempty' in attri:
        assert np.size(data) != 0, "Empty array"
    if 'vector' in attri:
        assert len(np.shape(data)) == 1, "Not a vector"
    if '2d' in attri:
        assert len(np.shape(data)) == 2, "Not a 2d array"
        
def computeCumulativeHistogram(img, nbins):
    nn = np.histogram(img.flatten(), nbins)[0]
    cum = np.cumsum(nn)
    return nn, cum

def createTransformationToIntensityImage(a, hgram, m, n, nn, cum):
    cumd = np.cumsum(hgram * np.size(a) / np.sum(hgram))
    
    # Create transformation to an intensity image by minimizing the error
    # between desired and actual cumulative histogram.
    tol = np.dot(np.ones((m, 1)), 
                 np.min(np.stack([np.append(nn[0:n-1], 0),np.append(0, nn[1:n])]), 
                        axis=0)[np.newaxis,:]/2
                )
    #import ipdb; ipdb.set_trace()
    err = (np.dot(cumd[:,np.newaxis], np.ones((1, n))) - 
           np.dot(np.ones((m, 1)), cum[np.newaxis,:])) + tol
    #here for some calculation error, we set epsilon= 2.2204e-15
    d = np.where(err < (-np.size(a)*np.sqrt(2.2204e-14)))
    if len(d) !=0:
        err[d] = np.size(a)
        
    T = np.argmin(err, axis=0)
    
    return T

def histeq(*param):
    assert len(param) in [2, 3], "Invalid number of input parameters"
    NPTS = 256
    
    if len(param) == 2:
        #HISTEQ(I, HGRAM)
        a = param[0]
        hgram = param[1]
        map_method = 'GML'
        validate_attributes(a, [np.uint8], ['2d'])
        validate_attributes(hgram,[np.float32, np.float64],
                            ['vector','notempty'])
        n = NPTS
    else:
        a = param[0]
        hgram = param[1]
        map_method = param[2]
        validate_attributes(a, [np.uint8], ['2d'])
        validate_attributes(hgram,[np.float32, np.float64],
                            ['vector','notempty'])
        n = NPTS
        
    #ipdb.set_trace()
    if map_method == 'mat':
        #++++++MAT++++++
        hgram = hgram * (np.size(a) / np.sum(hgram))
        m = len(hgram)
    
        nn, cum = computeCumulativeHistogram(a, n)
        tk = createTransformationToIntensityImage(a, hgram, m, n, nn, cum)
        #++++++++++++++++++
    else:
        hist, hist_c = computeCumulativeHistogram(a, n)
        #normalize
        hist = hist / np.sum(hist)
        hist_c = hist_c / hist_c[-1]
        assert len(hist) == len(hgram), "hgram must be as same as image"
        hgram = hgram / np.sum(hgram)
        hgram_c = np.cumsum(hgram)
        
        err = np.abs(np.dot(np.ones((n, 1)), hgram_c[np.newaxis,:]) - 
                 np.dot(hist_c[:,np.newaxis], np.ones((1, n))))
        if map_method == 'SML':
            tk = np.argmin(err, axis=0)
        elif map_method == 'GML':
            # method1
            col_min = np.argmin(err, axis=1)
            tk = np.zeros(256)
            start = 0
            for i, mi in enumerate(col_min):
                if mi != start:
                    if start == 0:
                        tk[range(start, mi + 1)] = i
                    else:
                        tk[range(start + 1, mi + 1)] = i
                    start = mi
            #method 2
            #tk1 = np.zeros(256)
            #lastStartY, lastEndY, startY, endY = [0]*4
            #for x in range(256):
                #minValue = err[x, 0]
                #for y in range(256):
                    #if minValue > err[x, y]:
                        #endY = y
                        #minValue = err[x, y]
                #if (startY != lastStartY) or (endY != lastEndY):
                    #for i in range(startY, endY+1):
                        #tk1[i] = x
                    #lastStartY = startY
                    #lastEndY = endY
                    #startY = lastEndY + 1
            #assert (tk1 == tk).all(), "tk is not the same, \n {}".format(err)
                    
    #print(tk)
    for i, j in enumerate(tk):
        a[a==i] = j
    #max min scale
    limit = [np.min(tk), np.max(tk)]
    
    a = np.floor((a - limit[0])/(limit[1]-limit[0])*255.0)
    
    hist = np.histogram(a.flatten(), bins=n)[0]
    return a.astype(np.uint8), hist    


def contrast_enhance(img_batch, color_mode, clahe):
    L_CHANNEL = 0
    V_CHANNEL = -1
    S_CHANNEL = 1
    channels = []
    hist_batch = None
    
    if color_mode == 'HSV_CLAHE_V':
        for_color = cv2.COLOR_BGR2HSV
        back_color = cv2.COLOR_HSV2BGR
        channels = [V_CHANNEL]
    elif color_mode == 'HSV_CLAHE_S':
        for_color = cv2.COLOR_BGR2HSV
        back_color = cv2.COLOR_HSV2BGR
        channels = [S_CHANNEL]
    elif color_mode == 'HSV_CLAHE_SV':
        for_color = cv2.COLOR_BGR2HSV
        back_color = cv2.COLOR_HSV2BGR
        channels = [S_CHANNEL, V_CHANNEL]
    elif color_mode == 'LAB_CLAHE_L':
        for_color = cv2.COLOR_BGR2LAB
        back_color = cv2.COLOR_LAB2BGR
        channels = [L_CHANNEL]
    elif color_mode == 'HIST_BATCH_EQ':
        for_color = cv2.COLOR_BGR2HSV
        back_color = cv2.COLOR_HSV2BGR
        channels = [V_CHANNEL]
        hist_batch = np.zeros(256)
    elif color_mode == 'HIST_BATCH_EQ_LAB':
        for_color = cv2.COLOR_BGR2LAB
        back_color = cv2.COLOR_LAB2BGR
        channels = [L_CHANNEL]
        hist_batch = np.zeros(256)
    elif color_mode == 'RGB':
        return None
    else:
        return None
    
    for i, img in enumerate(img_batch):
        img = cv2.cvtColor(img, for_color)
        img_batch[i] = img
        # if need to do hist batch equalization, sum the hist in a batch first
        if (hist_batch is not None) and channels:
            channel = img[..., channels[0]]
            hist = np.histogram(channel.flatten(), bins=256)[0]
            hist_batch = hist + hist_batch
        elif channels:
            for ch in channels:
                img[..., ch] = clahe.apply(img[..., ch])
            img_batch[i] = cv2.cvtColor(img, back_color)
            
    if hist_batch is not None:
        for i, img in enumerate(img_batch):
            img[..., channels[0]], _ = histeq(img[..., channels[0]], hist_batch)
            img_batch[i] = cv2.cvtColor(img, back_color)
