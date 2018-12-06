import requests
from requests.exceptions import RequestException
from libs import utils, contants, compare_contants


# get请求接口测试类
class TuBo_GetAPI(object):

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

    @staticmethod
    def deal_request(filename, url, e):
        req_err_content = utils.request_faile(url, e)
        filename.write(str(req_err_content) + '\n')

    @staticmethod
    def deal_json(filename, url, e, code):
        json_err_content = utils.json_faile(url, e, code)
        filename.write(str(json_err_content))

    @staticmethod
    def deal_lack(filename, url, lengths, code):
        content_lack = utils.response_faile(url, lengths, code)
        filename.write(str(content_lack))

    # 1.2.配置参数接口
    def url_config(self, url):
        # 防止请求时程序报错崩溃
        try:
            response = requests.get(self.domain + url)
        except RequestException as e:
            # 请求错误信息
            self.deal_request(self.request_err_file, url, e)
        else:
            # 防止转换json报错
            try:
                r_dict = response.json()
            except ValueError as e:
                # json转换错误信息
                self.deal_json(self.json_err_file, url, e, response.status_code)
            else:
                version = r_dict.get('data').get('updateInfo').get('version')
                file_name = r_dict.get('data').get('updateInfo').get('file')
                # 构造数据
                content = {
                    'url': url,
                    'pass': True,
                    '状态码': response.status_code,
                    '版本号': r_dict.get('data').get('updateInfo').get('version'),
                    '文件名': r_dict.get('data').get('updateInfo').get('file'),

                }
                self.file.write(str(content)+'\n')
                # 数据比较
                compare_content = {}
                if version != compare_contants.VERSION:
                    compare_content['版本号错误'] = version
                elif file_name != compare_contants.FILE_NAME:
                    compare_content['文件名错误'] = file_name
                else:
                    compare_content['url'] = url
                    compare_content['status'] = response.status_code
                    compare_content['pass'] = False
                if len(compare_content) > 3:
                    self.response_err_file.write(str(compare_content)+'\n')
                # data长度比较
                if len(r_dict.get('data').get('updateInfo')) != compare_contants.CONFIG_DATA_LENGTH:
                    # 缺少响应数据信息
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict.get('data').get('updateInfo')), response.status_code)

    # 升级更新接口
    def check_update(self, url):
        try:
            response = requests.get(self.domain + url)
        except RequestException as e:
            self.deal_request(self.request_err_file, url, e)
        else:
            try:
                r_dict = response.json()
            except ValueError as e:
                self.deal_json(self.json_err_file, url, e, response.status_code)
            else:
                version = r_dict.get('version')






if __name__ == '__main__':
    tuboAPI = TuBo_GetAPI(contants.DOMAIN)
    tuboAPI.url_config(contants.URL_CONFIG)

