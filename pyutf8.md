#Python, UTF-8, and Chinese characters.

######Python的UTF-8编码问题比较让人抓狂, 我之前抓狂过很多次之后决定写一个wiki,
######主要是为了解决我们在Python编码过程中遇到的UTF-8中文乱码问题.
######PS1: 本WIKI不会对UTF-8具体的细节进行过多的说明, 主要是提供各种不同的情况情况该如何解决提供一些方法.
######PS2: 图省事的话直接看第3, 4点以及conclusion即可:)

#### 1. 文件编码

* 文件的编码方式是什么?ASCII(default)还是其他的?在vim下可以用:set fileencoding查看.
或者使用iconv: iconv -f utf8 filename 如果输出正常, 无错误, 无乱码, 那么该文件也应该是正确地以UTF-8的编码方式保存的.
如果打算使用utf编码,可以使用:set fileencoding=utf8进行指定,vim会负责完成转换工作.

* 关于 [PEP-0263] [1]建议是在文件的头两行显示指定文件编码,方式有如下几种:

    * `# coding=<encoding name>`
    * `# -*- coding: <encoding name> -*-`
    * `# vim: set fileencoding=<encoding name> :`
    * 第2种比较少见,第1种比较漂亮,第0种是我使用的:)

* 文件编码的作用

    * 让阅读代码的人直到该文件的编码方式
    * 如果文件中有--显式--的需要特别编码处理的字符(如中文)时,通过指定文件的编码能够让editor知道如何处理,储存.
    * 显式具体指的是:
        *    a = "我是中文"
        *    a = u"我是中文"
* Example:


```python
File: 1-pyutf8.py

#!/usr/bin/env python
# encoding=utf-8 
import os
import sys
a = "我是中文"
b = u"我也是中文"
os.write(sys.stdin.fileno(), a)
os.write(sys.stdin.fileno(), b)
print a
print b
```

* 若缺少了了# encoding=utf-8 则文件在 执行时会出错: `SyntaxError: Non-ASCII character '\xe6' in file 1-pyutf8.py on line 5, but no encoding declared; see http://www.python.org/peps/pep-0263.html for details`

* 此时是Python解析器报的错误,而出错的原因正是Python解析器没有找到合适的编码方法去解析代码. 注意:
  此时,编码文件已经是正确地已UTF-8格式储存的, 只是Python不知道.所以需要显示地进行指定.

* 另外,关于使用print/os.write, print会根据终端的环境进行一些编码换转, 或许会"欺骗"我们, os.write的结果则是比较准确, 真实的.

* trick: 我们可以将字符串放如一个集合类型中,比如list. 然后再使用print打印该list, 这样可以得到真实的数据类型.

```python
>>> a = "中文"
>>> b = u"中文"
>>> c = u"sunus"
>>> print a, b, c
中文 中文 sunus
>>> print [a, b, c]
['\xe4\xb8\xad\xe6\x96\x87', u'\u4e2d\u6587', u'sunus']
```

* 第二个print的结果可以知道, a为str, b, c均为unicode. 而第一个print则不会显示这些信息.

* 在确定文件编码之后没问题之后,继续分析别的错误.


#### 2. unicode , str and UTF-8

* python2x里, 对于字符串有两个不同的类进行表示,分别是 __unicode__ 和 __str__, 对应的Constructor分别是unicode(), str(), 而且, 他们都是由同一个基类 __basestring__ 派生出来的. 顺便说一下,检验一个对象的正确方法是
`isinstance(value, basestring)`

* unicode是为了处理多字节字符(如中文)而设计的, 对于ASCII字符来说, 他们没什么区别而且能够兼容, 但是, 当有出现中文时, 问题就出来了.
* UTF-8是一个具体的unicode编码方式的实现.
* 我们将 __str__ 作为 __可读__ 的字符串, unicode作为python内部对字符串的一种 __抽象__ 实现并选择正确的储存方法, print var, 'xx', "xxx" 则都是str(没有打头的u)

#### 3. encode and decode

* __encode__: 是将unicode转换成str编码, 并且encoding参数为具体的实现, 如UTF-8
* __decode__: 是将str转换成unicode编码, 并且encoding参数为具体的实现, 如UTF-8

* 使用建议:
    * 对于unicode 尽量只让unicode对象存在于内存中, __打印输出__, __网络传输__, __写入文件__,  __之前__ 应该将其转换为 str, 而且,
    含有非ASCII码字符的unicode字符串, 是 __写不进文件__ 的.
    * 以str字符串形似, 或者通过外部手段(iconv, vim set fileencoding, etc)等方式形成的文件, 本身就能够 __无障碍__ 地被读取.
    * unicode字符串, 只作为"中间态"使用.如

        ```python
        a = u'OnlyIn内存'
        #if you want to see what's in a
        #use:
        ae = a.encode('utf8')
        #do whatever you want with a, net transporat or write to file.
        ```
    * 无encoding参数的encode, decode方法所使用的默认encoding为系统环境获取, 不建议使用.

#### 4. Examples:

```python
File: encode_or_decode_write.py

#!/usr/bin/env python
# encoding=utf-8

import sys
import os
import traceback

sstr1 = "Most Normal String\n"
sstr2 = "我是str string\n"
ustr1 = u"unicode string WITHOUT Chinese\n"
ustr2 = u"我是unicode string\n"

def test(new_file_name, method, *args):
    try:
        with open(new_file_name, 'w') as f:
            for s in args:
                so = s
                s = getattr(s, method)('utf-8')
                f.write(s)
                print 'write', so, [so], method, 'succeed!'
                print '%s to %s' % (str(so.__class__), str(so.__class__))
    except:
        traceback.print_exc()

def main():
    if sys.argv[1] == 'encode':
        test('str', 'encode', sstr1, sstr2)
        test('uni', 'encode', ustr1, ustr2)
    elif sys.argv[1] == 'decode':
        test('str', 'decode', sstr1, sstr2)
        test('uni', 'decode', ustr1, ustr2)
    else:
        print 'arg can only be decode or encode'

main()
```

* 执行 python encode_or_decode_write.py encode , sstr1, ustr1, ustr2 能够成功写入文件, sstr2 失败.
    * 对unicode使用encode使之变成可读, 可写, 可传输的str. 所以 ustr1, ustr2 均成功.
    * sstr1因为没有包含非ASCII字符, 所以也成功了. 而sstr1包含有中文, 失败. __一定不要使用unicode进行读写__, __传输__ 等操作

* 执行 python encode_or_decode_write.py decode , 只有sstr1, ustr1 能够成功写入, 因为他们没有非ASCII字符.
    * sstr2, decode之后变为unicode 该过程成功,失败是因为将unicode __写入文件__
    * ustr2, decode则直接失败了, 对unicode进行decode操作, 本身就是有问题的嘛!

#### 5. Conclusion:
* 将unicode留在内存中
* 读取, 写入文件, 网络传输使用str. 即
str_str = unicode_string.encode('utf8')

#### 6. 有错误, 不清楚的地方欢迎请指出, 谢谢:)

[1]: http://www.python.org/dev/peps/pep-0263/ "PEP-0263"
