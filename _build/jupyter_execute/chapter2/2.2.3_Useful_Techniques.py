#!/usr/bin/env python
# coding: utf-8

# ### Groupby
# Groupby 는 데이터를 요약할 때 많이 활용하는 기법입니다. 아래 예제에서 만들어진 DataFrame - df 의 'grp' 컬럼을 이용하여 'a', 'b', 'c' 등의 3 개의 그룹으로 나눌 수 있습니다.
# 먼저, 그룹을 무시하고 v1, v2 의 평균값을 알아봅니다. 그 다음, 그룹 별로 v1 과 v2 의 평균값을 알아봅니다.

# In[1]:


import pandas as pd

g_list = ['a','a','a','b','b','b','c','c','c','c']
v1_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
v2_list = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

df =  pd.DataFrame({'grp': g_list, 'v1': v1_list, 'v2': v2_list}) # 그룹핑을 할 수 있는 컬럼을 가진 DataFrame 생성


# In[2]:


df[['v1', 'v2']].mean() # 전체 평균


# In[3]:


df.groupby('grp')['v1'].mean() # 그룹별 평균


# <br>
# 그룹별로 v1 의 평균, 최대값, 총합을 알아봅니다.

# In[4]:


df.groupby('grp')['v1'].agg(['mean','max','sum'])


# <br>
# 그룹별로 v1 과 v2 의 평균, 최대값, 총합을 알아봅니다.

# In[5]:


df.groupby('grp')[['v1','v2']].agg(['mean','max','sum'])


# <br>
# 이번에는 그룹별로 v1 은 평균, v2 는 총합을 알아봅니다.

# In[6]:


s = {'v1':'mean', 'v2':'sum'}
df.groupby('grp').agg(s)


# <br>
# 그룹별 최대값에서 최소값을 뺀 값을 알아봅니다. lambda 함수를 이용했습니다. lambda 함수의 자세한 활용법은 다루지 않도록 하겠습니다. Apply 함수를 이용한 경우와 Transform 함수를 이용한 경우의 차이점을 알아야 합니다. Apply 를 이용하면 생성된 그룹의 갯 수 만큼의 행을 리턴합니다. Transform 은 그룹핑하기 전의 데이터 행의 갯 수 만큼을 반환합니다. 그룹별 요약된 정보를 원래 데이터에 추가하고 싶을 때는 Transform 이 사용됩니다.

# In[7]:


df.groupby('grp')['v1'].apply(lambda x: x.max() - x.mean())


# In[8]:


df.groupby('grp')['v1'].transform(lambda x: x.max() - x.mean())


# In[ ]:




