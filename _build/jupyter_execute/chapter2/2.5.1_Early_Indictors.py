#!/usr/bin/env python
# coding: utf-8

# <br>

# 나스닥 지수와 코스닥 지수가 상당히 연동되어 움직이는 것을 그래프로 확인할 수 있었습니다. 미국 3대 지수의 수익율에 따라 코스닥 지수의 수익율이 어떻게 변화는 지 알아보겠습니다.

# In[226]:


import yfinance as yf
import pandas as pd
import numpy as np

nasdaq = yf.download('^IXIC', start = '2021-01-01', end = '2022-06-30') # 나즈닥
dowjones = yf.download('^DJI', start = '2021-01-01', end = '2022-06-30') # 다우존스
sp500 =  yf.download('^GSPC', start = '2021-01-01', end = '2022-06-30') # S&P 500
kospi =  yf.download('^KS11', start = '2021-01-01', end = '2022-06-30') # 코스피
kosdaq =  yf.download('^KQ11', start = '2021-01-01', end = '2022-06-30') # 코스닥


# In[261]:


nasdaq['ns_return'] = nasdaq['Close']/nasdaq['Close'].shift(1)
sp500['sp_return'] = sp500['Close']/sp500['Close'].shift(1)
dowjones['dw_return'] = dowjones['Close']/dowjones['Close'].shift(1)
kosdaq['kq_return'] = kosdaq['Close'].shift(-1)/kosdaq['Open'].shift(-1)
kospi['ks_return'] = kospi['Close'].shift(-1)/kospi['Open'].shift(-1)

nasdaq['ns_count'] = np.where(nasdaq['ns_return']>1.005, 1, 0)
sp500['sp_count'] = np.where(sp500['sp_return']>1, 1, 0)
dowjones['dw_count'] = np.where(dowjones['dw_return']>1, 1, 0)

df = pd.concat([nasdaq[['ns_count','ns_return']], sp500[['sp_count','sp_return']], dowjones[['dw_count','dw_return']], kosdaq['kq_return'], kospi['ks_return']], axis=1, join='inner').dropna()


# In[278]:


ranks = pd.cut(df['ns_return'], bins=[0, 0.98, 0.99, 1, 1.01, 1.02, 2])
df.groupby(ranks)['kq_return'].mean().plot()


# In[279]:


ranks = pd.cut(df['sp_return'], bins=[0, 0.98, 0.99, 1, 1.01, 1.02, 2])
df.groupby(ranks)['kq_return'].mean().plot()


# In[280]:


ranks = pd.cut(df['dw_return'], bins=[0, 0.98, 0.99, 1, 1.01, 1.02, 2])
df.groupby(ranks)['kq_return'].mean().plot()


# In[270]:


df['ns_return'].between(0.98, 0.99)


# In[224]:


df.corr()


# In[252]:


df.groupby(['ns_count','dw_count','sp_count'])['kq_return'].describe()


# In[255]:


a = (df['ns_count']==1)*(df['dw_count']==0)*(df['sp_count']==0)
mdl = df[a]


# In[256]:


""
mdl['kq_return'].describe()


# In[258]:


nasdaq = yf.download('^IXIC', start = '2021-07-01', end = '2022-09-15') # 나즈닥
dowjones = yf.download('^DJI', start = '2021-07-01', end = '2022-09-15') # 다우존스
sp500 =  yf.download('^GSPC', start = '2021-07-01', end = '2022-09-15') # S&P 500
kospi =  yf.download('^KS11', start = '2021-07-01', end = '2022-09-15') # 코스피
kosdaq =  yf.download('^KQ11', start = '2021-07-01', end = '2022-09-15') # 코스닥

nasdaq['ns_return'] = nasdaq['Close']/nasdaq['Close'].shift(1)
sp500['sp_return'] = sp500['Close']/sp500['Close'].shift(1)
dowjones['dw_return'] = dowjones['Close']/dowjones['Close'].shift(1)
kosdaq['kq_return'] = kosdaq['Close'].shift(-1)/kosdaq['Open'].shift(-1)
kospi['ks_return'] = kospi['Close'].shift(-1)/kospi['Open'].shift(-1)

nasdaq['ns_count'] = np.where(nasdaq['ns_return']>1.005, 1, 0)
sp500['sp_count'] = np.where(sp500['sp_return']>1, 1, 0)
dowjones['dw_count'] = np.where(dowjones['dw_return']>1, 1, 0)

df = pd.concat([nasdaq[['ns_count','ns_return']], sp500['sp_count'], dowjones['dw_count'], kosdaq['kq_return'], kospi['ks_return']], axis=1, join='inner').dropna()

df.groupby(['ns_count','dw_count','sp_count'])['kq_return'].describe()


# In[ ]:





# In[ ]:





# In[111]:


from statsmodels.tsa.stattools import coint
df = pd.concat([sp500['Close'], kosdaq['Close']], axis=1, join='inner').dropna()
df.columns = ['sp_close','kq_close']
score, pvalue, _ = coint(df['sp_close'], df['kq_close'])
print(score, pvalue)


# In[109]:


df = pd.concat([sp500['sp_return'], kosdaq['kq_return']], axis=1, join='inner').dropna()
df[['sp_return','kq_return']].corr()


# In[110]:


rank = pd.qcut(df['sp_return'], q=10)
df.groupby(rank)['kq_return'].mean().plot()


# In[ ]:


# df['buy'] = np.where(df['sp_return']>1.01, 1, 0)


# In[ ]:





# In[85]:


df.groupby('buy')['kq_return'].mean()


# In[93]:


rank = pd.qcut(df['sp_return'], q=10)
df.groupby(rank)['kq_return'].mean().plot()


# In[ ]:




