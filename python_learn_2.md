>[Python 入门指南](http://www.pythondoc.com/pythontutorial3/)

#### 1.
3.1.1. 交互模式中，最近一个表达式的值赋给变量 \_。这样我们就可以把它当作一个桌面计算器，很方便的用于连续计算，例如:

```python
>>> tax = 12.5 / 100
>>> price = 100.50
>>> price * tax
12.5625
>>> price + _
113.0625
>>> round(_, 2)
113.06
```

####  2.
3.1.2. 字符串文本能够分成多行。一种方法是使用三引号："""...""" 或者 '''...'''。行尾换行符会被自动包含到字符串中，但是可以在行尾加上 \ 来避免这个行为。下面的示例： 可以使用反斜杠为行结尾的连续字符串，它表示下一行在逻辑上是本行的后续内容:

```python
print("""\
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to
""")
```

将生成以下输出（注意，没有开始的第一行）:
```python
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to
```

####  3.
3.1.3. 也可以对切片赋值，此操作可以改变列表的尺寸，或清空它:

```python
>>> letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
>>> letters
['a', 'b', 'c', 'd', 'e', 'f', 'g']
>>> # replace some values
>>> letters[2:5] = ['C', 'D', 'E']
>>> letters
['a', 'b', 'C', 'D', 'E', 'f', 'g']
>>> # now remove them
>>> letters[2:5] = []
>>> letters
['a', 'b', 'f', 'g']
>>> # clear the list by replacing all the elements with an empty list
>>> letters[:] = []
>>> letters
```
#### 4.
3.2. 用一个逗号结尾就可以禁止输出换行:

```python
>>> a, b = 0, 1
>>> while b < 1000:
...     print(b, end=',')
...     a, b = b, a+b
...
1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,
```

#### 5.
4.2. 在迭代过程中修改迭代序列不安全（只有在使用链表这样的可变序列时才会有这样的情况）。如果你想要修改你迭代的序列（例如，复制选择项），你可以迭代它的复本。使用切割标识就可以很方便的做到这一点:

```python
>>> for w in words[:]:  # Loop over a slice copy of the entire list.
...     if len(w) > 6:
...         words.insert(0, w)
...
>>> words
['defenestrate', 'cat', 'window', 'defenestrate']
```

#### 6.
4.3. 需要迭代链表索引的话，如下所示结合使 用 range() 和 len()

```python
>>> a = ['Mary', 'had', 'a', 'little', 'lamb']
>>> for i in range(len(a)):
...     print(i, a[i])
...
0 Mary
1 had
2 a
3 little
4 lamb
```
不过，这种场合可以方便的使用 enumerate()，请参见 循环技巧。


#### 7.
4.4. break 和 continue 语句, 以及循环中的 else 子句
break 语句和 C 中的类似，用于跳出最近的一级 for 或 while 循环。

循环可以有一个 else 子句；它在循环迭代完整个列表（对于 for ）或执行条件为 false （对于 while ）时执行，但循环被 break 中止的情况下不会执行。以下搜索素数的示例程序演示了这个子句:

```python
>>> for n in range(2, 10):
...     for x in range(2, n):
...         if n % x == 0:
...             print(n, 'equals', x, '*', n//x)
...             break
...     else:
...         # loop fell through without finding a factor
...         print(n, 'is a prime number')
...
2 is a prime number
3 is a prime number
4 equals 2 * 2
5 is a prime number
6 equals 2 * 3
7 is a prime number
8 equals 2 * 4
9 equals 3 * 3
```
(Yes, 这是正确的代码。看仔细：else 语句是属于 for 循环之中， 不是 if 语句。)

#### 8.
4.7.4. 参数列表的分拆
另有一种相反的情况: 当你要传递的参数已经是一个列表，但要调用的函数却接受分开一个个的参数值。这时候你要把已有的列表拆开来。例如内建函数 range() 需要要独立的 start，stop 参数。你可以在调用函数时加一个 * 操作符来自动把参数列表拆开:

```python
>>> list(range(3, 6))            # normal call with separate arguments
[3, 4, 5]
>>> args = [3, 6]
>>> list(range(*args))            # call with arguments unpacked from a list
[3, 4, 5]
```
以同样的方式，可以使用 ** 操作符分拆关键字参数为字典:
```
>>> def parrot(voltage, state='a stiff', action='voom'):
...     print("-- This parrot wouldn't", action, end=' ')
...     print("if you put", voltage, "volts through it.", end=' ')
...     print("E's", state, "!")
...
>>> d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
>>> parrot(**d)
-- This parrot wouldn't VOOM if you put four million volts through it. E's bleedin' demised !
```

#### 9.
4.6. 函数调用会为函数局部变量生成一个新的符号表。确切的说，所有函数中的变量赋值都是将值存储在局部符号表。变量引用首先在局部符号表中查找，然后是包含函数的局部符号表，然后是全局符号表，最后是内置名字表。因此，**全局变量不能在函数中直接赋值（除非用 global 语句命名），尽管他们可以被引用**。

函数引用的实际参数在函数调用时引入局部符号表，因此，实参总是*传值调用*（这里的*值*总是一个对象*引用*，而不是该对象的值）。[1] 一个函数被另一个函数调用时，一个新的局部符号表在调用过程中被创建。

#### 10.
5.1.2. 把列表当作队列使用
你也可以把列表当做队列使用，队列作为特定的数据结构，最先进入的元素最先释放（先进先出）。不过，列表这样用效率不高。相对来说从列表末尾添加和弹出很快；在头部插入和弹出很慢（因为，为了一个元素，要移动整个列表中的所有元素）。

要实现队列，使用 collections.deque，它为在首尾两端快速插入和删除而设计。例如:

```python
>>> from collections import deque
>>> queue = deque(["Eric", "John", "Michael"])
>>> queue.append("Terry")           # Terry arrives
>>> queue.append("Graham")          # Graham arrives
>>> queue.popleft()                 # The first to arrive now leaves
'Eric'
>>> queue.popleft()                 # The second to arrive now leaves
'John'
>>> queue                           # Remaining queue in order of arrival
deque(['Michael', 'Terry', 'Graham'])
```

#### 11.
6.1.2. 模块的搜索路径
导入一个叫 spam 的模块时，解释器先在当前目录中搜索名为 spam.py 的文件。如果没有找到的话，接着会到 sys.path 变量中给出的目录列表中查找。 sys.path 变量的初始值来自如下：

输入脚本的目录（**当前目录，而非脚本所在目录**）。
环境变量 PYTHONPATH 表示的目录列表中搜索

(这和 shell 变量 PATH 具有一样的语法，即一系列目录名的列表)。


#### 12.
6.4. 需要注意的是使用 `from package import item` 方式导入包时，这个子项（item）既可以是包中的一个子模块（或一个子包），也可以是包中定义的其它命名，像函数、类或变量。import 语句首先核对是否包中有这个子项，如果没有，它假定这是一个模块，并尝试加载它。如果没有找到它，会引发一个 ImportError 异常。

相反，使用类似 `import item.subitem.subsubitem` 这样的语法时，这些子项必须是包，最后的子项可以是包或模块，但不能是前面子项中定义的类、函数或变量。

> **扩展：**[Python 的 import 机制](https://loggerhead.me/posts/python-de-import-ji-zhi.html#import-import)


#### 13.
7.2.1. 你可以循环遍历文件对象来读取文件中的每一行。这是一种内存高效、快速，并且代码简介的方式:

```python
>>> for line in f:
...     print(line, end='')
...
This is the first line of the file.
Second line of the file
```

如果你想把文件中的所有行读到一个列表中，你也可以使用 list(f) 或者 f.readlines()。

#### 14.
7.2.1.  f.tell() 返回一个整数，代表文件对象在文件中的指针位置，该数值计量了自文件开头到指针处的比特数。需要改变文件对象指针话话，使用 f.seek(offset,from_what)。指针在该操作中从指定的引用位置移动 offset 比特，引用位置由 from_what 参数指定。 from_what 值为 0 表示自文件起始处开始，1 表示自当前文件指针位置开始，2 表示自文件末尾开始。from_what 可以忽略，其默认值为零，此时从文件头开始:

```python
>>> f = open('workfile', 'rb+')
>>> f.write(b'0123456789abcdef')
16
>>> f.seek(5)     # Go to the 6th byte in the file
5
>>> f.read(1)
b'5'
>>> f.seek(-3, 2) # Go to the 3rd byte before the end
13
>>> f.read(1)
b'd'
```
在文本文件中（没有以 b 模式打开），只允许从文件头开始寻找（有个例外是用 seek(0, 2) 寻找文件的最末尾处）而且合法的 偏移 值只能是 f.tell() 返回的值或者是零。其它任何 偏移 值都会产生未定义的行为。

#### 15.
标准模块 json 可以接受 Python 数据结构，并将它们转换为字符串表示形式；此过程称为序列化(serialization)。从字符串表示形式重新构建数据结构称为 反序列化。

#### 16.
最后一个 except 子句可以省略异常名称，以作为通配符使用。你需要慎用此法，因为它会轻易隐藏一个实际的程序错误！可以使用这种方法打印一条错误信息，然后重新抛出异常（允许调用者处理这个异常):

```python
import sys

try:
    f = open('myfile.txt')
    s = f.readline()
    i = int(s.strip())
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError:
    print("Could not convert data to an integer.")
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
```

try ... except 语句可以带有一个 else子句，该子句只能出现在所有 except 子句之后。当 try 语句没有抛出异常时，需要执行一些代码，可以使用这个子句。例如:

```python
for arg in sys.argv[1:]:
    try:
        f = open(arg, 'r')
    except IOError:
        print('cannot open', arg)
    else:
        print(arg, 'has', len(f.readlines()), 'lines')
        f.close()
```

使用 else 子句比在 try 子句中附加代码要好，因为这样可以避免 try ... except 意外的截获本来不属于它们保护的那些代码抛出的异常。

#### 17.
8.6. 定义清理行为
try 语句还有另一个可选的子句，目的在于定义在任何情况下都一定要执行的功能。例如:

```python
>>> try:
...     raise KeyboardInterrupt
... finally:
...     print('Goodbye, world!')
...
Goodbye, world!
KeyboardInterrupt
Traceback (most recent call last):
  File "<stdin>", line 2, in ?
```

不管有没有发生异常，finally子句 在程序离开 try 后都一定会被执行。当 try 语句中发生了未被 except 捕获的异常（或者它发生在 except 或 else 子句中），在 finally 子句执行完后它会被重新抛出。 try 语句经由 break ，continue 或 return 语句退 出也一样会执行 finally 子句。以下是一个更复杂些的例子:

```python
>>> def divide(x, y):
...     try:
...         result = x / y
...     except ZeroDivisionError:
...         print("division by zero!")
...     else:
...         print("result is", result)
...     finally:
...         print("executing finally clause")
...
>>> divide(2, 1)
result is 2
executing finally clause
>>> divide(2, 0)
division by zero!
executing finally clause
>>> divide("2", "1")
executing finally clause
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
  File "<stdin>", line 3, in divide
TypeError: unsupported operand type(s) for /: 'str' and 'str'
```

如你所见， finally 子句在任何情况下都会执行。TypeError 在两个字符串相除的时候抛出，未被 except 子句捕获，因此在 finally 子句执行完毕后重新抛出。

在真实场景的应用程序中，finally 子句用于释放外部资源（文件或网络连接之类的），无论它们的使用过程中是否出错。
