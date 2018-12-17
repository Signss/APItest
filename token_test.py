#coding:utf-8
# 测试文件
import requests, json

url_code = 'https://dapi.livepic.com.cn/code'
payload = {'mobile':'16601297365'}

response_code = requests.post(url_code, data=payload)
print(response_code.json())

url_login = 'https://dapi.livepic.com.cn/user/authorization'

login_data = {'mobile':'16601297365', 'code':'123456'}
response_login = requests.post(url_login, data=login_data)
print(response_login.url)
login_dict = response_login.json()

authon = 'Bearer ' + login_dict.get('data').get('access_token')
print(authon)

url_uploadsign = 'https://dapi.livepic.com.cn/uploadsign'
uploadsigin_data = {'type':1, 'extension': 'png'}
headers = {'Authorization': authon}
upsign = requests.get(url_uploadsign, params=uploadsigin_data, headers=headers)
print(upsign.json())

a = [1,2,3,4,5]
for b in a:
    print(a.index(b))
