# 请求失败函数
def request_faile(url, err):
    req_err_content = {
        'url': url,
        'pass': False,
        '请求状态': '请求失败',
        '配置参数接口': err,
    }
    return req_err_content

# json转换失败函数
def json_faile(url, err, code):
    json_err_content = {
        'url': url,
        'pass': False,
        '问题': 'json转换错误',
        'error': err,
        'status_code': code
    }
    return json_err_content

# 响应缺少数据
def response_faile(url, lg, code):
    content_lack = {
        'url': url,
        'pass': False,
        '响应缺少': lg,
        'status': code
    }
    return content_lack

# 响应数据比较
# def compare_dict(filename ,c_dict,url, code, ptest):
#     c_dict['url'] = url
#     c_dict['状态码'] = code
#     c_dict['pass'] = False
#     if len(c_dict) > 3:
#         filename.write(str(c_dict) + '\n')