import cv2
import numpy as np


def point_expand(r=5):
    _filter = np.zeros(4*r*r)
    _filter = _filter.reshape((2*r, 2*r))
    for i in range(-r, r):
        for j in range(-r, r):
            if (i**2 + j**2) < r**2:
                _filter[r+i][r+j] = 1.0/2*np.pi*r
    return _filter


def line_tremble(w=10, theta=0):
    _filter = np.zeros(4*w*w)
    _filter = _filter.reshape((2*w, 2*w))
    for i in range(-w, w):
        for j in range(-w, w):
            if i*np.cos(theta) + j*np.sin(theta) <= w/2.0:
                _filter[w+i][w+j] = 1.0/w
    return _filter


size = 500
# point_r = 5
img_p = np.zeros(size**2)
img_p = img_p.reshape((size, size))
for i in range(50, 451):
    for j in range(259, 262):
        img_p[i][j] = 255

filter_expand = point_expand()
filter_tremble = line_tremble()
ff = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])

img_p_expand = cv2.filter2D(img_p, -1, filter_tremble)
img_p_expand = np.array(img_p_expand, dtype='uint8')

"""
# save image
cv2.imwrite('img_dft.jpg', img_shift_log)
cv2.imwrite('img_low-pass.jpg', img_filter_norm)
"""

# show
cv2.imshow('original', img_p)
cv2.imshow('original2', img_p_expand)

cv2.waitKey(0)
