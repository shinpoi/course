## 画像信号処理特論 第11回 レポート

研究室
学籍番号

***
#### 1. 算術符号化のアルゴリズム

アルゴリズム:
1. シンボルの周波数フォームを作る.
2. フォームを逆ソートする, そして重ね積む.
3. 次のアルゴリズムを使って、符号化する:

* for each $i$ in $data$:
  * $range = high - low$
  * $low_i = low_{i-1} + range_i * range \ low_i$
  * $high_i = low_{i-1} + range_i * range \ high_i$

4. 複号化アルゴリズム:

* 以下の流れを繰り返す. (符号化の逆計算をする)
  * $low$ 値に対するシンボルを記録する.
  * $low$ 値をこのシンボルの下限値を引く.
  * $low$ 値をこのシンボルのレンジ値を割る.

***
#### 2.例

0~7 のシンボルをもつデータ '1234567205023' を算術符号化したい (長さは 13).

**2-1. シンボルの周波数フォームを作る:**

| シンボル | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|:-----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| 周波数 | 0.15 | 0.08 | 0.23 | 0.15 | 0.08 | 0.15 | 0.08 | 0.08 |

**2-2. フォームを逆ソート、重ね積む**

| シンボル | 2 | 5 | 3 | 0 | 7 | 6 | 4 | 1 |
|:---:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| 下限 | 0.0  | 0.23 | 0.38 | 0.53 | 0.68 | 0.76 | 0.84 | 0.92 |
| 上限 | 0.23 | 0.38 | 0.53 | 0.68 | 0.76 | 0.84 | 0.92 | 1.00 |
|レンジ| 0.23 | 0.15 | 0.15 | 0.15 | 0.08 | 0.08 | 0.08 | 0.08 |

**2-3. 符号化**

data: '1234567205023'

$low$ の数値:
——————————————————
$low_1$ -> $0.92 = (0 + 1\times0.92)$
$low_2$ -> $0.92 = (0.92 + 0.08\times0)$
$low_3$ -> $0.9270 = (0.92 + 0.0184\times0.38)$
$low_4$ -> $0.929310 = (0 + 0.002760\times0.84)$
$low_5$ -> $0.92936118 = (0 + 0.00022080\times0.23)$

...
...

$low_3$ -> 0.9293881850446214
——————————————————


**2-4. 複号化**

$low$:0.9293881850446214

——————————————————
$0.92 < 0.9293881850446214 < 1.00$
$0.9293881850446214 - 0.92 = 0.009388185044621356$
$0.009388185044621356\div0.08 = 0.117352313058$
 -----> '1'

$0.0 < 0.117352313058 < 0.23$
$0.117352313058 - 0.00 = 0.117352313058$
$0.117352313058\div0.23 = 0.510227448077$
 -----> '2'

...
...

$0.38 < 0.38000100751 < 0.53$
 -----> '3'
——————————————————

***

**Source code:**
```python
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

```
