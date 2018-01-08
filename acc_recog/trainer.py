# - coding: utf-8 -*-
# python 3.5

import os
import time
import logging
import numpy as np
from chainer import using_config, no_backprop_mode, Variable, optimizers, serializers, cuda
import chainer.functions as F
import model


#################
## init

ROOT = './dataset/'
xp = cuda.cupy
# xp = np   ### use CPU

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

class Model(object):
    def __init__(self):
        logging.info('reading dataset')
        dataset = np.load(ROOT + 'spec_dataset.npy')
        dataflag = np.load(ROOT + 'dataflag.npy')[:, 1]
        print("dataset.shape:", dataset.shape)
        length = len(dataset)
        gap = int(length*0.2)  # num of test samples
        ran_list = np.random.permutation(length)
        self.x_train = dataset[ran_list[gap:],]
        self.y_train = dataflag[ran_list[gap:],]

        self.x_test = xp.array(dataset[ran_list[:gap],])
        self.y_test = xp.array(dataflag[ran_list[:gap],])
        self.V_x_test = Variable(self.x_test)

        # x_train = dataset[ran_list,]  # test-data included
        # y_train = dataflag[ran_list,]  # test-data included

        ### confirm
        print("x_train.shape: ", self.x_train.shape)
        print("x_test.shape: ", self.x_test.shape)
        print("y_train.shape: ", self.y_train.shape)
        print("y_test.shape: ", self.y_test.shape)

        logging.info('setting model')

        self.model = model.TINY_D()  # input: x, output: one hot y
        self.lr = 0.002  # learning rate
        logging.info('start learning rate = %f' % self.lr)
        self.optimizer = optimizers.Adam(alpha=self.lr)
        self.optimizer.setup(self.model)

        ### to GPU
        cuda.get_device_from_id(0).use()
        self.model.to_gpu(0)
        logging.info('GPU used')

    def save_model(self, num):
        logging.info('save model at epoch: %s' % num)
        serializers.save_npz('cpu_model_%s.npz' % num, self.model)
        logging.info('Model \'cpu_model_%s.npz\' Saved' % num)

    def train(self, epoch=1000, bc=32):
        n = len(self.x_train)
        logging.info('training start, epoch = 0/%d' % epoch)
        for j in range(epoch):
            # train
            loss_sum = 0
            sff_index = np.random.permutation(n)
            for i in range(0, n, bc):
                x = Variable(xp.array(self.x_train[sff_index[i: (i + bc) if (i + bc) < n else n], ]))
                y = Variable(xp.array(self.y_train[sff_index[i: (i + bc) if (i + bc) < n else n], ]))
                self.model.cleargrads()
                loss = F.softmax_cross_entropy(self.model(x), y)
                loss.backward()
                self.optimizer.update()
                loss_sum += loss.data
            logging.debug("epoch: %d, loss = %f" % (j, loss_sum))

            if j % 10 == 0:
                self.evaluate()

            # update learning rate
            if j%100 == 0:
                rate = round(self.lr * ((epoch-j)/epoch), 4)
                if not rate:
                    rate = 0.000001
                self.optimizer.alpha = rate
                logging.debug("change alpha to %f" % rate)

            if j%500 == 0:
                self.save_model(str(j))
        return None

    # return oringal output (need softmax to probability)
    def predict(self, Vx=None):
        if not Vx:
            Vx = self.V_x_test
        with no_backprop_mode():
            with using_config('train', False):
                return self.model(Vx)

    def evaluate(self, true_yt=None, rt=False):
        if not true_yt:
            true_yt = self.y_test
        yt = self.predict()
        loss_test = F.softmax_cross_entropy(yt, true_yt).data
        logging.info("test: loss = %f" % loss_test)
        ans = yt.data
        if rt:
            return ans
        nrow, ncol = ans.shape
        acc = 0
        """
        ### print probability
        Sans = F.softmax(ans)
        for i in range(nrow):
            print("ans[%d]: " % i, Sans[i])
        """
        for i in range(nrow):
            cls = int(np.argmax(ans[i]))  # one hot -> int
            if cls == true_yt[i]:
                acc += 1
        print("accurate: %d/%d = %f" % (acc, self.y_test.shape[0], acc/self.y_test.shape[0]))


class SeqEvaluator(object):
    def __init__(self, model, seq_sepc, flag_list, spec_length, sepc_overlap):
        self.model = model
        self.seq_spec = seq_spec
        self.flag_list = flag_list
        self.spec_length = spec_length
        self.sepc_overlap = sepc_overlap

    def get_evaluate(self):
        pass
        # return eva_arr

    def plot(self):
        # https://stackoverflow.com/questions/9957637/how-can-i-set-the-background-color-on-specific-areas-of-a-pyplot-figure
        pass

if __name__ == '__main__':
    M = Model()
    M.train()
    M.save_model('end')
    logging.info('training end')
