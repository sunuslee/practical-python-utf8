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
