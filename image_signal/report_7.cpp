/* g++ `pkg-config --cflags --libs opencv` */

#include <iostream>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

int *mat2x2(float R_inv[2][2], int co[2]){
  static int co_[2];
  co_[0] = (int)(R_inv[0][0]*co[0] + R_inv[0][1]*co[1] + 0.5);
  co_[1] = (int)(R_inv[1][0]*co[0] + R_inv[1][1]*co[1] + 0.5);
  return co_;
}

int main(int argc, char** argv){
  int i,j;
  Mat img;
  int power = 2;
  img = imread("tokyoskytree.jpg", CV_LOAD_IMAGE_GRAYSCALE);
  Mat img2(img.rows*power, img.cols*power, CV_8U);
  float R_inv[2][2] = {{1.0/power, 0}, {0, 1.0/power}};

  for(i=0; i<img2.rows; i++)
    for(j=0; j<img2.cols; j++){
      int co[2] = {i, j};
      int *co_ = mat2x2(R_inv, co);
      img2.at<unsigned char>(i,j) = img.at<unsigned char>(co_[0],co_[1]);
    }

  /* cout << "rows: " << img2.cols << "\nclos: " << img2.rows << endl;
  for(i=0; i<=200; i++)
    for(j=0; j<=200; j++)
      img.at<unsigned char>(i,j) = 0;*/

  namedWindow("Original", WINDOW_AUTOSIZE);
  imshow("Original", img);
  namedWindow("Trans", WINDOW_AUTOSIZE);
  imshow("Trans", img2);
  waitKey(0);
  return 0;
}
