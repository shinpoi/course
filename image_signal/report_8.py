import cv2
import numpy as np


# mask
def circle_mask(shape, radius):
    x_center = int(shape[0]/2)
    y_center = int(shape[1]/2)
    if x_center < radius or y_center < radius:
        print('radius is too long!')
        return None
    mask = np.zeros((shape[0], shape[1], 2), dtype='uint8')
    one = np.array([1, 1], dtype='uint8')
    for x in range(-radius, radius + 1):
        y = int(round(np.sqrt(radius**2 - x**2)))
        mask[x_center + x][y_center - y:y_center + y] = one
    return mask


# Discrete Fourier transform
img = cv2.imread('tokyoskytree.jpg', 0)
img_c = np.zeros((img.shape[0], img.shape[1], 2))
img_c[:, :, 0] = img
img_dft = cv2.dft(img_c)
img_norm = np.zeros(img.shape)
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        img_norm[i][j] = np.linalg.norm(img_dft[i][j])

# take logarithm-image
img_shift = np.fft.fftshift(img_norm)
img_shift_log = np.log(img_shift)
img_shift_log = np.array((255/img_shift_log.max() - 1) * np.log(img_shift), dtype='uint8')

# use mask
mk = circle_mask(img.shape, 50)
img_dft_filter = np.fft.fftshift(img_dft) * mk
img_dft_filter = np.fft.ifftshift(img_dft_filter)

# Inverse Discrete Fourier transform
img_filter = np.zeros(img.shape)
img_filter = cv2.idft(img_dft_filter, img_filter, 2)
img_filter_norm = np.zeros(img.shape, dtype='uint8')
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        img_filter_norm[i][j] = round(np.linalg.norm(img_filter[i][j]))

# save image
cv2.imwrite('img_dft.jpg', img_shift_log)
cv2.imwrite('img_low-pass.jpg', img_filter_norm)

# show
cv2.imshow('original', img)
cv2.imshow('dft', img_shift_log)
cv2.imshow('filter', img_filter_norm)

cv2.waitKey(0)
