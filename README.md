# 自用的一些简单的python小脚本
## bugreport 和 bugreport_new
### 功能
自动抓取bugzilla上一段时间内的的bug信息生成excel格式的report并发送邮件。
两个脚本区别在于实现方式不同：
- bugreport是直接使用requests和beautifulsoup抓取bug信息
- bugreport_new使用了python-bugzilla直接获取bug信息

### 使用
- 直接在.py文件里面填写对应项：
```angular2html
EMAIL_USER = "xxx@example.com"
EMAIL_TO = "receiver@example.com"
EMAIL_CC = "all-dev@example.com"
REPORT_PATH = r"F:\bugs\reports"
BUGZILLA_URL = 'http://192.168.9.11/'
```
- 把bugreport.xlsx放到REPORT_PATH下
- 把/pyscript目录加到path中
- 直接在cmd中输入bugreport使用
 
```
Usage:
bugreport [datefrom] [dateto]
datefrom格式: YYYY-MM-DD
dateto格式: YYYY-MM-DD
```

## sendreport
### 功能
自动找到给定路径下最新的report文件并发送

### 使用
- 直接在.py文件里面填写对应项：
```angular2html
_user = "xxx@example.com"
_pwd = "xxxxxxx"
_to = "receiver@example.com"
_cc = "receiver@example.com"
_report_path = r'F:\bugs\reports'
```

- 把/pyscript目录加到path中
- 直接在cmd中输入sendreport使用

## renamefile
### 功能
根据创建时间对指定目录下的图片（jpg或png）进行改名，改名后格式为%Y-%m-%d-%H%M%S
### 使用
- 把/pyscript目录加到path中
- 直接在cmd中输入renamefile使用
```
Usage:
renamefile [path]
```
