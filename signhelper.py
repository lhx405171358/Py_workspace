#! python3
# coding: UTF-8

import hashlib
import re
import os
import pyperclip
import logging
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s:%(message)s')
LIVE_KEY = {'android': 'c893aff538416202d9a1',
                'ios': '5546722976dd89b6ec9cad5a17737562'}
# android： c893aff538416202d9a1    3d5cb3286b2543822861ef1cab99f223
def sign():
    params = pyperclip.paste()
    params = re.sub("\t(false\ttrue|true\ttrue|true\tfalse|false\tfalse)(?={sep}|$)".format(sep=os.linesep), '', params)
    params = params.replace('\t', '=')
    params_list = params.split(os.linesep)
    params_list.sort()
    params_str = ''.join(params_list)

    return params_str

# 例子：
# origin：appName=Camera360language=zh_cnliveId=596754a73f1f6628510147e5platform=androiduserId=041ac653f1cb8c2d076fc99b
# key: 'android': '3d5cb3286b2543822861ef1cab99f223',
#      'ios': '5546722976dd89b6ec9cad5a17737562'
# 返回：'android':'8d1ed458e8d8dc288bd813bb7802d99c'
#       'ios': '8b4fd50dbdd9dc298a8c45ea74088398'
def pingguoMD5(origin, key='PINGUOSOFT'):
    key_len = len(key)
    logging.debug("origin:"+origin)
    md5 = hashlib.md5(origin.encode('utf-8')).hexdigest()
    len_md5 = len(md5)//2
    out_string = ''

    for i in range(len_md5):
        if key:
            ch1 = int(md5[i*2] + md5[i*2+1], 16)    #16转10
            ch2 = ord(key[i % key_len])
            ch = ch1 ^ ch2
        else:
            if md5[i].isdigit():
                ch = int(md5[i])
            else:
                ch = 0
        ch = "{:02x}".format(ch)    #10转16
        out_string += ch
    return out_string


if __name__ == "__main__":
    while True:
        # 从粘贴板获得参数并处理
        params_str = sign()
        print("[parrms string]:\n" + params_str)
        # md5 加密
        selection = input("[select]: 1.Android 2.ios ")
        if selection == '1':
            sign_key = LIVE_KEY['android']
        elif selection == '2':
            sign_key = LIVE_KEY['ios']
        else:
            print("no such options!")
            continue
        sign_str = pingguoMD5(params_str, key=sign_key)
        print("[sign string]:\n" + sign_str)
        pyperclip.copy(sign_str)
        if input("Go on？Y/n ") != 'Y':
            break

