#!/usr/bin/env python
# coding: utf-8

# In[55]:


# keyring.set_password('real_app_key','occam123','PSFEvvteQEozUSIzNzkEaMJLI5u1UXidbEQr')
# keyring.set_password('real_app_secret','occam123','4jDvcydJucYSSrrT+6khBsjyvLhONQfOQbQjGunP0tEB0QOiSKuU1aNRWGTiCa9dnHB+/Fusxmryx8xRFFMln1scV9GE3mRqbOAui/myt/Pr3gMi14DnkD58xBk4X1gePTVz1fLsU5DVJ7qWii3LfbRY6CMzB4znkGSiGceCk57+dIHpvXc=')


# In[56]:


# keyring.set_password('mock_app_key','occam123','PSyACQnZTx0YfBqE2Ocn3iSsOa4uWWjptWjW')
# keyring.set_password('mock_app_secret','occam123','OfhLxJH9NEXeOG4fJwLSzxepeLl4FDDkG3n+1r03tRrYKgJ7fNbXOuQbA9sljT8qE0+We0jmkbwQs8DNkfcEIbyDlaRKeVdee/hjPKCZHBJFIOSGJrZAv63QIUulN1zbqIHe+nm6Uq35OkXurGgCm5rg6B5Ik1VY2E0LIGtElE7B/FQBDcw=')


# In[2]:


# keyring.get_password('mock_app_key','occam123')


# In[3]:


# DISCORD_WEBHOOK_URL = keyring.get_password('discord_webhook','occam123')


# In[11]:


# keyring.set_password('discord_webhook','occam123','https://discord.com/api/webhooks/1020800210001199187/X2Deqar0nI_mu0EVLxiKiCQGGQB7fmQh-a6H_46GRhdxChKtnzk1VUoBVgUTdyLIyPIh')
# import datetime
# import requests
# def send_message(msg):
#     """디스코드 메세지 전송"""
#     now = datetime.datetime.now()
#     message = {"content": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {str(msg)}"}
#     requests.post(DISCORD_WEBHOOK_URL, data=message)
#     print(message)


# ### 자동매매 코드

# In[ ]:


import requests
import json
import datetime
import time
import yaml
from IPython.display import clear_output
import keyring

import json
APP_KEY = keyring.get_password('real_app_key','occam123')
APP_SECRET =  keyring.get_password('real_app_secret','occam123')
URL_BASE = "https://openapi.koreainvestment.com:9443" # 실전 투자
CANO = '63566811'
ACNT_PRDT_CD = '01'



# APP_KEY = keyring.get_password('mock_app_key','occam123')
# APP_SECRET =  keyring.get_password('mock_app_secret','occam123')
# URL_BASE = "https://openapivts.koreainvestment.com:29443" #모의투자서비스
# CANO = ' 50070883'
# ACNT_PRDT_CD = '01'

# def print(msg):
#     """디스코드 메세지 전송"""
#     now = datetime.datetime.now()
#     message = {"content": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {str(msg)}"}
#     requests.post(DISCORD_WEBHOOK_URL, data=message)
#     print(message['content'])

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

def get_current_price(code="005930"):
    """현재가 조회"""
    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json",
            "authorization": f"Bearer {ACCESS_TOKEN}",
            "appKey":APP_KEY,
            "appSecret":APP_SECRET,
            "tr_id":"FHKST01010100"}
    params = {
    "fid_cond_mrkt_div_code":"J",
    "fid_input_iscd":code,
    }
    res = requests.get(URL, headers=headers, params=params)
    return int(res.json()['output']['stck_prpr']), float(res.json()['output']['prdy_vrss_vol_rate'])

def get_target_price(code="005930"):
    """전날 종가 조회"""
    PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-price"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json",
        "authorization": f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"FHKST01010400"}
    params = {
    "fid_cond_mrkt_div_code":"J",
    "fid_input_iscd":code,
    "fid_org_adj_prc":"1",
    "fid_period_div_code":"D"
    }
    res = requests.get(URL, headers=headers, params=params)
    stck_clpr = int(res.json()['output'][1]['stck_clpr']) #전일 종가
    target_price = stck_clpr
    return target_price


def get_stock_5d_before():
    def get_stock_before(date):
        PATH = "uapi/domestic-stock/v1/trading/inquire-daily-ccld"
        URL = f"{URL_BASE}/{PATH}"
        headers = {"Content-Type":"application/json",
            "authorization":f"Bearer {ACCESS_TOKEN}",
            "appKey":APP_KEY,
            "appSecret":APP_SECRET,
            "tr_id":"TTTC8001R",  # 실전 투자 "TTTC8001R", 모의투자 "VTTC8001R"
            "custtype":"P",
        }
        params = {
            "CANO": CANO,
            "ACNT_PRDT_CD": ACNT_PRDT_CD,
            "INQR_STRT_DT": date,
            "INQR_END_DT": date,
            "SLL_BUY_DVSN_CD": "02", # 00:전체, 01:매도, 02:매수
            "INQR_DVSN": "01", # 00: 역순
            "PDNO": "", 
            "CCLD_DVSN": "01",
            "ORD_GNO_BRNO":"",
            "ODNO":"",
            "INQR_DVSN_3": "01",
            "INQR_DVSN_1": "",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": ""
        }
        res = requests.get(URL, headers=headers, params=params)
        stock_dict = res.json()['output1']
        return stock_dict
    prev = 7
    while prev < 15:
        t_previous_5d = datetime.datetime.now().date() - datetime.timedelta(days=prev)
        t_previous_5d = t_previous_5d.strftime("%Y%m%d")
        bought_previous_5d_dict = get_stock_before(t_previous_5d)
        if len(bought_previous_5d_dict) > 0:
            break
        else:
            prev += 1
    sell_list_5d_over = []
    for stock in bought_previous_5d_dict:
        sell_list_5d_over.append(stock['pdno'])
    sell_list_5d_over = list(set(sell_list_5d_over))
    return sell_list_5d_over

def get_stock_balance():
    """주식 잔고조회"""
    PATH = "uapi/domestic-stock/v1/trading/inquire-balance"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json",
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC8434R",  # 실전 투자 "TTTC8434R" 모의투자 "VTTC8434R"
        "custtype":"P",
    }
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "AFHR_FLPR_YN": "N",
        "OFL_YN": "",
        "INQR_DVSN": "02",
        "UNPR_DVSN": "01",
        "FUND_STTL_ICLD_YN": "N",
        "FNCG_AMT_AUTO_RDPT_YN": "N",
        "PRCS_DVSN": "01",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": ""
    }
    res = requests.get(URL, headers=headers, params=params)
    stock_list = res.json()['output1']
    evaluation = res.json()['output2']
    stock_dict = {}
    print(f"====주식 보유잔고====")
    for stock in stock_list:
        if int(stock['hldg_qty']) > 0:
            stock_dict[stock['pdno']] = [stock['hldg_qty'], stock['evlu_pfls_rt']] # 0: 보유 수량, 1: 평가수익율
            print(f"{stock['prdt_name']}({stock['pdno']}): {stock['hldg_qty']}주")
            time.sleep(0.1)
    print(f"주식 평가 금액: {evaluation[0]['scts_evlu_amt']}원")
    time.sleep(0.1)
    print(f"평가 손익 합계: {evaluation[0]['evlu_pfls_smtl_amt']}원")
    time.sleep(0.1)
    print(f"총 평가 금액: {evaluation[0]['tot_evlu_amt']}원")
    time.sleep(0.1)
    print(f"=================")
    return stock_dict

def get_balance():
    """현금 잔고조회"""
    PATH = "uapi/domestic-stock/v1/trading/inquire-psbl-order"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json",
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC8908R", # 실전 투자 : "TTTC8908R" 모의투자 "VTTC8908R"
        "custtype":"P",
    }
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "PDNO": "005930",
        "ORD_UNPR": "65500",
        "ORD_DVSN": "01",
        "CMA_EVLU_AMT_ICLD_YN": "Y",
        "OVRS_ICLD_YN": "Y"
    }
    res = requests.get(URL, headers=headers, params=params)
    cash = res.json()['output']['ord_psbl_cash']
    print(f"주문 가능 현금 잔고: {cash}원")
    return int(cash)

def buy(code="005930", qty="1"):
    """주식 시장가 매수"""
    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{URL_BASE}/{PATH}"
    data = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "PDNO": code,
        "ORD_DVSN": "01",
        "ORD_QTY": str(int(qty)),
        "ORD_UNPR": "0",
    }
    headers = {"Content-Type":"application/json",
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC0802U",  # 실전 투자 : "TTTC0802U" 모의투자 'VTTC0802U'
        "custtype":"P",
        "hashkey" : hashkey(data)
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    if res.json()['rt_cd'] == '0':
        print(f"[매수 성공]{str(res.json())}")
        return True
    else:
        print(f"[매수 실패]{str(res.json())}")
        return False

def sell(code="005930", qty="1"):
    """주식 시장가 매도"""
    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{URL_BASE}/{PATH}"
    data = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "PDNO": code,
        "ORD_DVSN": "01",
        "ORD_QTY": qty,
        "ORD_UNPR": "0",
    }
    headers = {"Content-Type":"application/json",
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC0801U", # 실전 투자 : TTTC0801U "VTTC0801U"
        "custtype":"P",
        "hashkey" : hashkey(data)
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    if res.json()['rt_cd'] == '0':
        print(f"[매도 성공]{str(res.json())}")
        return True
    else:
        print(f"[매도 실패]{str(res.json())}")
        return False


# 자동매매 시작
try:
    ACCESS_TOKEN = get_access_token()
    symbol_list = ['071460','300080','227610','217480','089530'] # 매수 희망 종목 리스트

    bought_list = [] # 매수 완료된 종목 리스트
    total_cash = get_balance() # 보유 현금 조회
    stock_dict = get_stock_balance() # 보유 주식 조회
    
    for sym in stock_dict.keys():
        bought_list.append(sym)        
        
    symbol_list = list(set(symbol_list) - set(bought_list)) # 기 매수 종목 제거
    
    target_buy_count = len(symbol_list) # 매수할 종목 수
    buy_percent = 1/len(symbol_list) # 종목당 매수 금액 비율
    buy_amount = total_cash*0.5*buy_percent  # 종목별 주문 금액 계산
    soldout = False
    
   
    print("===국내 주식 자동매매 프로그램을 시작합니다===")
    while True:
        t_now = datetime.datetime.now()
        t_9 = t_now.replace(hour=9, minute=0, second=0, microsecond=0)
        t_start = t_now.replace(hour=9, minute=5, second=0, microsecond=0)
        t_sell = t_now.replace(hour=15, minute=15, second=0, microsecond=0)
        t_exit = t_now.replace(hour=15, minute=20, second=0,microsecond=0)
        today = datetime.datetime.today().weekday()

        if today == 5 or today == 6:  # 토요일이나 일요일이면 자동 종료
            print("주말이므로 프로그램을 종료합니다.")
            break

        if t_start < t_now < t_sell :  # AM 09:00 ~ PM 03:15
            # 매수 코드           
            
            for sym in symbol_list:
                if len(bought_list) < target_buy_count:
                    if sym in bought_list:
                        continue
                    target_price = get_target_price(sym) # 전날 종가, Get from Input dictionary
                    current_price, volume_rate = get_current_price(sym)
                    
                    t_progress= (t_now - t_9)/(t_exit - t_9)
                    c1 = (target_price < current_price < target_price*1.05)
                    c2 = (float(volume_rate/t_progress) > 100)
                    print(f'종목: {sym}, 현재가: {current_price}, 전일종가: {target_price}, 거래량지표: {float(volume_rate/t_progress):5.1f}')
                    if c1 and c2: # Max: 5% 상승 가격, Min: 전날 종가
                        
                        buy_qty = 0  # 매수할 수량 초기화
                        buy_qty = int(buy_amount // current_price)
                        if (buy_qty > 0):
                            
                            print(f"{sym} 목표가 달성({target_price} < {current_price}) 매수를 시도합니다.")
                            result = buy(sym, buy_qty)
                            if result:
                                soldout = False
                                bought_list.append(sym) # 매수 종목
                                get_stock_balance()
                                
                    time.sleep(1)
                    
                    
            # 매도 코드
            balance_dict = get_stock_balance()
            for sym, qty_rt in balance_dict.items(): # qty_rt / [0]: qty(보유수량), [1]: rt(평가수익율)
                current_price, volume_rate = get_current_price(sym)
                
                print(f'{sym} 현재 수익율: {float(qty_rt[1]): 5.2f}')
                if float(qty_rt[1]) > 5.0 or float(qty_rt[1]) < -3.0: # 익절 라인은 dynamic 하게 바꿀 수 있다 (단위 %)
                    sell(sym, qty_rt[0])

            time.sleep(1)

            if t_now.minute == 30 and t_now.second <= 5: # 매 30분 마다 코드가 잘 돌아가는 지 확인하는 코드
                get_stock_balance()
                time.sleep(5)

 
        if t_sell < t_now < t_exit:  # PM 03:15 ~ PM 03:20 : 5th Day 를 맞이한 종목들 일괄 매도
            ###############
            sell_list_5d_over = get_stock_5d_before()            
            stock_dict = get_stock_balance()
        
            sell_list = list(set(stock_dict.keys()) & set(sell_list_5d_over)) # 보유종목 중 5일이상 된 종목
            for sym in sell_list:
                sell(sym, stock_dict['sym'][0])  # 보유종목 중 5일이상 된 종목 전량 매도     
                   
            time.sleep(1)

        if t_exit < t_now:  # PM 03:20 ~ :프로그램 종료            
            print("프로그램을 종료합니다.")
            break

        clear_output(wait=True)

            
except Exception as e:
    print(f"[오류 발생]{e}")
    time.sleep(1)


# In[ ]:




