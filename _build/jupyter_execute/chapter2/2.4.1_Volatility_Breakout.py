#!/usr/bin/env python
# coding: utf-8

# ### 변동성 돌파전략 1
# 변동성 돌파전략은 래리 윌리암스가 개발한 전략인데요. 이 전략으로 윌리암스는 주식투자 대회에서 많은 상을 받았다고 하네요. 심지어 딸에게 이 전략을 전수해 주었다고 합니다. 전략은 아주 간단합니다. '전날 고가와 저가의 차'에 상수 K (0.4 ~ 0.6) 를 곱하여 변동성 값 V 를 만듭니다. 그리고 당일 장이 시작하면 시가에 이 변동성 값 V 를 더한 값을 매수 가격으로 설정합니다. 장 중에 매수 가격을 돌파하면 무조건 매수합니다. 그리고 다음날 장 시작할 때 전량 매도하는 전략입니다. 다음 링크는 변동성 돌파전략에 관련하여 참고할만한 블로그 입니다. https://blog.naver.com/niolpa/222436997945 다시 삼성전자 일봉을 가져옵니다.

# In[1]:


import FinanceDataReader as fdr 

code = '005930' # 삼성전자
stock_data = fdr.DataReader(code, start='2021-01-03', end='2021-12-31') 
stock_data.head()


# <br> K = 0.5 라고 하고 전날의 고가와 저가를 이용하여 변동성 값 V 를 구합니다. 그리고 시가를 더하여 매수가격을 만듭니다. shift(1) 은 바로 위에 있는 row 를 참조하게 됩니다. 따라서 전날 데이터가 됩니다.

# In[2]:


K = 0.5
stock_data['v'] = (stock_data['High'].shift(1) - stock_data['Low'].shift(1))*K  # 전날 고가에서 저가를 뺀 값에 K 를 곱함
stock_data['buy_price'] = stock_data['Open'] + stock_data['v']  # 변동성 값 V 에 당일 시가를 더하여 매수가를 만듦


# <br> 만약 당일의 고가가 buy_price 보다 높다면 매수할 기회가 있었을 것입니다. 매수 여부를 'buy' 라는 컬럼에 저장합니다. 그리고 수익율 'return' 을 생성합니다. 수익율은 다음날 시가를 매수가격로 나눈 값이 됩니다.

# In[3]:


stock_data['buy'] = ( stock_data['High']  > stock_data['buy_price']).astype(int) # 매수 기회 있으면 1 아니면 0
stock_data['return'] = stock_data['Open'].shift(-1)/stock_data['buy_price'] # 다음 날 시가를 이용하여 수익율 계산


# <br> 이제 'buy' = 1 인 날의 평균 수익율을 구해봅니다. 0.2% 기대수익율(일) 을 얻을 수 있는 전략입니다. 여기서 기대 수익율이란 매수를 한 날 중 랜덤한 어떤 날의 기대 수익율입니다.

# In[4]:


stock_data.groupby('buy')['return'].mean()


# <br> 다른 종목도 테스트할 수 있게 이 전략을 함수로 만들어 봅니다. 리턴은 평균수익율(일) 과 최대 손실율(일)로 하겠습니다.

# In[5]:


# 위 내용을 모아서 함수로 만듦
def avg_r(code, K):
    stock = fdr.DataReader(code,  start='2021-01-03', end='2021-12-31')    
    stock['v'] = (stock['High'].shift(1) - stock['Low'].shift(1))*K
    stock['buy_price'] = stock['Open'] + stock['v']
    stock['buy'] = ( stock['High']  > stock['buy_price']).astype(int)
    stock['return'] = stock['Open'].shift(-1)/stock['buy_price']
    return stock[stock['buy']==1]['return'].mean(), stock[stock['buy']==1]['return'].min()

a, b = avg_r('005930', 0.5)
print(a, b)

# 참고로 아래와 같이 f-string 이용하여 출력을 이쁘게 할 수 있습니다.
print(f' 평균 수익율: {(a-1):5.2%} 최대 손실: {(1-b):5.2%}')


# 
# <br> 다른 종목의 결과값도 함 보겠습니다. 네이버(035420)와 현대차(005380)를 함 볼까요? 둘 다 삼성전자보다는 좋아보입니다. 네이버가 현대차보다 수익율도 높고, 리스크도 낮습니다.

# In[6]:


a, b = avg_r('035420', 0.5)
print(f'네이버 평균 수익율: {(a-1):5.2%} 최대 손실: {(1-b):5.2%}')

a, b = avg_r('005380', 0.5)
print(f'현대차 평균 수익율: {(a-1):5.2%} 최대 손실: {(1-b):5.2%}')


# <br> 이번에는 누적 수익율도 궁금합니다. 즉, 2021년 1월 3일 100 원을 투자하면 2021년 12월 31일 얼마가 되어 있을까요? 함수의 리턴 값에 누적 수익율을 추가합니다. 

# In[7]:


def avg_r(code, K):
    stock = fdr.DataReader(code,  start='2021-01-03', end='2021-12-31')    
    stock['v'] = (stock['High'].shift(1) - stock['Low'].shift(1))*K
    stock['buy_price'] = stock['Open'] + stock['v']
    stock['buy'] = ( stock['High']  > stock['buy_price']).astype(int)
    stock['return'] = stock['Open'].shift(-1)/stock['buy_price']
    return stock[stock['buy']==1]['return'].mean(), stock[stock['buy']==1]['return'].min(), stock[stock['buy']==1]['return'].prod()

a, b, c = avg_r('005930', 0.5)
print(a, b, c)

# 참고로 아래와 같이 f-string 이용하여 출력을 이쁘게 할 수 있습니다.
print(f' 평균 수익율: {(a-1):5.2%} 최대 손실: {(1-b):5.2%} 누적수익율:{(c-1):5.2%}')


# <br> 네이버의 누적 수익율은 58.2%, 현대차의 누적 수익율은 38.7% 입니다. 즉 2021년 초에 각 각 100 원을 투자했다면 연말에 네이버는 158원, 현대차는 138 원이 되어 있습니다. 실제 장에서는 원하는 가격에 매수 매도를 할 수 없으므로 실전 수익율은 아니겠지만 예상 수익율을 추정해 볼 수 있습니다. 

# In[8]:


a, b, c = avg_r('035420', 0.5)
print(f'네이버 평균 수익율: {(a-1):5.2%} 최대 손실: {(1-b):5.2%} 누적수익율:{(c-1):5.2%}')

a, b, c = avg_r('005380', 0.5)
print(f'현대차 평균 수익율: {(a-1):5.2%} 최대 손실: {(1-b):5.2%} 누적수익율:{(c-1):5.2%}')


# In[ ]:




