## 確率システム制御特論 第16回 レポート

研究室
学籍番号:
————————————————————————————————————————
#### 課題：二次元平面位置推定へのパーティクルフィルターの適用

————————————————————————————————————————
>#### 1. 環境設定

状態方程式：
* $x(k+1) = Ax(k) + Bu(k) + v(k)$
* $y(k) = g(x(k)) + w(k)$

$A=\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$　$B=\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$　$g(x) = x^3$

$v\sim N(\mu=0, \sigma_v=5)$,　$w \sim N(\mu=0, \sigma_w=100)$

$u(k)$ は $[~random(0,16) ~ ~ ~ random(0,9)~]^T$ のランダム整数ベクトル

————————————————————————————————————————

* 次の位置 $x(k+1)$ は:　いまの位置 $x(k)$ プラス $u(k)$ プラス共分散行列は $\begin{bmatrix} \sigma_v & 0 \\ 0 & \sigma_v \end{bmatrix}$ のカウスノイズ $v(k)$,　$u(k)$ は各スッテプ違うけと、方向はすべて$x$と$y$軸の正方向です.


* 観測値は:　実際位置 $x(k)$ の３乗プラス共分散行列は $\begin{bmatrix} \sigma_w & 0 \\ 0 & \sigma_w \end{bmatrix}$ のカウスノイズ $w(k)$ .

————————————————————————————————————————

フィルターが知っている量：
* 状態方程 $x(k+1)$ と観測方程 $y(k)$ （よって、$\sigma_v$ と $\sigma_w$ も既知）
* 入力 $u(k)$
* 観測値 $y(k)$

————————————————————————————————————————
>#### 2. アルゴリズム

```{mermaid}
graph TD
0["粒子初期化（粒子を適当にばら撒く）"] --> 1["粒子位置更新（状態方程式を使う）"];
1["粒子位置更新（状態方程式を使う）"] --> 2["重み設定（平均重みを使う）"];
2["重み設定（平均重みを使う）"] --> 3["尤度計算（対数尤度）"];
3["尤度計算（対数尤度）"] --> 4["重み更新（重み*尤度）"];
4["重み更新（重み*尤度）"] --> 5["重み正規化（総数を１にする）"];
5["重み正規化（総数を１にする）"] --> 6["リサンプリング（重みに応じて）"];
6["リサンプリング（重みに応じて）"] --> 7["位置推定（粒子の平均値を取る）"];
6["リサンプリング"] --> 1["粒子位置更新（状態方程式を使う）"];
```
————————————————————————————————————————
**1. 粒子位置更新: 前時刻のリサンプリング粒子を状態方程式に代入する.**
  $x(k+1) = Ax(k) + Bu(k) + v(k)$ に代入する
  $v(k)$ と 実際の $v(k)$ は違う、各粒子にとって $v(k)$ も違う.
  よって、重ねている粒子が分散する


**2. 重み設定: すべて粒子の重みを１に設定する.**
  簡単のパーティクルフィルターなので、重みは全部１にする
  バイアスなし、粒子のリサンプリング確率は尤度だけで決める


**3. 尤度計算:ノイズの確率関数で尤度を計算する.**
  観測ノイズはカウス分布のとき、尤度は確率関数: $\dfrac{1}{\sqrt{2\pi\sigma_w}}exp(-\dfrac{(y-g(x))^2}{\sigma_w^2})$　となる
  観測値に近ければ、尤度が大きくなる
  観測ノイズは他の分布の場合、尤度の計算公式を変更することが必要
  逆に言えば、観測ノイズは非カウス分布の場合も、パーティクルフィルタが対応できます


**4. 重み更新**
  尤度$\times$重み で更新する


**5. 重み正規化**
  正規化：総数を１にする （$w_i = \dfrac{w_i}{\sum_1^n{w_i}}$）
  正規化後の重みがそのままリサンプリングの確率で使える


**6. リサンプリング: 重みに応じてリサンプル.**
  重みに応じて一部の粒子を選択する
  粒子の数が変わらない、重複選択可能


**7. 位置推定**
  一番簡単の方法は各粒子数値の平均を取る
  他の方法もある、例えばカウス分布にフィッティングして、$\mu$ を取る


————————————————————————————————————————
>#### 3. シミュレーション

標準偏差: $\sigma_v = 5, ~ \sigma_w=100$
ステップ: 40
粒子数: 10, 20, 50, 100, 300

————————————————————————————————————————

`Particle: 10:`　$\sigma=2.631515$
![](10.png)

`Particle: 20:`　$\sigma=2.314237$
![](20.png)

`Particle: 50:`　$\sigma=1.538661$
![](50.png)

`Particle: 100:`　$\sigma=1.072301$
![](100.png)

`Particle: 300:`　$\sigma=0.893361$
![](300.png)

————————————————————————————————————————
>##### 考察：

* パーティクルの数は多いほど良いではない、ある程度の数以上のパーティクルを出しでも、追跡性能も改善しない.　計算量が無駄に大きくなる.
* パーティクルフィルターはノイズに影響され易い、もし連続で真値と観測値の差が大きの場合であったら、推定値が簡単でズレる. (パーティクルフィルターの推定値は、時々大きくズレることがある)

————————————————————————————————————————
>##### 参考文献

1. [satomacoto - Pythonでパーティクルフィルタを実装してみる](http://satomacoto.blogspot.jp/2012/11/python.html)
（http://satomacoto.blogspot.jp/2012/11/python.html）

2. [Particle filter 紹介](http://daweb.ism.ac.jp/koza/koza2008/PF_Nakano20081030.pdf)
（http://daweb.ism.ac.jp/koza/koza2008/PF_Nakano20081030.pdf）

3. [Qita - 簡単な粒子フィルタの実装](http://qiita.com/shima_x/items/427c914445c9e8910056)
（http://qiita.com/shima_x/items/427c914445c9e8910056）

3. [Qita - なぜパーティクルフィルタの推定値に「重み付き平均」が使われるのかを考察してみた](http://qiita.com/MoriKen/items/da8d290dcefad81b478d)
（http://qiita.com/MoriKen/items/da8d290dcefad81b478d）

————————————————————————————————————————
> ##### Code (フィルター部分)

```python
# ParticleFilter
class ParticleFilter:
    def __init__(self, y_list, x_next, u_list, g, sig_w, particle_number, dimension):
        self.u_list = u
        self.dimension = dimension
        self.x_next = x_next
        self.u = u_list
        self.g = g
        self.y_list = y_list
        self.sig_w = sig_w
        self.particle_number = particle_number

        self.X = np.zeros(particle_number * self.dimension)
        self.X_weight = np.ones(particle_number)

    # init particle by Uniform Distribution
    def init_particle(self):
        for i in range(self.particle_number * self.dimension):
            self.X[i] = (np.random.rand()-0.5)*100
        self.X = self.X.reshape(-1, 2)

    def status_translate(self, u):
        for i in range(self.particle_number):
            self.X[i] = self.x_next(self.X[i], u)

    # likelihood = (1/sqrt(2*pi*sig_w)) * exp(-(y-g(x))**2 / sig_w**2)
    def likelihood(self, x, y):
        return np.exp(- np.linalg.norm(y - self.g(x)) / self.sig_w**2)

    def set_weight(self, y):
        for i in range(self.particle_number):
            self.X_weight[i] *= self.likelihood(self.X[i], y)

    def weight_normalization(self):
        sum_weight = sum(self.X_weight)
        for i in range(self.particle_number):
            self.X_weight[i] = (self.X_weight[i])/sum_weight

    def resample(self):
        X_resapmle = np.zeros(self.particle_number * self.dimension).reshape(-1, dimension)
        k = 0
        samples = np.random.multinomial(self.particle_number, self.X_weight)
        for i, n in enumerate(samples):
            for j in range(n):
                X_resapmle[k] = self.X[i]
                k += 1
        W_resample = np.ones(self.particle_number)
        return X_resapmle, W_resample

    def filter_step(self, y, u):
        self.status_translate(u)
        self.set_weight(y)
        self.weight_normalization()
        X_resapmle, W_resample = self.resample()
        return X_resapmle, W_resample

    def run_filter(self):
        X_list = np.zeros([len(self.y_list), self.particle_number, self.dimension])
        X_value_list = np.zeros([len(self.y_list), self.dimension])

        self.init_particle()

        for i in range(len(self.y_list))[1:]:
            self.X, self.X_weight = self.filter_step(self.y_list[i], self.u_list[i-1])
            X_list[i] = self.X
            X_value_list[i] = (np.mean(self.X, axis=0))  # predict x  = mean(X)
        return X_list, X_value_list
```
