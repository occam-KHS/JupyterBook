#!/usr/bin/env python
# coding: utf-8

# ## 실시간 데이터 받아오기

# 실시간 데이터 중, 자주 사용하는 Real 목록들을 차례대로 살펴 보겠습니다.
# 
# * [K3_] KOSDAQ 체결
# * [HA_] KOSDAQ 호가잔량
#     
# 앞 절과 마찬가지로 다음과 같은 순서로 체결 및 호가잔량 조회 코드를 살펴 보겠습니다. 
# <ol>
#   <li>변수를 관리하는 MyObjects 클래스</li>
#   <li>데이터를 요청하는 Main 클래스</li>
#   <li>데이터를 수신하는 XQ_event_handler 클래스</li>
# </ol>

# ### 1. [K3_] KOSDAQ 체결
# KOSDAQ체결 데이터는 매수/매도 주문을 넣을 때 꼭 필요한 실시간 데이터 입니다.

# 먼저 MyObjects 클래스에서 추가된 변수는 2개 입니다.
# 
# | 추가변수 | 정의 |
# | :----- | :----- |
# | K3_dict | 알고리즘 추천종목의 체결정보 저장 딕셔너리 변수 |
# | real_event | 체결정보 요청함수를 저장 변수 |

# In[ ]:


# 1. MyObjects: 변수관리 클래스 

class MyObjects:
    server = "demo" # hts:실투자, demo: 모의투자
    tr_ok = False # TR요청
    real_ok = False # 실시간 요청
    acc_num = 계좌번호 # 계좌번호
    acc_pw = 계좌비밀번호 # 계좌비밀번호

    t0424_dict = {} # 잔고내역2 종목들 모아 놓은 딕셔너리
    K3_dict = {} #< 종목의 체결정보들 모아 놓은 딕셔너리
    
    ####### 요청 함수 모음
    tr_event = None # TR요청에 대한 API 정보
    real_event = None #< 실시간 요청에 대한 API 정보
    t0424_request = None # 잔고내역2 조회 요청함수
    ##################


# Main 클래스에서는 실시간 데이터를 수신 할 XR_event_handler 클래스를 등록하고, KOSDAQ 체결 데이터를 조회 할 "K3_" Res 파일을 등록합니다. 조회하고 싶은 추천종목 코드를 모아 놓은 리스트 변수가 "code_list" 입니다. 추천종목 코드를 SetFieldData() 함수에 입력 변수 값으로 넣고, 체결이 이루어질 때 마다 데이터 수신이 이루어지도록 AdviseRealData() 함수를 호출합니다. 

# In[ ]:


# 2. Main: 실행용 클래스

class Main:
    def __init__(self):
        print("실행용 클래스이다")

        # ... 코드 생략 ...
        
        #<<<<<
        
        MyObjects.real_event = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", XR_event_handler)
        MyObjects.real_event.ResFileName = "C:/eBEST/xingAPI/Res/K3_.res"
        for shcode in MyObjects.code_list:
            print("체결정보 종목 등록 %s" % shcode)
            MyObjects.real_event.SetFieldData("InBlock", "shcode", shcode)
            MyObjects.real_event.AdviseRealData()
    
        #<<<<<
        
        while MyObjects.real_ok is False:
            pythoncom.PumpWaitingMessages()

        
    # ... 코드 생략 ...


# 데이터를 요청하는 Main 클래스에서 조회 결과 수신 클래스로 XR_event_handler 를 등록했습니다. 따라서, 증권서버에서 요청에 응답하면 XR_event_handler 클래스의 OnReceiveRealData() 함수에서 "K3_" 에 대한 결과를 확인 할 수 있습니다. "code" 변수를 통해 요청했던 데이터를 구분하고 GetFieldData() 함수를 통해 실시간 체결 데이터를 조회 할 수 있게 됩니다.

# In[ ]:


# 3. XR_event_handler: 실시간 데이터 수신 클래스

class XR_event_handler:

    def OnReceiveRealData(self, code):
        
        #<<<<<
        
        if code == "K3_":

            shcode = self.GetFieldData("OutBlock", "shcode")

            if shcode not in MyObjects.K3_dict.keys():
                MyObjects.K3_dict[shcode] = {}

            tt = MyObjects.K3_dict[shcode]
            tt["체결시간"] = self.GetFieldData("OutBlock", "chetime")
            tt["등락율"] = float(self.GetFieldData("OutBlock", "drate"))
            tt["현재가"] = int(self.GetFieldData("OutBlock", "price"))
            tt["시가"] = int(self.GetFieldData("OutBlock", "open"))
            tt["고가"] = int(self.GetFieldData("OutBlock", "high"))
            tt["저가"] = int(self.GetFieldData("OutBlock", "low"))
            tt["누적거래량"] = int(self.GetFieldData("OutBlock", "volume"))
            tt["매도호가"]= int(self.GetFieldData("OutBlock", "offerho"))
            tt["매수호가"] = int(self.GetFieldData("OutBlock", "bidho"))
        
        #<<<<<


# ### 2. [HA_] KOSDAQ 호가잔량
# KOSDAQ 호가 및 호가잔량 데이터도 매수/매도 주문을 넣을 때 꼭 필요한 실시간 데이터 입니다.

# 마찬가지로 먼저 MyObjects 클래스에서 추가된 변수는 2개 입니다.
# 
# | 추가변수 | 정의 |
# | :----- | :----- |
# | HA_dict | 호가 및 호가잔량 정보 저장 변수 |
# | real_event_ha | 호가 요청함수 저장 변수 |

# In[ ]:


# 1. MyObjects: 변수관리 클래스 

class MyObjects:
    server = "demo" # hts:실투자, demo: 모의투자
    tr_ok = False # TR요청
    real_ok = False # 실시간 요청
    acc_num = 계좌번호 # 계좌번호
    acc_pw = 계좌비밀번호 # 계좌비밀번호

    t0424_dict = {} # 잔고내역2 종목들 모아 놓은 딕셔너리
    K3_dict = {} # 종목의 체결정보들 모아 놓은 딕셔너리
    HA_dict = {} #< 종목의 호가잔량을 모아 놓은 딕셔너리
    
    ####### 요청 함수 모음
    tr_event = None # TR요청에 대한 API 정보
    real_event = None # 실시간 요청에 대한 API 정보
    real_event_ha = None #< 실시간 요청에 대한 API 정보
    t0424_request = None # 잔고내역2 조회 요청함수
    ##################


# Main 클래스에서는 실시간 데이터를 수신 할 XR_event_handler 클래스를 등록하고, KOSDAQ 체결 데이터를 조회 할  "HA_" Res 파일을 등록합니다. 조회하고 싶은 추천종목 코드를 모아 놓은 리스트 변수가 "code_list" 입니다. 추천종목 코드를 SetFieldData() 함수에 입력 변수 값으로 넣고, 호가 정보가 바뀔 때마다 데이터 수신이 이루어지도록 AdviseRealData() 함수를 호출합니다. 

# In[ ]:


# 2. Main: 실행용 클래스

class Main:
    def __init__(self):
        print("실행용 클래스이다")

        # ... 코드 생략 ...
        
        #<<<<<
        
        MyObjects.real_event_ha = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", XR_event_handler)
        MyObjects.real_event_ha.ResFileName = "C:/eBEST/xingAPI/Res/HA_.res"
        for shcode in MyObjects.code_list:
            print("호가잔량 종목 등록 %s" % shcode)
            MyObjects.real_event_ha.SetFieldData("InBlock", "shcode", shcode)
            MyObjects.real_event_ha.AdviseRealData()
    
        #<<<<<
        
        while MyObjects.real_ok is False:
            pythoncom.PumpWaitingMessages()

        
    # ... 코드 생략 ...


# 데이터를 요청하는 Main 클래스에서 조회 결과 수신 클래스로 XR_event_handler 를 등록했습니다. 따라서, 증권서버에서 요청에 응답하면 XR_event_handler 클래스의 OnReceiveRealData() 함수에서 "HA_" 에 대한 결과를 확인 할 수 있습니다. "code" 변수를 통해 요청했던 데이터를 구분하고 GetFieldData() 함수를 통해 실시간 체결 데이터를 조회 할 수 있게 됩니다. 체결된 종목의 코드를 "shcode" 변수에 저장하고 해당 종목이 "HA_dict" 딕셔너리에 없었던 종목이라면 새로운 Key 값으로 저장 합니다. "HA_dict" 의 Value 값에는 GetFieldData() 함수로 수신한 데이터를 저장합니다.

# In[ ]:


# 3. XR_event_handler: 실시간 데이터 수신 클래스

class XR_event_handler:

    def OnReceiveRealData(self, code):
        
        # ... 코드 생략 ...
        
        #<<<<<
        
        elif code == "HA_":
        
            shcode = self.GetFieldData("OutBlock", "shcode")
        
            if shcode not in MyObjects.HA_dict.keys():
                MyObjects.HA_dict[shcode] = {}
        
            tt = MyObjects.HA_dict[shcode]
            tt["매수호가1"] = int(self.GetFieldData("OutBlock", "bidho1"))
            tt["매수호가2"] = int(self.GetFieldData("OutBlock", "bidho2"))
            tt["매수호가3"] = int(self.GetFieldData("OutBlock", "bidho3"))
        
            tt["매도호가1"] = int(self.GetFieldData("OutBlock", "offerho1"))
            tt["매도호가2"] = int(self.GetFieldData("OutBlock", "offerho2"))


# 아래 전체 코드를 실행 시키고 체결 및 호가 요청 결과를 확인 합니다. 

# In[ ]:


'''
실시간 데이터 받아오기
'''

import win32com.client
import pythoncom
import time
import threading
import pandas as pd


# 앞으로 사용하게 될 변수들을 모아 놓는다.
class MyObjects:
    server = "demo" # hts:실투자, demo: 모의투자
    tr_ok = False # TR요청
    real_ok = False # 실시간 요청
    acc_num = "55500489801" # 계좌번호
    acc_pw = "E50330#" # 계좌비밀번호

    code_list = [] # 추천종목 코드 리스트
    t0424_dict = {} # 잔고내역2 종목들 모아 놓은 딕셔너리
    K3_dict = {} # 종목의 체결정보들 모아 놓은 딕셔너리
    HA_dict = {} # 종목의 호가잔량을 모아 놓은 딕셔너리
    

    ####### 요청 함수 모음
    tr_event = None # TR요청에 대한 API 정보
    real_event = None # 실시간 요청에 대한 API 정보
    real_event_ha = None # 실시간 요청에 대한 API 정보

    t8412_request = None # 차트데이터 조회 요청함수
    t0424_request = None # 잔고내역2 조회 요청함수
    ##################


# 실시간으로 수신받는 데이터를 다루는 구간
class XR_event_handler:

    def OnReceiveRealData(self, code):
        
        #<<<<<
        
        if code == "K3_":

            shcode = self.GetFieldData("OutBlock", "shcode")

            if shcode not in MyObjects.K3_dict.keys():
                MyObjects.K3_dict[shcode] = {}

            tt = MyObjects.K3_dict[shcode]
            tt["체결시간"] = self.GetFieldData("OutBlock", "chetime")
            tt["등락율"] = float(self.GetFieldData("OutBlock", "drate"))
            tt["현재가"] = int(self.GetFieldData("OutBlock", "price"))
            tt["시가"] = int(self.GetFieldData("OutBlock", "open"))
            tt["고가"] = int(self.GetFieldData("OutBlock", "high"))
            tt["저가"] = int(self.GetFieldData("OutBlock", "low"))
            tt["누적거래량"] = int(self.GetFieldData("OutBlock", "volume"))
            tt["매도호가"]= int(self.GetFieldData("OutBlock", "offerho"))
            tt["매수호가"] = int(self.GetFieldData("OutBlock", "bidho"))
            
            # 실시간 데이터 수신 성공 여부 확인을 위한 코드
            if shcode in MyObjects.HA_dict.keys()                     and MyObjects.HA_dict[shcode]["매수호가1"] > 0                         and MyObjects.HA_dict[shcode]["매도호가1"] >0                             and tt["현재가"] < 10000 :
            
                print("체결 및 호가 데이터 수신 성공: %s, 체결시간: %s" % (shcode, tt["체결시간"]), flush=True)
            
        elif code == "HA_":
        
            shcode = self.GetFieldData("OutBlock", "shcode")
        
            if shcode not in MyObjects.HA_dict.keys():
                MyObjects.HA_dict[shcode] = {}
        
            tt = MyObjects.HA_dict[shcode]
            tt["매수호가1"] = int(self.GetFieldData("OutBlock", "bidho1"))
            tt["매수호가2"] = int(self.GetFieldData("OutBlock", "bidho2"))
            tt["매도호가1"] = int(self.GetFieldData("OutBlock", "offerho1"))
            tt["매도호가2"] = int(self.GetFieldData("OutBlock", "offerho2"))
        
        #<<<<<

# TR 요청 이후 수신결과 데이터를 다루는 구간
class XQ_event_handler:

    def OnReceiveData(self, code):
        print("%s 수신" % code, flush=True)

        if code == "t0424":

            cts_expcode = self.GetFieldData("t0424OutBlock", "cts_expcode", 0)

            MyObjects.t0424_dict.clear()
            occurs_count = self.GetBlockCount("t0424OutBlock1")
            for i in range(occurs_count):
                expcode = self.GetFieldData("t0424OutBlock1", "expcode", i)

                if expcode not in MyObjects.t0424_dict.keys():
                    MyObjects.t0424_dict[expcode] = {}

                tt = MyObjects.t0424_dict[expcode]
                tt["잔고수량"] = int(self.GetFieldData("t0424OutBlock1", "janqty", i))
                tt["매도가능수량"] = int(self.GetFieldData("t0424OutBlock1", "mdposqt", i))
                tt["평균단가"] = int(self.GetFieldData("t0424OutBlock1", "pamt", i))
                tt["종목명"] = self.GetFieldData("t0424OutBlock1", "hname", i)
                tt["종목구분"] = self.GetFieldData("t0424OutBlock1", "jonggb", i)
                tt["수익률"] = float(self.GetFieldData("t0424OutBlock1", "sunikrt", i))

            print("잔고내역 %s" % MyObjects.t0424_dict, flush=True)
           
            # 과거 데이터를 더 가져오고 싶을 때는 연속조회를 해야한다.
            if self.IsNext is True: #< 과거 데이터가 더 존재한다.
                MyObjects.t0424_request(cts_expcode=cts_expcode, next=self.IsNext) 
            elif self.IsNext is False: 
                MyObjects.tr_ok = True 
            

    def OnReceiveMessage(self, systemError, messageCode, message):
        print("systemError: %s, messageCode: %s, message: %s" % (systemError, messageCode, message), flush=True)

        
# 서버접속 및 로그인 요청 이후 수신결과 데이터를 다루는 구간
class XS_event_handler:

    def OnLogin(self, szCode, szMsg):
        print("%s %s" % (szCode, szMsg), flush=True)
        if szCode == "0000":
            MyObjects.tr_ok = True
        else:
            MyObjects.tr_ok = False

            
# 실행용 클래스
class Main:
    def __init__(self):
        print("실행용 클래스이다")

        # 임의의 추천종목 리스트
        MyObjects.code_list = ['297890','051160','241520']

        session = win32com.client.DispatchWithEvents("XA_Session.XASession", XS_event_handler)
        session.ConnectServer(MyObjects.server + ".ebestsec.co.kr", 20001) # 서버 연결
        session.Login('kwangjae', 'E50330#', '', 0, False)
        # session.Login(아이디, 비밀번호, 공인인증서, 0, False) # 서버 연결

        while MyObjects.tr_ok is False:
            pythoncom.PumpWaitingMessages()
        
        MyObjects.tr_event = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XQ_event_handler)
        MyObjects.tr_event.ResFileName = "C:/eBEST/xingAPI/Res/t0424.res"
        MyObjects.t0424_request = self.t0424_request
        MyObjects.t0424_request(cts_expcode="", next=False)
        
        #<<<<<
        
        MyObjects.real_event = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", XR_event_handler)
        MyObjects.real_event.ResFileName = "C:/eBEST/xingAPI/Res/K3_.res"
        for shcode in MyObjects.code_list:
            print("체결정보 종목 등록 %s" % shcode)
            MyObjects.real_event.SetFieldData("InBlock", "shcode", shcode)
            MyObjects.real_event.AdviseRealData()
        
        MyObjects.real_event_ha = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", XR_event_handler)
        MyObjects.real_event_ha.ResFileName = "C:/eBEST/xingAPI/Res/HA_.res"
        for shcode in MyObjects.code_list:
            print("호가잔량 종목 등록 %s" % shcode)
            MyObjects.real_event_ha.SetFieldData("InBlock", "shcode", shcode)
            MyObjects.real_event_ha.AdviseRealData()
        
        #<<<<<
        
        while MyObjects.real_ok is False:
            pythoncom.PumpWaitingMessages()

        
    def t0424_request(self, cts_expcode=None, next=None):

        time.sleep(1.1)

        MyObjects.tr_event.SetFieldData("t0424InBlock", "accno", 0, MyObjects.acc_num)
        MyObjects.tr_event.SetFieldData("t0424InBlock", "passwd", 0, MyObjects.acc_pw)
        MyObjects.tr_event.SetFieldData("t0424InBlock", "prcgb", 0, "1")
        MyObjects.tr_event.SetFieldData("t0424InBlock", "chegb", 0, "2")
        MyObjects.tr_event.SetFieldData("t0424InBlock", "dangb", 0, "0")
        MyObjects.tr_event.SetFieldData("t0424InBlock", "charge", 0, "1")
        MyObjects.tr_event.SetFieldData("t0424InBlock", "cts_expcode", 0, "")

        MyObjects.tr_event.Request(next)

        MyObjects.tr_ok = False
        while MyObjects.tr_ok is False:
            pythoncom.PumpWaitingMessages()


if __name__ == "__main__":
    Main()

