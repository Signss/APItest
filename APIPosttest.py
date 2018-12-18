import requests, threading
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
        # 任务列表
        self.work_list = []
        # 接口参数列表
        self.url_list = []
        self.offset = 0
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
                if code != compare_contants.COMMON_CODE:
                    compare_content['code'] = code
                elif data_length != compare_contants.HOME_DATA_LENGTH:
                    compare_content['data_length'] = data_length
                elif content_length != compare_contants.HOME_CONTENT_LENGTH:
                    compare_content['content_length'] = content_length
                if content_length < compare_contants.HOME_CONTENT_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict.get('data')), response.status_code)
                elif len(compare_content) > compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    utils.correct_response(url, response, r_dict, self.file)

    # 设备页布局接口1
    def device_detail(self, url):
        try:
            headers = {
                'Authorization': self.Authorization
            }
            response = requests.post(self.domain + url, headers=headers)
        except RequestException as e:
            self.deal_request(self.request_err_file, url, e)
        else:
            try:
                r_dict = response.json()
            except ValueError as e:
                self.deal_json(self.json_err_file, url, e, response.status_code)
            else:
                code = r_dict.get('code')
                compare_content = {'url': url, '状态码': response.status_code, 'pass': False}
                if code != compare_contants.COMMON_CODE:
                    compare_content['code'] = code

                if len(r_dict.get('data')) < compare_contants.DEVICEDETAIL_DATA_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict.get('data')), response.status_code)
                elif len(compare_content) < compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    utils.correct_response(url, response, r_dict, self.file)

    # 个人名片页浏览接口1
    def visiting_card(self, url):
        try:
            headers = {
                'Authorization': self.Authorization
            }
            response = requests.post(self.domain + url, headers=headers)
        except RequestException as e:
            self.deal_request(self.request_err_file, url, e)
        else:
            try:
                r_dict = response.json()
            except ValueError as e:
                self.deal_json(self.json_err_file, url, e, response.status_code)
            else:
                code = r_dict.get('code')
                compare_content = {'url': url, '状态码': response.status_code, 'pass': False}
                if code != compare_contants.COMMON_CODE:
                    compare_content['code'] = code

                if len(r_dict.get('data')) < compare_contants.VISITCARD_DATA_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict.get('data')), response.status_code)
                elif len(compare_content) < compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    utils.correct_response(url, response, r_dict, self.file)

    # 个人名片页编辑接口1
    def edit_VisitingCard(self, url):
        try:
            headers = {
                'Authorization': self.Authorization
            }
            response = requests.post(self.domain + url, headers=headers)
        except RequestException as e:
            self.deal_request(self.request_err_file, url, e)
        else:
            try:
                r_dict = response.json()
            except ValueError as e:
                self.deal_json(self.json_err_file, url, e, response.status_code)
            else:
                code = r_dict.get('code')
                compare_content = {'url': url, '状态码': response.status_code, 'pass': False}
                if code != compare_contants.COMMON_CODE:
                    compare_content['code'] = code

                if len(r_dict.get('data')) < compare_contants.DEVICEDETAIL_DATA_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict.get('data')), response.status_code)
                elif len(compare_content) < compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    utils.correct_response(url, response, r_dict, self.file)


    # post请求运行函数
    def run(self):
        # 首页布局接口
        self.work_list.append(self.home_page)
        self.url_list.append(contants.URL_HOMEPAGE)
        # 设备页布局接口
        self.work_list.append(self.device_detail)
        self.url_list.append(contants.URL_DEVICEDETAIL)
        # 个人名片页浏览接口
        self.work_list.append(self.visiting_card)
        self.url_list.append(contants.URL_VISITCARD)
        self.edit_VisitingCard(contants.URL_EDITVISCARD)








def main():
    p_tubo = TuBoPostAPI(contants.DOMAIN)
    p_tubo.run()
    for work in p_tubo.work_list:
        work_thread = threading.Thread(target=work, args=(p_tubo.url_list[p_tubo.offset],))
        work_thread.start()
        p_tubo.offset += 1

if __name__ == '__main__':
    main()