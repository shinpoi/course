ロボット制御特論 レポート 1
----------------------
研究室
学籍番号:

***
#### 設定:

$\textbf{k}$ は目標単位ベクトル $(|~\textbf{k}~|=1)$
$k_x, k_y, k_z$ は $\textbf{k}$ を $x, y ,z$ 軸への投影の長さ
$k_{xy}$ は $\textbf{k}$ を $x-y$ 平面への投影の長さ
原点から軸を見ると、時計回り方向は正転

***
<img src="report1.png" height="260"></img>
***
三角関数によって:

$sin\gamma = \dfrac{k_{xy}}{|~\textbf{k}~|} = k_{xy} = \sqrt{k_x^2 + k_y^2}$

$cos\gamma = \dfrac{k_z}{|~\textbf{k}~|} = k_z$

$sin\beta = \dfrac{k_y}{k_{xy}} = \dfrac{k_y}{sin\gamma}$

$cos\beta = \dfrac{k_x}{k_{xy}} = \dfrac{k_x}{sin\gamma}$
