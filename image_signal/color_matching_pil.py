# need package:
# pip3 install numpy
# pip3 install pillow


import numpy as np
import PIL.Image as Image


def histogram_matching(srcArr, dstArr, srcPNG=False):
    srcHist = np.histogram(srcArr, 256)[0]
    srcHist.dtype = np.float64
    if srcPNG:
        srcHist[0] = 0
    srcHist /= sum(srcHist)
    srcHistMap = np.zeros(256, dtype=np.float32)
    for i in range(len(srcHist)):
        srcHistMap[i] = sum(srcHist[:i])

    dstHist = np.histogram(dstArr, 256)[0]
    dstHist.dtype = np.float64
    dstHist /= sum(dstHist)
    dstHistMap = np.zeros(256, dtype=np.float32)
    for i in range(len(dstHist)):
        dstHistMap[i] = sum(dstHist[:i])

    HistMap = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        minMap = 1
        minTag = None
        for j in range(256):
            if minMap > abs(srcHistMap[i] - dstHistMap[j]):
                minMap = abs(srcHistMap[i] - dstHistMap[j])
                minTag = j
        HistMap[i] = minTag


    for i in range(srcArr.shape[0]):
        for j in range(srcArr.shape[1]):
            srcArr[i, j] = HistMap[srcArr[i, j]]
    return srcArr

def hm_color(srcName, dstName, srcPNG=False):
    srcArr = np.array(Image.open(srcName))
    dstArr = np.array(Image.open(dstName))
    for i in range(3):
        srcArr[:,:,i] = histogram_matching(srcArr[:,:,i], dstArr[:,:,i], srcPNG=srcPNG)
    return srcArr


'''
# example
img = Image.fromarray(hm_color("a.bmp", "b.jpg"))
img.save("c.png")
"""
