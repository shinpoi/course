# - coding: utf-8 -*-
# python 3.5

import os
import csv
import re
import numpy as np
import pylab as P
import logging
import PIL.Image as Image

logging.basicConfig(level='DEBUG', format='[%(levelname)s]   \t%(message)s')

# <Parameter> dataset
DATA_DIR = './'
PRE_NUM_OF_SAMPLE = 7000
MAX_LENGTH = 2200
MIN_LENGTH = 1900

act_dict = {'stay':0, 'walk':1, 'jog':2, 'skip':3, 'stUp':4, 'stDown':5, 'stup':4, 'stdown':5, 'start':6, 'sequence':-1}  # act_dict['void'] -> KeyError
rev_act_dict = {0:'stay', 1:'walk', 2:'jog', 3:'skip', 4:'stUp', 5:'stDown', 6:'start', -1:'sequence'}

# <Parameter> spectrogram
frame_length = MAX_LENGTH  # 2200
nfft = int(MAX_LENGTH/20)  # 110
overlap = int(nfft / 2)  # 55

window = np.hamming(nfft)
sepc_row = int((frame_length - nfft)/overlap + 1)  # (2200 - 110)/55 + 1 = 39
spec_col = int(nfft/2 + 1)  # 110/2 + 1 = 56
sepc_channel = 3  # x, y, z


def float_(x):
    try:
        return float(x)
    except TypeError:
        return 0


def getact(root, num, p_act=re.compile('Activity: ([a-zA-z]+)'), **argd):
    with open(root + 'HASC%s.meta' % num) as f:
        meta = f.read()
        return p_act.search(meta).group(1)  # p_act = /Activity: ([a-zA-z]+)/


def readacc(root, num, **argd):
    with open(root + 'HASC%s-acc.csv' % num) as f:
        li = [x[1:] for x in csv.reader(f)]  # format: [time, x, y, z] -> [x, y, z]
        length = len(li)
    if length > argd['minl'] and length < argd['maxl']:   # (read all) if True:
        dataset_single = np.random.normal(0, 1e-8, argd['maxl']*3).reshape((argd['maxl'], 3))
        dataset_single[:length] += np.array(li, dtype=np.float64)
        return dataset_single
    else:
        return None


def readacc_seq(root, num, p_label=re.compile('([0-9]+\.[0-9]+E[0-9]?),([0-9]+\.[0-9]+E[0-9]?)?,([a-zA-Z]+)'), **argd):
    with open(root + 'HASC%s-acc.csv' % num) as f:
        li = [x for x in csv.reader(f)]  # format: [time, x, y, z] -> [x, y, z]
        length = len(li)
    with open(root + 'HASC%s.label' % num) as f:
        flag_list = []
        while True:
            line = f.readline()
            if not line:
                break
            res = p_label.match(line)
            if not res:
                continue
            try:
                flag_list.append([float_(res.group(1)), float_(res.group(2)), act_dict[res.group(3)]])
            except KeyError:
                try:
                    flag_list.append([float_(res.group(1)), float_(res.group(2)), act_dict[res.group(3).lower()]])
                except KeyError:
                    print(root + 'HASC%s.label' % num)
                    print([res.group(1), res.group(2), res.group(3)])
                    raise KeyError
    if length > argd['minl'] and length < argd['maxl']:   # (read all) if True:
        dataset_single = np.zeros((argd['maxl'], 4), dtype=np.float64)
        dataset_single[:, 1:] += np.random.normal(0, 1e-8, argd['maxl']*3).reshape((argd['maxl'], 3))
        dataset_single[:length] += np.array(li, dtype=np.float64)
        i = j = k = 0
        while True:
            try:
                if dataset_single[k, 0] > flag_list[i][j]:
                    flag_list[i][j] = k
                    if j == 1:
                        i +=1
                        j = 0
                    else:
                        j = 1
                k += 1
            except IndexError:
                # print('break in (i,j,k) = ', (i, j, k))
                break
        argd['dataflag'].append(flag_list)
        return dataset_single[:, 1:]
    else:
        return None


# read csv and dump to arr
def csv2arr(DIR=DATA_DIR, maxl=MAX_LENGTH, minl=MIN_LENGTH, seq=False, p_num=re.compile('HASC([0-9]+).meta')):
    n = 0
    dataset = np.zeros((PRE_NUM_OF_SAMPLE, maxl, 3), dtype=np.float64)  # shape: (7000, 2200, 3)
    if seq:
        dataflag = []
    else:
        dataflag = np.zeros((PRE_NUM_OF_SAMPLE, 2), dtype=np.int32)  # shape: (7000, 2)

    for root, dirs, files in os.walk(DIR):  # str, list, list
        if not root.endswith(r'/'):
            root = root + r'/'
        if not dirs:  # at /Person-xxxx
            for f_name in files:
                num = p_num.search(f_name)  # p_num = /HASC([0-9]+).meta/
                if num:
                    num = num.group(1)
                    if seq:
                        argd = {'maxl':maxl, 'minl':minl, 'dataflag':dataflag}
                        data_single = readacc_seq(root, num, **argd)
                    else:
                        argd = {'maxl':maxl, 'minl':minl}
                        act = getact(root, num)
                        data_single = readacc(root, num, **argd)

                    if data_single != None:
                        dataset[n] = data_single
                        if not seq:
                            dataflag[n] = (num, act_dict[act])
                        n += 1
                        if n % 500 == 0:
                            logging.debug("read samples: %d" % n)

    logging.info("%d sapmles have read" % n)
    dataset = dataset[:n]
    dataflag = dataflag[:n]
    return dataset, dataflag


def csv_len_list(DIR=DATA_DIR):
    len_list = []
    n = 0
    p_num = re.compile('HASC([0-9]+).meta')

    for root, dirs, files in os.walk(DIR):  # str, list, list
        if not root.endswith(r'/'):
            root = root + r'/'
        if not dirs:  # at /Person-xxxx
            for f_name in files:
                num = p_num.search(f_name)  # p_num = /HASC([0-9]+).mta/
                if num:
                    num = num.group(1)
                    with open(root + 'HASC%s-acc.csv' % num) as f:
                        li = [x[1:] for x in csv.reader(f)]  # format: [time, x, y, z] -> [x, y, z]
                        length = len(li)
                        len_list.append(length)
    return len_list


def spectrogram(array, channel=sepc_channel):
    data = np.zeros((sepc_row, spec_col, channel), dtype=np.float64)
    for ch in range(channel):
        arr = array[:, ch]
        start = 0
        for i in range(sepc_row):
            frame = arr[start: start + nfft]
            windowed = window * frame
            res = np.fft.rfft(windowed)
            # res_end = np.log(np.abs(res) ** 2 + 1e0)  # prevent log([0, 0, ..., 0])
            res_end = np.log(np.abs(res) ** 2)
            data[i, :, ch] = res_end
            start += overlap
            # print(i, ch, res_end)
    return data

def plot_spectrogram(arr, name='image.png'):
    arr += np.min(arr)
    arr = np.array((arr/np.max(arr))*255, dtype=np.uint8)
    img = Image.fromarray(arr)
    img.save(name)


# special custom
def muilt_plot(act):
    b_img = np.zeros((147, 264, 3), dtype=np.uint8)+255
    n = 0
    i = 0
    col = row = 0
    while (n<12):
        if act in f_list[i]:
            print(n)
            img = cv2.imread("./sepc/"+f_list[i])
            i += 1
            n += 1
            if (row >= 4):
                row = 0
                col += 1
            b_img[(col*49):(col*49 + 39), (row*66):(row*66+56)] = img
            row += 1
        else:
            i += 1
    cv2.imwrite(act + ".png", b_img)


########################################
if __name__ == '__main__':
    # read dataset
    if os.path.exists(DATA_DIR+'dataset.npy') and os.path.exists(DATA_DIR+'dataflag.npy'):
        logging.info(".npy files exist, dataset will be read from local file")
        dataset = np.load(DATA_DIR+'dataset.npy')
        dataflag = np.load(DATA_DIR+'dataflag.npy')
    else:
        logging.info("dataset.npy not exsits, start reading .csv files")
        dataset, dataflag = csv2arr()
        np.save('dataset.npy', dataset)
        np.save('dataflag.npy', dataflag)
        logging.info("dataset & dataflag have saved")

    # create spectrogram
    save_root = './sepc/'
    try:
        os.mkdir(save_root)
    except FileExistsError:
        pass

    spec_dataset = np.zeros((len(dataset), sepc_channel, sepc_row, sepc_col), dtype=np.float32)

    for i in range(len(dataset)):
        spec_arr = spectrogram(dataset[i])
        spec_dataset[i] = spec_arr.transpose((2, 0, 1))
        ### plot:
        # plot_spectrogram(spec_arr, (save_root + str(dataflag[i, 0]) + '_' + rev_act_dict[dataflag[i, 1]] + '.png'))
        if i % 100 == 0:
            logging.debug("spectrogram: %d" % i)

    np.save('spec_dataset.npy', spec_dataset)
    logging.info("spec_dataset have saved")
