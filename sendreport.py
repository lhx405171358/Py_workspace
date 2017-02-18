#! python3
# coding: UTF-8

import smtplib,os,openpyxl,sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

_user = "laihouxin@ghostcloud.cn"
_pwd = "lhx2900849"
_to = "qiaorong@ghostcloud.cn"
_cc = "all-dev@ghostcloud.cn"
_report_path = r'F:\bugs\reports'

def send_email(sender, receiver, msg):
    print("From [%s] to [%s], cc [%s] ..." % (msg["From"], msg["To"], msg["Cc"] ))
    s = smtplib.SMTP("smtp.ym.163.com", 25, timeout=30)  # 连接smtp邮件服务器,端口默认是25
    s.login(_user, _pwd)  # 登陆服务器
    s.sendmail(sender, receiver.split(","), msg.as_string())  # 发送邮件
    print('Send email done!')
    s.close()

def new_report(testreport):
    lists = os.listdir(testreport)
    lists.sort(key = lambda fn: os.path.getmtime(os.path.join(testreport, fn)))
    file_new = os.path.join(testreport, lists[-1])
    print(file_new)
    return file_new

if __name__ =='__main__':
    newReport = new_report(_report_path)
    wb = openpyxl.load_workbook(newReport)
    ws = wb.get_sheet_by_name("Summary")
    date = ws['b2'].value
    ws = wb.get_sheet_by_name("New")
    numNew = ws.max_row - 2
    ws = wb.get_sheet_by_name("Resolved")
    numResolved = ws.max_row - 2
    ws = wb.get_sheet_by_name("Verified")
    numVerified = ws.max_row - 2
    ws = wb.get_sheet_by_name("Open")
    numOpen = ws.max_row - 2

    msg = MIMEMultipart()
    msg["Subject"] = date + " Bug report"
    msg["From"] = _user
    msg["To"] = _to
    msg["Cc"] = _cc


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
    ''' % (date, numNew, numResolved, numVerified, numOpen)

    part = MIMEText(emailContent, 'html', 'utf-8')
    msg.attach(part)

    # ---这是附件部分---
    # xlsx类型附件

    part = MIMEApplication(open(newReport, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(newReport))
    msg.attach(part)
    if input("Input 'Y' to  send email") != "Y":
        sys.exit(0)
    send_email(_user, ','.join([_to, _cc]), msg)