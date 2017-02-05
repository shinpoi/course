
ロボット制御特論 レポート 4
----------------------
研究室
学籍番号:

***
問題：
３つのR-関節 O, i-1, i があります.

$$^0_{i-1}\textbf{R}^{i-1}\dot{\textbf{R}}_{O_i} + ^0\boldsymbol{\omega}_{i-1}\times(^0_{i-1}\textbf{R}^{i-1}\dot{\textbf{R}}_{O_i})
= \ ^0\boldsymbol{\omega}_i\times(^0_{i-1}\textbf{R}^{i-1}\textbf{R}_{O_i})$$
を証明する.
***
既知：
運動方程式の定義で：
$$^0\boldsymbol{\omega}_{i-1} = \ ^0\boldsymbol{\omega}_{i-1} + \ ^0_{i-1}\textbf{R}^{i-1}\boldsymbol{\omega}_i \ \ \ \ \ \ ①$$
円弧長方程式で：
$$^{i-1}\dot{\textbf{R}}_{O_i} = \ ^{i-1}\boldsymbol{\omega}_i\times \textbf{R}_{O_i} \ \ \ \ \ \ ②$$

***
式 ① を問題式の左式に代入する：

$$^0_{i-1}\textbf{R}^{i-1}(^{i-1}\boldsymbol{\omega}_i\times ^{i-1}t_{O_i}) +
 ^0\boldsymbol{\omega}_{i-1}\times(^0_{i-1}\textbf{R}^{i-1}\textbf{R}_{O_i}) \ \ \ \ \ \ ③$$　　　

 を得る.

 公式 $\textbf{R}(\textbf{a}\times \textbf{b}) = \textbf{Ra} \times \textbf{Rb}$ を使い、③を次の式へ変形できる：

 $$^0_{i-1}\textbf{R} \ ^{i-1}\boldsymbol{\omega}_i\times(^0_{i-1}\textbf{R} \
 ^{i-1}\textbf{R}_{O_i}) +
 ^0\boldsymbol{\omega}_{i-1}\times(^0_{i-1}\textbf{R}^{i-1}\textbf{R}_{O_i})$$ $$=
 (^0_{i-1}\textbf{R} \ ^{i-1}\boldsymbol{\omega}_i + \
 ^0\boldsymbol{\omega}_{i-1})\times(^0_{i-1}\textbf{R} \ ^{i-1}\textbf{R}_{O_i}) \ \ \ \ \ \ ④$$

式 ① を式 ④ に代入する:

$$^0\boldsymbol{\omega}_i\times(^0_{i-1}\textbf{R}^{i-1}\textbf{R}_{O_i})$$

を得る.

証明完了.
