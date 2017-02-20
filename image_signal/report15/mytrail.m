clear;
pkg load signal;

inputimage=imread("git_avatar.png");
outputimageR=inputimage(:,:,1);
outputimageG=inputimage(:,:,2);
outputimageB=inputimage(:,:,3);

[m,n]=size(outputimageR);
m=uint8(m);
n=uint8(n);

C1 = dct2(outputimageR);
C2 = dct2(outputimageG);
C3 = dct2(outputimageB);

# 低高周波数部分をカットする
v = 2
n_ = int32(n/v);
m_ = int32(m/v);
for i = 1:n_;
for j = 1:m_;
C1(i,j) = 0;
C2(i,j) = 0;
C3(i,j) = 0;
endfor
endfor
 
D1 = idct2(C1);
D2 = idct2(C2);
D3 = idct2(C3);

D1 = uint8((255-D1*3));
D2 = uint8((255-D2*3));
D3 = uint8((255-D3*3));

E(:,:,1) = D1;
E(:,:,2) = D2;
E(:,:,3) = D3;

imshow(E);
imwrite(E, "git_avatar_edge.png");



