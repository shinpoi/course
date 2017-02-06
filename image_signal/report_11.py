# -*- coding: utf-8 -*-
# Python 2.7
# Arithmetic coding

import numpy as np

data = '1234567205023'
print('length of data is: %s' % len(data))

##################
# create form

# summary
summary = np.zeros([8])
for i in data:
    summary[int(i)] += 1

# normalize
for i in range(8):
    summary[i] = round(summary[i]/len(data), 2)

for i in range(8):
    if summary[i] == max(summary):
        summary[i] = 1 + summary[i] - sum(summary)
print(summary)

# create low-high form
summary_sort = [(j, i) for i, j in enumerate(summary)]
summary_sort.sort()
summary_sort.reverse()

form = np.zeros((8, 3))
form[0] = (0, round(summary_sort[0][0], 2), summary_sort[0][1])
for i in range(1, 8):
    form[i] = (round(form[i-1][1], 2), round(form[i-1][1] + summary_sort[i][0], 2), summary_sort[i][1])

print(form)

# create mapped form ( symbol: sequence of array )
map_form = {}
for i in range(8):
    map_form[int(form[i][2])] = i


##################
# encode
low = np.float64(0.0)
high = np.float64(1.0)

for i in data:
    i = int(i)
    low_next = low + (high - low) * form[map_form[i]][0]
    high_next = low + (high - low) * form[map_form[i]][1]
    low = low_next
    high = high_next

print('code is: ', low)


##################
# decode
data_ = ''

for i in range(len(data)):
    for j in range(8):
        if form[j][1] >= low >= form[j][0]:
            data_ += str(int(form[j][2]))
            low = (low - form[j][0])/(form[j][1] - form[j][0])
            break

print('really?', data_ == data)
