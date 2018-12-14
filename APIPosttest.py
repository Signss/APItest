import requests
from requests.exceptions import RequestException
from libs import utils, contants, compare_contants

# get请求接口测试类
class TuBoPostAPI(object):

    # 初始化信息
    def __init__(self, domain):
        self.domain = domain
        # 正确响应保存文件
        self.file = open('test_result.txt', 'a')
        # 请求失败保存文件
        self.request_err_file = open('request_err_result.txt', 'a')
        # json转换失败保存文件
        self.json_err_file = open('json_err_file.txt', 'a')
        # 响应数据字段错误保存文件
        self.response_err_file = open('response_err_file.txt', 'a')
        # 响应数据字段缺少保存文件
        self.lack_response_err_file = open('lack_response_err_file.txt', 'a')
        # 获取token
        r_dict = None
        try:
            payload_code = {'mobile': contants.MOBILE}
            # 先请求验证码
            requests.post(self.domain + contants.URL_CODE, data=payload_code)
            # 再登录
            payload_login = {'mobile': contants.MOBILE, 'code': contants.FIX_CODE}
            response_login = requests.post(self.domain + contants.URL_LOGIN, data=payload_login)
            r_dict = response_login.json()
        except RequestException as e:
            print(e)
        self.Authorization = contants.TOKEN_PREFIX + r_dict.get('data').get('access_token')

    # 存储请求失败结果
    @staticmethod
    def deal_request(filename, url, e):
        req_err_content = utils.request_faile(url, e)
        filename.write(str(req_err_content) + '\n')
    # 存储json转换失败结果
    @staticmethod
    def deal_json(filename, url, e, code):
        json_err_content = utils.json_faile(url, e, code)
        filename.write(str(json_err_content) + '\n')
    # 存储响应缺少错误结果
    @staticmethod
    def deal_lack(filename, url, lengths, code):
        content_lack = utils.response_faile(url, lengths, code)
        filename.write(str(content_lack) + '\n')

    # 首页布局接口
    def home_page(self, url):
        try:
            payload = {'page': contants.HOME_PAGE,
                       'num': contants.HOME_NUM}
            headers = {
                'Authorization': self.Authorization,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.post(self.domain + url, data=payload, headers=headers)
            print(response.json().get('data'))
            print(len(response.json().get('data').get('content')))
        except RequestException as e:
            self.deal_request(self.request_err_file, url, e)
        else:
            try:
                r_dict = response.json()
            except ValueError as e:
                self.deal_json(self.json_err_file, url, e, response.status_code)
            else:
                code = r_dict.get('code')
                data_length = len(r_dict.get('data'))
                content_length = len(r_dict.get('data').get('content'))
                compare_content = {'url': url, '状态码': response.status_code, 'pass': False}
                pass


    # post请求运行函数
    def run(self):
        # 首页布局接口
        self.home_page(contants.URL_HOMEPAGE)

def main():
    p_tubo = TuBoPostAPI(contants.DOMAIN)
    p_tubo.run()

if __name__ == '__main__':
    main()