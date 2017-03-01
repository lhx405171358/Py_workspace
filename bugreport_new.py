#! python3
# coding: UTF-8

import os,openpyxl,sys,time,bugzilla
import sendreport
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
#利用python-bugzilla库重写下，不用慢慢爬信息了···

BUGZILLA_URL = "http://192.168.9.11"
EMAIL_USER = "laihouxin@ghostcloud.cn"
EMAIL_TO = "qiaorong@ghostcloud.cn"
EMAIL_CC = "all-dev@ghostcloud.cn"
REPORT_PATH = r"F:\bugs\reports"

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

bzapi = bugzilla.Bugzilla(BUGZILLA_URL)

newQuery = bzapi.build_query(
    product="GCE"
)
resolvedQuery = bzapi.build_query(
    product="GCE",
    status="RESOLVED"
)
verifiedQuery = bzapi.build_query(
    product="GCE",
    status="CLOSE"
)
openQuery = bzapi.build_query(
    product="GCE",
    status=['UNCONFIRMED', 'CONFIRMED', 'IN_PROGRESS', 'REOPEN']
)

#get new bugs
newQuery['creation_time'] = dateFrom
newBugsFrom = bzapi.query(newQuery)
newQuery['creation_time'] = dateTo
newBugsTo = bzapi.query(newQuery)
newBugs = newBugsFrom[0:len(newBugsFrom)-len(newBugsTo)]
print('Get %s new bugs' % len(newBugs))

#get resolved bugs
resolvedQuery['last_change_time'] = dateFrom
resolvedBugsFrom = bzapi.query(resolvedQuery)
resolvedQuery['last_change_time'] = dateTo
resolvedBugsTo = bzapi.query(resolvedQuery)
resolvedBugs = resolvedBugsFrom[0:len(resolvedBugsFrom)-len(resolvedBugsTo)]
print('Get %s resolved bugs' % len(resolvedBugs))

#get Verified bugs
verifiedQuery['last_change_time'] = dateFrom
verifiedBugsFrom = bzapi.query(verifiedQuery)
verifiedQuery['last_change_time'] = dateTo
verifiedBugsTo = bzapi.query(verifiedQuery)
verifiedBugs = verifiedBugsFrom[0:len(verifiedBugsFrom)-len(verifiedBugsTo)]
print('Get %s verified bugs' % len(verifiedBugs))
#get Open bugs
openBugs = bzapi.query(openQuery)
print('Get %s open bugs' % len(openBugs))

allBugsList = [newBugs, resolvedBugs, verifiedBugs, openBugs]

# TODO:存储信息到excel文件
print("Save to excel file...")
wb = openpyxl.load_workbook(os.path.join(REPORT_PATH, 'bugreport.xlsx'))
sheetNames = wb.get_sheet_names()
ws = wb.get_sheet_by_name('Summary')
ws['b2'] = dateFrom + ' to ' + dateTo
for i in range(len(allBugsList)):
    ws = wb.get_sheet_by_name(sheetNames[i + 1])
    for irow in range(len(allBugsList[i])):
        print('Save bug%s ...' % (allBugsList[i][irow].id))
        ws.cell(row=irow + 3, column=1).value = allBugsList[i][irow].id
        ws.cell(row=irow + 3, column=2).value = allBugsList[i][irow].component
        ws.cell(row=irow + 3, column=3).value = allBugsList[i][irow].summary
        ws.cell(row=irow + 3, column=4).value = allBugsList[i][irow].assigned_to
        ws.cell(row=irow + 3, column=5).value = allBugsList[i][irow].severity
        ws.cell(row=irow + 3, column=6).value = allBugsList[i][irow].status
        ws.cell(row=irow + 3, column=7).value = allBugsList[i][irow].creator
        ws.cell(row=irow + 3, column=8).value = str(allBugsList[i][irow].last_change_time)
    print('Write %s bugs info to %s sheet' % (len(allBugsList[i]), ws.title))

#以bugreport_YYYYMMDD-YYYYMMDD.xlsx形式保存
targetFilename = REPORT_PATH + '\\' + 'bugreport_'+ dateFrom.replace('-', '')+'-'+dateTo.replace('-', '')+'.xlsx'
print('save to ' + targetFilename)
wb.save(targetFilename)

if input("From %s to %s , cc %s\nInput 'Y' to  send email"  % (EMAIL_USER, EMAIL_TO, EMAIL_CC)) != "Y":
    sys.exit(0)

# TODO:发送邮件
# 如名字所示Multipart就是分多个部分
print("Send email...")
numNew = len(allBugsList[0])
numResolved = len(allBugsList[1])
numVerified = len(allBugsList[2])
numOpen  = len(allBugsList[3])

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
