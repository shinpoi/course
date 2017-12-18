# - coding: utf-8 -*-
# python 3.5

import os
import re
import numpy as np
import csv
import logging
from chainer import using_config, no_backprop_mode, Variable, optimizers, serializers, cuda
import chainer.functions as F
import model

ROOT = './'
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s]   \t %(asctime)s \t%(message)s\t',
                    datefmt='%Y/%m/%d (%A) - %H:%M:%S',
                    )

#################
## set model
logging.info('setting model')

model = model.TINY_D()  # input: x, output: one hot y

cuda.get_device_from_id(0).use()
model.to_gpu(0)
xp = cuda.cupy

logging.info('GPU used')

p_num = re.compile('HASC([0-9]+).label')
p_act = re.compile('Activity: ([a-zA-z]+)')
p_label = re.compile('([0-9]+\.[0-9]+E[0-9]?),([0-9]+\.[0-9]+E[0-9]?)?,([a-zA-Z]+)')

act_dict = {'stay':0, 'walk':1, 'jog':2, 'skip':3, 'stup':4, 'stdown':5, 'start':6}

def float_(x):
    try:
        return float(x)
    except TypeError:
        return 0

def read_sequence(seq_dir):
    labels_li = []
    data_li = []
    for root, dirs, files in os.walk(seq_dir):
        if not root.endswith(r'/'):
            root = root + r'/'
        if not dirs:  # at /Person-xxxx
            for f_name in files:
                num = p_num.match(f_name)  # p_num = /HASC([0-9]+).meta/
                if num:
                    num = num.group(1)
                    # read label
                    with open(root + f_name) as f:
                        label_list = [int(num)]
                        while True:
                            try:
                                line = f.readline()
                            except UnicodeDecodeError:
                                print(root + f_name)
                                raise UnicodeDecodeError
                            if not line:
                                break
                            res = p_label.match(line)
                            if not res:
                                continue
                            try:
                                label_list.append([float_(res.group(1)), float_(res.group(2)), act_dict[res.group(3).lower()]])
                            except KeyError:
                                print(root + f_name)
                                print([res.group(1), res.group(2), res.group(3)])
                                raise KeyError
                    # read acc
                    with open(root + 'HASC%s-acc.csv' % num) as f:
                        li = [[float(y) for y in x] for x in csv.reader(f)]  # format: [time, x, y, z]
                        length = len(li)
                        data = np.zeros((length, 3), dtype=np.float64)
                        # label: time to flame
                        j = 0
                        for k in range(1, len(label_list)):
                            label = label_list[k]
                            for i in range(2):
                                if not label[i]:
                                    continue
                                for j in range(j, length):
                                    if li[j][0] > label[i]:
                                        label[i] = j-1
                                        break
                        data_li.append(li[1:])  # [[[x1, y1, z1], [x2, y2, z2], ..., [xn, yn, zn]], [...], ..., [...]] (3-dim)
                        labels_li.append(label_list)  # [[num, [st, end, act], [st, end, act], ..., [...]], [...], ... , [...]] (3-dim)
    return [np.array(x, dtype=np.float32) for x in data_li], labels_li


def seq2arrs(seq_arr):
    """
    <need code>
    """
    return spec_arrs

def predict(spec_arrs, model=model):
    with no_backprop_mode():
        x = Variable(spec_arrs)
        with using_config('train', False):
            y = model(x)
            ans = F.softmax(y.data)
            del x
            del y
    return ans
