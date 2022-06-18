#!/usr/bin/env python
# coding: utf-8

# ### Append 
# append 는 반복문에서 발생하는 값을 순차적으로 모으는데 유용합니다. 아래 예제는 반복문에서 추출된 원소에 두제곱한 값을 계속 v_list 리스트에 추가하는 코드입니다. 

# In[2]:


v_list = []

aa = [1, 2, 3, 4, 5]

for a in aa:
    v_list.append(a**2)
    
print(v_list)    


# <br>
# 아래는 DataFrame 의 'c1' 컬럼을 List로 만들어, 반복을 수행합니다. 'c1' 의 제곱 값을 r_list 에 담은 후, 결과 값을 원래 DataFrame 에 'c3' Column 으로 추가하는 코드입니다.

# In[4]:


import pandas as pd

r_list = []

c1_list = [11,12,13,14,15]
c2_list = ['a','b','c','d','e']

df1 = pd.DataFrame({'c1': c1_list, 'c2': c2_list})

for i in list(df1['c1']): # List 함수가 꼭 필요하지는 않음  df1['c1'] => [11,12,13,14,15]
    r_list.append(i**2)
    
df1['c3'] = r_list # r_list 갯수와 df1 갯수가 동일해야 함
print(df1)


# <br>
# 아래와 같은 방식으로 처리를 해도 동일한 df1 가 생성됩니다.

# In[6]:


import pandas as pd

c1_list = [11,12,13,14,15]
c2_list = ['a','b','c','d','e']
df1 = pd.DataFrame({'c1': c1_list, 'c2': c2_list})

df1['c3'] = df1['c1']**2
print(df1)


# In[ ]:




