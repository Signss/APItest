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
        # 获取创建活动的ID以便访问删除接口
        self.create_delete_id = None
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

    # 首页布局接口2
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

    # 设备页布局接口
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
            print(len(response.json().get('data')))
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
    def editVisiting_card(self, url):
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

                if len(r_dict.get('data')) < compare_contants.EDITVISCARD_DATA_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict.get('data')), response.status_code)
                elif len(compare_content) < compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    utils.correct_response(url, response, r_dict, self.file)

    # 活动页接口
    def activity_create(self, url):
        try:
            payload = {
                'title': contants.CREATE_TITLE,
                'activity_time': contants.CREATE_TIME
            }
            headers = {
                'Authorization': self.Authorization,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.post(self.domain + url, data=payload, headers=headers)
            self.create_delete_id = response.json().get('data').get('id')
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

                if len(r_dict.get('data')) < compare_contants.CREATE_DATA_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict.get('data')), response.status_code)
                elif len(compare_content) < compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    utils.correct_response(url, response, r_dict, self.file)

    # 摄影师加入/退出
    def camerist_invite(self, url):
        try:
            payload = {'id': contants.CAMERIST_INVITE_ID}
            print(payload)
            headers = {
                'Authorization': self.Authorization
            }
            response = requests.post(self.domain + url, data=payload, headers=headers)
            print(response.json())
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
                if len(r_dict) < compare_contants.CAMERIST_INVITE_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict.get), response.status_code)
                elif len(compare_content) > compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    utils.correct_response(url, response, r_dict, self.file)

    # 摄影师被移除直播
    def camerist_out(self, url):
        try:
            payload = {'id': contants.CAMERIST_INVITE_ID,
                       'uid': contants.CAMERIST_UID}
            print(payload)
            headers = {
                'Authorization': self.Authorization
            }
            response = requests.post(self.domain + url, data=payload, headers=headers)
            print(response.json())
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
                if len(r_dict) < compare_contants.CAMERIST_INVITE_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict), response.status_code)
                elif len(compare_content) > compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    utils.correct_response(url, response, r_dict, self.file)
    # 开始直播
    def activity_start(self, url):
        try:
            payload = {'id': self.create_delete_id}
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
                compare_content = {'url': url, '状态码': response.status_code, 'pass': False}
                if code != compare_contants.COMMON_CODE:
                    compare_content['code'] = code

                if len(r_dict) < compare_contants.DELETE_DATA_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict), response.status_code)
                elif len(compare_content) < compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    utils.correct_response(url, response, r_dict, self.file)

    # 关闭直播
    def activity_close(self, url):
        try:
            payload = {'id': int(self.create_delete_id)}
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
                compare_content = {'url': url, '状态码': response.status_code, 'pass': False}
                if code != compare_contants.COMMON_CODE:
                    compare_content['code'] = code

                if len(r_dict) < compare_contants.DELETE_DATA_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict), response.status_code)
                elif len(compare_content) < compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    utils.correct_response(url, response, r_dict, self.file)


    # 删除直播
    def activity_delete(self, url):
        try:
            payload = {'id': int(self.create_delete_id)}
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
                compare_content = {'url': url, '状态码': response.status_code, 'pass': False}
                if code != compare_contants.COMMON_CODE:
                    compare_content['code'] = code

                if len(r_dict) < compare_contants.DELETE_DATA_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict), response.status_code)
                elif len(compare_content) < compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    utils.correct_response(url, response, r_dict, self.file)

    # 修改资料
    def user_update(self, url):
        try:
            headers = {
                'Authorization': self.Authorization
            }
            response = requests.post(self.domain + url, headers=headers)
            print(response.json())
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
                if len(r_dict.get('data')) < compare_contants.CAMERIST_UPDATE_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict.get('data')), response.status_code)
                elif len(compare_content) > compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    utils.correct_response(url, response, r_dict, self.file)

    # 认证摄影师
    def user_identity(self, url):
        try:
            payload = {'sn':contants.SN}
            headers = {
                'Authorization': self.Authorization
            }
            response = requests.post(self.domain + url, data=payload, headers=headers)
            print(response.json())
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
                if len(r_dict) < compare_contants.CAMERIST_INVITE_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict), response.status_code)
                elif len(compare_content) > compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    utils.correct_response(url, response, r_dict, self.file)

    # 预约摄影师
    def booking(self, url):
        try:
            headers = {
                'Authorization': self.Authorization,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.post(self.domain + url, data=contants.BOOK_DATA, headers=headers)
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

                if len(r_dict.get('data')) < compare_contants.URL_BOOKING_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict), response.status_code)
                elif len(compare_content) < compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    utils.correct_response(url, response, r_dict, self.file)

    # 举报活动
    def report_activity(self, url):
        try:
            headers = {
                'Authorization': self.Authorization,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.post(self.domain + url, data=contants.REPORT_DATA, headers=headers)
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

                if len(r_dict) < compare_contants.REPORT_DATA_LENGTH:
                    self.deal_lack(self.lack_response_err_file, url, len(r_dict), response.status_code)
                elif len(compare_content) < compare_contants.LACK_NUM:
                    self.response_err_file.write(str(compare_content) + '\n')
                else:
                    utils.correct_response(url, response, r_dict, self.file)







    # 图片上传成功回调
    def upload_callback(self, url):
        try:
            payload = contants.DATA
            headers = {
                'Authorization': self.Authorization,
                # 'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.post(self.domain + url, data=payload, headers=headers)
            print(response.json())
        except RequestException as e:
            self.deal_request(self.request_err_file, url, e)
        else:
            try:
                r_dict = response.json()
            except ValueError as e:
                self.deal_json(self.json_err_file, url, e, response.status_code)
            else:
                code = r_dict.get('code')





    # post请求运行函数
    def run(self):
        # 首页布局接口
        # self.home_page(contants.URL_HOMEPAGE)
        # 设备页布局接口
        # self.device_detail(contants.URL_DEVICEDETAIL)
        # 个人名片页浏览接口
        # self.visiting_card(contants.URL_VISITCARD)
        # 个人名片页编辑接口
        # self.editVisiting_card(contants.URL_EDITVISCARD)
        # 发起直播
        # self.activity_create(contants.URL_CREATE)

        # # 开始直播
        # self.activity_start(contants.URL_ACTIVITY_START)
        # 摄影师加入
        # self.camerist_invite(contants.URL_INVITE)
        # # 摄影师退出
        # self.camerist_invite(contants.URL_QUIT)
    # 摄影师加入/移除
    # self.camerist_invite(contants.URL_INVITE)
    # self.camerist_out(contants.URL_OUT)
        # 关闭直播
        # self.activity_close(contants.URL_ACTIVITY_CLOSE)
        # # 删除直播
        # self.activity_delete(contants.URL_ACTIVITY_DELETE)
        # 摄影师修改资料
        # self.user_update(contants.URL_USER_UPDATE)
        # 认证摄影师
    # self.user_identity(contants.URL_USER_IDENTITY)
        # 预约摄影师
        # self.booking(contants.URL_BOOKING)
        # 举报活动
        self.report_activity(contants.URL_REPORT)
        # 图片上传成功回调
        # self.upload_callback(contants.URL_CALLBACK)
        # 关闭文件
        # 请求失败保存文件
        self.request_err_file.close()
        # json转换失败保存文件
        self.json_err_file.close()
        # 响应数据字段错误保存文件
        self.response_err_file.close()
        # 响应数据字段缺少保存文件
        self.lack_response_err_file.close()


def main():
    p_tubo = TuBoPostAPI(contants.DOMAIN)
    p_tubo.run()

if __name__ == '__main__':
    main()