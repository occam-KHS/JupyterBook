#!/usr/bin/env python
# coding: utf-8

# ### 변동성 돌파전략 2
# 
# 외부 데이터를 이용하여 윌리암스의 변동성 돌파전략을 개선해보겠습니다.

# ### 주가지수 데이터로 전략 개선
# 변동성 돌파전략은 시장이 좋을 때 활용하면 효과가 더 좋을 것 같습니다. 아무래도 상승장에서는 전일의 변동성을 돌파할 올라갈 확률이 높지 않을까요? 코스피 주가지수 데이터를 불러와서, 전일 코스피 주가지수의 수익율(종가 기준) 2%이상 발생한 경우만 매수를  하면 어떤 결과가 나오는 지 테스트 해 보겠습니다. 매수일을 기준으로 2% 수익률이상으로 하면 더 좋을 것 같으나, 매수일의 종가 기준 수익율은 알 수 가 없기 때문에 전일을 기준으로 합니다. 먼저 지수데이터를 가져와서 종가 수익율을 계산합니다.

# In[6]:


import FinanceDataReader as fdr 
import pandas as pd

kospi_index = fdr.DataReader('KS11',  start='2021-01-03', end='2021-12-31') 
kospi_index['kospi_return'] = kospi_index['Close']/kospi_index['Close'].shift(1)
kospi_index.to_pickle('kospi_index.pkl')


# <br>
# 지수 데이터는 위에서서 같이 FinanceDataReader 로 획득이 가능하지만, 야후 파이낸스 라이브러리를 이용하여 다운로드도 가능합니다. 아나콘다 Prompt 에서 pip install yfinance 라고 적어서 설치할 수 도 있고, 쥬피터 노트북상에서는 !pip install yfinance 로 설치할 수 있습니다. 주피터 노트북 설치 코드에는 앞에 느낌표가 있는 것을 유의하세요. 저는 아나콘다 prompt 에서 설치를 선호합니다. 아나콘다 Prompt 에서는 설치 과정을 보여주기 때문에, 설치가 안 되면 어떤 문제가 있는 지도 알 수 있습니다.
# 
# ```python
# (주피터노트북 상에 설치할 경우) !pip install yfinance
# 그리고 yfinance 를 yf 이름으로 import 합니다.
# ```

# In[7]:


import yfinance as yf
import pandas as pd

kospi_index =  yf.download('^KS11', start = '2021-01-03', end = '2021-12-31') # 코스피
kosdaq_index =  yf.download('^KQ11', start = '2021-01-03', end = '2021-12-31') # 코스닥 

kospi_index['kospi_return'] = kospi_index['Close']/kospi_index['Close'].shift(1)


# 지수 데이터를 이용하면, 조건이 추가되므로 매수할 기회가 적어집니다. 지수데이터를 이용함으로써 예상수익율(일)이 0.3% 에서 1.6% 으로 올라갔습니다. 예상 최저수익율도 올라가서 리스크를 상당히 줄일 수 가 있습니다. 단, 매수 횟 수가 낮아 누적 수익율도 낮아졌습니다. 

# In[9]:


kospi_index = pd.read_pickle('kospi_index.pkl')
kospi_list = pd.read_pickle('kospi_list.pkl')

def avg_return(code, K, deci):
    
    stock = fdr.DataReader(code, start='2021-01-03', end='2021-12-31')       
    stock_data = stock.merge(kospi_index['kospi_return'], left_index=True, right_index=True, how='inner')
    stock_data['v'] = (stock_data['High'].shift(1) - stock_data['Low'].shift(1))*K
    stock_data['buy_price'] = stock_data['Open'] + stock_data['v']
    stock_data.dropna(inplace=True) # shift함수 이용으로 생긴 빈 셀 제거
    
    if deci == 1: # 지수 데이터를 이용한 경우
        stock_data['buy'] = (stock_data['High'] > stock_data['buy_price'])*(stock_data['Low'] < stock_data['buy_price'])*(stock_data['kospi_return'].shift(1) > 1.02).astype(int)
        
    else: # 지수 데이터를 이용하지 않은 경우 
        stock_data['buy'] = (stock_data['High'] > stock_data['buy_price'])*(stock_data['Low'] < stock_data['buy_price']).astype(int)
        
    stock_data['return'] = stock_data['Open'].shift(-1)/stock_data['buy_price']
    
    n = len(stock_data[stock_data['buy']==1])
    r = stock_data[stock_data['buy']==1]['return'].mean()
    w = stock_data[stock_data['buy']==1]['return'].min()
    c = stock_data[stock_data['buy']==1]['return'].prod()
    return n, r, w, c


print('------------- 지수 데이터를 이용하지 않은 경우 ---------------')
symbol_list = []
name_list = []
obs_list = []
return_list = []
worst_list = []
cumul_list = []

for code, name in zip(kospi_list['code'],  kospi_list['name']):
    n, r, w, c = avg_return(code, 0.5, 0)
    
    if (r > 0) and (n > 0):  # 수익율 값이 존재하고, 최소한 한번 이상 거래일 존재해야 진행
        symbol_list.append(code)
        name_list.append(name)
        obs_list.append(n)  # 매수 횟 수
        return_list.append(r)    
        worst_list.append(w)
        cumul_list.append(c)
        
    else:
        continue
    
outcome_0 = pd.DataFrame({'symbol': symbol_list, 'name': name_list, 'num_obs': obs_list, 'return': return_list, 'worst': worst_list, 'cumul': cumul_list})
print(outcome_0[['num_obs','return','worst','cumul']].describe())

print('\n')
print('------------- 지수 데이터를 이용한 경우 ---------------')
symbol_list = []
name_list = []
obs_list = []
return_list = []
worst_list = []
cumul_list = []

for code, name in zip(kospi_list['code'][:50],  kospi_list['name'][:50]):
    n, r, w, c = avg_return(code, 0.5, 1)    
   
    if (r > 0) and (n > 0) :  # 수익율 값이 존재하고, 최소한 한번 이상 거래일 존재해야 진행
        symbol_list.append(code)
        name_list.append(name)
        obs_list.append(n) # 매수 횟 수
        return_list.append(r)    
        worst_list.append(w)
        cumul_list.append(c)
        
    else:
        continue
    
outcome_1 = pd.DataFrame({'symbol': symbol_list, 'name': name_list,  'num_obs': obs_list, 'return': return_list, 'worst': worst_list, 'cumul': cumul_list})  
print(outcome_1[['num_obs','return','worst','cumul']].describe())


# In[ ]:




