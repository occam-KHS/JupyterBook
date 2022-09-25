#!/usr/bin/env python
# coding: utf-8

# ## 자동 로그인

# xingAPI 를 사용하면 자동으로 서버연결 및 로그인을 수행 할 수 있습니다. 다음과 같은 순서로 코드를 살펴 보겠습니다. 
# <ol>
#   <li>변수를 관리하는 MyObjects 클래스</li>
#   <li>데이터를 요청하는 Main 클래스</li>
#   <li>로그인 결과를 수신하는 XS_event_handler 클래스</li>
# </ol>

# MyObjects 클래스에서 추가된 변수는 2개 입니다.
# 
# | 추가변수 | 정의 |
# | :----- | :----- |
# | server | 실투자 혹은 모의투자 서버 선택 변수 |
# | login_ok | 로그인 상태를 나타내는 불 타입 변수 |

# In[ ]:


# 1. MyObjects: 변수관리 클래스 

class MyObjects:
    server = "demo" #< hts:실투자, demo: 모의투자
    login_ok = False #< login 여부를 확인하는 불 타입 변수


# Main 클래스에서는 로그인 결과를 수신 할 XS_event_handler 클래스를 등록하고, 서버 연결을 시도하는 ConnectServer() 함수를 호출 합니다. ConnectServer() 함수는 MyObjects 클래스에서 선언한 "server" 변수로 서버 타입을 정합니다. 서버 연결 후, Login() 함수를 호출하여 로그인을 시도합니다. 로그인이 완료될 때까지 while 루프로 대기 하는데, MyObjects 클래스에서 선언한 "login_ok" 변수 값을 기준으로 삼습니다.

# In[ ]:


# 2. Main: 데이터 요청 클래스

class Main:
    def __init__(self):
        print("자동 로그인을 시도합니다")

        session = win32com.client.DispatchWithEvents("XA_Session.XASession", XS_event_handler) #<
        session.ConnectServer(MyObjects.server + ".ebestsec.co.kr", 20001) # 서버 연결
        session.Login(아이디, 비밀번호, 공인인증, 0, False) # 로그인 정보 입력

        while MyObjects.login_ok is False: # 로그인 결과를 기다리는 루프
            pythoncom.PumpWaitingMessages() 


# 모의투자 서버에서 API 사용법을 익히기 위해 MyObjects.server 변수의 값은 'demo' 로 저장했으나, 실투자 서버 사용을 원할 경우엔 'hts' 로 변수 값을 저장하면 됩니다. 한편, 로그인 결과를 알기위해 MyObjects.login_ok 변수의 기본 값은 'False'로 저장하였고, 로그인 결과 메시지를 XS_event_handler 로 받으면 'True' 로 변경하여 위 코드의 while 문을 빠져 나옵니다.

# 다음은 로그인 결과 메시지를 받기 위한 XS_event_handler 클래스 입니다. 로그인에 성공하면 증권서버는 szCode 변수에 "0000" 값을 반환합니다. 로그인에 성공하였으므로 MyObjects.login_ok 의 값을 'True' 로 변환 합니다. 반면, 로그인이 실패 시, 'False' 값을 유지 합니다.

# In[ ]:


# 3. XS_event_handler: 로그인 결과 수신 클래스

class XS_event_handler:

    def OnLogin(self, szCode, szMsg):
        print("%s %s" % (szCode, szMsg), flush=True)
        if szCode == "0000": # 로그인 성공
            MyObjects.login_ok = True
        else: # 로그인 실패
            MyObjects.login_ok = False


# 모의투자 서버 접속 시, 공동인증은 필요 없습니다. 아래 전체 코드를 실행 시키고 로그인 결과를 확인 합니다. 

# In[1]:


import win32com.client #<
import pythoncom #<

'''
로그인 하기
'''

# 앞으로 사용하게 될 변수들을 모아 놓는다.
class MyObjects:
    server = "demo" #< hts:실투자, demo: 모의투자
    login_ok = False #<


# 서버접속 및 로그인 요청 이후 수신결과 데이터를 다루는 구간
class XS_event_handler:

    def OnLogin(self, szCode, szMsg): 
        print("%s %s" % (szCode, szMsg), flush=True) 
        if szCode == "0000": 
            MyObjects.login_ok = True 
        else: 
            MyObjects.login_ok = False 

# 실행용 클래스
class Main:
    def __init__(self):
        print("자동 로그인을 시도합니다")

        session = win32com.client.DispatchWithEvents("XA_Session.XASession", XS_event_handler) #<
        session.ConnectServer(MyObjects.server + ".ebestsec.co.kr", 20001) #< 서버 연결
        session.Login(아이디, 비밀번호, '', 0, False) #< 서버 연결

        while MyObjects.login_ok is False: #<
            pythoncom.PumpWaitingMessages() #<

if __name__ == "__main__":
    Main()

