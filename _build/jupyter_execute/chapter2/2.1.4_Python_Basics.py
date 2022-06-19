#!/usr/bin/env python
# coding: utf-8

# ### If Condition
# 파이썬의 조건문 if ~ else 형식으로 다른 컴퓨터 언어와 다르지 않습니다. 단지 else if 부분은 줄여서 elif 로 씁니다. 아래 예제를 보시면 쉽게 이해가 되실 것으로 생각합니다.

# In[1]:


a = 3
b = 2
if a > b:
    print('a > b')
else:
    print('a <= b')


# In[2]:


num_list = [1,2,3,4,5,6]

for i in num_list:
    if i < 3:
        print(i, 'the number is less than 3')
    elif i > 3:
        print(i, 'The number is greater than 3')
    else:
        print(i, 'The number is 3')


# In[3]:


for i in num_list:
    if i < 3:
        print(i, 'the number is less than 3')
    elif i > 3:
        pass  # 아무런 처리를 하지 않음
    else:
        print(i, 'The number is 3')


# In[ ]:




