#! python3
import os,time,shutil,sys
print("Current work dir is", os.getcwd())
if len(sys.argv) == 2:
    workdir = sys.argv[1]
else:
    workdir = r'D:\tester\screenshots'
print('Change dir to', workdir)
os.chdir(workdir)

for filename in os.listdir("."):
    suffix = os.path.splitext(filename)[-1] #取得后缀
    if suffix == '.png' or suffix == '.jpg':
        timeStamp = os.path.getctime(filename) #取得文件创建时间戳
        timeArray = time.localtime(timeStamp)  #时间戳转换为时间数组
        formatTime = time.strftime("%Y-%m-%d-%H%M%S", timeArray) #间时间格式转换
        shutil.move(filename,formatTime + suffix)
        print("rename %s to %s" % (filename, formatTime + suffix))