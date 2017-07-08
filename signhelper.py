#! python3
# coding: UTF-8

import hashlib
import pyperclip
import re

LIVE_KEY = {'android': '3d5cb3286b2543822861ef1cab99f223',
                'ios': '5546722976dd89b6ec9cad5a17737562'}

def sign():
    params = pyperclip.paste()
    params = re.sub("\t(false\ttrue|true\ttrue|true\tfalse|false\tfalse)(?=\r\n|$)", '', params)
    params = params.replace('\t', '=')
    params_list = params.split('\r\n')
    params_list.sort()
    params_str = ''.join(params_list)

    return params_str


def pingguoMD5(origin, key='PINGUOSOFT'):
    key_len = len(key)
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
        out_string = out_string + ch
    return out_string


if __name__ == "__main__":
    #从粘贴板获得参数并处理
    params_str = sign()
    print("parrms string:\n" + params_str)
    #md5 加密
    sign_str = pingguoMD5(params_str, key=LIVE_KEY['android'])
    print("sign string:\n" + sign_str)
    pyperclip.copy(sign_str)