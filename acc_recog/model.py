# - coding: utf-8 -*-
# python 3.5

from chainer import Chain
import chainer.functions as F
import chainer.links as L


class TINY_D(Chain):
    def __init__(self):
        super(TINY_D, self).__init__(
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
