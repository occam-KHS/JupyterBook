#!/usr/bin/env python
# coding: utf-8

# In[2]:


import FinanceDataReader as fdr
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.expand_frame_repr', False)


# ### 가설 검증을 위한 데이터 처리
# 앞서 만든 return_all (주가 데이터에 지수데이터가 추가된 파일) 을 아래와 같이 로드하고, Missing Data 는 제거합니다. 
# 

# In[4]:


return_all = pd.read_pickle('return_all.pkl').dropna()  
return_all.index = [datetime.datetime.strftime(dt, '%Y-%m-%d') for dt in return_all.index]


# In[5]:


return_all.head().style.set_table_attributes('style="font-size: 12px"')


# <br>일주일(5영업일)을 수익율의 관찰 기간으로 하고, 관찰 기간 동안 주가 상승이 있으면 저희가 세운 가설들을 유의미한 가설로 판단하겠습니다. 여기서 주가 상승의 기준은  "종가 매수 일부터 다음 5 영업일 동안 최고 종가 수익율" 하겠습니다. 
# 
# 첫 번째 종목 060310 에 대하여 처리를 먼저 해 보겠습니다. df['close'] * shift(-1) 은 다음 영업일의 종가 수익율을 참조하고, df['close']*shift(-2) 은 그 다음의 영업일의 종가 수익율을 참조합니다. 따라서 매수 후 2 영업일 후, 종가 수익율은 { df['close'] * shift(-1) } * { df['close'] * shift(-2) } 로 계산됩니다. 이렇게 1 영업일, 2 영업일, 3 영업일, 4 영업일, 5 영업일 후 종가 수익율을 새로운 컬럼에 생성하고, 그 중에서 가장 큰 수익율을 고르면 됩니다. 생성된 컬럼 중 가장 큰 값은 max(axis=1) 로 찾습니다. 참고로 max() 에서는 axis=0 이 Default 라서 axis=1 로 정해주지 않으면 열에서 가장 큰 값을 찾게 됩니다. 이 부분을 유의해 주세요.

# In[6]:


s = '060310'
df = return_all[return_all['code']==s].sort_index().copy()

df['close_r1'] = df['close'].shift(-1)/df['close'] # 1 일후 종가 수익률
df['close_r2'] = df['close'].shift(-2)/df['close'] # 2 일후 종가 수익률
df['close_r3'] = df['close'].shift(-3)/df['close'] # 3 일후 종가 수익률
df['close_r4'] = df['close'].shift(-4)/df['close'] # 4 일후 종가 수익률
df['close_r5'] = df['close'].shift(-5)/df['close'] # 5 일후 종가 수익률

''' 위 코드와 같은 결과
df['return_1'] = df['return'].shift(-1)
df['return_2'] = df['return'].shift(-2)*df['return'].shift(-1)
df['return_3'] = df['return'].shift(-3)*df['return'].shift(-2)*df['return'].shift(-1)
df['return_4'] = df['return'].shift(-4)*df['return'].shift(-3)*df['return'].shift(-2)*df['return'].shift(-1)
df['return_5'] = df['return'].shift(-5)*df['return'].shift(-4)*df['return'].shift(-3)*df['return'].shift(-2)*df['return'].shift(-1)
'''

df['target'] = df[['close_r1','close_r2','close_r3','close_r4','close_r5']].max(axis=1) # 주어지 컬럼에서 최대 값을 찾고 'target' 에 저장
df.dropna(subset=['close_r1','close_r2','close_r3','close_r4','close_r5'], inplace=True) # 주어진 컬럼 중에 missing 값이 있으면 행을 제거(dropna)하고, 자신을 덮어 씀(inplace=True).


# In[7]:


df.head(10).style.set_table_attributes('style="font-size: 12px"')


# <br>이제 모든 종목에 대하여 For loop 로 매수 종가로 매도 시 수익율을 최대값을 생성합니다. 'max_close' 의 분포를 보니 평균은 1.033, 최소값 0.326, 최대값 3.703 입니다. 단, max_close 는 가설 검정으로 활용할 지표입니다. 매수 후, 몇 번 째 영업일이 최고 수익율인지 알 수 없기 때문에 기간 중 최고 수익율을 이용합니다.

# In[7]:


kosdaq_list = pd.read_pickle('kosdaq_list.pkl')

mdl_data = pd.DataFrame()

for code in kosdaq_list['code']:
    df = return_all[return_all['code']==code].sort_index().copy()

    df['close_r1'] = df['close'].shift(-1)/df['close']
    df['close_r2'] = df['close'].shift(-2)/df['close']
    df['close_r3'] = df['close'].shift(-3)/df['close']
    df['close_r4'] = df['close'].shift(-4)/df['close']
    df['close_r5'] = df['close'].shift(-5)/df['close']

    df['max_close'] = df[['close_r1','close_r2','close_r3','close_r4','close_r5']].max(axis=1) # 주어지 컬럼에서 최대 값을 찾음
    df.dropna(subset=['close_r1','close_r2','close_r3','close_r4','close_r5'], inplace=True) # 주어진 컬럼 중에 missing 값이 있으면 행을 제거(dropna)하고, 자신을 덮어 씀(inplace=True).
    
    mdl_data = pd.concat([mdl_data, df], axis=0)    
    
mdl_data.to_pickle('mdl_data.pkl')


# <br> 'max_close' 의 분포를 확인합니다.

# In[9]:


mdl_data = pd.read_pickle('mdl_data.pkl')
print(mdl_data['max_close'].describe(percentiles=[0.1, 0.2, 0.5, 0.8, 0.9]))


# ### <br> 매도 전략 데이터 프로세싱
# 모델 개발을 위해서는 매도 전략에 따는 수익을 계산을 할 수 있어야 합니다. 이번 장에서는 기본적인 몇 가지 전략의 수익율을 계산해보겠습니다. 저장해 둔 mdl_data pickle 파일을 읽습니다. mdl_data 는 수익률 결과값이 있는 데이터입니다. 
# 

# In[9]:


mdl_data = pd.read_pickle('mdl_data.pkl')


# <br> **매도 전략 1 - 모든 종목 종가 매수 후, 5 영업일 기간 6% 익절 매도**     
# 한가지 전략을 테스트 해 보겠습니다. 모든 종목을 같은 금액으로 매일 종가 매수합니다. 매수 후 5 영업일 동안 수익율이 6% 이상되면 곧바로 익절합니다. 나머지 종목은 5 영업일에 전부 종가 매도하면 수익율은 어떻게 될까요?   

# In[10]:


kosdaq_list = pd.read_pickle('kosdaq_list.pkl')

data_all_5 = pd.DataFrame()

ub = 1.06

for code in kosdaq_list['code']:
    
    # 종목별 처리
    data = mdl_data[mdl_data['code']==code].sort_index().copy()
    
    # 고가, 저가, 종가 수익율
    for i in [1, 2, 3, 4, 5]:

        data['high_r' + str(i)] = data['high'].shift(-1*i)/data['close']      
        data['low_r' + str(i)] = data['low'].shift(-1*i)/data['close']   
        data['close_r' + str(i)] = data['close'].shift(-1*i)/data['close']    
        
    data['max_high']  = (data[['high_r1','high_r2','high_r3','high_r4','high_r5']].max(axis=1) > ub).astype(int) # 5 영업일 최고가 중 최고가         
    data['ub_return'] = np.where(data['max_high']==1, ub, data['close_r5']) # 종가 수익률이 6% 이면 매도, 아니면 마지막 5 영업일 수익률
       
    data.dropna(subset=['close_r1','close_r2','close_r3','close_r4','close_r5'], inplace=True)   
    data_all_5 = pd.concat([data, data_all_5], axis=0)

data_all_5.to_pickle('data_all_5.pkl') 


# In[12]:


data_all_5.head().style.set_table_attributes('style="font-size: 12px"')


# <br> 수익률의 분포를 확인합니다. 수익이 되는 전략은 아닙니다.

# In[13]:


data_all_5 = pd.read_pickle('data_all_5.pkl')
print(data_all_5['ub_return'].describe(percentiles=[0.01, 0.1, 0.5, 0.9, 0.99]))
print(data_all_5.groupby('max_high')['ub_return'].describe())


# <br> **매도 전략 2 - 모든 종목을 종가 매수 후, 아래와 같은 순서로 매도**        
# 1. 익일 고가가 당일 고가 보다 크면 2 영업일 시가 매도   
# 2.  1 조건 만족하지 않으면 2 영업일 종가 매도  
# 
# 위와 같은 매도 전략은 수익율이 어떻게 될까요?   

# In[13]:


kosdaq_list = pd.read_pickle('kosdaq_list.pkl')

data_all_5 = pd.DataFrame()

def final_r(x):
    
    if   x['high_r0'] < x['high_r1']:  #  (당일 고가/매수 종가) 비율이 (익일 고가/매수 종가) 비율 값이 작으면 2 영업일 시가 매도     
        return x['open_r2']    
    
    else:
        return x['close_r2'] # 매도 안된 종목은 전부 2 영업일 종가 매도         
    
for code in kosdaq_list['code']:    
    
    # 종목별 처리
    data = mdl_data[mdl_data['code']==code].sort_index().copy()
    
    # 최고/최저 수익율
    for i in [0, 1, 2]:

        data['high_r' + str(i)] = data['high'].shift(-1*i)/data['close']        
        data['close_r' + str(i)] = data['close'].shift(-1*i)/data['close']
        data['open_r' + str(i)] = data['open'].shift(-1*i)/data['close']
        
    data['final_return'] = data.apply(final_r, axis=1) # 각 row 에 대하여 final_r 함수를 적용
                                                                                                                                                 
    data.dropna(subset=['close_r0','close_r1', 'close_r2','high_r0', 'high_r1', 'open_r2'], inplace=True)   # 데아터 처리 중 missing 값이 사용된 경우는 제거
    data_all_5 = pd.concat([data, data_all_5], axis=0)

data_all_5.to_pickle('data_all_5.pkl')    


# <br> 수익률을 확인합니다.

# In[14]:


data_all_5 = pd.read_pickle('data_all_5.pkl')  
data_all_5['final_return'].describe(percentiles=[0.01, 0.1, 0.5, 0.9, 0.99])


# ### <br> 매수 전략 데이터 프로세싱
# 모델 개발을 위해서는 매수 전략에 따라 매수 종목을 결정할 수 있어야 합니다. 이번 장에서는 기본적인 매수 종목을 찾는 데이터처리를 진행해 보겠습니다. 결과 수익률 데이터가 있는
# mdl_data pickle 파일을 읽습니다.
# 

# In[15]:


mdl_data = pd.read_pickle('mdl_data.pkl')


# <br> **매수 전략 1 - 시장 수익율보다 더 좋은 수익율을 보인 종목을 매수**    
# 시장 수익율보다 더 좋은 수익율을 보인 종목을 알기 위해 4.4.5 절에 'win_market' 이라는 변수를 생성했습니다. 이것을 이용할 것인데요. 더 의미있는 지표를 생성하기 위해서 과거 60일 누적 합을 보겠습니다. 수익율은 max_close(5 영업일 중 최고 종가 수익율) 이용하겠습니다.
# 

# In[16]:


kosdaq_list = pd.read_pickle('kosdaq_list.pkl')

data_all_6 = pd.DataFrame()

for code in kosdaq_list['code']:
    
    # 종목별 처리
    data = mdl_data[mdl_data['code']==code].sort_index().copy()
    
    # 과거 60일 win_market 누적 합
    data['win_market_sum'] = data['win_market'].rolling(60).sum() # 과거 60일 누적합
    
    # 고가, 저가, 종가 수익율
    for i in [1,2,3,4,5]:

        data['high_r' + str(i)] = data['high'].shift(-1*i)/data['close']      
        data['low_r' + str(i)] = data['low'].shift(-1*i)/data['close']   
        data['close_r' + str(i)] = data['close'].shift(-1*i)/data['close']    
        
    data['max_close']  = data[['close_r1','close_r2','close_r3','close_r4','close_r5']].max(axis=1) # 5 영업일 종가 수익율 중 최고 값
    data.dropna(subset=['win_market_sum','close_r1','close_r2','close_r3','close_r4','close_r5'], inplace=True) # missing 이 있는 행은 제거   
 
    data_all_6 = pd.concat([data, data_all_6], axis=0)

data_all_6.to_pickle('data_all_6.pkl')    
data_all_6.head().style.set_table_attributes('style="font-size: 12px"')


# <br> win_market_sum 에 따른 수익률의 변화를 확인합니다. win_market_sum 이 클수록 수익률이 높아지는 경향이 있다는 것을 확인했습니다.

# In[17]:


data_all_6 = pd.read_pickle('data_all_6.pkl')    
ranks = pd.qcut(data_all_6['win_market_sum'], q=8)
print(data_all_6.groupby(ranks)['max_close'].mean())
data_all_6.groupby(ranks)['max_close'].mean().plot(figsize=(12,5))


# <br> **매수 전략 2 - 섹터 평균 수익율보다 더 높은 수익율을 보인 종목을 매수**    
# kosdaq_list 에 있는 종목별 섹터 정보를 이용하겠습니다. 우선, 종목별 최근 60일 평균 수익율을 rolling 함수를 이용하여 으로 계산합니다. for Loop 을 이용하여 종목에 섹터 정보를 추가합니다. 
# 

# In[18]:


kosdaq_list = pd.read_pickle('kosdaq_list.pkl')

data_all_6 = pd.DataFrame()

for code, sector in zip(kosdaq_list['code'], kosdaq_list['sector']):
    
    # 종목별 처리
    data = mdl_data[mdl_data['code']==code].sort_index().copy()
    data.dropna(inplace=True)
    
    # 최근 60일 평균 수익율            
    data['return_mean'] = data['return'].rolling(60).mean() # 종목별 최근 60 일 수익율의 평균
    data['sector'] = sector     
  
    data.dropna(subset=['return_mean'], inplace=True)    
    data_all_6 = pd.concat([data, data_all_6], axis=0)

data_all_6.to_pickle('data_all_6.pkl')   


# In[19]:


data_all_6 = pd.read_pickle('data_all_6.pkl') 
data_all_6.head().style.set_table_attributes('style="font-size: 12px"')


# 최근 60 일 평균수익율 정보를 섹터 별, 일 별로 요약한 값을 추가합니다. 이때 apply 대신 Transform 함수가 이용되었습니다. apply 는 그룹의 숫자 만큼 행을 리턴하나, transform 은 그룹핑 하기 전의 행 수 를 리턴합니다. 그 값을 'return over sector' 라는 변수에 저장합니다.

# In[20]:


data_all_6['sector_return'] = data_all_6.groupby(['sector', data_all_6.index])['return'].transform(lambda x: x.mean())
data_all_6['return over sector'] = (data_all_6['return']/data_all_6['sector_return']) # 섹터의 평균 수익률 대비 종목 수익률의 비율


# 결과를 보니, 섹터를 이용하여 종목을 선정할 때는 섹터 평균 수익율보다 많이 높거나, 많이 낮는 종목을 선정하는 것이 수익율이 좋게 나왔습니다. 섹터 평균 수익율 대비 종목 수익율은 미래 수익율 예측에 도움이 되는 정보입니다.

# In[21]:


pd.options.display.float_format = '{:,.3f}'.format
ranks = pd.qcut(data_all_6['return over sector'], q=10)
print(data_all_6.groupby(ranks)['max_close'].describe(percentiles=[0.01, 0.99]))
data_all_6.groupby(ranks)['max_close'].mean().plot(figsize=(12,5))


# 한 섹터에 최소 10 개 이상의 종목이 있어야 섹터의 평균 수익율이 의미가 있을 것 같습니다. 10개 이상의 종목이 있는 섹터만을 매수 대상으로 해서 다시 수익율을 계산해봅니다. 같은 결과를 얻었습니다. 섹터의 평균 수익율보다 아주 낮거나 높은 종목의 수익율의 상승이 높았습니다. 그래프 곡선이 더 부드러워졌습니다.

# In[22]:


sector_count = data_all_6.groupby('sector')['code'].nunique().sort_values()
data_all_6x = data_all_6[data_all_6['sector'].isin(sector_count[sector_count>=10].index)]
ranks = pd.qcut(data_all_6x['return over sector'], q=10)
print(data_all_6x.groupby(ranks)['max_close'].describe(percentiles=[0.01, 0.99]))
data_all_6x.groupby(ranks)['max_close'].mean().plot(figsize=(12,5))


# In[ ]:




