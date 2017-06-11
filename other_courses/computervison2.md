# 視覚情報解析 レポート02

研究室
学籍番号
***
## 「 3D Motion Reconstruction for Real-World Camera Motion」4.2 & 5 節

### 4.2 Real-World Results

**内容**：本論文提案した手法の現実世界で実験する。

>**実験環境**：

<img src="01.jpg" width=600></img>

* 1998 年のドイツ映画「Run Lola Run」から抽出した連続画像フレーム
* 順番は右から左
* 人為的に各関節に2Dポイントを付きました

>**実験内容**：
1. 本論文で提案した手法でサンプルを再構築する
比べとして、 NRSFM という過去の研究で提案した手法にもサンプルを再構築しました。


2. 2Dポイントが連続的に付いていない時、本手法も正しく再構築できるのことについての検証


>**実験結果**：

1. 再構築した結果は真実に近い
　
  1.1　本論文で提案した手法の結果
  <img src="02.jpg" width=600></img>
  　
  1.2　NRSFMの結果
  <img src="03.jpg" width=600></img>


2. 2Dポイントが連続的に付いていない時も、モーションを再構築しました
　
<img src="04a.jpg" width=240></img>
　　↓　　　　　↓　　　　↓
<img src="04b.jpg" width=240></img>


>**まとめ**：

本研究で提案した手法は式6で示したように、3Dキーフレーム、2Dフレーム、L1ペナルティを使って3Dフレームを再構築しました。

式6:　$arg \ min_{\beta}(1-\gamma)||\textbf{x}-\textbf{P}\boldsymbol{\Theta\beta}||^2+\gamma||\textbf{X}'-\boldsymbol{\Theta'\beta}||^2+\lambda||\boldsymbol{\beta}||^p$

<br/>
<br/>
<br/>
<br/>

### 5. Discussion and Conclusions
>**まとめ**:

* 私たちは新しいの2D画像点投影から3Dフレーム再構築手法を提案しました。
* 私たちはいい再構築手法なら、ちょっとだけ不連続なサンプルでも再構築できると思います。それはNRSFMができないことです。
* 二つの論文をもとにした、そして人手でランダム3Dケーフレームを取ることによって、私たちはかつてのNRSFMができない実世界完全3D再構築のをできました。

>**二つの論文**:

1. J. Valmadre Valmadre and and S.Lucey. Deterministic 3d humanpose estimation using rigid
structure. In European Conference on ComputerVision(ECCV),2010.
2. J.Xiao, J.Chai, and T. Kanade. closed form solution to non-rigid shape and motion recovery. International Journal ofComputerVision,67:233–246,2006.
