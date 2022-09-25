#!/usr/bin/env python
# coding: utf-8

# ### For Loop
# 컴퓨터를 잘 활용한다는 것의 컴퓨터의 3 가지 강점 - 기억, 반복, 계산을 잘 활용한다는 뜻입니다. 그 중에서도 인간보다 탁월한 능력이 바로 반복입니다. 컴퓨터는 수만번, 수천번의 반복도 금방 해 치웁니다. 이번에는 그 반복문을 배우겠습니다. 반복문 중에 for ~ in 구분이 가장 많이 활용됩니다. for ~ in 형식에서 in 다음에 List 를 넣으면 List 의 원소를 순서대로 꺼내어 처리합니다. 단순히 출력만 해보겠습니다. 다음에는 제곱한 값을 출력해 보겠습니다.

# In[1]:


num_list = [1,2,3,4,5,6]
for i in num_list:
    print(i)

print('\n')    
for i in num_list:
    print(i**2)    


# <br>
# for 반복문에서 break 와 continue 의 활용법도 배워보겠습니다. i 가 3 일때 for 반복문을 빠져나오고 싶으면 break 를 사용하고, i 가 3 일때는 패스하고, 4 부터 다시 시작하고 싶으면 continue를 사용합니다.

# In[2]:


# break
for i in num_list:
    if i == 3:
        break
    print(i**2)  


# In[3]:


# continue
for i in num_list:
    if i == 3:
        continue
    print(i**2)    


# ### While Loop
# While 반복문도 자주 활용됩니다. While 안의 조건이 만족하는 한, 계속 반복합니다. break 문으로 While Loop 를 빠져나올 수 있습니다.

# In[4]:


i = 0
while(True):
    i = i + 1
    print(i**2)
    if i == 10:
        break


# In[5]:


i = 0
while(i<10):
    i = i + 1
    print(i**2)

