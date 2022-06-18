#!/usr/bin/env python
# coding: utf-8

# ### Functions
# 파이썬의 함수는 def 로 시작하고 결과값을 return 으로 반환합니다. 결과값의 반환은 여러 개도 가능합니다. 단, 함수 호출 후 결과 값을 받을 때, 함수가 return 하는 결과 값 갯수가 동일해야 합니다. 함수도 아래 예제를 보시면 쉽게 이해가 되시리라 생각합니다.

# In[9]:


def cal(x, y):
    z = x + y
    return z

result = cal(2,3)
print(result)


# In[10]:


def cal(x, y):
    z1 = x + y
    z2 = x*y
    return z1, z2

result1, result2 = cal(2,3)
print(result1, result2)


# In[14]:


def cal(x, y):
    return  (x+y), (x*y), (x**y)

result1, result2, result3 = cal(2,3)
print(result1, result2, result3)


# In[ ]:




