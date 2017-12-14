#! python3
# coding: UTF-8

import os
import subprocess
import platform
import pyperclip
import time
import logging
import bugzilla
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

APP_PATH = r"D:\tester\camera360\apk\camera360"
APP_PACKAGE = "vStudio.Android.Camera360"
LOG_PATH = r"/sdcard/Android/data/vStudio.Android.Camera360/files"

FONT_BULE = "\033[36m"
FONT_GREEN = "\033[32m"
FONT_RED = "\033[31m"

def set_color(color=FONT_BULE):
    if platform.system() == "Windows":
        print(color)


def unset_color():
    if platform.system() == "Windows":
        print("\033[0m")


def get_latest_apk(apk_dir=APP_PATH):
    apk_dir = apk_dir if os.path.exists(apk_dir) else APP_PATH
    dir_lists = os.listdir(apk_dir)
    dir_lists.sort(key=lambda file: os.path.getmtime(os.path.join(apk_dir, file)))
    dir_lists = list(filter(lambda file: file.endswith(".apk"), dir_lists))
    latest_apk = os.path.join(apk_dir, dir_lists[-1])
    return latest_apk


def execute_selection(selection):
    if selection == "1":
        pkg_dir = input("Input app path(default {default_path}):".format(default_path=APP_PATH))
        app_path = get_latest_apk(pkg_dir)
        while input("Install {path} to device?(Y/n)".format(path=app_path)) == "Y":
            rc = subprocess.run("adb uninstall {package}".format(package=APP_PACKAGE), stdout=True, stderr=True)
            if rc.returncode == 0:
                subprocess.run('adb install -r "{path}"'.format(path=app_path), stdout=True)
                print("Done")
    elif selection == "2":
        print("uninstall...")
        rc = subprocess.run("adb uninstall {package}".format(package=APP_PACKAGE), stdout=True, stderr=subprocess.PIPE)
        if rc.returncode == 0 and "Unknown package" in str(rc.stderr):
            set_color(FONT_RED)
            print("package not exists\n")
            unset_color()
    elif selection == "3":
        print("clear data...")
        os.system("adb shell pm clear {package}".format(package=APP_PACKAGE))
        print("")
    elif selection == "4":
        print("kill app...")
        os.system("adb shell am force-stop {package}".format(package=APP_PACKAGE))
        print("")
    elif selection == "5":
        print("get package name...")
        os.system("adb shell dumpsys window w | findstr \/ | findstr name=")
        print("")
    elif selection == "6":
        print("get system version...")
        os.system("adb shell getprop ro.build.version.release")
        print("")
    elif selection == "7":
        print("get device info...")
        device_man = ""
        device_model = ""
        andr_version = ""
        try:
            device_man = str(subprocess.check_output("adb shell getprop  ro.product.manufacturer", shell=True),
                             encoding='gbk').replace("\r", "").replace("\n", '')
            device_model = str(subprocess.check_output("adb shell getprop  ro.product.model",shell=True), encoding='gbk').replace("\r", "").replace("\n", '')
            andr_version = str(subprocess.check_output("adb shell getprop ro.build.version.release",shell=True), encoding='gbk').replace("\r", "").replace("\n", '')
        except Exception as err:
            logging.error(err)
            print("None")
        print(device_man, device_model, andr_version)
        today = time.strftime("%Y-%m-%d", time.localtime())
        bug_info = '''【版本信息】
{device_man} {device_model}  android {andr_version}

【预设条件】
#

【操作步骤】
1.

【预期结果】


【实际结果】


【发生概率】
100%

【发生日期】
{today}
'''.format(device_man=device_man, device_model=device_model, andr_version=andr_version, today=today)

        pyperclip.copy(bug_info)
        print("Done")
    elif selection == "8":
        print("get crash log...")
        file_list = None
        try:
            file_list = str(subprocess.check_output('adb shell ls {err_path} | find ".err"'.format(err_path=LOG_PATH), shell=True), encoding='gbk').replace("\r", "").rstrip("\n").split("\n")
        except Exception as err:
            logging.error(err)
        if file_list:
            for index, log_file in enumerate(file_list):
                print(str(index)+". "+log_file)
if __name__ == "__main__":
    is_quit = False
    while not is_quit:
        set_color()
        os.system("cls")
        selection = input("Input your selection:\n"
                          "1.Install latest app\n"
                          "2.remove app\n"
                          "3.clear app data\n"
                          "4.stop app\n"
                          "5.get package name\n"
                          "6.get system version\n"
                          "7.copy bug info\n"
                          "8.get crash log\n")
        unset_color()
        execute_selection(selection)
        if input("go on(input ‘n’ to quit)? ") == "n":
            is_quit = True
