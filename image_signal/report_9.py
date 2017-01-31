# -*- coding: utf-8 -*-
# Python 2.7
# OpenCV 3.1

import cv2
import numpy as np


# create point-expand filter
def point_expand(r=20):
    _filter = np.zeros(4*r*r)
    _filter = _filter.reshape((2*r, 2*r))
    for i in range(-r, r):
        for j in range(-r, r):
            if (i**2 + j**2) < r**2:
                _filter[r+i][r+j] = 1
    value = 1/_filter.sum()
    _filter *= value
    return _filter


# create tremble filter
def line_tremble(w=20, theta=np.pi/2):
    _filter = np.zeros(4*w*w)
    _filter = _filter.reshape((2*w, 2*w))
    for i in range(-w, w):
        for j in range(-w, w):
            if abs(i*np.cos(theta) + j*np.sin(theta)) <= w/2.0:
                _filter[w+i][w+j] = 1
    value = 1/_filter.sum()
    _filter *= value
    return _filter

# read image
img = cv2.imread('tokyoskytree.jpg', 0)

# build filter
filter_expand = point_expand()
filter_tremble = line_tremble()

# use filter to image
img_expand = cv2.filter2D(img, -1, filter_expand)
img_expand = np.array(img_expand, dtype='uint8')

img_tremble = cv2.filter2D(img, -1, filter_tremble)
img_tremble = np.array(img_tremble, dtype='uint8')

# save image
cv2.imwrite('tokyoskytree_expand.jpg', img_expand)
cv2.imwrite('tokyoskytree_tremble.jpg', img_tremble)

# show
cv2.imshow('expand', img_expand)
cv2.imshow('tremble', img_tremble)

cv2.waitKey(0)
