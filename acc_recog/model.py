# - coding: utf-8 -*-
# python 3.5

from chainer import Chain
import chainer.functions as F
import chainer.links as L


class TINY_D_3ch(Chain):
    def __init__(self):
        super(TINY_D_3ch, self).__init__(
            conv1  = L.Convolution2D(3, 64, ksize=3, stride=1, pad=1, nobias=True),
            bn1    = L.BatchNormalization(64, use_beta=False),
            bias1  = L.Bias(shape=(64,)),
            # MaxPool(3x3, 2)
            conv2  = L.Convolution2D(64, 128, ksize=3, stride=1, pad=1, nobias=True),
            bn2    = L.BatchNormalization(128, use_beta=False),
            bias2  = L.Bias(shape=(128,)),
            # MaxPool(3x3, 2)
            conv3  = L.Convolution2D(128, 256, ksize=3, stride=1, pad=1, nobias=True),
            bn3    = L.BatchNormalization(256, use_beta=False),
            bias3  = L.Bias(shape=(256,)),
            # MaxPool(3x3, 2)
            conv4  = L.Convolution2D(256, 512, ksize=3, stride=1, pad=1, nobias=True),
            bn4    = L.BatchNormalization(512, use_beta=False),
            bias4  = L.Bias(shape=(512,)),

            conv5  = L.Convolution2D(512, 512, ksize=1, stride=1, pad=0, nobias=True),
            # AvgPool(3x3, 2)
            conv6 = L.Convolution2D(512, 6, ksize=1, stride=1, pad=0),
        )

    def __call__(self, x):
        h = F.leaky_relu(self.bias1(self.bn1(self.conv1(x))), slope=0.1)
        h = F.max_pooling_2d(h, ksize=3, stride=2, pad=0)

        h = F.leaky_relu(self.bias2(self.bn2(self.conv2(h))), slope=0.1)
        h = F.max_pooling_2d(h, ksize=3, stride=2, pad=0)

        h = F.leaky_relu(self.bias3(self.bn3(self.conv3(h))), slope=0.1)
        h = F.max_pooling_2d(h, ksize=3, stride=2, pad=0)

        h = F.leaky_relu(self.bias4(self.bn4(self.conv4(h))), slope=0.1)
        h = F.max_pooling_2d(h, ksize=3, stride=2, pad=0)

        h = self.conv5(h)
        h = F.average_pooling_2d(h, ksize=(h.shape[-2], h.shape[-1]))
        h = self.conv6(h)
        # h = F.dropout(h, ratio=0.4)
        # h = self.out(h)
        return h.reshape((h.shape[0], -1))


class TINY_D_6ch(Chain):
    def __init__(self):
        super(TINY_D_6ch, self).__init__(
            conv1a  = L.Convolution2D(3, 64, ksize=3, stride=1, pad=1, nobias=True),
            bn1a    = L.BatchNormalization(64, use_beta=False),
            bias1a  = L.Bias(shape=(64,)),
            conv1b  = L.Convolution2D(3, 64, ksize=3, stride=1, pad=1, nobias=True),
            bn1b    = L.BatchNormalization(64, use_beta=False),
            bias1b  = L.Bias(shape=(64,)),
            # MaxPool(3x3, 2)
            conv2a  = L.Convolution2D(64, 128, ksize=3, stride=1, pad=1, nobias=True),
            bn2a    = L.BatchNormalization(128, use_beta=False),
            bias2a  = L.Bias(shape=(128,)),
            conv2b  = L.Convolution2D(64, 128, ksize=3, stride=1, pad=1, nobias=True),
            bn2b    = L.BatchNormalization(128, use_beta=False),
            bias2b  = L.Bias(shape=(128,)),
            # MaxPool(3x3, 2)
            conv3a  = L.Convolution2D(128, 256, ksize=3, stride=1, pad=1, nobias=True),
            bn3a    = L.BatchNormalization(256, use_beta=False),
            bias3a  = L.Bias(shape=(256,)),
            conv3b  = L.Convolution2D(128, 256, ksize=3, stride=1, pad=1, nobias=True),
            bn3b    = L.BatchNormalization(256, use_beta=False),
            bias3b  = L.Bias(shape=(256,)),
            # MaxPool(3x3, 2)
            conv4a  = L.Convolution2D(256, 512, ksize=3, stride=1, pad=1, nobias=True),
            bn4a    = L.BatchNormalization(512, use_beta=False),
            bias4a  = L.Bias(shape=(512,)),
            conv4b  = L.Convolution2D(256, 512, ksize=3, stride=1, pad=1, nobias=True),
            bn4b    = L.BatchNormalization(512, use_beta=False),
            bias4b  = L.Bias(shape=(512,)),
            ##### F.concat() ####
            conv5  = L.Convolution2D(1024, 1024, ksize=1, stride=1, pad=0, nobias=True),
            # AvgPool(3x3, 2)
            conv6 = L.Convolution2D(1024, 6, ksize=1, stride=1, pad=0),
        )

    def __call__(self, x):
        ### x.shape = [bc, ch, row, col]
        xa = x[:, :3]
        xb = x[:, 3:]
        del x
        ha = F.leaky_relu(self.bias1a(self.bn1a(self.conv1a(xa))), slope=0.1)
        ha = F.max_pooling_2d(ha, ksize=3, stride=2, pad=0)
        ha = F.leaky_relu(self.bias2a(self.bn2a(self.conv2a(ha))), slope=0.1)
        ha = F.max_pooling_2d(ha, ksize=3, stride=2, pad=0)
        ha = F.leaky_relu(self.bias3a(self.bn3a(self.conv3a(ha))), slope=0.1)
        ha = F.max_pooling_2d(ha, ksize=3, stride=2, pad=0)
        ha = F.leaky_relu(self.bias4a(self.bn4a(self.conv4a(ha))), slope=0.1)
        ha = F.max_pooling_2d(ha, ksize=3, stride=2, pad=0)

        hb = F.leaky_relu(self.bias1b(self.bn1b(self.conv1b(xb))), slope=0.1)
        hb = F.max_pooling_2d(hb, ksize=3, stride=2, pad=0)
        hb = F.leaky_relu(self.bias2b(self.bn2b(self.conv2b(hb))), slope=0.1)
        hb = F.max_pooling_2d(hb, ksize=3, stride=2, pad=0)
        hb = F.leaky_relu(self.bias3b(self.bn3b(self.conv3b(hb))), slope=0.1)
        hb = F.max_pooling_2d(hb, ksize=3, stride=2, pad=0)
        hb = F.leaky_relu(self.bias4b(self.bn4b(self.conv4b(hb))), slope=0.1)
        hb = F.max_pooling_2d(hb, ksize=3, stride=2, pad=0)

        h = F.concat((ha, hb), axis=1)
        del ha
        del hb
        h = self.conv5(h)
        h = F.average_pooling_2d(h, ksize=(h.shape[-2], h.shape[-1]))
        h = self.conv6(h)
        # h = F.dropout(h, ratio=0.4)
        # h = self.out(h)
        return h.reshape((h.shape[0], -1))

############################

class TEST_I_6ch(Chain):
    def __init__(self):
        super(TEST_I_6ch, self).__init__(
            conv1a  = L.Convolution2D(3, 64, ksize=3, stride=1, pad=1, nobias=True),
            bn1a    = L.BatchNormalization(64, use_beta=False),
            bias1a  = L.Bias(shape=(64,)),
            conv1b  = L.Convolution2D(3, 64, ksize=3, stride=1, pad=1, nobias=True),
            bn1b    = L.BatchNormalization(64, use_beta=False),
            bias1b  = L.Bias(shape=(64,)),
            # MaxPool(3x3, 2)
            conv2a  = L.Convolution2D(64, 128, ksize=3, stride=1, pad=1, nobias=True),
            bn2a    = L.BatchNormalization(128, use_beta=False),
            bias2a  = L.Bias(shape=(128,)),
            conv2b  = L.Convolution2D(64, 128, ksize=3, stride=1, pad=1, nobias=True),
            bn2b    = L.BatchNormalization(128, use_beta=False),
            bias2b  = L.Bias(shape=(128,)),
            # MaxPool(3x3, 2)
            conv3a  = L.Convolution2D(128, 256, ksize=3, stride=1, pad=1, nobias=True),
            bn3a    = L.BatchNormalization(256, use_beta=False),
            bias3a  = L.Bias(shape=(256,)),
            conv3b  = L.Convolution2D(128, 256, ksize=3, stride=1, pad=1, nobias=True),
            bn3b    = L.BatchNormalization(256, use_beta=False),
            bias3b  = L.Bias(shape=(256,)),
            # MaxPool(3x3, 2)
            ##### F.concat() ####
            conv5  = L.Convolution2D(512, 512, ksize=1, stride=1, pad=0, nobias=True),
            # AvgPool(3x3, 28)
            conv6 = L.Convolution2D(512, 6, ksize=1, stride=1, pad=0),
        )

    def __call__(self, x):
        ### x.shape = [bc, ch, row, col]
        xa = x[:, :3]
        xb = x[:, 3:]
        del x
        ha = F.leaky_relu(self.bias1a(self.bn1a(self.conv1a(xa))), slope=0.1)
        ha = F.max_pooling_2d(ha, ksize=3, stride=2, pad=0)
        ha = F.leaky_relu(self.bias2a(self.bn2a(self.conv2a(ha))), slope=0.1)
        ha = F.max_pooling_2d(ha, ksize=3, stride=2, pad=0)
        ha = F.leaky_relu(self.bias3a(self.bn3a(self.conv3a(ha))), slope=0.1)
        ha = F.max_pooling_2d(ha, ksize=3, stride=2, pad=0)

        hb = F.leaky_relu(self.bias1b(self.bn1b(self.conv1b(xb))), slope=0.1)
        hb = F.max_pooling_2d(hb, ksize=3, stride=2, pad=0)
        hb = F.leaky_relu(self.bias2b(self.bn2b(self.conv2b(hb))), slope=0.1)
        hb = F.max_pooling_2d(hb, ksize=3, stride=2, pad=0)
        hb = F.leaky_relu(self.bias3b(self.bn3b(self.conv3b(hb))), slope=0.1)
        hb = F.max_pooling_2d(hb, ksize=3, stride=2, pad=0)

        h = F.concat((ha, hb), axis=1)
        del ha
        del hb
        h = self.conv5(h)
        h = F.average_pooling_2d(h, ksize=(h.shape[-2], h.shape[-1]))
        h = self.conv6(h)
        # h = F.dropout(h, ratio=0.4)
        # h = self.out(h)
        return h.reshape((h.shape[0], -1))

#########################

class TEST_II_6ch(Chain):
    def __init__(self):
        super(TEST_II_6ch, self).__init__(
            conv1a  = L.Convolution2D(3, 64, ksize=(3,2), stride=1, pad=(1,0), nobias=True),
            bn1a    = L.BatchNormalization(64, use_beta=False),
            bias1a  = L.Bias(shape=(64,)),
            conv1b  = L.Convolution2D(3, 64, ksize=(3,2), stride=1, pad=(1,0), nobias=True),
            bn1b    = L.BatchNormalization(64, use_beta=False),
            bias1b  = L.Bias(shape=(64,)),
            # MaxPool(3x3, 2)
            conv2a  = L.Convolution2D(64, 128, ksize=(3,2), stride=1, pad=(1,0), nobias=True),
            bn2a    = L.BatchNormalization(128, use_beta=False),
            bias2a  = L.Bias(shape=(128,)),
            conv2b  = L.Convolution2D(64, 128, ksize=(3,2), stride=1, pad=(1,0), nobias=True),
            bn2b    = L.BatchNormalization(128, use_beta=False),
            bias2b  = L.Bias(shape=(128,)),
            # MaxPool(3x3, 2)
            conv3a  = L.Convolution2D(128, 256, ksize=(3,2), stride=1, pad=(1,0), nobias=True),
            bn3a    = L.BatchNormalization(256, use_beta=False),
            bias3a  = L.Bias(shape=(256,)),
            conv3b  = L.Convolution2D(128, 256, ksize=(3,2), stride=1, pad=(1,0), nobias=True),
            bn3b    = L.BatchNormalization(256, use_beta=False),
            bias3b  = L.Bias(shape=(256,)),
            # MaxPool(3x3, 2)
            ##### F.concat() ####
            conv5  = L.Convolution2D(512, 512, ksize=1, stride=1, pad=0, nobias=True),
            # AvgPool(3x3, 28)
            conv6 = L.Convolution2D(512, 6, ksize=1, stride=1, pad=0),
        )

    def __call__(self, x):
        ### x.shape = [bc, ch, row, col]
        xa = x[:, :3]
        xb = x[:, 3:]
        del x
        ha = F.leaky_relu(self.bias1a(self.bn1a(self.conv1a(xa))), slope=0.1)
        ha = F.max_pooling_2d(ha, ksize=3, stride=2, pad=0)
        ha = F.leaky_relu(self.bias2a(self.bn2a(self.conv2a(ha))), slope=0.1)
        ha = F.max_pooling_2d(ha, ksize=3, stride=2, pad=0)
        ha = F.leaky_relu(self.bias3a(self.bn3a(self.conv3a(ha))), slope=0.1)
        ha = F.max_pooling_2d(ha, ksize=3, stride=2, pad=0)

        hb = F.leaky_relu(self.bias1b(self.bn1b(self.conv1b(xb))), slope=0.1)
        hb = F.max_pooling_2d(hb, ksize=3, stride=2, pad=0)
        hb = F.leaky_relu(self.bias2b(self.bn2b(self.conv2b(hb))), slope=0.1)
        hb = F.max_pooling_2d(hb, ksize=3, stride=2, pad=0)
        hb = F.leaky_relu(self.bias3b(self.bn3b(self.conv3b(hb))), slope=0.1)
        hb = F.max_pooling_2d(hb, ksize=3, stride=2, pad=0)

        h = F.concat((ha, hb), axis=1)
        del ha
        del hb
        h = self.conv5(h)
        h = F.average_pooling_2d(h, ksize=(h.shape[-2], h.shape[-1]))
        h = self.conv6(h)
        # h = F.dropout(h, ratio=0.4)
        # h = self.out(h)
        return h.reshape((h.shape[0], -1))

#########################

class TEST_III_6ch(Chain):
    def __init__(self):
        super(TEST_III_6ch, self).__init__(
            conv1a  = L.Convolution2D(3, 64, ksize=(2,3), stride=1, pad=1, nobias=True),
            bn1a    = L.BatchNormalization(64, use_beta=False),
            bias1a  = L.Bias(shape=(64,)),
            conv1b  = L.Convolution2D(3, 64, ksize=(2,3), stride=1, pad=1, nobias=True),
            bn1b    = L.BatchNormalization(64, use_beta=False),
            bias1b  = L.Bias(shape=(64,)),
            # MaxPool(3x3, 2)
            conv2a  = L.Convolution2D(64, 128, ksize=(2,3), stride=1, pad=(0,1), nobias=True),
            bn2a    = L.BatchNormalization(128, use_beta=False),
            bias2a  = L.Bias(shape=(128,)),
            conv2b  = L.Convolution2D(64, 128, ksize=(2,3), stride=1, pad=(0,1), nobias=True),
            bn2b    = L.BatchNormalization(128, use_beta=False),
            bias2b  = L.Bias(shape=(128,)),
            # MaxPool(3x3, 2)
            conv3a  = L.Convolution2D(128, 256, ksize=(2,3), stride=1, pad=1, nobias=True),
            bn3a    = L.BatchNormalization(256, use_beta=False),
            bias3a  = L.Bias(shape=(256,)),
            conv3b  = L.Convolution2D(128, 256, ksize=(2,3), stride=1, pad=1, nobias=True),
            bn3b    = L.BatchNormalization(256, use_beta=False),
            bias3b  = L.Bias(shape=(256,)),
            # MaxPool(3x3, 2)
            ##### F.concat() ####
            conv5  = L.Convolution2D(512, 512, ksize=1, stride=1, pad=0, nobias=True),
            # AvgPool(3x3, 28)
            conv6 = L.Convolution2D(512, 6, ksize=1, stride=1, pad=0),
        )

    def __call__(self, x):
        ### x.shape = [bc, ch, row, col]
        xa = x[:, :3]
        xb = x[:, 3:]
        del x
        #print(xa.shape)
        ha = F.leaky_relu(self.bias1a(self.bn1a(self.conv1a(xa))), slope=0.1)
        #print(ha.shape)
        ha = F.max_pooling_2d(ha, ksize=3, stride=2, pad=0)
        #print(ha.shape)
        ha = F.leaky_relu(self.bias2a(self.bn2a(self.conv2a(ha))), slope=0.1)
        #print(ha.shape)
        ha = F.max_pooling_2d(ha, ksize=3, stride=2, pad=0)
        #print(ha.shape)
        ha = F.leaky_relu(self.bias3a(self.bn3a(self.conv3a(ha))), slope=0.1)
        #print(ha.shape)
        ha = F.max_pooling_2d(ha, ksize=3, stride=2, pad=0)
        #print(ha.shape)

        hb = F.leaky_relu(self.bias1b(self.bn1b(self.conv1b(xb))), slope=0.1)
        hb = F.max_pooling_2d(hb, ksize=3, stride=2, pad=0)
        hb = F.leaky_relu(self.bias2b(self.bn2b(self.conv2b(hb))), slope=0.1)
        hb = F.max_pooling_2d(hb, ksize=3, stride=2, pad=0)
        hb = F.leaky_relu(self.bias3b(self.bn3b(self.conv3b(hb))), slope=0.1)
        hb = F.max_pooling_2d(hb, ksize=3, stride=2, pad=0)

        h = F.concat((ha, hb), axis=1)
        del ha
        del hb
        h = self.conv5(h)
        h = F.average_pooling_2d(h, ksize=(h.shape[-2], h.shape[-1]))
        h = self.conv6(h)
        # h = F.dropout(h, ratio=0.4)
        # h = self.out(h)
        return h.reshape((h.shape[0], -1))
