#Python, UTF-8, and Chinese characters.

######Python的UTF-8编码问题比较让人抓狂, 我之前抓狂过很多次之后决定写一个wiki,
######主要是为了解决我们在Python编码过程中遇到的UTF-8中文乱码问题.
######PS: 本WIKI不会对UTF-8具体的细节进行过多的说明, 主要是提供各种不同的情况情况该如何解决提供一些方法.

#### 1. 关于文件的编码:

*   文件的编码方式是什么?ASCII(default)还是其他的?在vim下可以用:set fileencoding查看.
或者使用iconv: iconv -f utf8 filename 如果输出正常, 无错误, 无乱码, 那么该文件也应该是正确地以UTF-8的编码方式保存的.
如果打算使用utf编码,可以使用:set fileencoding=utf8进行指定,vim会负责完成转换工作.

*   关于 [PEP-0263] [1]建议是在文件的头两行显示指定文件编码,方式有如下几种:      

> 1.   `# coding=<encoding name>`
2.   `# -*- coding: <encoding name> -*-`
3.   `# vim: set fileencoding=<encoding name> :`
 
> > 第3种比较少见,第2种比较漂亮,第1种是我使用的:)

*   文件编码的作用

> 1.    让阅读代码的人直到该文件的编码方式
2.    如果文件中有--显式--的需要特别编码处理的字符(如中文)时,通过指定文件的编码能够让editor知道如何处理,储存.
3.            显式具体指的是:

> > * a = "我是中文"
* a = u"我是中文"

* Example: `1-pyutf8.py`

```python
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

> 若缺少了了# encoding=utf-8 则文件在 执行时会出错:

> `SyntaxError: Non-ASCII character '\xe6' in file 1-pyutf8.py on line 5, but no encoding declared;
see http://www.python.org/peps/pep-0263.html for details`

> 此时是Python解析器报的错误,而出错的原因正是Python解析器没有找到合适的编码方法去解析代码. 注意: 此时,编码文件已经是正确地已UTF-8格式储存的, 只是Python不知道.所以需要显示地进行指定.

> 另外,关于使用print/os.write, print会根据终端的环境进行一些编码换转, 或许会"欺骗"我们, os.write的结果则是比较准确, 真实的.

* 在确定文件编码之后没问题之后,继续分析别的错误.

[1]: http://www.python.org/dev/peps/pep-0263/ "PEP-0263"
