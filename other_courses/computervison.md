# 視覚情報解析 レポート

研究室　
学籍番号
——————————————————————————————————————
### 第３章　幾何学的カメラキャリブレーション ３.５～３.６
——————————————————————————————————————
#### Chapter 3.5　An application: mobile robot localization

**目的**：単眼カメラで移動ロボットの位置推定

実験環境：

<img src="t1.jpg" width=400></img>
図１.環境の側面図

<img src="t2.jpg" width=400></img>
図２.環境の俯瞰図 (２０枚の入力写真の１枚)


>**手順**：

* カメラで撮る画像から実際位置を推定する（正規化座標系と世界座標系の関係を見つけ出す）
* 射影行列と歪曲行列を求める
* 内部変数、外部変数、歪曲係数を求める
* 3.3 節の手法を使う
  * 内部変数の初期値はカメラの製造元から貰える
  * 外部変数の初期値は式3.20で推定する
  * 歪曲係数の初期値は0
  * 最小二乗法で全てのパラメーターを最適化する


—————————————————————————————————————
基本手順は３.３節と同じですか、一つだけ違うどころがあります：
図で示す通り、今回応用にｚ軸がありません（$ｚ軸座標 \equiv 0$）

よって、式３.２０
$Q = \begin{bmatrix}
v_1\textbf{P}^T_1 & -u_1\textbf{P}^T_1 \\
... & ... \\
v_n\textbf{P}^T_n & -u_n\textbf{P}^T_n
\end{bmatrix}$ の $\textbf{P}$ は $[\ x \ \  y \ \ z \ \ 1\ ]$ から　$[\ x \ \ y \ \ 1\ ]$　に変換する

ローリング行列
$\textbf{r}_n = [\ r_{11} \ \ r_{12} \ \ r_{13}\ ]$ は $[\ r_{11} \ \ r_{12}\ ]$ に変換する

よって、射影行列 $Q\textbf{n} = 0$ の $Q$ は：
$Q = \begin{bmatrix}
v_1x_1 & v_1y_1 & v_1z_1 & v_1 & -u_1x_1 & -u_1y_1 & -u_1z_1 & -u_1\\
& ... & & & & & ... \\
v_nx_n & v_ny_n & v_nz_n & v_n & -u_nx_n & -u_ny_n & -u_nz_n & -u_n
\end{bmatrix}$

から

$Q = \begin{bmatrix}
v_1x_1 & v_1y_1  & v_1 & -u_1x_1 & -u_1y_1 & -u_1\\
& ... & & & ... \\
v_nx_n & v_ny_n & v_n & -u_nx_n & -u_ny_n & -u_n
\end{bmatrix}$　へ変化しましょた

$\textbf{n} = \begin{bmatrix}
\textbf{m}_1 \\ \textbf{m}_2
\end{bmatrix}$ なかの $\textbf{M}$ = $\begin{bmatrix}
\alpha \textbf{r}^T_1 - \alpha cot\theta \textbf{r}^T_2 + u_0\textbf{r}^T_3 & \alpha t_x - \alpha cot\theta t_y + u_0t_z \\
\dfrac{\beta}{sin\theta}\textbf{r}^T_2 + v_0\textbf{r}^T_3 & \dfrac{\beta}{sin\theta}t_y + v_0t_z \\
\textbf{r}^T_3 & t_z
\end{bmatrix}$

は $R^{3\times 4}$ から $R^{3\times 3}$ に変化しました
以降の手順は３.３と同じ
———————————————————————————————————————

実験結果：

<img src="t3.jpg" width=400></img>
図３.実験結果 (２０枚画像の平均誤差と最大誤差、単位は画素)

平均位置誤差：2cm
平均方向誤差：1

最大位置誤差：5cm
最大方向誤差：5

———————————————————————————————————————
#### Chapter 3.6　notes
>**出典まとめ**：

3.2 線形校正法: *Faugeras(1993)*

3.3 放射歪曲: *Tsai(1987a)*
[「 A Versatile Camera Calibration Techniaue  for High-Accuracy 3D Machine Vision Metrology Using Off-the-shelf  TV  Cameras and Lenses 」
 IEEE JOURNAL OF ROBOTICS AND AUTOMATION, VOL. RA-3, NO. 4, AUGUST 1987 ](#)

3.4 写真測量法: *HaralickとShapiro(1992)*

3.5 カメラ校正非線形アプローチ: *Devy, et al(1997)*
[「Camera calibration from multiple views of a 2D object, using a global non linear minimization method」
Intelligent Robots and Systems, 1997. IROS '97., Proceedings of the 1997 IEEE/RSJ International Conference on](#)
