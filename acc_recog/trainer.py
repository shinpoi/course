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
    def __init__(self, load_data=True, load_model=None):
        logging.info('reading dataset')
        if load_data:
            dataset_name = ROOT + 'spec_dataset.npy'
            dataflag_name = ROOT + 'dataflag.npy'
            dataset = np.load(dataset_name)
            dataflag = np.load(dataflag_name)[:, 1]
            print("dataset.shape:", dataset.shape)
            print("read dataset from: %s" % dataset_name)
            print("read dataflag from: %s" % dataflag_name)
            length = len(dataset)
            gap = int(length*0.2)  # num of test samples
            ran_list = np.random.permutation(length)
            self.x_train = dataset[ran_list[gap:],]
            self.y_train = dataflag[ran_list[gap:],]

            # self.x_test = xp.array(dataset[ran_list[:gap],])
            # self.y_test = xp.array(dataflag[ran_list[:gap],])
            self.x_test = xp.array(dataset[ran_list,])
            self.y_test = xp.array(dataflag[ran_list,])
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

        if not load_model:
            self.model = model.TINY_D_6ch()  # input: x, output: one hot y
        else:
            self.model = load_model()
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
                rate = round(self.lr * ((epoch-j)/epoch)**2, 6)
                if rate <= 0:
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
            # extra -- detail of evaluate
            detail_acc[int(true_yt[i]), cls] += 1
            if cls == true_yt[i]:
                acc += 1
        logging.info("accurate: %d/%d = %f" % (acc, self.y_test.shape[0], acc/self.y_test.shape[0]))


from dataset import act_dict, rev_act_dict, MAX_LENGTH, overlap, nfft, spectrogram, spec_col, spec_row
import matplotlib.pyplot as plt
import os
import pickle as pk

class SeqEvaluator(object):
    def __init__(self, model, seq_spec, dataflag, spec_length=MAX_LENGTH, sepc_overlap=overlap):
        self.model = model
        # self.seq_spec = np.array(seq_spec, dtype=xp.float32)
        self.seq_spec = seq_spec
        self.data = None
        self.dataflag = dataflag
        #self.len_data = dataset.shape[2]
        self.len_spec = int((self.len_data - nfft)/overlap + 1)
        #self.f2f_rate = len_spec/len_data
        self.f2f_rate = 0.01815
        self.spec_length = spec_length
        self.sepc_overlap = sepc_overlap
        self.act_dict = act_dict
        self.rev_act_dict = rev_act_dict
        self.colors = ['red', 'orange', 'green', 'blue', 'darkviolet', 'black']
        self.delay = 20  ## frames(spec) of delay
        # logging.debug("data.shape: %s" % str(self.seq_spec.shape))
        # logging.debug("len of flag: %d" % len(self.dataflag))

    def flag2time(self, flag_list):
        new_flag = []
        for sec in flag_list:  # flag_list = [[st_frame, ed_frame, act_code], ..., ...]
            if sec[2] < 0 or sec[2] > 5:
                continue
            st = sec[0]*self.f2f_rate
            ed = sec[1]*self.f2f_rate
            new_flag.append([int(st), int(ed), int(sec[2])])
        return new_flag

    # spectrogram(array, channel, spec_row, spec_col)
    def data2sepc(self, arr, step=spec_row):
        ch = self.dataset.shape[1]
        spec = spectrogram(arr, ch, self.len_spec, spec_col)
        spec_batch = np.zeros((self.len_spec, ch, step, spec_col), dtype=np.float32)
        for i in range(self.len_spec-step):
            spec_batch[i] = spec[i:i+step].transpose((2,0,1))
        return spec_batch

    def eva_overlap(self, eva_arr, flag_time):
        n = eva_arr.shape[0]
        t_len_sum = 0
        wrong = 0
        eva_arr = np.array([np.argmax(x) for x in eva_arr], dtype=np.int32)
        eva_arr[self.delay:] = eva_arr[:-self.delay]
        eva_arr[:self.delay] *= 0
        eva_arr[:self.delay] += eva_arr[self.delay+1]
        for t in flag_time:
            t_len = t[1]-t[0]
            t_len_sum += (t_len)
            ### equal = 0, unequal = 1
            #-------detail eva----------
            # t[0]:real start, t[1]:real end, t[2]:label, eva_arr[t[0]:t[1]]:predict ans
            for i in eva_arr[t[0]:t[1]]:
                detail_acc[t[2], i] += 1
            #-------detail eva----------
            ans = eva_arr[t[0]:t[1]] - (np.zeros(t_len, dtype=np.int32) + t[2])
            wrong += np.sum(np.logical_xor(ans, np.zeros(t_len, dtype=np.int32)))
        try:
            return 1 - wrong/t_len_sum
        except ZeroDivisionError:
            logging.error("wrong flag!: %s" % str(flag_time))
            return 0.9   # just for emergency, need fix (flag_time has bad data)

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
        plt.xlabel("frames (1 frame = 0.55s)")
        plt.ylabel("probability")

        for i in range(n_acr):
            plt.plot(range(self.delay, n), eva_arr[:-self.delay, i], label=self.rev_act_dict[i], color=self.colors[i], linewidth=1)

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
            self.plot(eva, flag_time, save_name=save_root + ('%d_.svg' % (i+n_st)))
            if i % 10 == 0:
                print("eva_all(): %d/%d" % (i, n))
        logging.info("overlap rate = %f" % np.average(overrate_arr))
        return eva, flag_time

if __name__ == '__main__':
    # extra -- detail of evaluate
    detail_acc = np.zeros((6, 6), dtype=np.uint32)

    """
    ### training
    M = Model()
    M.train()
    M.save_model('end')
    logging.info('training end')
    """
    ### eval seq
    data_root = "./dataset/seq_6ch_NoS3/"
    model = Model(load_data=False)
    # model = Model(load_model=model.TINY_D_3ch)
    serializers.load_npz(data_root + "cpu_model_end.npz", model.model)
    with open(data_root + "dataflag.pkl", 'rb') as f:
        dataflag = pk.load(f)
    se = SeqEvaluator(model, None, dataflag)

    for i in range(20, 81, 20):
        print("read dataset: %d" % i)
        sp_data = np.load(data_root + "seq_spec_%d.npy" % i).transpose((0, 1, 4, 2, 3))
        se.set_seq_spec(sp_data)
        se.eva_all(n_st=(round(i/20)*20-20))
        del sp_data
    """
    # detail evaluate -- static
    data_root = "./dataset/seq_3ch_acc_NoS3/"
    ROOT = data_root
    M = Model(load_model=model.TINY_D_3ch)
    serializers.load_npz(data_root + "cpu_model_end.npz", M.model)
    M.evaluate()
    """
    print(detail_acc)
