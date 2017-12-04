#! python3
# coding: UTF-8

import os
import subprocess
import platform

APP_PATH = r"D:\tester\camera360\apk\test_apk"
APP_PACKAGE = "vStudio.Android.Camera360"

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
if __name__ == "__main__":
    is_quit = False
    while not is_quit:
        set_color()
        os.system("cls")
        selection = input("Input your selection:\n1.Install latest app\n2.remove app\n3.clear app data\n4.stop app\n5.get package name\n")
        unset_color()
        execute_selection(selection)
        if input("go on(input ‘n’ to quit)? ") == "n":
            is_quit = True
