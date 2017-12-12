import os
import csv
import re
import numpy as np
import pylab as P
import logging
import PIL.Image as Image

logging.basicConfig(level='DEBUG', format='[%(levelname)s]   \t%(message)s')
logging.info('init...')

# <Parameter> dataset
DATA_DIR = './'
PRE_NUM_OF_SAMPLE = 7000
MAX_LENGTH = 2200
MIN_LENGTH = 1900

act_dict = {'stay':1, 'walk':2, 'jog':3, 'skip':4, 'stUp':5, 'stDown':6}  # act_dict['void'] -> KeyError
rev_act_dict = {1:'stay', 2:'walk', 3:'jog', 4:'skip', 5:'stUp', 6:'stDown'}

# <Parameter> spectrogram
frame_length = MAX_LENGTH  # 2200
nfft = int(MAX_LENGTH/20)  # 110
overlap = int(nfft / 2)  # 55

window = np.hamming(nfft)
sepc_row = int((frame_length - nfft)/overlap + 1)  # (2200 - 110)/55 + 1 = 39
spec_col = int(nfft/2 + 1)  # 110/2 + 1 = 56

# read csv and dump to arr
def csv2arr():
    n = 0
    p_num = re.compile('HASC([0-9]+).meta')
    p_act = re.compile('Activity: ([a-zA-z]+)')

    dataset = np.zeros((PRE_NUM_OF_SAMPLE, MAX_LENGTH, 3), dtype=np.float64)  # shape: (7000, 2200, 3)
    dataflag = np.zeros((PRE_NUM_OF_SAMPLE, 2), dtype=np.int32)  # shape: (7000, 2)

    for root, dirs, files in os.walk(DATA_DIR):  # str, list, list
        if not root.endswith(r'/'):
            root = root + r'/'
        if not dirs:  # at /Person-xxxx
            for f_name in files:
                num = p_num.search(f_name)  # p_num = /HASC([0-9]+).meta/
                if num:
                    num = num.group(1)
                    with open(root + f_name) as f:
                        meta = f.read()
                        act = p_act.search(meta).group(1)  # p_act = /Activity: ([a-zA-z]+)/
                    with open(root + 'HASC%s-acc.csv' % num) as f:
                        li = [x[1:] for x in csv.reader(f)]  # format: [time, x, y, z]
                        length = len(li)
                        """
                        # test code
                        if length<1500 or length>2500:
                            print("num: %s, act: %s, length: %d" % (num, act, length))
                        if act not in act_list:
                            print('act: %s is not in act_list!' % act)
                        """                        
                        if length > MIN_LENGTH and length < MAX_LENGTH:
                        # (read all) if True:
                            dataset[n, :length] = li
                            dataflag[n] = (num, act_dict[act])
                            n += 1
                            del li
                            if n % 500 == 0:
                                logging.debug("read samples: %d" % n)
                        
    logging.info("%d sapmles have read" % n)
    dataset = dataset[:n]
    dataflag = dataflag[:n]
    return dataset, dataflag

def spectrogram(array, channel=3):
    data = np.zeros((sepc_row, spec_col, channel), dtype=np.float64)
    for ch in range(channel):
        arr = array[:, ch]
        start = 0
        for i in range(sepc_row):
            frame = arr[start: start + nfft]
            windowed = window * frame
            res = np.fft.rfft(windowed)
            res_end = np.log(np.abs(res) ** 2)
            data[i, :, ch] = res_end
            start += overlap
            print(ch, res_end)
    return data

def plot_spectrogram(arr, name='image.png'):
    arr = np.array(arr, dtype=np.uint8)
    img = Image.fromarray(arr)
    img.save(name)


########################################
# run

if os.path.exists(DATA_DIR+'dataset.npy') and os.path.exists(DATA_DIR+'dataflag.npy'):
    logging.info(".npy files exist")
    dataset = np.load(DATA_DIR+'dataset.npy')
    dataflag = np.load(DATA_DIR+'dataflag.npy')
    logging.info("dataset has read from local file")
else:
    logging.info("dataset.npy not exsits, start reading .csv")
    dataset, dataflag = csv2arr()
    logging.info("saving dataset & dataflag")
    np.save('dataset.npy', dataset)
    np.save('dataflag.npy', dataflag)
    logging.info("dataset & dataflag have saved")


save_root = './sepc/'
try:
    os.mkdir(save_root)
except FileExistsError:
    pass

for i in range(len(dataset)):
    spec_arr = spectrogram(dataset[i])
    plot_spectrogram(spec_arr, (save_root + str(dataflag[i, 0]) + '_' + rev_act_dict[dataflag[i, 1]] + '.png'))
    if i % 100 == 0:
        logging.debug("spectrogram: %d" % i)


"""
# plot
arr = np.array(num_list, dtype=np.uint32)
num, bins = np.histogram(arr, 40)

P.figure(figsize=(32, 18))
P.hist(arr, bins, rwidth=0.9)
P.title(r'length of samples')
P.xlabel('length')
P.ylabel('number')
P.legend()
P.savefig('1.svg')
"""
