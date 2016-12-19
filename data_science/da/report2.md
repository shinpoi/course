データ科学特論レポート
=============================
研究室
学籍番号
2016.12.12

***

#### 1. 概要と目的
解像度を半分にする MNISTデータ(28x28 -> 14x14) を単純ベイズフィルタで分類する.
違うサンプル数のサンプルを使い、単純ベイズフィルタの性能評価したいとは目的です.

***
#### 2. 取得するデータと実験または調査方法
レポート１と同じ、データセットは[MNIST](http://yann.lecun.com/exdb/mnist/)をもっと小型化して使いました.

***
#### 3. データ入力と整形の方法
レポート１と同じデータセットを使いました


***
#### 4.分析方法
単純ベイズフィルタでデータセットを分類しました.
パッケージは e1071を使いました.
トレーニングデータは 550枚、1100枚、5500枚３種類あります.

前回の簡単な[四層CNN](https://github.com/shinpoi/tensorflow_learn/blob/master/mnist_cnn_R.py "自分のgithubページ")とSVMを対照組とします.

評価方法は各方法の正解率 (accuracy) と実行時間を比べです.
***
#### 5. 分析結果と考察
`実行環境: Core i7-4710M(2.5GHz), Nvidia GTX860M(2G DDR5), Ubuntu16.04 LTS`

正解率と訓練時間：
| トレーリングサンプル数 \ 分類器 | Leaner SVM | Radial SVM | 二層CNN | 単純ベイズフィルタ |
|:-----------:|:---------:|:---------:|:----------:|:----------:|
| **550 枚** | NA | NA| NA | 66.7%, < 1s |
| **1100 枚** | 87.7%, 1s | 90.6%, 3s | 95.4%, 52s | 63.3%, < 1s |
| **5500 枚** | 91.1%, 3s | 93.9%, 4s | 97.7%, 57s | 62.1%, < 1s |
* テストサンプル数どちでも 1000 です.

**NA:** <span style="font-size:0.9em;">前回は550枚のデータで訓練しなっかたので、NAとなります.</span>
**< 1s:** <span style="font-size:0.9em;">単純ベイズフィルタの訓練はどっちでも一瞬で終わりました.</span>

> **詳細結果:**

`ソースコードの中で、"detail = FALSE" を "detail = TRUE" に変れば、詳細結果が表示されます`

```
### result of 550 Samples  ###

accuracy= 0.667

precision[ 0 ]= 0.8349515
precision[ 1 ]= 0.6845638
precision[ 2 ]= 0.6666667
precision[ 3 ]= 0.7654321
precision[ 4 ]= 0.6923077
precision[ 5 ]= 0.75
precision[ 6 ]= 0.7211538
precision[ 7 ]= 0.8631579
precision[ 8 ]= 0.3333333
precision[ 9 ]= 0.7368421

recall[ 0 ]= 0.8958333
recall[ 1 ]= 0.8869565
recall[ 2 ]= 0.6516854
recall[ 3 ]= 0.504065
recall[ 4 ]= 0.7241379
recall[ 5 ]= 0.2121212
recall[ 6 ]= 0.8522727
recall[ 7 ]= 0.7387387
recall[ 8 ]= 0.6966292
recall[ 9 ]= 0.5436893

F­-Measure[ 0 ]= 0.8643216
F­-Measure[ 1 ]= 0.7727273
F­-Measure[ 2 ]= 0.6590909
F­-Measure[ 3 ]= 0.6078431
F­-Measure[ 4 ]= 0.7078652
F­-Measure[ 5 ]= 0.3307087
F­-Measure[ 6 ]= 0.78125
F­-Measure[ 7 ]= 0.7961165
F­-Measure[ 8 ]= 0.4509091
F­-Measure[ 9 ]= 0.6256983

Average of F­-Measure: 0.6596531
——————————————————————————————————————

### result of 1100 Samples  ###

accuracy= 0.633

precision[ 0 ]= 0.9111111
precision[ 1 ]= 0.7482517
precision[ 2 ]= 0.7466667
precision[ 3 ]= 0.8358209
precision[ 4 ]= 0.8723404
precision[ 5 ]= 0.78125
precision[ 6 ]= 0.7168142
precision[ 7 ]= 0.6818182
precision[ 8 ]= 0.2431373
precision[ 9 ]= 0.7173913

recall[ 0 ]= 0.8541667
recall[ 1 ]= 0.9304348
recall[ 2 ]= 0.6292135
recall[ 3 ]= 0.4552846
recall[ 4 ]= 0.4712644
recall[ 5 ]= 0.2525253
recall[ 6 ]= 0.9204545
recall[ 7 ]= 0.8108108
recall[ 8 ]= 0.6966292
recall[ 9 ]= 0.3203883

F­-Measure[ 0 ]= 0.8817204
F­-Measure[ 1 ]= 0.8294574
F­-Measure[ 2 ]= 0.6829268
F­-Measure[ 3 ]= 0.5894737
F­-Measure[ 4 ]= 0.6119403
F­-Measure[ 5 ]= 0.3816794
F­-Measure[ 6 ]= 0.8059701
F­-Measure[ 7 ]= 0.7407407
F­-Measure[ 8 ]= 0.3604651
F­-Measure[ 9 ]= 0.442953

Average of F­-Measure: 0.6327327
——————————————————————————————————————

### result of 5500 Samples  ###


accuracy= 0.621

precision[ 0 ]= 0.8317757
precision[ 1 ]= 0.7446809
precision[ 2 ]= 0.7586207
precision[ 3 ]= 0.8301887
precision[ 4 ]= 0.90625
precision[ 5 ]= 0.5666667
precision[ 6 ]= 0.7333333
precision[ 7 ]= 0.8333333
precision[ 8 ]= 0.2443609
precision[ 9 ]= 0.6339286

recall[ 0 ]= 0.9270833
recall[ 1 ]= 0.9130435
recall[ 2 ]= 0.494382
recall[ 3 ]= 0.3577236
recall[ 4 ]= 0.3333333
recall[ 5 ]= 0.1717172
recall[ 6 ]= 0.875
recall[ 7 ]= 0.7207207
recall[ 8 ]= 0.7303371
recall[ 9 ]= 0.6893204

F­-Measure[ 0 ]= 0.8768473
F­-Measure[ 1 ]= 0.8203125
F­-Measure[ 2 ]= 0.5986395
F­-Measure[ 3 ]= 0.5
F­-Measure[ 4 ]= 0.487395
F­-Measure[ 5 ]= 0.2635659
F­-Measure[ 6 ]= 0.7979275
F­-Measure[ 7 ]= 0.7729469
F­-Measure[ 8 ]= 0.3661972
F­-Measure[ 9 ]= 0.6604651

Average of F­-Measure: 0.6144297
```
***
#### 6. まとめ

実行速度はとても速いが、分類性能も低い.
画素を特徴量にするようなデータは、単純ベイズフィルタにとって不向きです.
特徴はっきりのデータ、もしくは他の特徴量抽出器を組み合わせて使う方がいいと思います.

トレーニングデータ数を増やすとき、正解率逆に下がります. ノイズの対応能力低いが原因と思います.


***
#### 7.ファイルズ説明

* [tr2.r](https://github.com/shinpoi/course/blob/master/data_science/da/tr2.r): Rプログラムのソースコード


* **train_data_550.txt**: 1100 枚のトレーニングデータ.
* **train_data_1100.txt**: 1100 枚のトレーニングデータ.
* **train_data_5500.txt**: 5500 枚のトレーニングデータ.


* **test_data_1000.txt**: 1000 枚のテストデータ.

(データセットとCNNのソースコードは前回と同じなので、省略しました.)
***
#### 8.実行注意
* パッケージ"e1071"を必要です.

***
#### 参考文献:
1. 九州工業大学 データ科学特論 講義資料: [R入門PDF](http://pbl.sozolab.jp/system/page_images/images/000/000/023/original/r-howto.pdf) (2016-12-12 アクセス)
2. 九州工業大学 データ科学特論 講義資料: [単純ベイズフィルタPDF](https://pbl.sozolab.jp/system/page_images/images/000/000/017/original/naive.pdf) (2016-12-12 アクセス)
3. [THE MNIST DATABASE of handwritten digits](http://yann.lecun.com/exdb/mnist/) (2016-12-12 アクセス)
4. [Tensorflow Tutorials - Deep MNIST for Experts](https://www.tensorflow.org/versions/r0.11/tutorials/mnist/pros/index.html#deep-mnist-for-experts) (2016-12-12 アクセス)
