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
        filename.write(str(json_err_content) + '\n')

    @staticmethod
    def deal_lack(filename, url, lengths, code):
        content_lack = utils.response_faile(url, lengths, code)
        filename.write(str(content_lack) + '\n')

    # 配置参数接口
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
                # 数据比较
                compare_content = {'url': url, '状态码': response.status_code, 'pass': False}

                if version != compare_contants.VERSION:
                    compare_content['版本号错误'] = version
                elif file_name != compare_contants.FILE_NAME:
                    compare_content['文件名错误'] = file_name

                # data长度比较
                if len(r_dict.get('data').get('updateInfo')) < compare_contants.CONFIG_DATA_LENGTH:
                    # 缺少响应数据信息
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict.get('data').get('updateInfo')), response.status_code)
                elif len(compare_content) > compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    # 构造数据
                    content = {
                        'url': url,
                        'pass': True,
                        '状态码': response.status_code,
                        '版本号': r_dict.get('data').get('updateInfo').get('version'),
                        '文件名': r_dict.get('data').get('updateInfo').get('file'),

                    }
                    # 保存正确响应
                    self.file.write(str(content) + '\n')

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
                file_name = r_dict.get('file')
                compare_content = {'url': url, '状态码': response.status_code, 'pass': False}
                if version != compare_contants.VERSION_UP:
                    compare_content['升级版本号错误'] = version
                elif file_name != compare_contants.FILE_ADDR:
                    compare_content['升级文件名错误'] = file_name

                if len(r_dict) < compare_contants.UP_DATA_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict), response.status_code)
                elif len(compare_content) > compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    content = {
                        'url': url,
                        'pass': True,
                        '状态码': response.status_code,
                        'version': r_dict.get('version'),
                        'filename': r_dict.get('file')
                    }
                    self.file.write(str(content) + '\n')
    # 购买页
    def buy(self, url):
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
                status_code = r_dict.get('code')
                jd_url = r_dict.get('data').get('jd')
                tb_url = r_dict.get('data').get('tb')
                compare_content = {'url': url, '状态码': response.status_code, 'pass': False}
                if status_code != compare_contants.BUY_Z_CODE:
                    compare_content['code'] = status_code
                elif jd_url != compare_contants.JD:
                    compare_content['jd_url'] = jd_url
                elif tb_url != compare_contants.TB:
                    compare_content['tb_url'] = tb_url

                if len(r_dict.get('data')) < compare_contants.BUY_DATA_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict.get('data')), response.status_code)
                elif len(compare_content) > compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    content = {
                        'url': url,
                        'pass': True,
                        '状态码': response.status_code,
                        'data': r_dict.get('data')
                    }
                    self.file.write(str(content) + '\n')

    # 城市列表
    def city(self, url):
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
                status_code = r_dict.get('code')
                compare_content = {'url': url, '状态码': response.status_code, 'pass': False}
                if status_code != compare_contants.CITY_Z_CODE:
                    compare_content['code'] = status_code
                if len(r_dict.get('data')) < compare_contants.CITY_DATA_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict.get('data')), response.status_code)
                elif len(compare_content) > compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    content = {
                        'url': url,
                        'pass': True,
                        '状态码': response.status_code,
                        'data': r_dict.get('data')
                    }
                    self.file.write(str(content) + '\n')


    # 启动函数
    def run(self):
        # 配置参数接口
        self.url_config(contants.URL_CONFIG)
        # 升级更新接口
        self.check_update(contants.URL_CHECKUPDATE)
        # 购买页接口
        self.buy(contants.URL_BY)
        # 城市列表接口
        self.city(contants.URL_CITY)




if __name__ == '__main__':
    tuboAPI = TuBo_GetAPI(contants.DOMAIN)
    tuboAPI.run()
