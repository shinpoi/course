// opencv 3.0
// g++ `pkg-config --cflags --libs opencv`

#include <iostream>
#include <math.h>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

// Matrix multiplicative of R2x2 * R2x1
int *mat2x2(float R[2][2], int co[2]){
  static int co_[2];
  co_[0] = (int)(R[0][0]*co[0] + R[0][1]*co[1] + 0.5);
  co_[1] = (int)(R[1][0]*co[0] + R[1][1]*co[1] + 0.5);
  return co_;
}

// calculate size of translated image
int *expand_size(float R[2][2], int x, int y){
  int *size;
  int i = 0;
  int vertices[4][2] = {{0, 0}, {x, 0}, {0, y}, {x, y}};
  size = mat2x2(R, vertices[0]);
  double max_x, min_x, max_y, min_y;
  max_x = min_x = size[0];
  max_y = min_y = size[1];
  for(i=1; i<4; i++){
    size = mat2x2(R, vertices[i]);
    if (size[0] > max_x)
      max_x = size[0];
    if (size[0] < min_x)
      min_x = size[0];
    if (size[1] > max_y)
      max_y = size[1];
    if (size[1] < min_y)
      min_y = size[1];
  }

  int ma_x,ma_y,mi_x,mi_y;
  mi_x = (int)(min_x + 0.5);
  mi_y = (int)(min_y + 0.5);

  ma_x = (int)(max_x - min_x + 0.5);
  ma_y = (int)(max_y - min_y + 0.5);
  static int exp_size[4];

  exp_size[0] = ma_x;
  exp_size[1] = ma_y;
  exp_size[2] = mi_x;
  exp_size[3] = mi_y;

  return exp_size;
}

// run function
int main(int argc, char** argv){
  int i,j;
  // power of expand
  int power = 2;

  // read original image
  Mat img;
  img = imread("tokyoskytree.jpg", CV_LOAD_IMAGE_GRAYSCALE);

  // rotation angle
  double theta = -M_PI/6;
  // rotation matrix, inverse of rotation matrix
  float R_ro[2][2] = {{cos(theta), -sin(theta)}, {sin(theta), cos(theta)}};
  float R_ro_inv[2][2] = {{cos(theta), sin(theta)}, {-sin(theta), cos(theta)}};
  // expand matrix, inverse of expand matrix
  float R_expand[2][2] = {{power, 0}, {0, power}};
  float R_expand_inv[2][2] = {{1.0/power, 0}, {0, 1.0/power}};

  // calculate size of rotation image
  int *rotation_size = expand_size(R_ro, img.rows, img.cols);
  Mat img_rotation(rotation_size[0], rotation_size[1], CV_8U);

  // rotate image
  for(i=0; i<img_rotation.rows; i++)
    for(j=0; j<img_rotation.cols; j++){
      int co[2] = {i + rotation_size[2], j + rotation_size[3]};
      int *co_ = mat2x2(R_ro_inv, co);
      if ((co_[0] < 0) or (co_[1] < 0))
        continue;
      if ((co_[0] > img.rows) or (co_[1] > img.cols))
        continue;

      img_rotation.at<unsigned char>(i,j) = img.at<unsigned char>(co_[0],co_[1]);
    }

  // calculate size of expanded image
  int *exp_size = expand_size(R_expand, img_rotation.rows, img_rotation.cols);
  Mat img_expand(exp_size[0], exp_size[1], CV_8U);

  // expand image
  for(i=0; i<img_expand.rows; i++)
    for(j=0; j<img_expand.cols; j++){
      int co[2] = {i, j};
      int *co_ = mat2x2(R_expand_inv, co);
      if ((co_[0] < 0) or (co_[1] < 0))
        continue;
      if ((co_[0] > img_rotation.rows) or (co_[1] > img_rotation.cols))
        continue;

      img_expand.at<unsigned char>(i,j) = img_rotation.at<unsigned char>(co_[0],co_[1]);
    }

  // show image
  namedWindow("Original", WINDOW_AUTOSIZE);
  imshow("Original", img);

  namedWindow("Trans", WINDOW_AUTOSIZE);
  imshow("Trans", img_rotation);

  namedWindow("Expand", WINDOW_AUTOSIZE);
  imshow("Expand", img_expand);

  waitKey(0);
  return 0;
}
