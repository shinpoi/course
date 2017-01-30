// opencv 3.0
// g++ `pkg-config --cflags --libs opencv`
// UTF-8

/*
j1 is Bessel function of the first kind, alpha = 1, in <cmath>.
How to use dft: http://www.docs.opencv.org/2.4/doc/tutorials/core/discrete_fourier_transform/discrete_fourier_transform.html
*/

//don't finished!

#include <iostream>
#include <cmath>
#include <opencv2/opencv.hpp>
#include <typeinfo>

using namespace std;
using namespace cv;

float h_ponit(int u, int v){
  const int R = 10;
  return (2*M_PI*R)*(j1(R*sqrt(u*u + v*v)) / (sqrt(u*u + v*v)));
}

int main(int argc, char** argv){
  const int size = 5;
  const int point_R = 0;

  Mat img_point = Mat::zeros(size ,size, CV_8UC1);
  int i,j;
  for (i = -point_R; i <= point_R; i++)
    for (j = -sqrt(point_R*point_R - i*i); j <= sqrt(point_R*point_R - i*i); j++){
      img_point.at<unsigned char>(size/2 + i, size/2 + j) = 255;
    }

  Mat img_point_list[] = {Mat_<float>(img_point), Mat::zeros(img_point.size(), CV_32F)};
  Mat complexI;
  merge(img_point_list, 2, complexI);
  dft(complexI, complexI);
  split(complexI, img_point_list);
  //cout << "img_point_list[0].size() = " << img_point_list[0].size() << endl;
  //cout << img_point_list[0].at<float>(0,1) << endl;
  for(i=0; i<img_point.rows; i++)
    for(j=0; j<img_point.cols; j++){
      complexI.at<float>(i,2*j) *= h_ponit(i,j);
    }

  idft(complexI, complexI);
  Mat img_point_idft = Mat::zeros(size ,size, CV_8UC1)
  for(i=0; i<img_point.rows; i++)
    for(j=0; j<img_point.cols; j++){
      img_point_idft<unsigned char>(i,2*j) = int(complexI.at<float>(i,2*j));
    }

  //namedWindow("img_point", WINDOW_AUTOSIZE);
  //imshow("img_point", img_point);
  //waitKey(0);

  return 0;
}
