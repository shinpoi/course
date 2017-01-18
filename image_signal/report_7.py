import cv2
import numpy as np
import time


def size(tr, size=(0, 0)):
    x, y = size
    vertexs = np.array([[[0], [0]], [[x], [0]], [[0], [y]], [[x], [y]]])
    x_ = []
    y_ = []
    for vertex in vertexs:
        vertex_trans = np.dot(tr, vertex)
        x_.append(vertex_trans[0][0])
        y_.append(vertex_trans[1][0])
    x_min = round(min(x_))
    y_min = round(min(y_))
    x_ = round(max(x_)) - x_min
    y_ = round(max(y_)) - y_min
    return np.int(x_), np.int(y_), x_min, y_min


img = cv2.imread('git.png', 0)
theta = -np.pi/6
tr = np.matrix([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


def trans_in(img, tr):
    tr_in = tr**-1
    x, y, shift_x, shift_y = size(tr, img.shape)
    print(shift_x, shift_y)
    img_tr = np.zeros([x, y], dtype='uint8')
    for i in range(img_tr.shape[0]):
        for j in range(img_tr.shape[1]):
            co = np.array([[i + shift_x], [j + shift_y]])
            co = np.array(np.dot(tr_in, co))
            i_ = int(round(co[0][0]))
            j_ = int(round(co[1][0]))
            try:
                img_tr[i][j] = img[i_][j_]
            except IndexError:
                pass
    return img_tr


def trans(img, tr):
    x, y, shift_x, shift_y = size(tr, img.shape)
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


"""
def trans_inverse(img, img2, tr_inverse, shit=(0, 0)):
    for i in range(img2.shape[0]):
        for j in range(img2.shape[1]):
            co = np.dot(tr_inverse, np.array([[i + shit[0]], [j + shit[1]]]))
            try:
                img2[i][j] = img[np.int(co[0][0])][np.int(co[1][0])]
            except IndexError:
                img2[i][j] = 255
"""

start = time.clock()
img2 = trans_in(img, tr)
img3 = trans(img, tr)
print('time = %f s' % (time.clock() - start))

cv2.imshow('or', img)
cv2.imshow('tr_in', img2)
cv2.imshow('tr', img3)
cv2.waitKey(0)




# dft
"""
img = cv2.imread('git.png', 0)

img_c = np.zeros((img.shape[0], img.shape[1], 2))
for i in range(img.shape[0]):
    for j in range(img.shape[0]):
        img_c[i][j][0] = img[i][j]
img_dft = cv2.dft(img_c)
img_norm = np.zeros((img.shape[0], img.shape[1]))
for i in range(img.shape[0]):
    for j in range(img.shape[0]):
        img_norm[i][j] = np.linalg.norm(img_dft[i][j])

img_log = np.log(img_norm)
img_log = np.array(img_log, dtype='uint8')
img_log = cv2.equalizeHist(img_log)

f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
s1 = np.log(np.abs(f))
s2 = np.log(np.abs(fshift))


# cv2.imshow('or', img)
# cv2.imshow('dft', img_log)
cv2.imshow('or', np.array(s1, dtype='uint8'))
cv2.imshow('dft', np.array(s2, dtype='uint8'))
cv2.waitKey(0)
"""

