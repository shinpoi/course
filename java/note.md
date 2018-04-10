Java Note
================

### 1. 文件声明规则
* 一个源文件中只能有一个public类
* 一个源文件可以有多个非public类
* 源文件的名称应该和public类的类名保持一致
* 如果一个类定义在某个包中，那么package语句应该在源文件的首行
* 如果源文件包含import语句，那么应该放在package语句和类定义之间

### 2. 系统变量:  
```shell
echo $CLASSPATH=xxxx
```

### 3. 数值：  
final 关键字来修饰常量  
前缀 0 表示 Octal，而前缀 `0x` 代表 Hexadecimal, 例如：

### 4. 变量类型：
**局部变量**`没有默认值`，所以局部变量必须初始化后使用，否则编译出错  
局部变量是在栈上分配的  
访问修饰符不能用于局部变量  

**实例变量**`有默认值`  
`数值型变量`的默认值是0; `布尔型变量`的默认值是false; `引用类型变量`的默认值是null  
访问修饰符可以修饰实例变量  

**静态变量**`默认值`和实例变量相似

### 5. 访问修饰符：

* `public`：完全可见
* `protect`：同一包和子类中可见，不能修饰类和接口
* `default`：同一包内可见（子类不可见）
* `private`：同一类中可见

|修饰符|当前类|同一包内|子类|其他包|其他包子类|
|---|:---:|:---:|:---:|:---:|:---:|
|public|〇|〇|〇|〇|〇|
|protect|〇|〇|〇|✕|△|
|default|〇|〇|✕|✕|✕|
|private|〇|✕|✕|✕|✕|
>子类与基类不在同一包时：子类实例可以访问其从基类继承而来的`protected`方法，但不能访问基类实例的protected方法

### 6. 非访问修饰符：
`final`：类中的`final方法`可以被子类继承，但是不能被子类修改  

`abstract`:
* 抽象类不能用来实例化对象  
* 抽象类不能同时被`final`修饰    
* 抽象方法不能被声明成`final`和`static`
* 如果一个类包含抽象方法，那么该类一定要声明为抽象类，否则会编译错误

`synchronized`：声明的方法同一时间只能被一个线程访问
`volatile`：变量在每次被线程访问时，都强制从共享内存中重新读取该成员变量的值。当成员变量发生变化时，会强制线程将变化值回写到共享内存
`transient`：序列化的对象包含被修饰的实例变量时，跳过该变量
```c
// synchronous[ˈsɪŋkrənəs]: 同步的
// asynchronous[eɪˈsɪŋkrənəs]: 异步的
// volatile[ˈvɒlətʌɪl]: 易变的，不稳定的
// transient[ˈtranzɪənt]: 短暂的, 瞬态
```

### 7.运算符
`&`(and)，`|`(or)，`^`(xor)，`~`(no) ：位运算符  
`&&`(and)，`||`(or)，`!`(no)： 逻辑运算符

与C/C++相同，存在逻辑短路

`?:`：`(expression)`**?** `value if true`**:** `value if false`
`instanceof`：`Object/reference/variable` **instanceof** `class/interface type`

e.g: `boolean res = name instanceof String`

**运算优先级：** 一元 > 四则 > 位移 > 大小关系 > 相等关系 > 位运算 > 逻辑运算 > 三目 > 赋值 > 逗号
