#! python3
# coding: UTF-8

import pyperclip
import sys

str = pyperclip.paste()
print("Before:[%s]" % str)
character = []
if len(sys.argv) == 1:
    print("Remove \\")
    str = str.replace('\\', '')
elif len(sys.argv) == 2:
    print("Remove "+ sys.argv[1])
    str = str.replace(sys.argv[1], '')
elif len(sys.argv) == 3:
    print("Replace %s by %s" % (sys.argv[1], sys.argv[2]))
    str = str.replace(sys.argv[1], sys.argv[2])
else:
    print("usage: remove_character old new")

print("After:[%s]" % str)
pyperclip.copy(str)

