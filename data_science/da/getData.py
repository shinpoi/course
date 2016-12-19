# -*- coding: utf-8 -*-
# Python2.7 & Python3.5
# TensorFlow r0.11

from tensorflow.examples.tutorials.mnist import input_data
import numpy as np

mnist = input_data.read_data_sets('MNIST_data', one_hot=False)

a = mnist.train.images
b = mnist.train.labels
c = mnist.test.images
d = mnist.test.labels

'''
# check list
for i in range(rank*rank):
    if i % rank == 0:
        print("\n")
    if i in li:
        print "[", i, "]",
    else:
        print i,
'''

# Parameter
rank = 28
pool = 2


# Function
# Reduce Data's Dimension By Pooling
def func_reduce(images, rank, pool):
    li = []
    for i in range(rank)[::pool]:
        for j in range(rank)[::pool]:
            li.append(28 * i + j)

    reduce_list = []
    for img in images:
        temp_list = []
        for n in li:
            temp_list.append((img[n] + img[n+1] + img[n+rank] + img[n+1+rank]) / pool**2)
        reduce_list.append(temp_list)
    return np.array(reduce_list)


# Write Into Files
def write_to_r(feature_set, label_set, name):
    n = len(feature_set[0])

    f = open(name, "w")

    for i in range(1, n + 1):
        f.write("v" + str(i) + "\t")

    f.write("class")
    f.write("\n")

    for i in range(len(feature_set)):
        for v in feature_set[i]:
            f.write(str(v) + "\t")

        f.write("[" + str(label_set[i]) + "]")
        f.write("\n")

    f.close()


# Reduce DataSet
scale_train = 100
train_images = func_reduce(images=mnist.train.images[::scale_train], rank=rank, pool=pool)
train_labels = mnist.train.labels[::scale_train]

scale_test = 10
test_images = func_reduce(images=mnist.test.images[::scale_test], rank=rank, pool=pool)
test_labels = mnist.test.labels[::scale_test]


# Check Length
print("len of images and labels of train and test is:", len(train_images), len(train_labels), len(test_images), len(test_labels))


# Test Function "write_to_r()"
"""
t = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [0, 2, 3, 5, 6]]
l = [1, 2, 3]
write_to_r(feature_set=t, label_set=l, name="test_func.txt")
"""

# Write Into Files
write_to_r(feature_set=train_images, label_set=train_labels, name="train_data.txt")
write_to_r(feature_set=test_images, label_set=test_labels, name="test_data.txt")
