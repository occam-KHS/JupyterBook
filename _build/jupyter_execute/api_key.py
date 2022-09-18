#!/usr/bin/env python
# coding: utf-8

# In[1]:


import keyring


# In[2]:


keyring.set_password('real_app_key','occam123','PS4JCzNypY0tab3OA4ibiUub5ajCcAT2E7Uu')
keyring.set_password('real_app_secret','occam123','T6jn0eBkoV+/y+1qgm9XUiCZ3Gkq0NNX7kjHnKFCTJxeiavmR+0VQUQBP+lSFRhuNQyBBTFd/YFpDmjAjPhYbflcrDpm90KX03KbyIiwfTqPuWoy/Rv6oXfWeLrU/NU4OU2xB2w7Q1SSBY/DUQhNlShlDxyFypqJfYTjuW/5OitLlG0osYE=')


# In[3]:


keyring.set_password('mock_app_key','occam123','PSEhFrkjaWhtKkQI9cjHmJGmPyg2MhG2HNIo')
keyring.set_password('mock_app_secret','occam123','awmouEMNGnniIRHDhtgBtDopV4E2t6kNVHBNv1TyNIbvYNmk/kTGmT9zBcCLk+QQXOPhozttouajsjYGGOJDbBhGB+S9ESLaqeQ5i1hAoBYTkHx2wtGD4SAE9EEkZ5Alcvl1ScFf7UdvWeVese81uMA+2/jYC7oxENu85tdgk8wxqmadOHo=')


# In[4]:


keyring.get_password('mock_app_key','occam123')


# In[14]:


DISCORD_WEBHOOK_URL = keyring.get_password('discord_webhook','occam123')


# In[15]:


keyring.set_password('discord_webhook','occam123','https://discord.com/api/webhooks/1020800210001199187/X2Deqar0nI_mu0EVLxiKiCQGGQB7fmQh-a6H_46GRhdxChKtnzk1VUoBVgUTdyLIyPIh')
import datetime
import requests
def send_message(msg):
    """디스코드 메세지 전송"""
    now = datetime.datetime.now()
    message = {"content": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {str(msg)}"}
    requests.post(DISCORD_WEBHOOK_URL, data=message)
    print(message)


# In[16]:


send_message('Hello')


# In[32]:


import json
APP_KEY = keyring.get_password('real_app_key','occam123')
APP_SECRET =  keyring.get_password('real_app_secret','occam123')


# In[25]:


def hashkey(datas):
    """암호화"""
    PATH = "uapi/hashkey"
    URL = f"{URL_BASE}/{PATH}"
    headers = {
    'content-Type' : 'application/json',
    'appKey' : APP_KEY,
    'appSecret' : APP_SECRET,
    }
    res = requests.post(URL, headers=headers, data=json.dumps(datas))
    hashkey = res.json()["HASH"]
    return hashkey


# In[26]:


def get_access_token():
    """토큰 발급"""
    headers = {"content-type":"application/json"}
    body = {"grant_type":"client_credentials",
    "appkey":APP_KEY,
    "appsecret":APP_SECRET}
    PATH = "oauth2/tokenP"
    URL = f"{URL_BASE}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    ACCESS_TOKEN = res.json()["access_token"]
    return ACCESS_TOKEN


# In[30]:


ACCESS_TOKEN = get_access_token()

"""주식 종목 현재가 조회"""

# 다음 장에서 더 자세히 설명 드립니다. 
# requests.get() 함수의 구성 요소를 집중적으로 봐주세요 (e.g. URL, headers, params)

URL_BASE = "https://openapi.koreainvestment.com:9443" # 실전 투자
PATH = "uapi/domestic-stock/v1/quotations/inquire-price" # 현재가 조회를 위한 URL 경로
URL = f"{URL_BASE}/{PATH}"
code = "005930" # 삼성전자 종목 코드

headers = {
    "Content-Type":"application/json",
    "authorization": f"Bearer {ACCESS_TOKEN}", # 보안인증키
    "appKey":APP_KEY, # API 신청으로 발금 받은 Key
    "appSecret":APP_SECRET, # API 신청으로 발금 받은 Secret
    "tr_id":"FHKST01010100" # 현재가 조회를 위한 id
}
params = {
    "fid_cond_mrkt_div_code":"J", # J: 주식
    "fid_input_iscd":code, # 조회 하고 싶은 주식 종목의 코드 ex) 삼성전자: 005930
}

res = requests.get(URL, headers=headers, params=params) # <<<<<<<<<

print(int(res.json()['output']['stck_prpr']))


# In[31]:


res.json()['output']


# In[ ]:




