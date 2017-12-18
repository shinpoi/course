# - coding: utf-8 -*-
# python 3.5

import os
import time
import logging
import numpy as np
from chainer import using_config, no_backprop_mode, Variable, optimizers, serializers, cuda
import chainer.functions as F
import model

ROOT = './'

#################
## init
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s]   \t %(asctime)s \t%(message)s\t',
                    datefmt='%Y/%m/%d (%A) - %H:%M:%S',
                    filename= ROOT + 'train-model_' + time.strftime('%Y-%m-%d_%H-%M') + '.log',
                    filemode='a'
                    )

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s]  \t%(message)s\t')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

#################
### read dataset
logging.info('reading dataset')

dataset = np.load(ROOT + 'spec_dataset_e0.npy')
dataflag = np.load(ROOT + 'dataflag.npy')[:, 1]

print("dataset.shape:", dataset.shape)

length = len(dataset)
gap = int(length*0.2)  # num of test samples

ran_list = np.random.permutation(length)
x_train = dataset[ran_list[gap:],]
# x_train = dataset[ran_list,]  # test-data included
x_test = dataset[ran_list[:gap],]

y_train = dataflag[ran_list[gap:],]
# y_train = dataflag[ran_list,]  # test-data included
y_test = dataflag[ran_list[:gap],]

#################
## set model and optimizer
logging.info('setting model')

model = model.TINY_D()  # input: x, output: one hot y
optimizer = optimizers.Adam()
optimizer.setup(model)

cuda.get_device_from_id(0).use()
model.to_gpu(0)
xp = cuda.cupy

x_test = xp.array(x_test)
y_test = xp.array(y_test)

logging.info('GPU used')

#################
## train
print("x_train.shape: ", x_train.shape)
print("x_test.shape: ", x_test.shape)
print("y_train.shape: ", y_train.shape)
print("y_test.shape: ", y_test.shape)

epoch = 3000
n = len(x_train)
bc = 32

def save_model(model, num):
    serializers.save_npz('cpu_model_%s.npz' % num, model)
    logging.info('Model \'cpu_model_%s.npz\' Saved' % num)

logging.info('training start')
for j in range(epoch):
    # train
    loss_sum = 0
    sff_index = np.random.permutation(n)
    for i in range(0, n, bc):
        x = Variable(xp.array(x_train[sff_index[i: (i + bc) if (i + bc) < n else n], ]))
        y = Variable(xp.array(y_train[sff_index[i: (i + bc) if (i + bc) < n else n], ]))
        model.cleargrads()
        loss = F.softmax_cross_entropy(model(x), y)
        loss.backward()
        optimizer.update()
        loss_sum += loss.data
    logging.debug("loop: %d, loss = %f" % (j, loss_sum))
    # update learning rate
    # optimizer.lr = learning_rate * (1 - batch / max_batches) ** lr_decay_power

    # evaluated
    if j % 10 == 0:
        with no_backprop_mode():
            xt = Variable(x_test)
            with using_config('train', False):
                yt = model(xt)
        loss_test = F.softmax_cross_entropy(yt, y_test).data
        logging.info("test: loss = %f" % loss_test)
        ans = yt.data
        nrow, ncol = ans.shape
        acc = 0
        """
        # print probability
        anss = F.softmax(ans)
        for i in range(nrow):
            print("ans[%d]: " % i, anss[i])
        """
        for i in range(nrow):
            cls = int(np.argmax(ans[i]))  # one hot -> int
            if cls == y_test[i]:
                acc += 1
        print("accurate: %d/%d = %f" % (acc, y_test.shape[0], acc/y_test.shape[0]))

        if j%100 == 0:
            rate = round(0.001*((epoch-j)/epoch), 6)
            if not rate:
                rate = 0.000001
            optimizer.alpha = rate
            logging.debug("change alpha to %f" % rate)

        if j%500 == 0:
            logging.info('save model at epoch: %d' % j)
            save_model(model, str(j))

logging.info('training end')
save_model(model, 'end')

#################
## test

#################
## evaluate
