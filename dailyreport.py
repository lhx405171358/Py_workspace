#! python3
# coding: UTF-8

import requests, bs4, sys, time, os
import sendreport
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



EMAIL_USER = "laihouxin@camera360.com"
EMAIL_TO = "laihouxin@camera360.com"
EMAIL_CC = "laihouxin@camera360.com"
REPORT_PATH = r"D:\tester\camera360\daily_reports"
BUGZILLA_URL = "https://bugzilla.camera360.com/"
BUGZILLA_USER = "laihouxin@camera360.com"
BUGZILLA_PASSWORD = "lhx2900849"

PRODUCT = "Camera360 for Android 8.X"
VERSION = "8.8.0"
BUG_TYPE = ('A', 'B', 'C', 'D', 'Enh', 'Total')

# 设置默认时间区间为今日
DATE_FROM = time.strftime("%Y-%m-%d", time.localtime(time.time()))
DATE_TO = DATE_FROM

# 读取日期参数
def get_date(argv=sys.argv):
    date_from = DATE_FROM
    date_to = DATE_TO

    if len(argv) == 3:
        try:
            time.strptime(argv[1], "%Y-%m-%d")
            time.strptime(argv[2], "%Y-%m-%d")
        except ValueError:
            print('Usage: python dailyreport.py [datefrom] [dateto]\n'
                  'datefrom and dateto should be like: 2017-03-02')
            sys.exit()
        date_from = argv[1]
        date_to = argv[2]
    elif len(argv) == 2:
        try:
            time.strptime(argv[1], "%Y-%m-%d")
        except ValueError:
            print('Usage: python dailyreport.py [datefrom] [dateto]\n'
                  'datefrom and dateto should be like: 2017-03-02')
            sys.exit()
        date_from = argv[1]
        date_to = date_from
    print("DATE:%s to %s" % (date_from, date_to))
    return date_from, date_to


def get_bug_summary():
    # 四种搜索bug URL,对应 总BUG数	未修复BUG	今日修复BUG	新增BUG
    total_url = "{url}report.cgi?x_axis_field=bug_status&y_axis_field=bug_severity&product={product}&version={version}&chfield=[Bug+creation]&chfieldfrom={datefrom}&chfieldto={dateto}&j_top=AND&format=table&action=wrap".format(
        url=BUGZILLA_URL, product=PRODUCT, version=VERSION, datefrom='', dateto='')
    open_url = "{url}report.cgi?x_axis_field=bug_status&y_axis_field=bug_severity&product={product}&version={version}&chfield=[Bug+creation]&chfieldfrom={datefrom}&chfieldto={dateto}&j_top=AND&format=table&action=wrap&bug_status=NEW&bug_status=RE-OPEN&bug_status=IN_PROGRESS".format(
        url=BUGZILLA_URL, product=PRODUCT, version=VERSION, datefrom='', dateto='')
    today_resolved_url = "{url}report.cgi?x_axis_field=bug_status&y_axis_field=bug_severity&product={product}&version={version}&chfield=resolution&chfieldfrom={datefrom}&chfieldto={dateto}&j_top=AND&format=table&action=wrap&resolution=FIXED&resolution=WONTFIX&resolution=DUPLICATE".format(
        url=BUGZILLA_URL, product=PRODUCT, version=VERSION, datefrom=DATE_FROM, dateto=DATE_TO)
    today_new_url = "{url}report.cgi?x_axis_field=bug_status&y_axis_field=bug_severity&product={product}&version={version}&chfield=[Bug+creation]&chfieldfrom={datefrom}&chfieldto={dateto}&j_top=AND&format=table&action=wrap".format(
        url=BUGZILLA_URL, product=PRODUCT, version=VERSION, datefrom=DATE_FROM, dateto=DATE_TO)

    # 四种bug字典存入一个list，方便迭代
    bug_info_list = []
    # 抓取bug概况
    bug_urls = [total_url, open_url, today_resolved_url, today_new_url]
    for url in bug_urls:
        bug_count_dict = dict.fromkeys(BUG_TYPE, 0)
        res = requests.post(url, data={'Bugzilla_login': BUGZILLA_USER, 'Bugzilla_password': BUGZILLA_PASSWORD})
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        if soup.tbody == None:
            bug_info_list.append(bug_count_dict)
            continue
        trs = soup.tbody.findAll('tr')
        for tr in trs:
            bug_tag = tr.td.string.strip()
            bug_count_dict[bug_tag] = str(tr.findAll('td')[-1].find('a')).replace('buglist.cgi',
                                                                                  BUGZILLA_URL + "buglist.cgi")
        bug_info_list.append(bug_count_dict)
    return bug_info_list


def get_module_bug_summary():
    # 每个模块剩余未修复的bug url
    module_bug_url = "{url}report.cgi?x_axis_field=bug_severity&y_axis_field=component&product={product}&version={version}&chfield=[Bug+creation]&chfieldfrom={datefrom}&chfieldto={dateto}&j_top=AND&format=table&action=wrap&bug_status=NEW&bug_status=RE-OPEN".format(
        url=BUGZILLA_URL, product=PRODUCT, version=VERSION, datefrom='', dateto='')
    module_bug_list = []
    res = requests.post(module_bug_url, data={'Bugzilla_login': BUGZILLA_USER, 'Bugzilla_password': BUGZILLA_PASSWORD})
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    if soup.tbody != None:
        soup.thead.tr.attrs['bgcolor'] = '#1f4e78'
        module_bug_list.append(str(soup.thead))
        for tr in soup.tbody.findAll('tr'):
            tr.td.attrs['bgcolor'] = '#a6a6a6'
            tr.td.attrs['align'] = 'center'
            module_bug_list.append(str(tr).replace('buglist.cgi', BUGZILLA_URL + 'buglist.cgi'))
    return module_bug_list

def get_everyone_bug_summary():
    # 每人新报的bug url
    today_new_everyone_url = "{url}report.cgi?x_axis_field=bug_status&y_axis_field=bug_severity&z_axis_field=reporter&product={product}&version={version}&chfield=[Bug+creation]&chfieldfrom={datefrom}&chfieldto={dateto}&j_top=AND&format=table&action=wrap".format(
        url=BUGZILLA_URL, product=PRODUCT, version=VERSION, datefrom=DATE_FROM, dateto=DATE_TO)
    res = requests.post(today_new_everyone_url,
                        data={'Bugzilla_login': BUGZILLA_USER, 'Bugzilla_password': BUGZILLA_PASSWORD})
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    name_list = soup.findAll('h2')
    name_list = [str(x) for x in name_list]
    everyone_bug_list = soup.findAll(id='tabular_report')
    for x in everyone_bug_list:
        x.attrs.setdefault('cellspacing', '0')
    everyone_bug_list = [str(x).replace('buglist.cgi', BUGZILLA_URL + 'buglist.cgi') for x in everyone_bug_list]

    return name_list, everyone_bug_list


# 获取A级Bug概况
def get_A_bug_summary():
    A_bug_url = "{url}buglist.cgi?bug_severity=A&bug_status=NEW&bug_status=RE-OPEN&bug_status=IN_PROGRESS&version={version}&product={product}".format(
        url=BUGZILLA_URL, product=PRODUCT, version=VERSION)
    #print(A_bug_url)
    res = requests.post(A_bug_url, data={'Bugzilla_login': BUGZILLA_USER, 'Bugzilla_password': BUGZILLA_PASSWORD})
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    A_bug_list  = soup.select('tr[id]')
    A_bug_list = [str(x) for x in A_bug_list]
    return A_bug_list

def construct_email_content(bug_info_list, module_bug_list, A_bug_list,name_list, everyone_bug_list):
    mail_msg = MIMEMultipart()
    mail_msg["From"] = EMAIL_USER
    mail_msg["To"] = EMAIL_TO
    mail_msg["Cc"] = EMAIL_CC
    if DATE_FROM == DATE_TO:
        mail_msg["Subject"] = DATE_FROM + ' Bug report'
    else:
        mail_msg["Subject"] = DATE_FROM + ' to ' + DATE_TO + ' Bug report'

    #  bug总览部分
    bug_summary = '''
    <h1>BUG概览如下:</h1>
    <table border="1" cellspacing="0" cellpadding="2"  width="400">
          <tr  bgcolor="#1f4e78" align="center" >
              <th>BUG情况</th> 
              <th>总BUG数</th>
              <th>未修复BUG</th>
              <th>今日修复BUG</th>
              <th>新增BUG</th>
          </tr>
          <tr bgcolor="#fff" align="center" >
              <td bgcolor="#a6a6a6" ><b>A</b></td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
          </tr>
          <tr bgcolor="#fff" align="center" >
              <td bgcolor="#a6a6a6" ><b>B</b></td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
          </tr>
          <tr bgcolor="#fff" align="center" >
              <td bgcolor="#a6a6a6" ><b>C</b></td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
          </tr>
          <tr bgcolor="#fff" align="center" >
              <td bgcolor="#a6a6a6" ><b>D</b></td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
          </tr>
          <tr bgcolor="#fff" align="center" >
              <td bgcolor="#a6a6a6" ><b>Enh</b></td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
          </tr>
          <tr bgcolor="#fff" align="center" >
              <td bgcolor="#a6a6a6" ><b>Total</b></td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
          </tr>
      </table>
    ''' % (bug_info_list[0]['A'], bug_info_list[1]['A'], bug_info_list[2]['A'], bug_info_list[3]['A'],
           bug_info_list[0]['B'], bug_info_list[1]['B'], bug_info_list[2]['B'], bug_info_list[3]['B'],
           bug_info_list[0]['C'], bug_info_list[1]['C'], bug_info_list[2]['C'], bug_info_list[3]['C'],
           bug_info_list[0]['D'], bug_info_list[1]['D'], bug_info_list[2]['D'], bug_info_list[3]['D'],
           bug_info_list[0]['Enh'], bug_info_list[1]['Enh'], bug_info_list[2]['Enh'], bug_info_list[3]['Enh'],
           bug_info_list[0]['Total'], bug_info_list[1]['Total'], bug_info_list[2]['Total'], bug_info_list[3]['Total'])


    # 模块bug部分
    module_bug_summary = '''
    <h1>模块待解决bug概览如下:</h1>
    <table border="1" cellspacing="0" cellpadding="2"  width="400">
    '''
    for module_bug_item in module_bug_list:
        module_bug_summary = module_bug_summary + module_bug_item
    module_bug_summary = module_bug_summary + '</table>'

    # A级bug
    A_bug_summary = '''
     <h1>待解决A级bug如下:</h1>
     <table border="1" cellspacing="0" cellpadding="2"  width="700">
     <tr bgcolor="#a6a6a6">
          <th colspan="1">ID</th>
          <th colspan="1">Product</th>
          <th colspan="1">Comp</th>
          <th colspan="1">Assignee</th>
          <th colspan="1">Status</th>
          <th colspan="1">Resolution</th>
          <th colspan="1">Summary</th>
          <th colspan="1">Changed</th>
        </tr>
    '''
    for A_bug_item in A_bug_list:
        A_bug_summary = A_bug_summary + A_bug_item
    A_bug_summary = A_bug_summary + '</table>'


    # 个人bug部分
    everyone_bug_summary = '''
    <h1>每人bug概览如下:</h1>
    '''
    for name, bug_info in zip(name_list, everyone_bug_list):
        everyone_bug_summary = everyone_bug_summary + name + bug_info

    # 将email内容保存到html文件
    email_content = bug_summary + module_bug_summary + A_bug_summary + everyone_bug_summary
    report_filename = os.path.join(REPORT_PATH, 'daily_report_' + DATE_FROM + '_to_' + DATE_TO + '.html')
    with open(report_filename, 'w') as report_file:
        report_file.write(email_content)
    print('report save to ' + report_filename)

    # 将html格式的内容添加到邮件中
    part = MIMEText(email_content, 'html', 'utf-8')
    mail_msg.attach(part)
    return mail_msg

if __name__ =='__main__':
    if len(sys.argv) > 1:
        DATE_FROM, DATE_TO = get_date(sys.argv)
    # 获取bug概况
    summary_list = get_bug_summary()
    # 获取模块bug概况
    module_summary_list = get_module_bug_summary()
    # 获取A级bug
    A_summary_list = get_A_bug_summary()
    # 获取个人bug概况
    reporter_list, everyone_summary_list = get_everyone_bug_summary()
    # 构建邮件内容
    msg = construct_email_content(summary_list, module_summary_list, A_summary_list, reporter_list, everyone_summary_list)

    if input("From %s to %s , cc %s\nInput 'Y' to  send email" % (EMAIL_USER, EMAIL_TO, EMAIL_CC)) != "Y":
        sys.exit(0)
    else:
        sendreport.send_email(EMAIL_USER, ','.join([EMAIL_TO, EMAIL_CC]), msg)





