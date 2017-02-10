#! python3
# coding: UTF-8

import requests,os,bs4,openpyxl,sys,time,pprint
from openpyxl.styles import Font, NamedStyle

#new: http://192.168.9.11/buglist.cgi?chfield=%5BBug%20creation%5D&chfieldfrom=2017-02-01&chfieldto=Now&product=GCE
#resovled: http://192.168.9.11/buglist.cgi?bug_status=RESOLVED&chfield=%5BBug%20creation%5D&chfieldfrom=2017-02-01&chfieldto=Now&product=GCE
#closed: http://192.168.9.11/buglist.cgi?bug_status=CLOSE&chfield=%5BBug%20creation%5D&chfieldfrom=2017-02-01&chfieldto=Now&product=GCE
#remain： http://192.168.9.11/buglist.cgi?bug_status=UNCONFIRMED&bug_status=CONFIRMED&bug_status=IN_PROGRESS&bug_status=REOPEN&product=GCE

# TODO:读取日期参数
today = time.time()
ONEDAYSECONDS = 3600*24

if len(sys.argv) > 1:
    try:
        time.strptime(sys.argv[1], "%Y-%m-%d")
        time.strptime(sys.argv[2], "%Y-%m-%d")
    except ValueError:
        print('Usage: python bugreport.py [datefrom] [dateto]\n'
              'datefrom and dateto should be like: 2017-03-02')
        sys.exit()
    dateFrom = sys.argv[1]
    dateTo = sys.argv[2]
else:
    fiveDaysAgo =  today - 5 * ONEDAYSECONDS
    fiveDaysAgoFormatTime = time.strftime("%Y-%m-%d", time.localtime(fiveDaysAgo))
    dateFrom = fiveDaysAgoFormatTime
    dateTo = "Now"
print("DATE:%s to %s" % (dateFrom, dateTo))
# TODO:爬取bugzilla上bug信息
# 四种搜索bug URL
newBugsURL = 'http://192.168.9.11/buglist.cgi?chfield=%5BBug%20creation%5D&product=GCE' + '&chfieldfrom=' + dateFrom + '&chfieldto=' + dateTo
resolvedBugsURL = 'http://192.168.9.11/buglist.cgi?bug_status=RESOLVED&product=GCE'+ '&chfieldfrom=' + dateFrom + '&chfieldto=' + dateTo
closedBugsURL = 'http://192.168.9.11/buglist.cgi?bug_status=CLOSE&product=GCE'+ '&chfieldfrom=' + dateFrom + '&chfieldto=' + dateTo
remainBugsURL = 'http://192.168.9.11/buglist.cgi?bug_status=UNCONFIRMED&bug_status=CONFIRMED&bug_status=IN_PROGRESS&bug_status=REOPEN&product=GCE'
bugsURL = [newBugsURL, resolvedBugsURL, closedBugsURL, remainBugsURL]
# bugsURL = [newBugsURL]

#四种bug字典存入一个list，方便迭代
allBugsList = []
for i in range(len(bugsURL)):
    bugs = {}
    bugs.setdefault('url', bugsURL[i])
    bugs.setdefault('bug_info', [])
    allBugsList.append(bugs)

#不使用代理，防止出现502
proxies = {
    "http": None,
    "https": None,
}

#分别开始提取每个url中的bug
for bugs in allBugsList:
    print('Get %s ...'% bugs['url'])
    res = requests.get(bugs['url'], proxies = proxies)
    res.raise_for_status()
    print('Get succeed')

    #提取出所有bug信息
    print('Extract all bugs info...')
    soup = bs4.BeautifulSoup(res.text,"html.parser")
    bugInfos = soup.select('tr[id]')
    #遍历所有bug信息，将bug信息条目存入一个list，在将此list添加到对应字典中
    for bugInfo in bugInfos:
        bugsList = []
        for bugInfoItem in bugInfo.select('td'):
            bugInfoItemStr = bugInfoItem.get_text().replace('\n', '').strip()
            bugsList.append(bugInfoItemStr)
        print('Get bug%s'% bugsList[0])
        bugs['bug_info'].append(bugsList)
    bugs.setdefault('sum', len(bugs['bug_info']))
    print('Done, sum: %s bugs'%bugs['sum'])
    # pprint.pprint(bugs)

# TODO:存储信息到excel文件
print("Save to excel file...")
wb = openpyxl.load_workbook('bugreport.xlsx')
sheetNames = wb.get_sheet_names()

for i in range(1, len(sheetNames)):
    ws = wb.get_sheet_by_name(sheetNames[i])
    for row in ws.rows:
        #todo 添加bug信息
# TODO:发送邮件
