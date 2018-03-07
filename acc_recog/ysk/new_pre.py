# -*- endoce: utf-9 -*-
# Python3

import os
import csv
import numpy as np

###########################################
# spectrogram para
maxlen = 2400
nfft = 120
overlap = int(nfft / 2)  # 60

window = np.hamming(nfft)
spec_col = int((maxlen - nfft)/overlap + 1)  # (2400 - 120)/60 + 1 = 39
spec_row = int(nfft/2 + 1)  # 60/2 + 1 = 31

def spectrogram(arr):
    if len(arr.shape)>1:
        ch = arr.shape[1]
        data = np.zeros((ch, spec_row, spec_col), dtype=np.float32)
        for channel in range(ch):
            data[channel] = spectrogram(arr[:,channel])
        return data
    data = np.zeros((spec_row, spec_col), dtype=np.float32)
    start = 0
    for i in range(spec_col):
        frame = arr[start: start + nfft]
        windowed = window * frame
        res = np.fft.rfft(windowed)
        res_end = np.log(np.abs(res) ** 2 + 1e0)
        data[:, i] = np.flip(res_end, axis=0)
        start += overlap
    return data

################################################
def readcsv(name, ig_row=3, ig_col=1):
    with open(name) as f:
        data = [i for i in csv.reader(f)]
    data = data[ig_row:]
    data = [i[ig_col:] for i in data]
    return data


def list2array(li, dtype=np.int64):
    ############
    # extra
    for rows in li:
        for i in range(len(rows)):
            if rows[i] == 'ON':
                rows[i] = 1
            if rows[i] == 'OFF':
                rows[i] = 0
    ############
    arr = np.array(li, dtype=dtype)
    del li
    return arr


def traversal(_dir='./', ends='.csv'):
    filelist = os.listdir(_dir)
    filelist.sort()
    print("get %d files" % len(filelist))
    data = []
    n = 0
    for name in filelist:
        if name.endswith(ends):
            data.append(list2array(readcsv(_dir+name)))
        n += 1
        if n % 100 == 0:
            print(n)
    return data

def get_arry(savename, _dir='./', ends='.csv'):
    data = traversal(_dir, ends)
    arr = np.concatenate(data)
    np.save(savename, arr)
    print("saved array as %s" % savename)

###############################################################################
##
import matplotlib.pyplot as plt
import numpy as np
import os

def cut_by_id(array, ch=13):
    list_ = []
    item_now = array[0, 1:5]
    arr_item = np.zeros((252, 4), dtype=np.int32)
    n = 0
    for i in range(len(array)):
        if array[i, ch]==30 and (array[i, 1:5] != item_now).any():
            list_.append(i)
            item_now = array[i, 1:5]
            arr_item[n] = array[i, 1:5]
            n += 1
    list_.append(len(array))
    return list_, arr_item


# st: ch13: 30 -> 40
# end: ch13: 150 -> 10
def cut_st_end(arr, st_i=13, end_i=13):
    st_list = []
    end_list = []
    st_30 = False
    end_150 = False
    for i in range(len(arr)):
        if arr[i, st_i] == 30:
            st_30 = True
        elif st_30 and arr[i, st_i]==40:
            st_list.append(i)
            st_30 = False

        if arr[i, end_i] == 150:
            end_150 = True
        elif end_150 and arr[i, end_i]==10:
            end_list.append(i)
            end_150 = False

    return st_list, end_list

# cut: 1.has label and label != 3//  2.len < maxlen
def cut_arr(arr, st_li, en_li, id_li2, maxlen=maxlen, ch=36):
    en_st = [en_li[i]-st_li[i] for i in range(len(st_id))]
    n = len(st_li)
    cut_arr = np.zeros((n, maxlen, ch), dtype=np.float32)
    label_arr = np.zeros(n, dtype=np.int32)
    k = 0
    for i in range(len(st_id)):
        if en_st[i] > maxlen:
            continue
        if len(id_li2[i]) < 3:
            print("no label, pass...", id_li2[i])
            continue
        if id_li2[i][2] > 1:
            print("wrong label, pass...", id_li2[i])
            continue
        l = en_st[i]
        cut_arr[k,:l] = arr[i, -ch:]
        label_arr[k] = id_li2[i][2]
        k += 1
    return cut_arr[:k], label_arr[:k]

# be used to log3-3 & log3-4
def get_result_list(arr):
    id_now = arr[0, 1:5]
    res_list = []
    res = np.zeros(3, dtype=np.int32)
    for flame in arr:
        if (flame[1:5] != id_now).any():
            res_list.append([id_now, res])
            res = np.zeros(3, dtype=np.int32)
            id_now = flame[1:5]
        else:
            res += flame[-3:]
    for id_now, res in res_list:
        if sum(res!=0)>1 or sum(res!=0)==0:  # <have more than one label> or <don't have any label>
            if np.array(res!=0, dtype=np.int32)[-1]!=0:  # <ok> and <conditionally ok> --> <Conditionally ok> only
                temp = np.array(res!=0, dtype=np.int32)
                temp[0] = 0
                res[:] = temp[:]
            else:
                print("sample error!, id=%s, res=%s" % (str(id_now), str(res)))
        else:
            res[:] = np.array(res!=0, dtype=np.int32)[:] # only one label
    return np.array(res_list)

# ok -> 1, ng & conditionally ok -> 0, others --> 3
def parse_label(arr): #arr[ok, ng, c_ok]
    if arr[1] == 1 or arr[2] == 1:
        return 0
    elif arr[0] == 1:
        return 1
    else:
        print("error label: ", arr)
        return 3

# id_l2 = [[num, arr[id]],...] --> [[num, arr[id], label],...]
# lg = [[arr[id], arr[label]], ...]
def res2id_li(id_li2, *lgs):
    n = 0
    for lg in lgs:
        for p_lg in lg:
            for p_id in id_li2:
                if (p_lg[0] == p_id[1]).all():
                    # print("get pair!", p_lg, p_id)
                    label = parse_label(p_lg[1])
                    p_id.append(label)
                    n += 1
    print("n:", n)


##############
## global
if __name__ == "__main__":
    arr = np.load("log2-1.npy")
    lg33 = np.load("log33_res.npy")
    lg34 = np.load("log34_res.npy")

    print("read end, len of array = %d" % len(arr))
    id_li = cut_by_id(arr)   # [[id], [number]]
    id_li = [id_li[0][1:], id_li[1]]
    print("cut_id end, num of item = %d" % len(id_li[0]))
    st_li, en_li = cut_st_end(arr)

    en_st = [en_li[i]-st_li[i] for i in range(len(st_li))]
    id_en = [id_li[0][i+1]-en_li[i] for i in range(len(st_li)-1)]
    st_id = [st_li[i]-id_li[0][i] for i in range(len(st_li))]

    id_li2 = [[id_li[0][i], id_li[1][i]] for i in range(len(id_li[1]))]
    res2id_li(id_li2, lg33, lg34)

    arr, arr_label = cut_arr(arr, st_li, en_li, id_li2)
    print("cut_arr() over, arr.shape: %s" % str(arr.shape))

    print("arr -> spectrogram")
    spec_arr = np.zeros((arr.shape[0], arr.shape[2], spec_row, spec_col))
    for i in range(arr.shape[0]):
        spec_arr[i] = spectrogram(arr[i])

    np.save("log21_2400.npy", np.array(arr, dtype=np.float32))
    np.save("log21_2400_label.npy", np.array(arr_label, dtype=np.int32))
    np.save("log21_2400_spec.npy", np.array(spec_arr, dtype=np.float32))
    print("log21_2400.npy.shape: %s" % str(arr.shape))
    print("log21_2400_label.npy.shape: %s" % str(spec_arr.shape))
    print("log21_2400_spec.npy.shape: %s" % str(spec_arr.shape))
