import cv2
import numpy as np
import time


def expand_size(tr_matrix, size=(0, 0)):
    x, y = size
    vertices = np.array([[[0], [0]], [[x], [0]], [[0], [y]], [[x], [y]]])
    x_ = []
    y_ = []
    for vertex in vertices:
        vertex_trans = np.dot(tr_matrix, vertex)
        x_.append(vertex_trans[0][0])
        y_.append(vertex_trans[1][0])
    x_min = round(min(x_))
    y_min = round(min(y_))
    x_ = round(max(x_)) - x_min
    y_ = round(max(y_)) - y_min
    return np.int(x_), np.int(y_), x_min, y_min


img = cv2.imread('tokyoskytree.jpg', 0)
theta = -np.pi/6
tr = np.matrix([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


def trans_in(img, tr):
    tr_in = tr**-1
    x, y, shift_x, shift_y = expand_size(tr, img.shape)
    img_tr = np.zeros((x, y), dtype='uint8')
    for i in range(img_tr.shape[0]):
        for j in range(img_tr.shape[1]):
            co = np.array([[i + shift_x], [j + shift_y]])
            co = np.array(np.dot(tr_in, co))
            i_ = int(round(co[0][0]))
            j_ = int(round(co[1][0]))
            try:
                if i_ < 0 or j_ < 0:
                    raise IndexError
                img_tr[i][j] = img[i_][j_]
            except IndexError:
                pass
    return img_tr


def trans(img, tr):
    x, y, shift_x, shift_y = expand_size(tr, img.shape)
    img_tr = np.zeros([x, y], dtype='uint8')
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            co = np.array(np.dot(tr, np.array([[i], [j]])))
            i_, j_ = co[0][0] - shift_x, co[1][0] - shift_y
            try:
                img_tr[i_][j_] = img[i][j]
            except IndexError:
                pass
    return img_tr


def trans_inverse(img, tr_inverse, shift=(0, 0)):
    img2 = np.zeros((img.shape[0]*2, img.shape[1]*2), dtype='uint8')
    for i in range(img2.shape[0]):
        for j in range(img2.shape[1]):
            co = np.dot(tr_inverse, np.array([[i + shift[0]], [j + shift[1]]]))
            try:
                img2[i][j] = img[np.int(co[0][0])][np.int(co[1][0])]
            except IndexError:
                img2[i][j] = 255
    return img2


start = time.clock()
img2 = trans_in(img, tr)
img3 = trans_inverse(img2, np.matrix([[2,0],[0,2]])**-1)
print('time = %f s' % (time.clock() - start))

cv2.imshow('or', img)
cv2.imshow('tr_in', img2)
cv2.imshow('tr', img3)
cv2.waitKey(0)
