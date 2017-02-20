## 画像信号処理１５回目　レポート１:
西田研究室
学籍番号
——————————————————————————————————————————————

1. 画像 "lena.tiff" を読み込んて、各チャンネルを分けで保存する.
まだ、チャンネルを交換、上書、補色などの処理.

```python
# lena.tiff を読み込む
inputimage=imread("lena.tiff");

# RGBチャンネルで分ける
outputimageR=inputimage(:,:,1);
outputimageG=inputimage(:,:,2);
outputimageB=inputimage(:,:,3);

# 各チャンネルの画像を表示する
imshow(outputimageR);
printf("Hit any key!\n"); pause;
imshow(outputimageG);
printf("Hit any key!\n"); pause;
imshow(outputimageB);
printf("Hit any key!\n"); pause;

# 各チャンネルの画像を保存する
imwrite(outputimageR, "outputimageR.png");
imwrite(outputimageG, "outputimageG.png");
imwrite(outputimageB, "outputimageB.png");

# ３つのチャンネルをひとつに合わせて、表示し、保存する
B(:,:,1)=outputimageR;
B(:,:,2)=outputimageG;
B(:,:,3)=outputimageB;
imshow(B);
imwrite(B, "outputimageRGB.png");

printf("Hit any key!\n"); pause;

# RとGチャンネルを交換して、表示する
B(:,:,2)=outputimageR;
B(:,:,1)=outputimageG;
B(:,:,3)=outputimageB;
imshow(B);

printf("Hit any key!\n"); pause;

# RをBチャンネルに上書きして、表示する
B(:,:,1)=outputimageR;
B(:,:,3)=outputimageG;
B(:,:,1)=outputimageB;
imshow(B);

printf("Hit any key!\n"); pause;

# 画像の補色を取って、表示し、保存する
B(:,:,1)=255-outputimageR;
B(:,:,2)=255-outputimageG;
B(:,:,3)=255-outputimageB;
imshow(B);
imwrite(B, "outputimageRGB.png");

printf("Hit any key!\n"); pause;
```

——————————————————————————————————————————————
2. 画像の高周波数データをゼロにする処理.
判別の境目は 50%, 25%, 16.7%, 12.5%, 10% .

```python
# compressFactor = 2, 4, 6 ,8 10
for compressFactor = 2 : 2 :10;

# 画像の離散コサイン変換を取る
C = dct2(outputimageR);

# 画像のサイズを取る
[m,n]=size(C);

# 画像の高周波数データ(50%, 25% ... 10%)をゼロにする
C(uint16(m/compressFactor):m,:)=[0.0];
C(:, uint16(n/compressFactor):n)=[0.0];

# 画像の逆離散コサイン変換を取る
D = idct2(C);

# 画像のヒストグラムを拡張して、表示する
maxRev = max(max(D));
minRev = min(min(D));
Rev_outputimageR=uint8(255.0*(D-minRev)/(maxRev-minRev));
imshow(Rev_outputimageR);

printf("Hit any key!\n"); pause;

endfor
```
——————————————————————————————————————————————
3. 画像の周波数データの符号だけを残る処理.

```python
# 画像の離散コサイン変換を取る
C = dct2(outputimageB);
[m,n]=size(C);

# 離散コサイン変換した画像データの符号を取る（数値を-1、0、1だけにする）
Csign = sign(C);

# 逆離散コサイン変換を取る
D = idct2(Csign);

# 画像のヒストグラムを拡張して、表示する
minRev = min(min(D));
Rev_outputimageB=uint8(255.0*(D-minRev)/(maxRev-minRev));
imshow(Rev_outputimageB);

printf("Hit any key!\n"); pause;
```

——————————————————————————————————————————————
4. 画像周波データの充填による画像拡大処理.

```python
M = uint16(m);
N = uint16(n);

# サイズは画像Cの二倍のゼロ値画像を作る
enlargeC = zeros(M*2,N*2);

# 離散コサイン変換した画像Cのデータを画像enlargeCの左上に置く
enlargeC(1:m,1:n) = C;

# 画像enlargeCを逆離散コサイン変換する
enlargeD = idct2(enlargeC);

# 画像のヒストグラムを拡張して、表示する
maxRev = max(max(enlargeD));
minRev = min(min(enlargeD));
Rev_enlargeOutputimageB=uint8(255.0*(enlargeD-minRev)/(maxRev-minRev));
imshow(Rev_enlargeOutputimageB);

printf("Hit any key!\n"); pause;
```

——————————————————————————————————————————————
5. ２つの画像の周波数データの符号を交換する処理.

```python
# tifferni.tiffとlena.tiffを読み込む
inputimage1=imread("tifferni.tiff");

inputimage2=imread("lena.tiff");

# tifferni.tiffとlena.tiffを表示する
imshow([inputimage1 inputimage2]);

printf("Hit any key!\n"); pause;

# tifferni.tiffとlena.tiffのBチャンネルを離散コサイン変換する
C1 = dct2(inputimage1(:,:,3));

C2 = dct2(inputimage2(:,:,3));

# tifferni.tiffとlena.tiffのBチャンネルデータの離散コサイン変換値の符号を交換する
PAExchangeC1 = abs(C2).*sign(C1);
PAExchangeC2 = abs(C1).*sign(C2);

# 逆離散コサイン変換する
revImageC1 = idct2(PAExchangeC1);
revImageC2 = idct2(PAExchangeC2);

# ２つの画像のヒストグラムを拡張して、表示する
maxRev = max(max(revImageC1));
minRev = min(min(revImageC1));
outputRevImageC1=uint8(255.0*(revImageC1-minRev)/(maxRev-minRev));

maxRev = max(max(revImageC2));
minRev = min(min(revImageC2));
outputRevImageC2=uint8(255.0*(revImageC2-minRev)/(maxRev-minRev));

imshow([inputimage1(:,:,3) inputimage2(:,:,3); outputRevImageC1 outputRevImageC2]);
printf("Hit any key!\n"); pause;
```

——————————————————————————————————————————————
6. 中心対称画像の周波数データの一部だけをとって、逆変換する処理.
中心対称画像の周波数データも軸対称のことを証明できる.

```python
# 中心対称のGチャンネルlenaさんを作る
E = [outputimageG fliplr(outputimageG) ; flipud(outputimageG) fliplr(flipud(outputimageG))];
imshow(E);

# 画像を離散フリエ変換する（高速フーリエ変換の手法で）
F = fft2(E);

# 離散フリエ変換画像の実部を取る
R = real(F);

# 離散フリエ変換画像の左上四分の一部分の実部だけを逆離散フリエ変換るす
QR = R(1:M,1:N);
RevDCTR = idct2(QR);

# 画像のヒストグラムを拡張して、表示する
maxRevDCTR = max(max(RevDCTR));
minRevDCTR = min(min(RevDCTR));
imgRevDCTR=uint8(255.0*(RevDCTR-minRevDCTR)/(maxRevDCTR-minRevDCTR));
imshow(imgRevDCTR);

printf("Hit any key!\n"); pause;
```
——————————————————————————————————————————————
7. lenaさんのモノクローム画像に行列$
\begin{bmatrix} 0 & -1 & 0 \\ -1 & 4 & -1 \\ 0 & -1 & 0 \end{bmatrix}
$と畳み込み計算する.
効果はエッジの抽出.

```python
# 重み付けの計算によって、lenaさんのモノクローム画像を取る
grayScaleImage=0.29*outputimageR+0.606*outputimageG+0.105*outputimageB;
imshow(grayScaleImage);

# 画像を離散フリエ変換する
FFTgrayScaleImage = fft2(grayScaleImage);

# 畳み込みコアを作る
operator = zeros(M,N);
operator(1,1)=0;
operator(1,2)=-1;
operator(1,3)=0;
operator(2,1)=-1;
operator(2,2)=4;
operator(2,3)=-1;
operator(3,1)=0;
operator(3,2)=-1;
operator(3,3)=0;

# 畳み込みコアを離散フリエ変換する
FFToperator = fft2(operator);

# 画像データに畳み込み計算を掛ける
innerproduct = FFTgrayScaleImage.*FFToperator;

convGO = ifft2(innerproduct);
realConvGO = real(convGO);

# 画像のヒストグラムを拡張して、表示する
maxRealConvGO = max(max(realConvGO));
minRealConvGO = min(min(realConvGO));
imgRealConvGO=uint8(255.0*(realConvGO-minRealConvGO)/(maxRealConvGO-minRealConvGO));
imshow(imgRealConvGO);

printf("Hit any key!\n"); pause;
```

——————————————————————————————————————————————
7. 畳み込み計算で画像の劣化過程をシミュレーションする処理.
(でも点広がり関数は中心対称の形で作っていませんので、処理は失敗しました.)

```python
# ガウス分布による点広がり関数を作る
sigma = 3.0;
gaussian = zeros(M,N);
for i = 1:N
for j = 1:M
gaussian(i,j) = exp(-((double(M)/2.0-j)^2+(double(N)/2.0-i)^2)/(2.0*sigma^2));
endfor
endfor

# 畳み込み計算で画像の劣化過程をシミュレーションする
FFTGaussian = fft2(gaussian);

innerproduct = FFTgrayScaleImage.*FFTGaussian;

convGG = ifft2(innerproduct);
realconvGG = real(convGG);

# 画像のヒストグラムを拡張して、表示する
maxRealconvGG = max(max(realconvGG));
minRealconvGG = min(min(realconvGG));
imgRealconvGG=uint8(255.0*(realconvGG-minRealconvGG)/(maxRealconvGG-minRealconvGG));
imshow(imgRealconvGG);

printf("Hit any key!\n"); pause;
```
——————————————————————————————————————————————
8. 畳み込み計算で画像の劣化過程をシミュレーションする処理.

```python
# ガウス分布による点広がり関数を作る
gaussianShift = [ gaussian(M/2+1:M,N/2+1:N) gaussian(M/2+1:M,1:N/2) ; gaussian(1:M/2,N/2+1:N) gaussian(1:M/2, 1:N/2)];


# 畳み込み計算で画像の劣化過程をシミュレーションする
FFTGaussian = fft2(gaussianShift);

innerproduct = FFTgrayScaleImage.*FFTGaussian;

convGG = ifft2(innerproduct);
realconvGG = real(convGG);

# 画像のヒストグラムを拡張して、表示する
maxRealconvGG = max(max(realconvGG));
minRealconvGG = min(min(realconvGG));
imgRealconvGG=uint8(255.0*(realconvGG-minRealconvGG)/(maxRealconvGG-minRealconvGG));
imshow(imgRealconvGG);
```
