>http://es.ise.kyutech.ac.jp/lecture/

java
--------------------------------
```java
import xxxx.xxxx  
//xxxx.xxxx.function()

str1 == str2 		//参照値(ポインター)同じ？  
str1.equals(str2)	//内容同じ？
//java: object == object >> 参照値同じ？
//cpp: object == object >> 内容同じ？


//adout new:  
String str1 = "aaa";  
String str2 = "aaa";  
//str1 == str2    //同じ空間を指している

String str1 = "aaa";  
String str2 = new String("aaa");  
//str1 != str2    //違う空間を指している
```



cpp
-------------------------------------
```cpp
using namespace xxxx  
//xxxx::function()

class ~= struct
//struct == default public's class
```

### 比べ：

|java                                                     |c++                |
|---------------------------------------------------------|:-----------------:|
|java class 定義                                          |c++ class 定義     |
|java fild // xxx.xxx                                     |c++ メンバ変数     |
|java method // function in class                         |c++ メンバ関数     |
|java setter&gater // function in class to edit member    |c++ setter&gater   |
|java constructor // function names same as class name >> |c++ constructor    |
|>> to initialize class member ||
|java アクセス修飾子                                      |c++ アクセス指定子 |
|java package // different package can use the same >>    |c++ name space     |
|>> class name  ||
|java overload // the method has the same name but >>     |c++ overload       |
|>> different parameter ||
|                                                         |c++ friend function|
|java static member & final menber                        |c++ static member ;const member |
|java class extend                                        |c++ inheritance    |
|java overwrite // overwrite the method in extend class   |c++ overwrite      |
|java polymorphism // pointer of super class'object >>    |c++ polymorphism|
|>> can point extend class'object ||
|java abstract class   名前と引数だけが定まっていて、>>   |c++ abstract class |
|>> その実装がないメソッドを含むクラス ||
|java interface // like abstract but all members are public|c++ interface class |
|java Generics                                            |c++ Template       |






