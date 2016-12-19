

>**OpenCV**
>[StackOverflow](http://stackoverflow.com/questions/12335848/opencv-program-compile-error-libopencv-core-so-2-4-cannot-open-shared-object-f)　　　　

#### question　1:  

\>> g++ xxx.cpp -o xxx \`pkg-config opencv --cflags --libs\`  
\>> ./xxx  

**error:**　　
`error while loading shared libraries: libopencv_highgui.so.3.1: cannot open shared object file: No such file or directory`

**solve:**　　
`export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib (<- what your opencv lib is)`


#### question　2:  
(WITH_CUDA=OFF, but have graphic_card)  
>[GitHub](https://github.com/opencv/opencv/issues/5852)  
  
\> ./xxx

**error:**  
/usr/bin/ld: cannot find -lippicv

**solve:**　　
`cmake -DWITH_IPP=ON -DINSTALL_CREATE_DISTRIB=ON`
