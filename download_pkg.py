#! python3
# coding: UTF-8

import requests
import os
import sys

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
        pkg = requests.get(pkgUrl)
        pkg.raise_for_status()

        with open(pkgPath, 'wb') as newPkg:
            newPkg.write(pkg.content)
        print("save to " + pkgPath)
    else:
        exit(1)

if __name__ =='__main__':
    save_path = get_save_path()
    project_url = get_pakage_url()
    download_package(project_url, save_path)
    while input("继续下载？Y/n ") == 'Y':
        project_url = get_pakage_url()
        download_package(project_url, save_path)

