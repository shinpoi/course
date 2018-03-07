# - coding: utf-8 -*-
# python 3.5

import os
import time
import logging
import numpy as np
from chainer import using_config, no_backprop_mode, Variable, optimizers, serializers, cuda
import chainer.functions as F
import model
import pickle as pk


#################
## init

ROOT = './'
xp = cuda.cupy
# xp = np   ### use CPU

logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s]   \t %(asctime)s \t%(message)s\t',
                    datefmt='%Y/%m/%d (%A) - %H:%M:%S',
                    filename= ROOT + 'log/train-model_' + time.strftime('%Y-%m-%d_%H-%M') + '.log',
                    filemode='a'
                    )

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s]  \t%(message)s\t')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

class Model(object):
    def __init__(self, dataset, dataflag, load_data=True, load_model=None):
        logging.info('reading dataset')
        if load_data:
            print("dataset.shape:", dataset.shape)
            self.dataset = dataset
            self.dataflag = dataflag
            self.x_train = None
            self.y_train = None
            self.x_test = None
            self.y_test = None
            self.yl = None
            self.V_x_test = None
            ### confirm
            print("dataset.shape: ", self.dataset.shape)
            print("dataflag.shape: ", self.dataflag.shape)
            self.acclist = []
            self.loss_list = []
            self.test_loss_list = []
        else:
            self.x_train = self.y_train = self.x_test = self.y_test = self.V_x_test = None

        logging.info('setting model')

        if not load_model:
            self.model = model.TINY_D_36ch()  # input: x, output: one hot y
        else:
            self.model = load_model()
        self.lr = 0.002  # learning rate
        logging.info("basic lr = %f" % self.lr)
        logging.info('start learning rate = %f' % self.lr)
        self.optimizer = optimizers.Adam(alpha=self.lr)
        self.optimizer.setup(self.model)

        ### to GPU
        cuda.get_device_from_id(0).use()
        self.model.to_gpu(0)
        logging.info('GPU used')

    def clear_dataset(self):
        try:
            del self.x_train
            del self.y_train
            del self.x_test
            del self.y_test
            del self.yl
            del self.V_x_test
        except NameError as mes:
            logging.error("error at clear_dataset()!")
            logging.error(mes)

    def set_dataset(self, gap_rate=0.2):
        self.clear_dataset()
        length = len(self.dataset)
        gap = int(length*gap_rate)  # num of test samples
        ################
        # temp
        gap = 150
        ################
        # logging.info("gap rate = %f" % gap_rate)
        ran_list = np.random.permutation(length)
        self.x_train = self.dataset[ran_list[gap:],]
        self.y_train = self.dataflag[ran_list[gap:],]
        self.x_test = xp.array(self.dataset[ran_list[:gap],])
        self.y_test = xp.array(self.dataflag[ran_list[:gap],])
        self.yl = self.y_test.shape[0]
        self.V_x_test = Variable(self.x_test)
        logging.info("dataset reset!")
        ### confirm
        print("x_train.shape: ", self.x_train.shape)
        print("x_test.shape: ", self.x_test.shape)
        print("y_train.shape: ", self.y_train.shape)
        print("y_test.shape: ", self.y_test.shape)

    def save_model(self, num):
        logging.info('save model at epoch: %s' % num)
        serializers.save_npz('cpu_model_%s.npz' % num, self.model)
        logging.info('Model \'cpu_model_%s.npz\' Saved' % num)

    def train(self, epoch=1000, bc=30):
        self.acclist = []
        self.loss_list = []
        self.test_loss_list = []
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
            logging.debug("epoch: %d, loss = %f" % (j, loss_sum/bc))
            if j % 10 == 0:
                logging.info('epoch = %d/1000' % j)
                self.loss_list.append(float(loss_sum/bc))
                self.evaluate()
            # update learning rate
            if j%100 == 0:
                rate = round(self.lr * ((epoch-j)/epoch)**2, 6)
                if rate <= 0:
                    rate = 0.000001
                self.optimizer.alpha = rate
                logging.debug("change alpha to %f" % rate)
            #if j%500 == 0:
                #self.save_model(str(j))
        return self.acclist, self.loss_list, self.test_loss_list

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
        logging.info("test: loss = %f" % (loss_test/self.yl))
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
        tp = fp = tn = fn = 0
        for i in range(nrow):
            cls = int(np.argmax(ans[i]))  # one hot -> int
            if true_yt[i] == 1:
                if cls == true_yt[i]:
                    tp += 1
                else:
                    fp += 1
            else:
                if cls == true_yt[i]:
                    tn += 1
                else:
                    fn += 1

        # logging.info("precison: %d/%d = %f" % (tp, tp+fp, (tp/(tp+fp)) ))
        # logging.info("recall: %d/%d = %f" % (tp, tp+fn, (tp/(tp+fn)) ))
        logging.info("accurate: %d/%d = %f" % (tp+tn, tp+fp+fn+tn, ((tp+tn)/(tp+fp+fn+tn)) ))
        self.acclist.append((tp+tn)/(tp+fp+fn+tn))
        self.test_loss_list.append(float(loss_test/self.yl))


if __name__ == '__main__':
    ### read data
    # dataset.shape = (sample, channel, x-axis, y-axis)
    dataset = np.load(ROOT + 'log21_2400_spec.npy')
    dataflag = np.load(ROOT + 'log21_2400_label.npy')
    """
    ### training
    M = Model(dataset, dataflag, load_model=model.TINY_D_2ch)
    # M = Model(dataset, dataflag)
    acclist = M.train()
    # M.save_model('end')
    #####################################
    # single ch
    for i in range(18):
        print("ch: %d" % i)
        li_list = []
        dataset_ch = dataset[:,(i*2):(i*2+2)]
        M = Model(dataset_ch, dataflag, load_model=model.TINY_D_2ch)
        for j in range(100):
            M.set_dataset()
            li = M.train()  # [acclist, loss_list, test_loss_list]
            li_list.append(li)
        with open("./log/acclist_ch%d.pkl" % i, "wb") as f:
            pk.dump(li_list, f)
    """
    #####################################
    # all ch
    acclist_list = []
    M = Model(dataset, dataflag)
    for i in range(100):
        print("all ch: %d/%d" % (i,200))
        M.set_dataset()
        acclist = M.train()
        acclist_list.append(acclist)

    logging.info("finish!")
    with open("./log/acclist_allch.pkl", "wb") as f:
        pk.dump(acclist_list, f)

    """
    ### plot
    for i in range(100):
        plt.figure(0, figsize=(16,9))
        plt.subplot(311)
        plt.title("accurate")
        plt.xlabel("epoch(x0.1)")
        plt.plot(range(100), a[i,0], color="red")

        plt.subplot(312)
        plt.title("loss of training")
        plt.xlabel("epoch(x0.1)")
        plt.plot(range(99), a[i,2,1:], color="green")

        plt.subplot(313)
        plt.title("loss of test")
        plt.xlabel("epoch(x0.1)")
        plt.plot(range(100), a[i,1])
        plt.tight_layout(pad=1.0, w_pad=0.1, h_pad=1.5)
        plt.savefig("plot/%d.svg" % i)
        plt.close()
        print("%d/99" % i)
    """
