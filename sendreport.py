#! python3
# coding: UTF-8

import smtplib,os,openpyxl,sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

USER = "laihouxin@camera360.com"
PWD = "Lhx2900849"
TO = "laihouxin@camera360.com"
CC = "laihouxin@camera360.com"
REPORT_PATH = r'D:\tester\reports'
SMTP_SERVER = 'smtp.exmail.qq.com'

def send_email(sender, receiver, msg):
    s = smtplib.SMTP(SMTP_SERVER, 25, timeout=30)  # 连接smtp邮件服务器,端口默认是25
    s.login(USER, PWD)  # 登陆服务器
    s.sendmail(sender, receiver.split(","), msg.as_string())  # 发送邮件
    print('Send email done!')
    s.close()

def new_report(reportpath):
    lists = os.listdir(reportpath)
    lists.sort(key = lambda fn: os.path.getmtime(os.path.join(reportpath, fn)))
    file_new = os.path.join(reportpath, lists[-1])
    report_file = file_new.replace('html', 'xlsx')
    print(report_file)
    return report_file

if __name__ =='__main__':
    newReport = new_report(REPORT_PATH)
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
    msg["From"] = USER
    msg["To"] = TO
    msg["Cc"] = CC


    # ---这是文字部分---
    htmlfile = open(newReport.replace('xlsx', 'html'), 'r')
    emailContent = htmlfile.read()
    htmlfile.close()

    part = MIMEText(emailContent, 'html', 'utf-8')
    msg.attach(part)

    # ---这是附件部分---
    # xlsx类型附件

    part = MIMEApplication(open(newReport, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(newReport))
    msg.attach(part)
    print("From [%s] to [%s], cc [%s]" % (msg["From"], msg["To"], msg["Cc"]))
    if input("Input 'Y' to  send email") != "Y":
        sys.exit(0)
    send_email(USER, ','.join([TO, CC]), msg)