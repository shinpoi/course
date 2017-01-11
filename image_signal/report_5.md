## 画像信号処理特論 第5回 レポート

研究室
学籍番号:

***
#### 1.説明

三つの方法で試しました:
* ヒストグラム均等化関数`hist_equalize()`
* ヒストグラム平坦化関数`hist_flatten()`
* OpenCVライブラリのヒストグラム平坦化関数`cv2.equalizeHist()`

前２つは自分でコーディングして実装した関数です.
比べとして、OpenCVライブラリのヒストグラム平坦化関数も使いました.
***
#### 2. アルゴリズム

————————————————————————————
##### 2-1 ヒストグラム均等化関数`hist_equalize()`

グレースケールを前提として：

1. ヒストグラムを均等化ため、毎階級の度数を次の式で計算する：$\dfrac{length\times width}{256}$
2. 画像データを１次元 array で展開する.
3. 画像データをソートする. でも得られるのはソートした array ではなく、元画像データの番号です.
(例えば、[10, 100, 0, -5] をソートしたら、[3, 2, 0, 1] が得れる)
4. 毎階級に対して、ソート順番に、元画像データに階級値を度数回入り変わる.

————————————————————————————
##### 2-2 ヒストグラム平坦化関数`hist_flatten()`
ネートで調べたヒストグラム平坦化アルゴリズム<span style="font-size:0.75em">(参考文献2)</span>です：

1. 画像のヒストグラムを計算する（）
2. ヒストの値を正規化する,　階級 $i$ の度数を $P(i)$ で表す


3. 毎画素に対して、元画素値を $d$ で表す、平坦化した画素値 $d(i)$ を次の式で計算する: $d(i) = \dfrac{255}{length\times width}\sum\limits_{i=0}^dP(i)$

***
#### 3. 実行結果

**1. 元画像**：
![](lowcontrast.jpg)
![](original_hist.png)


**2. ヒストグラム均等化関数**`hist_equalize()`**で処理した画像**
![](image_equalize.png)
![](equalize_hist.png)

**3. ヒストグラム平坦化関数**`hist_flatten()`**で処理した画像**
![](image_flatten.png)
![](flatten_hist.png)

**4. OpenCVライブラリ ヒストグラム平坦化関数**`cv2.equalizeHist()`**で処理した画像**
![](image_cv2equalize.png)
![](cv2equalize_hist.png)

**5-1. 均等化と平坦化の差分画像**
![](differ_equalize_flatten.png)

**5-2. 均等化とOpenCVライブラリの差分画像**
![](differ_equalize_cv2equalize.png)

**5-3. 平坦化とOpenCVライブラリの差分画像**
![](differ_flatten_cv2equalize.png)
***
#### 4. 考察

##### 4-1. 実行時間考察：
`環境: CPU:Intel Core i5-4440 3.10GHz　no-GPU　Ubuntu 16.04LTS　Python2.7　OpenCV3.1`
| 回数 \ 関数 | ヒストグラム均等化 | ヒストグラム平坦化 | OpenCVライブラリ |
|:-----------:|:---------:|:---------:|:----------:|
| 第１回 | 1.200900 s | 0.478348 s | 0.003515 s |
| 第２回 | 1.194660 s | 0.457897 s | 0.003693 s |
| 第３回 | 1.192458 s | 0.459075 s | 0.003776 s |

* Pythonの実行速度をがやはりC言語より遥かに遅い（OpenCVはC言語のダイナミックリンクライブラリを使っています）

##### 4-2. 実際効果:
画素値に対して、中間部分整体的に明るく（もしくは暗く）がありますか、見た目には殆ど違いがない.
両端（白と黒の部分）の差が明らかです. ヒストグラム平坦化関数で処理した画像の上部の空と山の境目は、元画像より見辛い.

また、均等化関数はヒストグラムを完璧な四角形に調整できますか、実際消耗が大きいので、その実用性があるかどうか検討が必要です.


***
>##### 参考文献

1. [OpenCV 3.1.0 - Python Tutorials](http://docs.opencv.org/3.1.0/d6/d00/tutorial_py_root.html)
2. [ヒストグラムの拡張・平坦化によるカラー画像の補正](https://codezine.jp/article/detail/214)
3. [Wikipedia - Histogram equalization](https://en.wikipedia.org/wiki/Histogram_equalization)
