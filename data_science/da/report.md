データ科学特論レポート
=============================
研究室
学籍番号：
2016.11.17

***

#### 1. 概要と目的
解像度を半分にする MNISTデータ(28x28 -> 14x14) をSVMで分類する.
違うサンプル数とカーネルを使い、SVM の性能評価したいとは目的です.

***
#### 2. 取得するデータと実験または調査方法
データセットはMNISTをもっと小型化して使いました.

[MNIST](http://yann.lecun.com/exdb/mnist/)とは:
* ネートで公開され、28x28 ピクセル、各ピクセルは0から255の値をとり、70000サンプルの数字の手書き画像データです.
* 各画像データを 28x28 = 784 次元のヴェクトルとしで読み込みできます.
* 前処理も終わりました（ 背景は除去され、ピクセルの数値が 0~255 を 0~1 に写像されました）

***
#### 3. データ入力と整形の方法
MNIST が [tensorflow](https://www.tensorflow.org/ "An Open Source Software Library for Machine Intelligence") に内蔵されていますので、Python でデータセットを読み出し、R言語を読みやすい形で処理し、テキストファイルに書き込む.
そしてR言語で`read.table()`で読み込みます.

* 具体的：
  読み込むの画像データは 784 (28x28) 次元のベクトル、そのなか訓練用データ 55000枚、テスト用データ 10000枚があります.
  各画像データを 2x2 [mean pooling](http://ufldl.stanford.edu/wiki/index.php/Pooling "pooling 範囲内の画素値の平均値を取る")して、196 (14x14) 次元のベクトルになにます、そして 50/10 枚ごとに一枚を選びます.（サンプル数を縮るの原因は５節で説明します）
  よってトレーニングデータを 5500 / 1100 枚、テストデータを 1000 枚を用意しました.
  最後に heaher 付きで .txt テキストファイルに書き込みます.

テキストの中身はこのような形になにます：
```
v1	v2	v3	v4	v5	class
1	2	3	4	5	[1]
2	3	4	5	6	[2]
0	2	3	5	6	[3]
```

***
#### 4.分析方法
C-SVC による SVM でデータセットを分類する.
SVM の kernel を２つを使いました、一つは線形カーネル、もうひとつは放射基底関数. (Radial Basis kernel)
正規化係数 C の調整も行いました.`(デフォルト値は C=0.1. C=0.001 と C=3でテストした)`

対照として、簡単な[四層CNN](https://github.com/shinpoi/tensorflow_learn/blob/master/mnist_cnn_R.py "自分のgithubページ") (python-tensorflow で組み立て) で同じサンプルを使い、分類器を作りました.

評価方法は各方法の正解率 (accuracy) と実行時間を比べです.
***
#### 5. 分析結果と考察
`実行環境: Core i7-4710M(2.5GHz), Nvidia GTX860M(2G DDR5), Ubuntu16.04 LTS`

正解率と訓練時間：
| トレーリングサンプル数 \ 分類器 | Leaner SVM | Radial SVM | 二層CNN |
|:-----------:|:---------:|:---------:|:----------:|
| **1100 枚** | 87.7%, 1s | 90.6%, 3s | 95.4%, 52s |
| **5500 枚** | 91.1%, 3s | 93.9%, 4s | 97.7%, 57s |
| **55000 枚** | NA | NA| 98.4%, 64s |
* テストサンプル数どちでも 1000 です.

**NA:** <span style="font-size:0.9em;">SVMで 55000 枚サンプルを訓練するとき、プログラムは 10 分以上実行しかつ応答なしの状態になってしまいました、したがって実行困難と判断しました）</span>

***
#### 6. まとめ

>**分類性能ついて：**

実験によって、複雑サンプルにkernel を使ったら性能があがることが分かりました. 時間があれば、kernel をもっと工夫し、性能がもっと上がるこどが出来ると思います.
当然のことですか、サンプル数を上がると性能も上がります.

まだ、C 値を変わって実験しましたが、結果がほどんど変わりません`(0.1%以下)`.
今回のテータセットの前処理がうまくやり過ぎると思います`(実際はいいことですが、実験に対しては実験できないデータとなってしまいました.)`

>**実行性能ついて：**

ビッグデータに対する性能が低い.
アルゴリズムの性質`(すべての点に対する距離が最も短い超平面を計算する)`により、サンプル数が上がるたびに、実行時間が上がることが分かっていますか、今回の実験で検証しました.

対照として、CNNがループ訓練`(毎回はすべての訓練データを使いではなく、代わりに、全部訓練データの一部を順番にとって、CNNに送ります)`をしていますので、データセット大きくなれでも、時間があんまり上がっていない.

しかし、ツールの性能差がありますので、厳密に見えば、アルゴリズムの差の証明になれません.
R言語のメモリ管理が混乱をよく言われています.　今回実行不可能の原因がそこにも関係あると思っています.
Python と R言語の実行速度が同じレベルですが、tensorflow は [computation graph](https://www.tensorflow.org/versions/r0.11/get_started/basic_usage.html#the-computation-graph "プログラムを実行する前にグラフを作り、実行を最適化する手法") を作り、c/c++ ライブラリにリングことが出来る. そして CUDA による GPU 計算加速もできます. 実際の効率が大きく上がれます.

でも、SVM は 小型データセットに最適`(正解率が高い、かつ実行時間が短い)`、ビッグデータに不向き`(正解率はそれなりに高いですか、実行時間が上がりすぎ)`という一般的な認識をある程度で検証しました.
(次元の呪いのサンプルプログラムを作るとき、同じ現像も観察しました.)

***
#### 7.ファイルズ説明

* [tr.r](https://github.com/shinpoi/course/blob/master/data_science/da/tr.r): Rプログラムのソースコード（実行する前に、`>library(kernlab)`をお願いします.）
* [getData.py](https://github.com/shinpoi/course/blob/master/data_science/da/getData.py): データセットを生成するプログラム.（データセットも添付しますので、実行する必要はありません）
* **train_data_1100.txt**: 1100 枚のトレーニングデータ.
* **train_data_5500.txt**: 5500 枚のトレーニングデータ.
* **test_data.txt**: 1000 枚のテストデータ.


* [mnist_cnn_R.py](https://github.com/shinpoi/tensorflow_learn/blob/master/mnist_cnn_R.py): CNNのソースコード. (トレーニングサンプル数が1100と設定しています)

***
#### 8.実行注意
* R:
  * 実行する前に、kernlab ライブラリをインポート(`>library(kernlab)`)して下さい
  * そして、`>source("tr.r")`で実行して下さい
  * ソースコードの中の`detail = FALSE`を`detail = TRUE`すると、`precision`、`recall`、`f-measure` の具体数値もプリントされます


* Python
  * Python2.7と3.5どちでも実行できます
  * 必要なライブラリは`numpy`と`tensorflow`です
  * 始めての実行とき、MNISTデータセットをダンロードに少し時間が掛ります (5分くらい)

***
#### 参考文献:
1. 九州工業大学 データ科学特論 - R入門 講義資料: [R入門PDF](http://pbl.sozolab.jp/system/page_images/images/000/000/023/original/r-howto.pdf) (2016-11-18 アクセス)
2. [Package ‘kernlab’](https://cran.r-project.org/web/packages/kernlab/kernlab.pdf) page 54~60 (2016-11-18 アクセス)
3. [THE MNIST DATABASE of handwritten digits](http://yann.lecun.com/exdb/mnist/) (2016-11-18 アクセス)
4. [Tensorflow Tutorials - Deep MNIST for Experts](https://www.tensorflow.org/versions/r0.11/tutorials/mnist/pros/index.html#deep-mnist-for-experts) (2016-11-18 アクセス)
