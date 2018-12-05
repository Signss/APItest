# 请求失败函数
def request_faile(url, err):
    req_err_content = {
        'url': url,
        '请求状态': '请求失败',
        '配置参数接口': err,
    }
    return req_err_content

# json转换失败函数
def json_faile(url, err, code):
    json_err_content = {
        'url': url,
        '问题': 'json转换错误',
        'error': err,
        'status_code': code
    }
    return json_err_content

# 响应缺少数据
def response_faile(url, lg, code):
    content_lack = {
        'url': url,
        '响应缺少': lg,
        'status': code
    }
    return content_lack