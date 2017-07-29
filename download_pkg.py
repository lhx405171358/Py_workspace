#! python3
# coding: UTF-8

import requests
import os
import sys
from contextlib import closing


URL_LIST = ("https://toolchain.camera360.com/apollo/getModuleDetail?module=Camera360-photoTask",
            "https://toolchain.camera360.com/apollo/getModuleDetail?module=Camera360_Live")

COOKIES = dict(c360_oa_user_info="MmlNRGFrcWxMVXNkTzdDZzFzbjU1eVV4LzFBa2VTOUJoWjB2Y2xkZUx4MzIzMWtaamt0SUVTTGVhcXdXMU5oZkZFUHVpTlRPdDd5cURHMGhwUEdpZ3UyM20xNG9NSWNLZVBNZmhnbVFqcW54blF4Q3M0QkVOWHBkRHllUmhNeVIxL1JYYVdPenlTY09vdGxZQitlVm1hOVpsRnQ5Ukp1MmxiTTFpKzlkSnV6aVJ0TndIcTVhVVE9PQ%3D%3D")
SAVE_PATH = r"D:\tester\camera360\apk"


def get_save_path():
    if len(sys.argv) == 1:
        save_path = SAVE_PATH
    elif len(sys.argv) == 2:
        if not os.path.exists(sys.argv[1]):
            print("The path " + sys.argv[1] + " does not exist")
            exit(1)
        save_path = sys.argv[1]
    else:
        print("usage: download_pkg pkg_path")
        exit(1)
    return save_path


def get_pakage_url():
    # get new package url
    projectName = [url.split("=")[-1] for url in URL_LIST]
    print("select project:")
    for index, name in enumerate(projectName):
        print(str(index) + ":" + name)
    selection = int(input("\n"))
    projectUrl = ""
    if 0 <= selection < len(projectName):
        project_url = URL_LIST[selection]
    else:
        print("no such options")
        get_pakage_url()
    return project_url


def download_package(url, path):
    res = requests.get(url, cookies=COOKIES)
    res.raise_for_status()
    data = res.json()
    pkgUrl = data['data']['list'][0]['setupUrl']
    pkgLogs = data['data']['list'][0]['log']
    print("[package url]:" + pkgUrl)
    print("[package log]:")
    for log in pkgLogs:
        print(log)
    print("[save path]:" + SAVE_PATH)
    if input("download?(Y/n)") == 'Y':
        pkgName = pkgUrl.split("/")[-2] + "-" + pkgUrl.split("/")[-1]
        pkgPath = os.path.join(SAVE_PATH, pkgName)
        print("Downloading... ")
        #下载并显示进度条
        with closing(requests.get(pkgUrl, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            progress = ProgressBar(pkgName, total=content_size, unit="KB", chunk_size=chunk_size, run_status="正在下载",
                                   fin_status="下载完成")
            with open(pkgPath, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))
        print("apk save to " + pkgPath)
        return pkgPath
    else:
        exit(1)



"""
作者：微微寒
链接：https://www.zhihu.com/question/41132103/answer/93438156
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0,    unit='', sep='/', chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status, self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)


if __name__ =='__main__':
    save_path = get_save_path()

    while True:
        project_url = get_pakage_url()
        pkg_path = download_package(project_url, save_path)
        while input("安装？Y/n ") == 'Y':
            if not os.system("adb uninstall vStudio.Android.Camera360"):
                os.system("adb install -r {pkg_path}".format(pkg_path=pkg_path))
        if input("继续下载? Y/n") != 'Y':
            break



