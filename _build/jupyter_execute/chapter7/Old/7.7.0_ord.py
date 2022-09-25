#!/usr/bin/env python
# coding: utf-8

# ## 자동으로 주문넣기

# 이번 절에는 매수와 매도 주문을 넣는 방법에 대해서 살펴 보겠습니다. 매수와 매도 모두 같은 요청 함수를 사용 합니다. 주문 요청 함수의 매개변수를 통해서 매수/매도를 구분하게 됩니다. 앞 절과 마찬가지로 다음과 같은 순서로 코드를 살펴 보겠습니다.
# <ol>
#   <li>변수를 관리하는 MyObjects 클래스</li>
#   <li>데이터를 요청하는 Main 클래스</li>
#   <li>데이터를 수신하는 XQ_event_handler 클래스</li>
# </ol>

# MyObjects 클래스에서 추가된 변수는 1개 입니다.
# 
# | 추가변수 | 정의 |
# | :----- | :----- |
# | CSPAT00600_request | 신규 주문 요청함수 저장 변수 |

# In[ ]:


# 1. MyObjects: 변수관리 클래스 

class MyObjects:
    server = "demo" # hts:실투자, demo: 모의투자
    tr_ok = False # TR요청
    real_ok = False # 실시간 요청
    acc_num = 계좌번호 # 계좌번호
    acc_pw = 계좌비밀번호 # 계좌비밀번호

    ########################################
    # 추천종목 및 지정가
    t0424_dict = {} # 잔고내역2 종목들 모아 놓은 딕셔너리
    K3_dict = {} # 종목의 체결정보들 모아 놓은 딕셔너리
    HA_dict = {} # 종목의 호가잔량을 모아 놓은 딕셔너리

    ####### 요청 함수 모음
    tr_event = None # TR요청에 대한 API 정보
    real_event = None # 실시간 요청에 대한 API 정보
    real_event_ha = None # 실시간 요청에 대한 API 정보
    
    t0424_request = None # 잔고내역2 조회 요청함수
    CSPAT00600_request = None #< 신규주문 요청함수
    ##################


# Main 클래스에서는 주문 요청 결과를 수신 할 XQ_event_handler 클래스를 등록하고, 신규 주문을 넣는 "CSPAT00600" Res 파일을 등록합니다. CSPAT00600_request() 주문 함수는 계좌번호, 계좌비밀번호, 종목번호, 주문수량, 매수/매도 구분 그리고 호가유형코드를 SetFieldData() 함수를 통해 설정해야 합니다. 특별히 대출을 받아서 투자를 하거나 특정 조건으로 주문을 넣지 않는 경우에는 아래 코드와 같이 신용거래코드는 "000", 대출일은 "", 주문조건구분은 "0" 값을 지정합니다.

# In[ ]:


# 2. Main: 실행용 클래스


class Main:
    def __init__(self):
        print("실행용 클래스이다")

        # ... 코드 생략 ...
        
        #<<<<<
        
        MyObjects.CSPAT00600_event = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XQ_event_handler)
        MyObjects.CSPAT00600_event.ResFileName = "C:/eBEST/xingAPI/Res/CSPAT00600.res"
        MyObjects.CSPAT00600_request = self.CSPAT00600_request
    
        #<<<<<
        
        # ... 코드 생략 ...
        
    # ... 코드 생략 ...
    
    def CSPAT00600_request(self, AcntNo=None, InptPwd=None, IsuNo=None, OrdQty=0, BnsTpCode=None):

        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "AcntNo", 0, AcntNo) # 계좌번호
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "InptPwd", 0, InptPwd) # 계좌번호 비밀번호

        if MyObjects.server == "demo":
            IsuNo = "A"+IsuNo

        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "IsuNo", 0, IsuNo) # 종목번호
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "OrdQty", 0, OrdQty) # 주문수량
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "OrdPrc", 0, 0) # 주문가
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "BnsTpCode", 0, BnsTpCode) # 1:매도, 2:매수
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "OrdprcPtnCode", 0, "03") # 호가유형코드, 03:시장가
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "MgntrnCode", 0, "000") # 신용거래코드, 000:보통
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "LoanDt", 0, "") # 대출일
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "OrdCndiTpCode", 0, "0") # 주문조건구분 0:없음, 1:IOC, 2:FOK


# XQ_event_handler 클래스는 주문 결과 메시지를 수신 받는 곳이기 때문에 CSPAT00600_request() 함수를 사용하지 않습니다. 주문 요청은 체결 및 호가 데이터를 조합한 조건식과 함께 사용되는 경우가 많습니다. 따라서, XR_event_handler 클래스에서 주문 요청을 진행 하겠습니다.

# In[ ]:


# 3. TR 요청 이후 수신결과 데이터를 다루는 구간

class XQ_event_handler:

    def OnReceiveData(self, code):
        print("%s 수신" % code, flush=True)
        
    def OnReceiveMessage(self, systemError, messageCode, message):
        print("systemError: %s, messageCode: %s, message: %s" % (systemError, messageCode, message), flush=True)


# In[ ]:


# 3. XR_event_handler: 실시간 데이터 수신 클래스
## 실시간 정보를 활용한 주문 요청

class XR_event_handler:

    def OnReceiveRealData(self, code):

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
            if shcode in MyObjects.HA_dict.keys()                     and MyObjects.HA_dict[shcode]["매수호가1"] > 0                         and MyObjects.HA_dict[shcode]["매도호가1"] >0                             and tt["현재가"] < 10000                                 and shcode not in MyObjects.t0424_dict.keys():
            

                print(f'매수 종목: {shcode}')
                MyObjects.CSPAT00600_request(AcntNo=MyObjects.acc_num, InptPwd=MyObjects.acc_pw, IsuNo=shcode, OrdQty=5,  BnsTpCode="2", OrdprcPtnCode="03")

            # 매도
            if shcode in MyObjects.t0424_dict.keys():
                earning_rate = MyObjects.t0424_dict[shcode]["수익률"]
                qty = MyObjects.t0424_dict[shcode]["매도가능수량"]
                if earning_rate > 5.0 or earning_rate < -6.0:
                    MyObjects.CSPAT00600_request(AcntNo=MyObjects.acc_num, InptPwd=MyObjects.acc_pw, IsuNo=medo_shcode, OrdQty=qty, BnsTpCode="1", OrdprcPtnCode="03")
            
            #<<<<<


# 아래 전체 코드를 실행 시키고 체결 및 호가 요청 결과를 확인 합니다. 

# In[ ]:


'''
매수/매도 주문 넣기
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

    t0424_request = None # 잔고내역2 조회 요청함수
    CSPAT00600_request = None # 신규주문 요청함수
    ##################


# 실시간으로 수신받는 데이터를 다루는 구간
class XR_event_handler:

    def OnReceiveRealData(self, code):

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
            
            # 매수
            if shcode in MyObjects.HA_dict.keys()                     and MyObjects.HA_dict[shcode]["매수호가1"] > 0                         and MyObjects.HA_dict[shcode]["매도호가1"] >0                             and tt["현재가"] < 100000                                 and shcode not in MyObjects.t0424_dict.keys():
            

                print(f'매수 종목: {shcode}')
                MyObjects.CSPAT00600_request(AcntNo=MyObjects.acc_num, InptPwd=MyObjects.acc_pw, IsuNo=shcode, OrdQty=1,  BnsTpCode="2", OrdprcPtnCode="03")

            #<<<<<
            
        elif code == "HA_":
        
            shcode = self.GetFieldData("OutBlock", "shcode")
        
            if shcode not in MyObjects.HA_dict.keys():
                MyObjects.HA_dict[shcode] = {}
        
            tt = MyObjects.HA_dict[shcode]
            tt["매수호가1"] = int(self.GetFieldData("OutBlock", "bidho1"))
            tt["매수호가2"] = int(self.GetFieldData("OutBlock", "bidho2"))
            tt["매도호가1"] = int(self.GetFieldData("OutBlock", "offerho1"))
            tt["매도호가2"] = int(self.GetFieldData("OutBlock", "offerho2"))


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
            # if self.IsNext is True: # 과거 데이터가 더 존재한다.
                # MyObjects.t0424_request(cts_expcode=cts_expcode, next=self.IsNext)
            # elif self.IsNext is False:

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
        
        # 임의의 추천종목 리스트
        MyObjects.code_list = ['002680','048530','013720']

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
        
        MyObjects.CSPAT00600_event = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XQ_event_handler)
        MyObjects.CSPAT00600_event.ResFileName = "C:/eBEST/xingAPI/Res/CSPAT00600.res"
        MyObjects.CSPAT00600_request = self.CSPAT00600_request

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

        self.t0424_loop()

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
    
    #<<<<<
    
    def CSPAT00600_request(self, AcntNo=None, InptPwd=None, IsuNo=None, OrdQty=0, OrdPrc=0, OrdprcPtnCode="", BnsTpCode=None):

        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "AcntNo", 0, AcntNo) # 계좌번호
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "InptPwd", 0, InptPwd) # 비밀번호

        if MyObjects.server == "demo":
            IsuNo = "A"+IsuNo

        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "IsuNo", 0, IsuNo) # 종목번호
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "OrdQty", 0, OrdQty) # 주문수량
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "OrdPrc", 0, OrdPrc) # 주문가
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "BnsTpCode", 0, BnsTpCode) # 1:매도, 2:매수
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "OrdprcPtnCode", 0, OrdprcPtnCode) # 호가유형코드, 00:지정가, 03:시장가
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "MgntrnCode", 0, "000") # 신용거래코드, 000:보통
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "LoanDt", 0, "") # 대출일
        MyObjects.CSPAT00600_event.SetFieldData("CSPAT00600InBlock1", "OrdCndiTpCode", 0, "0") # 주문조건구분 0:없음, 1:IOC, 2:FOK

        err = MyObjects.CSPAT00600_event.Request(False)
        if err < 0:
            print("\nXXXXXXXXXXXXXXX "
                             "\nCSPAT00600 주문에러"
                             "\n계좌번호: {0}"
                             "\n종목코드: {1}"
                             "\n주문수량: {2}"
                             "\n매매구분: {3}"
                             "\n주문에러: {4}"
                             "\n\n".format(AcntNo, IsuNo, OrdQty, BnsTpCode, err), flush=True)

        else:
            print("\n============="
                             "\nCSPAT00600 주문 실행"
                             "\n계좌번호: {0}"
                             "\n종목코드: {1}"
                             "\n주문수량: {2}"
                             "\n매매구분: {3}"
                             "\n주문에러: {4}"
                             "\n\n".format(AcntNo, IsuNo, OrdQty, BnsTpCode, err), flush=True)
    
    #<<<<<
    
    def t0424_loop(self):

        MyObjects.t0424_request(cts_expcode="", next=False)
        
        #<<<<<
        
        # 매도
        for medo_shcode in MyObjects.t0424_dict.keys():
            earning_rate = MyObjects.t0424_dict[medo_shcode]["수익률"]
            qty = MyObjects.t0424_dict[medo_shcode]["매도가능수량"]
                
            if earning_rate > 1.0 or earning_rate < -1.0:
                MyObjects.CSPAT00600_request(AcntNo=MyObjects.acc_num, InptPwd=MyObjects.acc_pw, IsuNo=medo_shcode, OrdQty=qty, BnsTpCode="1", OrdprcPtnCode="03")
            
        #<<<<<
        
        threading.Timer(10, self.t0424_loop).start()


if __name__ == "__main__":
    Main()
    

