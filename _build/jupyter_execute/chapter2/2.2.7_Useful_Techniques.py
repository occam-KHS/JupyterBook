#!/usr/bin/env python
# coding: utf-8

# ### Rolling
# 주식을 하신 분들은 이동평균선에 대하여 많이 들어보셨을 것이라고 생각합니다. rolling 은 이동평균선을 간단하게 만들어줄 수 있는 메소드입니다. 예제를 보시면 금방 이해가 되 실 것이라고 생각합니다. 일단 삼성전자 일봉을 가져오겠습니다.

# In[1]:


import FinanceDataReader as fdr 

code = '005930' # 삼성전자
stock_data = fdr.DataReader(code, start='2021-01-03', end='2021-12-31') 

stock_data.head()


# <br>
# 일봉의 종가에 대하여 5 일 이동평균선을 만들어 '5 day moving average' 라는 이름의 컬럼에 담았습니다. rolling(5) 은 5 개 row 로 만들어진 창(window) 을 한 단계씩 진행하라는 뜻이고, mean() 을 한 이유는 각 창의 평균값을 구하라는 뜻입니다. 처음 4개의 row 에는 5 일의 창이 만들어지지 않으므로 'NaN'(값 없음) 이 되고 처음으로 시작하는 '5 day moving average' 값은 2021년 1월 8일부터 시작하게 됩니다. 2021년 1월 8일의 5일 이동평균선 값 84,160 은 1월 4일 ~ 1월 8일까지 5일 종가들의 평균값입니다. 

# In[2]:


stock_data['5 day moving average'] = stock_data['Close'].rolling(5).mean()
stock_data.head(6)


# <br>
# 같은 방식으로 20일 이동평균선도 만들어 보겠습니다. 그리고 골든크로스(5일 이동평균선이 20일 이동평균선을 뚫고 올라가는) 지점이 어디 인지도 알아보겠습니다. 5일 이동평균선과 동일하게 20일 이동평균선은 20번째 열부터 존재합니다. 

# In[3]:


stock_data['20 day moving average'] = stock_data['Close'].rolling(20).mean()
stock_data.head(21)


# <br>
# 우선 NaN 으로 표시가 된 값이 없는 모든 열을 제거하고 싶습니다. dropna 라는 메소드도 활용할 것인데요. dropna 를 하면 NaN 가 있는 모든 열을 제거합니다. 제거한 후 자기 자신을 덮어쓰라고 명령하는 것은 inplace=True 라는 인수인데요. 새로운 DataFrame 을 만들지 않고 dropna(inplace=True) 하여 값이 없는 모든 열을 제거한 후, 자기 자신을 덮어쓰도록 하겠습니다.

# In[4]:


stock_data.dropna(inplace=True) # NaN 이 있는 모든 row 제거
stock_data.head()


# <br>
# 이제 5일 이동평균선이 20일 이동평균선보다 작았다가 커지는 지점을 찾으면 됩니다. DataFrame 의 필터링에 대하여는 아직 다루지 않았습니다. 설명을 드리면, df(DataFrame) 에서 원하는 row 를 가져오고 싶을 때는 df[조건] 처럼 대괄호 안에 조건을 넣어 주면 됩니다. 아래에서 stock_data['cross_flag'==1] 은 stock_data 에서 True 인 열과 False 인 열을 구분하는 역할을 합니다.  stock_data['cross_flag'].shift(1)==0 은 전 날의 cross_flag 값이 0 인 경우를 찾는 것인데요. 결국 전날은 cross_flag 값이 0, 당일은 cross_flag 값이 1 날을 찾는 조건이 됩니다. 최종 결과를 보시면 2021년은 3월 3일에 최초 골든크로스가 일어났습니다. 

# In[6]:


stock_data['cross_flag'] = (stock_data['5 day moving average'] > stock_data['20 day moving average']).astype(int) # True/False 결과 값을 1/0 으로 바꿔줌
stock_data[(stock_data['cross_flag'].shift(1)==0) & (stock_data['cross_flag']==1)] # 조건 - 전날에는 5일 이평선이 20일 이평선보다 작거나 같아는데, 당일은 5일 이평선이 20일 이평선 보다 커짐


# In[ ]:




