#! python3
# coding: UTF-8

import requests,os,bs4,openpyxl,sys,time
import sendreport
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


EMAIL_USER = "xxx@xxx.cn"
EMAIL_TO = "xxx@xxx.cn"
EMAIL_CC = "xxx@xxx.cn"
REPORT_PATH = r"F:\bugs\reports"
BUGZILLA_URL = 'http://192.168.9.11/'

ONEDAYSECONDS = 3600*24

# TODO:读取日期参数
today = time.time()

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
    dateTo =  time.strftime("%Y-%m-%d", time.localtime(today))
print("DATE:%s to %s" % (dateFrom, dateTo))

# TODO:爬取bugzilla上bug信息
# 四种搜索bug URL
newBugsURL = BUGZILLA_URL+'buglist.cgi?chfield=%5BBug%20creation%5D&product=GCE' + '&chfieldfrom=' + dateFrom + '&chfieldto=' + dateTo
resolvedBugsURL = BUGZILLA_URL+'buglist.cgi?bug_status=RESOLVED&product=GCE'+ '&chfieldfrom=' + dateFrom + '&chfieldto=' + dateTo
verifiedBugsURL = BUGZILLA_URL+'buglist.cgi?bug_status=CLOSE&product=GCE'+ '&chfieldfrom=' + dateFrom + '&chfieldto=' + dateTo
openBugsURL = BUGZILLA_URL+'buglist.cgi?bug_status=UNCONFIRMED&bug_status=CONFIRMED&bug_status=IN_PROGRESS&bug_status=REOPEN&product=GCE'
bugsURL = [newBugsURL, resolvedBugsURL, verifiedBugsURL, openBugsURL]
# bugsURL = [newBugsURL]

#四种bug字典存入一个list，方便迭代
allBugsList = []
for i in range(len(bugsURL)):
    bugs = {}
    bugs.setdefault('url', bugsURL[i])
    bugs.setdefault('bug_info', [])
    allBugsList.append(bugs)

#不使用代理，防止出现502
# proxies = {
#     "http": None,
#     "https": None,
# }

#分别开始提取每个url中的bug
for bugs in allBugsList:
    print('Get %s ...'% bugs['url'])
    res = requests.get(bugs['url'])
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

# TODO:存储信息到excel文件
print("Save to excel file...")
wb = openpyxl.load_workbook(os.path.join(REPORT_PATH, 'bugreport.xlsx'))
sheetNames = wb.get_sheet_names()
ws = wb.get_sheet_by_name('Summary')
ws['b2'] = dateFrom + ' to ' + dateTo
for i in range(len(allBugsList)):
    ws = wb.get_sheet_by_name(sheetNames[i + 1])
    for irow in range(len(allBugsList[i]['bug_info'])):
        ws.append(allBugsList[i]['bug_info'][irow])
    print('write %s bugs info to %s' % (len(allBugsList[i]['bug_info']), ws.title))

#以bugreport_YYYYMMDD-YYYYMMDD.xlsx形式保存
targetFilename = REPORT_PATH + '\\' + 'bugreport_'+ dateFrom.replace('-', '')+'-'+dateTo.replace('-', '')+'.xlsx'
print('save to ' + targetFilename)
wb.save(targetFilename)

if input("Input 'Y' to  send email") != "Y":
    sys.exit(0)

# TODO:发送邮件
# 如名字所示Multipart就是分多个部分
print("Send email...")
wb2 = openpyxl.load_workbook(targetFilename, data_only = True)
ws2 = wb2.get_sheet_by_name("Summary")
numNew = len(allBugsList[0]['bug_info'])
numResolved = len(allBugsList[1]['bug_info'])
numVerified = len(allBugsList[2]['bug_info'])
numOpen  = len(allBugsList[3]['bug_info'])

msg = MIMEMultipart()
msg["Subject"] = dateFrom + ' to ' + dateTo + ' Bug report'
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_TO
msg["Cc"] = EMAIL_CC

# ---这是文字部分---
emailContent = '''
<p>BUG概览如下，详细统计情况见附件:</p>
<table border="1" cellspacing="0" cellpadding="2"  width="400">
      <tr  bgcolor="#1f4e78" align="center" >
          <th colspan='2'><font color="#fff">bug统计</font></th>
      </tr>
      <tr bgcolor="#fff" align="left" >
          <td bgcolor="#a6a6a6" ><b>时间</b></td><td>%s</td>
      </tr>
      <tr bgcolor="#fff" align="left" >
          <td bgcolor="#a6a6a6" ><b>新增</b></td><td>%s</td>
      </tr>
      <tr bgcolor="#fff" align="left" >
          <td bgcolor="#a6a6a6" ><b>已解决待验证</b></td><td>%s</td>
      </tr>
      <tr bgcolor="#fff" align="left" >
          <td bgcolor="#a6a6a6" ><b>已验证</b></td><td>%s</td>
      </tr>
      <tr bgcolor="#fff" align="left" >
          <td bgcolor="#a6a6a6" ><b>待解决</b></td><td>%s</td>
      </tr>
  </table>
'''% (dateFrom+" To "+dateTo, numNew, numResolved, numVerified, numOpen)

part = MIMEText(emailContent, 'html', 'utf-8')
msg.attach(part)

# ---这是附件部分---
# xlsx类型附件
part = MIMEApplication(open(targetFilename, 'rb').read())
part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(targetFilename))
msg.attach(part)

sendreport.send_email(EMAIL_USER, ','.join([EMAIL_TO, EMAIL_CC]), msg)
