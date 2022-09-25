#!/usr/bin/env python
# coding: utf-8

# ## 계좌 정보 조회

# 계좌 정보 조회는 매수 가능한 잔액, 매도 가능한 종목별 수량 등을 확인 할 수 있는 유용한 정보를 제공합니다. 다음과 같은 순서로 코드를 살펴 보겠습니다. 
# <ol>
#   <li>변수를 관리하는 MyObjects 클래스</li>
#   <li>데이터를 요청하는 Main 클래스</li>
#   <li>데이터를 수신하는 XQ_event_handler 클래스</li>
# </ol>

# MyObjects 클래스에서 추가된 변수는 2개 입니다.
# 
# | 추가변수 | 정의 |
# | :----- | :----- |
# | t0424_dict | 계좌 잔고내역 저장 딕셔너리 변수 |
# | t0424_request | 잔고내역 조회 요청함수 저장 변수 |

# In[ ]:


# 1. MyObjects: 변수관리 클래스 

class MyObjects:
    server = "demo" # hts:실투자, demo: 모의투자
    tr_ok = False # TR요청
    acc_num = 계좌번호 # 계좌번호
    acc_pw = 계좌비밀번호 # 계좌비밀번호

    t0424_dict = {} #< 잔고내역2 종목들 모아 놓은 딕셔너리

    ####### 요청 함수 모음
    tr_event = None # TR요청에 대한 API 정보
    t0424_request = None #< 잔고내역2 조회 요청함수
    ##################


# Main 클래스에서는 계좌 정보 조회 결과를 수신 할 XQ_event_handler 클래스를 등록하고, TR목록에서 [잔고내역2]에 해당하는 "t0424" Res 파일을 등록합니다. 이어서, 요청함수를 MyObjects 에서 새로 생성한 t0424_request 요청함수에 저장하고 함수를 호출합니다. 요청함수 정의 부분에서는 SetFieldData() 함수를 통해 입력 변수를 입력하고 while 문을 통해 조회 결과를 기다립니다. 

# In[ ]:


# 2. Main: 데이터 요청 클래스

class Main:
    def __init__(self):
        print("실행용 클래스이다")

        # ... 코드 생략 ...
        
        #<<<<<
        
        MyObjects.tr_event = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XQ_event_handler)
        MyObjects.tr_event.ResFileName = "C:/eBEST/xingAPI/Res/t0424.res"
        MyObjects.t0424_request = self.t0424_request
        MyObjects.t0424_request(cts_expcode="", next=False)
        
        #<<<<<
    
    #<<<<<    
    
    def t0424_request(self, cts_expcode=None, next=None): #<

        time.sleep(1.1) #<

        MyObjects.tr_event.SetFieldData("t0424InBlock", "accno", 0, MyObjects.acc_num) 
        MyObjects.tr_event.SetFieldData("t0424InBlock", "passwd", 0, MyObjects.acc_pw) 
        MyObjects.tr_event.SetFieldData("t0424InBlock", "prcgb", 0, "1") 
        MyObjects.tr_event.SetFieldData("t0424InBlock", "chegb", 0, "2") 
        MyObjects.tr_event.SetFieldData("t0424InBlock", "dangb", 0, "0") 
        MyObjects.tr_event.SetFieldData("t0424InBlock", "charge", 0, "1") 
        MyObjects.tr_event.SetFieldData("t0424InBlock", "cts_expcode", 0, cts_expcode) 

        MyObjects.tr_event.Request(next) 

        MyObjects.tr_ok = False 
        while MyObjects.tr_ok is False: 
            pythoncom.PumpWaitingMessages() 
    
    #<<<<<


# 데이터를 요청하는 Main 클래스에서 조회 결과 수신 클래스로 XQ_event_handler 를 등록했습니다. 따라서, 증권서버에서 요청에 응답하면 XQ_event_handler 클래스의 OnReceiveData() 함수를 통해 "t0424"의 결과를 확인 할 수 있습니다. "code" 변수를 통해 요청했던 데이터를 구분하고 GetFieldData() 함수를 통해 계좌 정보를 변수에 저장 및 조회를 할 수 있게 됩니다.

# In[ ]:


# 3. XQ_event_handler: 데이터 수신 클래스

class XQ_event_handler:

    def OnReceiveData(self, code):
        print("%s 수신" % code, flush=True)
        
        #<<<<<
        
        if code == "t0424": 

            cts_expcode = self.GetFieldData("t0424OutBlock", "cts_expcode", 0) 

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

                print("잔고내역 %s" % tt, flush=True)

            # 과거 데이터를 더 가져오고 싶을 때는 연속조회를 해야한다.
            if self.IsNext is True: #< 과거 데이터가 더 존재한다.
                MyObjects.t0424_request(cts_expcode=cts_expcode, next=self.IsNext) 
            elif self.IsNext is False: 
                MyObjects.tr_ok = True 
        
        #<<<<<
    
    def OnReceiveMessage(self, systemError, messageCode, message):
        print("systemError: %s, messageCode: %s, message: %s" % (systemError, messageCode, message), flush=True)


# 아래 전체 코드를 실행하고 계좌 정보 조회 결과를 확인 합니다.

# In[4]:


import win32com.client
import pythoncom
import time

'''
잔고내역 가져오기
'''

# 앞으로 사용하게 될 변수들을 모아 놓는다.
class MyObjects:
    server = "demo" # hts:실투자, demo: 모의투자
    tr_ok = False # TR요청
    acc_num = 계좌번호 #< 계좌번호
    acc_pw = 계좌비밀번호 #< 계좌비밀번호

    t8436_list = [] # 종목코드 모아놓는 리스트
    t0424_dict = {} #< 잔고내역2 종목들 모아 놓은 딕셔너리

    ####### 요청 함수 모음
    tr_event = None # TR요청에 대한 API 정보

    t0424_request = None #< 잔고내역2 조회 요청함수
    ##################


# TR 요청 이후 수신결과 데이터를 다루는 구간
class XQ_event_handler:

    def OnReceiveData(self, code):
        print("%s 수신" % code, flush=True)

        if code == "t0424": 

            cts_expcode = self.GetFieldData("t0424OutBlock", "cts_expcode", 0) 

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

                print("잔고내역 %s" % tt, flush=True)

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

        session = win32com.client.DispatchWithEvents("XA_Session.XASession", XS_event_handler)
        session.ConnectServer(MyObjects.server + ".ebestsec.co.kr", 20001) # 서버 연결
        session.Login(아이디, 비밀번호, 공인인증, 0, False) # 서버 연결

        while MyObjects.tr_ok is False:
            pythoncom.PumpWaitingMessages()

        MyObjects.tr_event = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XQ_event_handler)
        MyObjects.tr_event.ResFileName = "C:/eBEST/xingAPI/Res/t0424.res"
        MyObjects.t0424_request = self.t0424_request
        MyObjects.t0424_request(cts_expcode="", next=False)

    def t0424_request(self, cts_expcode=None, next=None): #<

        time.sleep(1.1) #<

        MyObjects.tr_event.SetFieldData("t0424InBlock", "accno", 0, MyObjects.acc_num) #<
        MyObjects.tr_event.SetFieldData("t0424InBlock", "passwd", 0, MyObjects.acc_pw) #<
        MyObjects.tr_event.SetFieldData("t0424InBlock", "prcgb", 0, "1") #<
        MyObjects.tr_event.SetFieldData("t0424InBlock", "chegb", 0, "2") #<
        MyObjects.tr_event.SetFieldData("t0424InBlock", "dangb", 0, "0") #<
        MyObjects.tr_event.SetFieldData("t0424InBlock", "charge", 0, "1") #<
        MyObjects.tr_event.SetFieldData("t0424InBlock", "cts_expcode", 0, cts_expcode) #<

        MyObjects.tr_event.Request(next) #<

        MyObjects.tr_ok = False #<
        while MyObjects.tr_ok is False: #<
            pythoncom.PumpWaitingMessages() #<

if __name__ == "__main__":
    Main()

