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
                    # 响应错误数据保存
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
                if status_code != compare_contants.COMMON_CODE:
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
                if status_code != compare_contants.COMMON_CODE:
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

    # 又拍云上传签名
    def uploadsign(self, url):
        try:
            payload = {
                'type': 1,
                'extension': 'png',
            }
            headers = {
                'Authorization': self.Authorization
            }
            response = requests.get(self.domain + url, params=payload,headers=headers)
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

                if len(r_dict.get('data')) < compare_contants.SIGN_DATA_LENGTH:
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

    # 计费商品
    def goods(self, url):
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
                code = r_dict.get('code')
                img_price = r_dict.get('data')[0].get('price')
                water_mark_price = r_dict.get('data')[1].get('price')
                water_zmark_price = r_dict.get('data')[2].get('price')
                phone_price = r_dict.get('data')[3].get('price')
                psd_price = r_dict.get('data')[4].get('price')
                compare_content = {'url': url, '状态码': response.status_code, 'pass': False}
                if code != compare_contants.COMMON_CODE:
                    compare_content['code'] = code
                elif img_price != compare_contants.IMG_PRICE:
                    compare_content['img_price'] = img_price
                elif water_mark_price != compare_contants.WATER_MARK_PRICE:
                    compare_content['water_mark_price'] = water_mark_price
                elif water_zmark_price != compare_contants.WATER_Z_MARK_PRICE:
                    compare_content['water_zmark_price'] = water_zmark_price
                elif phone_price != compare_contants.PHONE_PRICE:
                    compare_content['phone_price'] = phone_price
                elif psd_price != compare_contants.PSD_PRICE:
                    compare_content['psd_price'] = psd_price
                if len(r_dict.get('data')) < compare_contants.GOODS_DATA_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict.get('data')), response.status_code)
                elif len(compare_content) > compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    content = {
                        'url': url,
                        'pass': True,
                        '状态码': response.status_code,
                        'data' : r_dict.get('data')
                    }
                    self.file.write(str(content)+'\n')


    # 活动列表
    def activity(self, url):
        try:
            payload = {'type': 0}
            headers = {
                'Authorization': self.Authorization
            }
            response = requests.get(self.domain + url, params=payload, headers=headers)
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
                if len(r_dict.get('data')[0]) < compare_contants.ACTIVITY_DATA_LENGTH:
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

    # 活动资料页
    def activity_data(self, url):
        try:
            payload = {'id': 1032}
            headers = {
                'Authorization': self.Authorization
            }
            response = requests.get(self.domain + url, params=payload, headers=headers)
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

                if len(r_dict.get('data')) < compare_contants.ACTIVITYDATA_LENGTH:
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

    # 摄影师管理1
    def camerist(self, url):
        try:
            payload = {'id': 1032}
            headers = {
                'Authorization': self.Authorization
            }
            response = requests.get(self.domain + contants.URL_CAMERIST, params=payload, headers=headers)
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

                if len(r_dict.get('data')) < compare_contants.CAMERIST_DATA_LENGTH:
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

    # 直播原相册1
    def picture_album(self, url):
        try:
            payload = {'id': compare_contants.PICTURE_ALBUM_ID}
            headers = {
                'Authorization': self.Authorization
            }
            response = requests.get(self.domain + url, params=payload, headers=headers)
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

                if len(r_dict.get('data')) < compare_contants.PICTUREALBUM_DATA_LENGTH:
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

    # 直播详情1
    def picture_detail(self, url):
        try:
            payload = {'id': compare_contants.PICTURE_DETAIL_ID}
            headers = {
                'Authorization': self.Authorization
            }
            response = requests.get(self.domain + url, params=payload, headers=headers)
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

                if len(r_dict.get('data')) < compare_contants.PICTUREDETAIL_LENGTH:
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

    # 用户已上传图的图片列表1
    def user_picture(self, url):
        try:
            payload = {'id': compare_contants.USER_PICTURE_ID}
            headers = {
                'Authorization': self.Authorization
            }
            response = requests.get(self.domain + url, params=payload, headers=headers)
            print(response.json().get('data'))
        except RequestException as e:
            self.deal_request(self.request_err_file, url, e)
        else:
            try:
                r_dict = response.json()
            except ValueError as e:
                self.deal_json(self.json_err_file, url, e, response.status_code)
            else:
                code = r_dict.get('code')
                count = r_dict.get('data').get('release_picture_count')
                compare_content = {'url': url, '状态码': response.status_code, 'pass': False}
                if code != compare_contants.COMMON_CODE:
                    compare_content['code'] = code
                elif count != compare_contants.USER_PICTURE_COUNT:
                    compare_content['pic_count'] = count
                if len(r_dict.get('data')) < compare_contants.USERPICTURE_DATA_LENTH:
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

    # 导播管理界面1
    def editor_list(self, url):
        try:
            payload = {'id': compare_contants.USER_PICTURE_ID}
            headers = {
                'Authorization': self.Authorization
            }
            response = requests.get(self.domain + url, params=payload, headers=headers)
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
                if len(r_dict.get('data')) < compare_contants.EDITORLIST_DATA_LENGTH:
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
        # self.url_config(contants.URL_CONFIG)
        # 升级更新接口
        # self.check_update(contants.URL_CHECKUPDATE)
        # 购买页接口
        # self.buy(contants.URL_BY)
        # 城市列表接口
        # self.city(contants.URL_CITY)
        # 又拍云上传签名
        # self.uploadsign(contants.URL_UPLOADSIGN)
        # 活动列表
        # self.activity(contants.URL_ACTIVITY)
        # 计费商品列表
        # self.goods(contants.URL_GOODS)
        # 活动资料页
        # self.activity_data(contants.URL_ACTIVITY_DATA)
        # 摄影师管理
        # self.camerist(contants.URL_CAMERIST)
        # 直播原相册
        # self.picture_album(contants.URL_PIC_ALBUM)
        # 直播详情
        # self.picture_detail(contants.URL_PIC_DETAIL)
        # 用户已上传的图片列表
        # self.user_picture(contants.URL_USER_PIC)
        # 导播管理界面
        self.editor_list(contants.URL_EDITOR)

        # 关闭文件
        # 请求失败保存文件
        self.request_err_file.close()
        # json转换失败保存文件
        self.json_err_file.close()
        # 响应数据字段错误保存文件
        self.response_err_file.close()
        # 响应数据字段缺少保存文件
        self.lack_response_err_file.close()



if __name__ == '__main__':
    tuboAPI = TuBo_GetAPI(contants.DOMAIN)
    tuboAPI.run()


