import requests

url = 'https://dapi.livepic.com.cn/code'
payload = {'mobile': '16601297365'}

response = requests.post(url, data=payload)
print(response.json())