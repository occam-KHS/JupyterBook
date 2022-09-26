#!/usr/bin/env python
# coding: utf-8

# ### 파이썬 패키징
# 
# 'selection.py' 와 'trading.py' 파이썬 파일을 생성하고 두 모듈을 import 합니다. 아래와 같이 'main.py' 에 최근 영업일 입력한 후, 프로그램을 실행시킵니다. 8장에서도 설명드린 바와 같이 'gam.pkl' 는 예측모델이 저장된 파일이고 'kosdaq_list.pkl' 은 코스닥 종목 리스트가 있는 파일입니다. 프로그램이 추천종목을 받아, 자동매매를 시작하는 지 우선적으로 테스트 해 봅니다. 두 파일은 깃허브 chapter 9 에서 찾으실 수 있습니다. 깃허브 주소 - https://github.com/occam-KHS/JupyterBook/tree/master/chapter9

# ![GET_IMAGE](images/main_py.PNG)

# 참고로 별도의 가상환경 설정없이 주피터노트북으로 알고리즘을 만들었으므로, 아나콘다 Base 에 라이브러리가 모두 설치되어 있습니다. 아나콘다 base 를 아래와 같이 인터프리터로 설정해서 필요한 라이브러리를 모두 활용할 수 있도록 합니다. 

# ![GET_IMAGE](images/interpreter.PNG)

# <br>
# 본서에서 구현된 알고리즘에서 자동매매를 실행하는 날과 추천 종목을 받은 날은 서로 다릅니다. 예를 들어 2022년 9월 26일(월요일) 자동매매를 실행하려면, 매매할 추천종목은 전 주 금요일(2022년 9월 23일) 로 조회를 해야 합니다. 또한 긴 연휴가 있을 수 있으므로 전 영업일을 알아내는 로직이 필요할 것으로 생각이 됩니다. 삼성전자의 일봉을 매매일까지 추출하면, 마지막에서 2 번 째 레코드가 전 영업일이 됩니다. 코드로 간단하게 구현해보겠습니다. 아래와 같이 오늘이 2022년 9월 26일이면 직전 영업일은 2022년 9월 23일이 됩니다. 

# In[27]:


import FinanceDataReader as fdr
import datetime
today_dt = datetime.datetime.today().strftime('%Y-%m-%d')
prev_dt = fdr.DataReader('005930', end = today_dt).index[-2].strftime('%Y-%m-%d')


# In[28]:


print(f' 자동매매 일: {today_dt}')
print(f' 전 영업일: {prev_dt}')

