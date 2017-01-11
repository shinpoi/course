# -*- coding: utf-8 -*-
# Python 2.7
# OpenCV 3.1

import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

# img = cv2.imread('git_avatar.png')
# size = (330, 330)

img = cv2.imread('lowcontrast.jpg')
img = cv2.resize(img, (1200, 900))
img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
size = (900, 1200)

#########################################################
# function definition start


# equalize histogram
def hist_equalize(src):
    # sort
    img_new = np.array(src).reshape((-1,))
    img_list = [(j, i) for i, j in enumerate(img_new)]
    img_list.sort()

    # equalize
    bins_number = int(img_new.shape[0] / 256.0) + 1
    n = 0
    for color in range(256):
        try:
            for i in range(bins_number):
                j = img_list[n][1]
                img_new[j] = color
                n += 1
        except IndexError:
            break
    return img_new


# flatten histogram
def hist_flatten(src):
    img_new = np.array(src).reshape((-1,))
    hist = cv2.calcHist((img_new,), (0,), None, (256,), (0, 256))
    n = float(len(img_new))

    # normalize
    for i in range(len(hist)):
        hist[i] /= n

    # accumulate
    hist_sum = np.zeros(len(hist))
    for i in range(len(hist)):
        hist_sum[i] = sum(hist[:i])

    # flatten
    for i in range(len(img_new)):
        img_new[i] = 255 * hist_sum[img_new[i]]
    return img_new


# run (with HSV color-space)
def run(src, func, shape):
    time_start = time.clock()
    img_new = np.array(img)
    img_new[:, :, 2] = func(src[:, :, 2]).reshape(shape)
    print("runtime = %f" % (time.clock() - time_start))
    return img_new


# show hist (with HSV color-space)
def show_hist(src, number, name='hist'):
    hist = cv2.calcHist((src[:, :, 2],), (0,), None, (256,), (0, 256))

    n = 256
    plt.figure(number, figsize=(16, 9))
    plt.xlim((0, 255))
    plt.bar(range(n), hist, label='Lightness', color='#99aabb', edgecolor='#ddeeff')
    plt.xlabel("value")
    plt.ylabel("frequency")
    plt.title(name)
    plt.legend()

# function definition end
#########################################################

# run
img_equalize = run(img, func=hist_equalize, shape=size)
img_flatten = run(img, func=hist_flatten, shape=size)
img_cv2equalize = run(img, func=cv2.equalizeHist, shape=size)

# show hist
show_hist(img, 0, name='original hist')
show_hist(img_equalize, 1, name='equalize hist')
show_hist(img_flatten, 2, name='flatten hist')
show_hist(img_cv2equalize, 3, name='cv2equalize hist')
plt.show()

# transform HSV -> RGB
img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
img_equalize = cv2.cvtColor(img_equalize, cv2.COLOR_HSV2RGB)
img_flatten = cv2.cvtColor(img_flatten, cv2.COLOR_HSV2RGB)
img_cv2equalize = cv2.cvtColor(img_cv2equalize, cv2.COLOR_HSV2RGB)

# write to file
cv2.imwrite('image_equalize.png', img_equalize)
cv2.imwrite('image_flatten.png', img_flatten)
cv2.imwrite('image_cv2equalize.png', img_cv2equalize)

cv2.imwrite('differ_equalize_flatten.png', cv2.absdiff(img_equalize, img_flatten))
cv2.imwrite('differ_equalize_cv2equalize.png', cv2.absdiff(img_equalize, img_cv2equalize))
cv2.imwrite('differ_flatten_cv2equalize.png', cv2.absdiff(img_flatten, img_cv2equalize))
cv2.waitKey(0)

# show image
cv2.imshow('image_original', img)
cv2.imshow('image_equalize', img_equalize)
cv2.imshow('image_flatten', img_flatten)
cv2.imshow('image_cv2equalize', img_cv2equalize)
cv2.waitKey(0)
