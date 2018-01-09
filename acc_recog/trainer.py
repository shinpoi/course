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
    def __init__(self, load_data=True):
        logging.info('reading dataset')
        if load_data:
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
        else:
            self.x_train = self.y_train = self.x_test = self.y_test = self.V_x_test = None

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
    def predict(self, Vx):
        with no_backprop_mode():
            with using_config('train', False):
                return self.model(Vx)

    def evaluate(self, Vx=None, rt=False):
        if not Vx:
            true_yt = self.y_test
            Vx = self.V_x_test
        yt = self.predict(Vx)
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


from dataset import act_dict, rev_act_dict, MAX_LENGTH, overlap
import matplotlib.pyplot as plt
import os
import pickle as pk

class SeqEvaluator(object):
    def __init__(self, model, seq_spec, dataflag, spec_length=MAX_LENGTH, sepc_overlap=overlap):
        self.model = model
        self.seq_spec = np.array(seq_spec, dtype=xp.float32)
        self.dataflag = dataflag
        self.spec_length = spec_length
        self.sepc_overlap = sepc_overlap
        self.act_dict = act_dict
        self.rev_act_dict = rev_act_dict
        self.colors = ['red', 'orange', 'green', 'blue', 'darkviolet', 'black']
        logging.debug("data.shape: %s" % str(self.seq_spec.shape))
        logging.debug("len of flag: %d" % len(self.dataflag))

    @staticmethod
    def flag2time(flag_list):
        new_flag = []
        for sec in flag_list:  # [[st_time, ed_time, act_code], ..., ...]
            if sec[2] < 0 or sec[2] > 5:
                continue
            st = (sec[0]-2200)/55 + 20
            st = st if st > 0 else 0
            ed = (sec[1]-2200)/55 + 20
            ed = ed if ed > 0 else 0
            new_flag.append([int(st), int(ed), int(sec[2])])
        return new_flag

    @staticmethod
    def eva_overlap(eva_arr, flag_time):
        n = eva_arr.shape[0]
        t_len_sum = 0
        wrong = 0
        eva_arr = np.array([np.argmax(x) for x in eva_arr], dtype=np.int32)
        for t in flag_time:
            t_len = t[1]-t[0]
            t_len_sum += (t_len)
            ans = eva_arr[t[0]:t[1]] - (np.zeros(t_len, dtype=np.int32) + t[2])
            wrong += np.sum(np.logical_xor(ans, np.zeros(t_len, dtype=np.int32)))
        try:
            return 1 - wrong/t_len_sum
        except ZeroDivisionError:
            logging.error("error flag!: %s" % str(flag_time))
            return 0.9

    def set_seq_spec(self, seq_spec):
        self.seq_spec = None
        self.seq_spec = np.array(seq_spec, dtype=xp.float32)
        logging.debug("set new seq_spec, shape: %s" % str(self.seq_spec.shape))

    def get_a_evaluate(self, x):
        return F.softmax(self.model.predict(Variable(x))).data

    def plot(self, eva_arr, flag_time, save_name='uname.svg'):
        n = eva_arr.shape[0]
        n_acr = eva_arr.shape[1]
        plt.figure(0, figsize=(16, 9))
        plt.xlim(0, n)
        plt.ylim(0, 1.3)
        plt.xlabel("time")
        plt.ylabel("probability")

        for i in range(n_acr):
            plt.plot(range(n), eva_arr[:, i], label=self.rev_act_dict[i], color=self.colors[i], linewidth=1)

        for flag in flag_time:
            act = flag[2]
            plt.axvspan(flag[0], flag[1], facecolor=self.colors[act], alpha=0.2)

        plt.legend()
        plt.savefig(save_name, dpi=150)
        plt.close()

    def eva_all(self, save_root='./plot_seq_eva/', n_st=0):
        try:
            os.mkdir(save_root)
        except FileExistsError:
            pass

        n = self.seq_spec.shape[0]
        overrate_arr = np.zeros(n, dtype=np.float64)
        for i in range(n):
            flag_time = self.flag2time(dataflag[i+n_st])
            eva = cuda.to_cpu(self.get_a_evaluate(xp.array(self.seq_spec[i])))
            overrate_arr[i] = self.eva_overlap(eva, flag_time)
            self.plot(eva, flag_time, save_name=save_root + ('%d.svg' % (i+n_st)))
            if i % 10 == 0:
                print("eva_all(): %d/%d" % (i, n))
        logging.info("overlap rate = %f" % np.average(overrate_arr))

if __name__ == '__main__':
    """
    M = Model()
    M.train()
    M.save_model('end')
    logging.info('training end')
    """
    model = Model(load_data=False)
    serializers.load_npz('cpu_model_end.npz', model.model)
    with open("./dataset/seq/dataflag.pkl", 'rb') as f:
        dataflag = pk.load(f)
    sp_data = np.load("./dataset/seq/seq_spec_30.npy")
    sp_data = sp_data.transpose((0, 1, 4, 2, 3))
    se = SeqEvaluator(model, sp_data, dataflag)
    se.eva_all()

    for i in [60, 90, 120, 150, 177]:
        del sp_data
        print("read dataset: %d" % i)
        sp_data = np.load("./dataset/seq/seq_spec_%d.npy" % i).transpose((0, 1, 4, 2, 3))
        se.set_seq_spec(sp_data)
        se.eva_all(n_st=(round(i/30)*30-30))


"""
import trainer as tr
import numpy as np
import pickle as pk
from chainer import serializers, cuda
import matplotlib.pyplot as plt

xp = cuda.cupy
model = tr.Model(load_data=False)
serializers.load_npz('cpu_model_end.npz', model.model)
with open("./dataset/seq/dataflag.pkl", 'rb') as f:
    dataflag = pk.load(f)
sp_data = np.load("./dataset/seq/seq_spec_30.npy")
sp_data = sp_data.transpose((0, 1, 4, 2, 3))
se = tr.SeqEvaluator(model, sp_data, sp_data)

d = cuda.to_cpu(se.get_a_evaluate(xp.array(sp_data[0], dtype=xp.float32)))
se.plot(d, dataflag[0])
"""
