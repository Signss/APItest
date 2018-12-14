import os
from libs import contants, utils
from APIGettest import TuBoGetAPI


# time.sleep(10)
# os.remove('json_err_file.txt')
email_str = '<h1>图播接口测试结果</h1><br/>'


# 处理测试结果文件
def deal_get():
    get_test = TuBoGetAPI(contants.DOMAIN)
    get_test.run()
    send_list = []
    json_result = utils.deal_err_file('json_err_file.txt',  'json转换')
    send_list.append(json_result)
    request_result = utils.deal_err_file('request_err_result.txt', '请求失败测试')
    send_list.append(request_result)
    response_result = utils.deal_err_file('response_err_file.txt', '响应数据错误测试')
    send_list.append(response_result)
    lack_result = utils.deal_err_file('lack_response_err_file.txt', '缺少响应测试')
    send_list.append(lack_result)
    return send_list

def email_content(send_list):
    pass_list = []
    pass_str = ''
    url_str = ['<h4>json转换失败:</h4>','<h4>请求接口失败:</h4>','<h4>响应数据错误:</h4>','<h4>响应数据缺少:</h4>']
    send_url = ''
    i = 0
    for content in send_list:
        if type(content) == list :
            # 根据循环次数拼接错误类型
            send_url = send_url + url_str[i]
            for url_err in content:
                # 同一错误类型下拼接错误接口
                send_url = send_url + '<h5>' + url_err + '</h5>'

        else:
            # 拼接通过测试类型
            err_str = '<h5>' + content.get('type') + ':' + content.get('test_status') + '</h5>'
            pass_list.append(err_str)
        i = i + 1
    for err_data in pass_list:
        pass_str = err_data + pass_str
    pass_str  = pass_str + send_url
    return pass_str

def main():
    send_list = deal_get()
    pass_str = email_content(send_list)
    content = email_str + pass_str
    utils.send_email(content)
    os.remove('json_err_file.txt')
    os.remove('request_err_result.txt')
    os.remove('response_err_file.txt')
    os.remove('lack_response_err_file.txt')


if __name__ == '__main__':
    main()