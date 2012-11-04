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
