>http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000

#### 1. 输入输出
print()会依次打印每个字符串，遇到逗号“,”会输出一个空格，  
input()可以让你显示一个字符串来提示用户,e.g.`name = input('please enter your name: ')`
* input()只能返回str

#### 2.变量

##### 2.1 int , float , string , bool , None

Python允许用r''表示''内部的字符串默认不转义  
bool:True,False  //can and,or,not

动态语言:变量本身类型不固定的语言
静态语言:在定义变量时必须指定变量类型

`a = 'ABC'`
  * 1.在内存中创建了一个'ABC'的字符串；
  * 2.在内存中创建了一个名为a的变量，并把它指向'ABC'。  

`b = a`
  * 1.把b指向'ABC'（和a同一个内存空间）  

`a = ‘xyz’`
  * 1.在内存中创建了一个'xyz'的字符串；
  * 2.把a指向'xyz'。（b仍然指向‘ABC’）

##### 2.2 string
python中默认以Unicode编码（内存里）
文件常用utf-8编码（可变长度编码）
当Python解释器读取源代码时，为了让它按UTF-8编码读取，我们通常在文件开头写上这两行：  
```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

ord()获取字符编码  
chr()把编码转换为对应的字符

encode()：把str变为bytes  
decode()：把bytes变为str  
len()：计算字符（str），计算字节数（byte），计算list元素个数

```python
a = '汉字'
>>> a
'\xe6\xb1\x89\xe5\xad\x97' #byte
>>> a.decode('utf-8')
u'\u6c49\u5b57' #str

>>> len(a)
6
>>> len(a.decode('utf-8'))
2

>>> a = 'abc'
>>> a.replace('a', 'A')
'Abc'
>>> a
'abc'


# 判断变量类型
>>> x = 'abc'
>>> y = 123
>>> isinstance(x, str)
True
>>> isinstance(y, str)
False
```

**格式化：**（用%分隔）  
```python
>>> 'Hi, %s, you have $%d.' % ('Michael', 1000000)`
'Hi, Michael, you have $1000000.'
```

##### 2.2 list & tuple

**list[ ]** method：  
  * append()  //插到末尾
  * insert(int,element)  
  * pop() //删除，无参默认-1
  * classmates()
  * sort()

**tuple( )：** 不可更改的list    
只有1个元素的tuple定义时必须加一个逗号,，来消除歧义：
```python
>>> t = (1)
>>> t
1
>>> t = (1,)
>>> t
(1,)
```

**切片**   
* [:] 原样复制一个list  
* [:10:2] 前10个里，每两个取一个  
* [::5] 所有数，每5个取一个  
* tuple同样适用，返回值也是tuple

**列表生成式**
```python
>>> [x * x for x in range(1, 11)]
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

>>> [x * x for x in range(1, 11) if x % 2 == 0]
[4, 16, 36, 64, 100]

>>> [m + n for m in 'ABC' for n in 'XYZ']
['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']
```

**生成器（generator）**
```python
#如果列表元素可以按照某种算法推算出来，可以在循环的过程中不断推算出后续的元素（节省内存空间）
#定义list
>>> L = [x * x for x in range(10)]
>>> L
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

#定义generator
>>> g = (x * x for x in range(10))
>>> g
<generator object <genexpr> at 0x1022ef630>

>>> g = (x * x for x in range(10))
>>> for n in g:
      print(n)

#函数定义法
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'

>>> f = fib(6)
>>> f
<generator object fib at 0x104feaaa0>
#函数是顺序执行，遇到return语句或者最后一行函数语句就返回。
#而变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。
```

#### 3.if
```Python
if:
  pass
else:
  pass
```

#### 4.for ，while

```python
names = ['Michael', 'Bob', 'Tracy']
for x in names:
    print(x)
#'x' can use any string

>>> list(range(5))
[0, 1, 2, 3, 4]

while :
  pass


>>> for x, y in [(1, 1), (2, 4), (3, 9)]:
...     print(x, y)
...
1 1  
2 4
3 9
```

```python
#判断一个对象是否可迭代
>>> from collections import Iterable
>>> isinstance('abc', Iterable) # str是否可迭代
True
>>> isinstance([1,2,3], Iterable) # list是否可迭代
True
>>> isinstance(123, Iterable) # 整数是否可迭代
False
```
#### 5. dict( map , key-value ) ， set

##### 5.1 dict

```python
>>> d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
>>> d['Michael']
95

#add
>>> d['Adam'] = 67
>>> d
{'Bob': 75, 'Michael': 95, 'Tracy': 85, 'Adam': 67}

#search
>>> 'Thomas' in d
False

>>> d.get('xxx')
None #shell下不会显示任何东西
>>> d.get('xxx', -1)
-1

#delet
>>> d.pop('Bob')
75

# dict -> list
>>> d
{0: (1, 2), 2: (2, 4), 4: (3, 9)}
>>> d.items()
dict_items([(0, (1, 2)), (2, (2, 4)), (4, (3, 9))])
>>>
```

##### 5.2 set（集合）
```python
>>> s = set([1, 2, 3])
>>> s
set([1, 2, 3])

>>> s = set([1,1,1,2])
>>> s
set([1, 2])

#method
add()
remove()

>>> s1 = set([1, 2, 3])
>>> s2 = set([2, 3, 4])
>>> s1 & s2
{2, 3}
>>> s1 | s2
{1, 2, 3, 4}
```

#### 6.function

##### 6.1 default arguments

```python
# return x^n
def power(x, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s

>>> power(5)
25
>>> power(5, 2)
25

def enroll(name, gender, age=6, city='Beijing'):
    print('name:%s gender:%s age:%d city:%s' % (name,gender,age,city))

>>>enroll('Adam', 'M', city='Tianjin')
name:Adam gender:M age:6 city:Tianjin
```

**Trap!**
```python
def add_end(L=[]):
    L.append('END')
    return L

>>> add_end()
['END']
>>> add_end()
['END', 'END']
>>> add_end()
['END', 'END', 'END']
```
`why? because L -> [] when function was defined , but [] can be edited`

##### 6.2 Variable-length arguments

```python
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum

#function can recive a tuple
>>> calc(1, 2)
5
>>> calc()
0

>>> nums = [1, 2, 3]  # or nums = (1,2,3)
>>> calc(*nums)
14
```
##### 6.3 Keyword arguments

```python
#recive a extra dict(key:value)

def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)

>>> person('Adam', 45, gender='M', job='Engineer')
name: Adam age: 45 other: {'gender': 'M', 'job': 'Engineer'}

>>> extra = {'city': 'Beijing', 'job': 'Engineer'}

>>> person('Jack', 24, city=extra['city'], job=extra['job'])
name: Jack age: 24 other: {'city': 'Beijing', 'job': 'Engineer'}

>>> person('Jack', 24, **extra)
name: Jack age: 24 other: {'city': 'Beijing', 'job': 'Engineer'}
```

**only in python3:**
```python
# if you want limit Keyword
def person(name, age, *, city='Beijing', job):
    print(name, age, city, job)

>>> person('Jack', 24, job='Engineer')
Jack 24 Beijing Engineer

# if the function has a Variable-length arguments , aslo can:
def person(name, age, *args, city, job):
    print(name, age, args, city, job)
# city,job is Keyword arguments

def person(*,s):
    print(s)

>>> person('a')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: person() takes 0 positional arguments but 1 was given

>>> person(s='hha')
hha
```
**\* 本质上是将 \*后的参数变为键值对(dict)参数**

**f2 only can be used in python3**
```python
def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)

>>> f1(1, 2)
a = 1 b = 2 c = 0 args = () kw = {}
>>> f1(1, 2, c=3)
a = 1 b = 2 c = 3 args = () kw = {}
>>> f1(1, 2, 3, 'a', 'b')
a = 1 b = 2 c = 3 args = ('a', 'b') kw = {}
>>> f1(1, 2, 3, 'a', 'b', x=99)
a = 1 b = 2 c = 3 args = ('a', 'b') kw = {'x': 99}
>>> f2(1, 2, d=99, ext=None)
a = 1 b = 2 c = 0 d = 99 kw = {'ext': None}  

>>> args = (1, 2, 3, 4)
>>> kw = {'d': 99, 'x': '#'}
>>> f1(*args, **kw)
a = 1 b = 2 c = 3 args = (4,) kw = {'d': 99, 'x': '#'}
>>> args = (1, 2, 3)
>>> kw = {'d': 88, 'x': '#'}
>>> f2(*args, **kw)
a = 1 b = 2 c = 3 d = 88 kw = {'x': '#'}
```

尾递归（优化后可防止一般递归的栈溢出）:   
在函数返回的时候，调用自身本身，并且，return语句不能包含表达式。
```python
#一般递归：
def fact(n):
    if n==1:
        return 1
    return n * fact(n - 1)

===> fact(5)
===> 5 * fact(4)
===> 5 * (4 * fact(3))
===> 5 * (4 * (3 * fact(2)))
===> 5 * (4 * (3 * (2 * fact(1))))
===> 5 * (4 * (3 * (2 * 1)))
===> 5 * (4 * (3 * 2))
===> 5 * (4 * 6)
===> 5 * 24
===> 120

#尾递归：
def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)

===> fact_iter(5, 1)
===> fact_iter(4, 5)
===> fact_iter(3, 20)
===> fact_iter(2, 60)
===> fact_iter(1, 120)
===> 120
```

##### 6.5 map&reduce

* python2.x : map(fun,list&tuple) return list  
* python3.x : map(fun,list&tuple) retrun Iterator
