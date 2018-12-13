import json
import time
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
from email.utils import formataddr

# 请求失败函数
def request_faile(url, err):
    req_err_content = {
        'url': url,
        'pass': 'False',
        '请求状态': '请求失败',
        '配置参数接口': err,
    }
    return req_err_content

# json转换失败函数
def json_faile(url, err, code):
    json_err_content = {
        'url': url,
        'pass': 'False',
        '问题': 'json转换错误',
        'error': err,
        'status_code': code
    }
    return json_err_content

# 响应缺少数据
def response_faile(url, lg, code):
    content_lack = {
        'url': url,
        'pass': 'False',
        '响应缺少': lg,
        'status': code
    }
    return content_lack

# 对保存文件结果处理
def deal_err_file(filename):
    url_lsit = []
    err_json = []
    with open('json_err_file.txt', 'r') as f:
        data = f.readline()
        if not data:
            content_j = {
                'type': 'json转换',
                'test_status': '通过'
            }
            return content_j
        else:
            str2 = data.replace('\n', '').replace(' ', '').replace("'", '"')
            for line in f:
                # print(line)
                str1 = line.replace('\n','').replace(' ','').replace("'",'"')
                # print(str1)
                err_json.append(str1)
            err_json.append(str2)
            for url in err_json:

                url_lsit.append(json.loads(url).get('url'))
            return url_lsit


# 邮件发送测试结果
def send_email(content):
    host_server = 'smtp.163.com'
    sender = '15058221727@163.com'
    pwd = '763541xia'
    send_mail = '15058221727@163.com'
    receivers = 'xiayong411528@163.com'
    #邮件的正文内容
    mail_time = time.strftime('%Y-%m-%d %X', time.localtime())
    mail_content = content + '<br/><br/><br/><br/><br/>'+mail_time

    #邮件标题
    print(mail_content)
    # 邮件标题
    mail_title = '图播的接口测试邮件'
    smtp = SMTP_SSL(host_server)
    # smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender, pwd)

    msg = MIMEText(mail_content, 'html', 'utf-8')
    msg['Subject'] = Header(mail_title, 'utf-8')
    msg['From'] = formataddr(['tubo', sender])
    msg['To'] = formataddr(['feige', receivers])
    smtp.sendmail(send_mail,receivers,msg.as_string())
    smtp.quit()