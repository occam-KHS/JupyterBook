#!/usr/bin/env python
# coding: utf-8

# In[34]:


import gym
import collections
import random

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

#Hyperparameters
learning_rate = 0.0001
gamma         = 0.98
buffer_limit  = 30000
batch_size    = 32

class ReplayBuffer():
    def __init__(self):
        self.buffer = collections.deque(maxlen=buffer_limit)
    
    def put(self, transition):
        self.buffer.append(transition)
    
    def sample(self, n): # 버퍼에서 샘플링
        mini_batch = random.sample(self.buffer, n)
        s_lst, a_lst, r_lst, s_prime_lst, done_mask_lst = [], [], [], [], []
        
        for transition in mini_batch:
            s, a, r, s_prime, done_mask = transition
            s_lst.append(s)
            a_lst.append([a])
            r_lst.append([r])
            s_prime_lst.append(s_prime)
            done_mask_lst.append([done_mask])

        return torch.tensor(s_lst, dtype=torch.float), torch.tensor(a_lst),                torch.tensor(r_lst), torch.tensor(s_prime_lst, dtype=torch.float),                torch.tensor(done_mask_lst)
    
    def size(self):
        return len(self.buffer)

class Qnet(nn.Module):
    def __init__(self):
        super(Qnet, self).__init__()
        self.fc1 = nn.Linear(4, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 2)

    def forward(self, x): # Q Value 리턴 (음수가 될 수 도 있음)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
      
    def sample_action(self, obs, epsilon):
        out = self.forward(obs)
        coin = random.random() # 0 ~ 1 
        if coin < epsilon:
            return random.randint(0, 1)
        else : 
            return out.argmax().item()
            
def train(q, q_target, memory, optimizer):
    for i in range(10):
        s, a, r, s_prime, done_mask = memory.sample(batch_size)
        q_out = q(s) # input size (32,4) return size (32,2)
        q_a = q_out.gather(1, a) # 취한 액션의 큐값만 골라냄 (32,1)
        max_q_prime = q_target(s_prime).max(1)[0].unsqueeze(1)
        target = r + gamma * max_q_prime * done_mask
        loss = F.smooth_l1_loss(q_a, target)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()


env = gym.make('CartPole-v1')
q = Qnet()
q_target = Qnet()
q_target.load_state_dict(q.state_dict()) # Copy network weights
memory = ReplayBuffer()

print_interval = 50
score = 0.0  
optimizer = optim.Adam(q.parameters(), lr=learning_rate) # q_target 은 업데이트 안 함!

for n_epi in range(1000):
    epsilon = max(0.01, 0.08 - 0.01*(n_epi/200)) #Linear annealing from 8% to 1%. 에피소드 증가하면 입실로 작아짐
    s = env.reset()[0]
    done = False

    while not done:
        a = q.sample_action(torch.from_numpy(s).float(), epsilon)      
        s_prime, r, done, _ ,info = env.step(a)
        done_mask = 0.0 if done else 1.0
        memory.put((s, a, r/100.0, s_prime, done_mask))
        s = s_prime

        score += r
        if done:
            break

    if memory.size()>2000:
        train(q, q_target, memory, optimizer)

    if n_epi%print_interval==0 and n_epi!=0:
        q_target.load_state_dict(q.state_dict()) # 타겟 네트워크 업데이트 (20 번 에피소드 마다)
        print("n_episode :{}, score : {:.1f}, n_buffer : {}, eps : {:.1f}%".format(n_epi, score/print_interval, memory.size(), epsilon*100))                
        
        if (score/print_interval) > 300:
            break
            
        score = 0.0
        
env.close()


# In[35]:


import time
env = gym.make('CartPole-v1')

for i_episode in range(5):
    observation = env.reset()[0]
    for t in range(550):
        time.sleep(0.01)
        env.render()
        action = q_target(torch.Tensor(observation)).argmax().item() 
        observation, reward, done, _, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            time.sleep(1)
            break
env.close()


# In[253]:


import FinanceDataReader as fdr
df = fdr.DataReader('056090', start='2021-01-01')


# In[527]:






for  j in range(30):

    buy_dt =  random.choice(df.index[7:-21]).strftime('%Y-%m-%d') # 매수일

    def obs_data(buy_dt):
        i = 0
        s_list = []

        for i in range(20):

            end_dt = df[buy_dt:].index[5 + i].strftime('%Y-%m-%d')   # 관찰 6 일
            action_dt = df[buy_dt:].index[6 + i].strftime('%Y-%m-%d') # 매도 일

            s = df[buy_dt:end_dt].copy()
            s['return'] = s['Close']/df.loc[buy_dt]['Close']
            s1 = s['return'].mean()  # 관찰기간(6일) 수익율 평균
            s2 = s['return'].max()  # 관찰기간(6일) 수익율 최대
            s3 = s['return'].min()  # 관찰기간(6일) 수익율 최소
            s4 = s['return'][-1]  # 관찰 기간 6일(매도 전날) 수익율
            s5 = (s['Volume']/s['Volume'].shift(1)).loc[end_dt] # 매도 전일 거래량 변화
            s6 = df.loc[action_dt]['Open']/df.loc[buy_dt]['Close'] # 매도 일 시가 수익율

            r = df.loc[action_dt]['Close']/df.loc[buy_dt]['Close'] # 종가 매도시 수익률

            s_list.append([s1, s2, s3, s4, s5, s6, r])   

        return np.array(s_list)

    print(j, obs_data('2022-02-22').shape)


# In[478]:


obs_data('2022-02-22').shape


# In[608]:


import FinanceDataReader as fdr
df = fdr.DataReader('005930', start='2019-01-01')

class Stock:
    
    def __init__(self, df):
        self.actions = [0, 1]
        self.count = 0        
        self.sample_data = df
        self.buy_dt = '2021-01-01'
        
    def collect_data(self, buy_dt):

        i = 0
        s_list = []

        for i in range(20):

            end_dt = df[buy_dt:].index[5 + i].strftime('%Y-%m-%d')   # 관찰 6 일
            action_dt = df[buy_dt:].index[6 + i].strftime('%Y-%m-%d') # 매도 일

            s = df[buy_dt:end_dt].copy()
            s['return'] = s['Close']/df.loc[buy_dt]['Close']
            s1 = s['return'].mean()  # 관찰기간(6일) 수익율 평균
            s2 = s['return'].max()  # 관찰기간(6일) 수익율 최대
            s3 = s['return'].min()  # 관찰기간(6일) 수익율 최소
            s4 = s['return'][-1]  # 관찰 기간 6일(매도 전날) 수익율
            s5 = (s['Volume']/s['Volume'].shift(1)).loc[end_dt] # 매도 전일 거래량 변화
            s6 = df.loc[action_dt]['Open']/df.loc[buy_dt]['Close'] # 매도 일 시가 수익율
            r = df.loc[action_dt]['Close']/df.loc[buy_dt]['Close'] # 종가 매도시 수익률

            s_list.append([s1, s2, s3, s4, s5, s6, r])   

        return np.array(s_list)     
    
    def reset(self):         
        self.buy_dt = random.choice(df.index[10:-30]).strftime('%Y-%m-%d') # 관찰기간 매도 기간 확보
        self.state = collect_data(self.buy_dt)        
        return np.delete(self.state, 6, axis=1)  # 마지막 컬럼은 수익율 (뺴고 리턴)    

    def random_action(self):
        sample = [0, 1]
        return random.choice(sample)  
        
    def step(self, action):         
       
        if action == 1:
            r = (self.state[self.count][-1] > 1).astype(int) # 매도시 수익율            
            
        else:
            r = 1 
            
        self.count += 1                

        if action==0 and self.count < 19:            
                 
            next_state = self.state[self.count][:6]     
            done = False
            info = ''
            return  next_state, r, done, info
            
        else:
            next_state = self.state[self.count][:6]    
            done = True                            
            self.count = 0       
            info = ''
            return next_state, r, done, info


# In[609]:


import gym
import collections
import random

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

#Hyperparameters
learning_rate = 0.001
gamma         = 0.98
buffer_limit  = 3000
batch_size    = 64

class ReplayBuffer():
    def __init__(self):
        self.buffer = collections.deque(maxlen=buffer_limit)
    
    def put(self, transition):
        self.buffer.append(transition)
    
    def sample(self, n): # 버퍼에서 샘플링
        mini_batch = random.sample(self.buffer, n)
        s_lst, a_lst, r_lst, s_prime_lst, done_mask_lst = [], [], [], [], []
        
        for transition in mini_batch:
            s, a, r, s_prime, done_mask = transition
            s_lst.append(s)
            a_lst.append([a])
            r_lst.append([r])
            s_prime_lst.append(s_prime)
            done_mask_lst.append([done_mask])

        return torch.tensor(s_lst, dtype=torch.float), torch.tensor(a_lst),                torch.tensor(r_lst), torch.tensor(s_prime_lst, dtype=torch.float),                torch.tensor(done_mask_lst)
    
    def size(self):
        return len(self.buffer)

class Qnet(nn.Module):
    def __init__(self):
        super(Qnet, self).__init__()
        self.fc1 = nn.Linear(6, 32)
        self.fc2 = nn.Linear(32, 32)   
        self.fc3 = nn.Linear(32, 2)

    def forward(self, x): # Q Value 리턴 (음수가 될 수 도 있음)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))    
        x = self.fc3(x)
        return x
      
    def sample_action(self, obs, epsilon):
        out = self.forward(obs)
        coin = random.random() # 0 ~ 1 
        if coin < epsilon:
            return random.randint(0, 1)
        else : 
            return out.argmax().item()
            
def train(q, q_target, memory, optimizer):
    for i in range(10):
        s, a, r, s_prime, done_mask = memory.sample(batch_size)
        q_out = q(s).reshape(batch_size,2) # input size (32,2) return size (32,2)
        q_a = q_out.gather(1, a) # 취한 액션의 큐값만 골라냄 (32,1)
        max_q_prime = q_target(s_prime).max(1)[0].unsqueeze(1)
        target = r + gamma * max_q_prime * done_mask
        loss = F.smooth_l1_loss(q_a, target)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()


q = Qnet()
q_target = Qnet()
q_target.load_state_dict(q.state_dict())
memory = ReplayBuffer()

print_interval = 500
score = 1.0  
optimizer = optim.Adam(q.parameters(), lr=learning_rate) # q_target 은 업데이트 안 함!

stock_env = Stock(df)

for n_epi in range(8000):
    

    epsilon = max(0.01, 0.08 - 0.01*(n_epi/200)) #Linear annealing from 8% to 1%    
    stock = stock_env.reset()
    done = False

    while not done:
        a = q.sample_action(torch.from_numpy(stock[0]).float(), epsilon)  
        s_prime, r, done, info = stock_env.step(a)      

        done_mask = 0.0 if done else 1.0
        memory.put((s, a, r*2, s_prime, done_mask))
        s = s_prime   
        
        score *= r

        if done:       
            break
            

    if memory.size()>1000:
        train(q, q_target, memory, optimizer)

    if n_epi%print_interval==0 and n_epi!=0:
        q_target.load_state_dict(q.state_dict()) # 타겟 네트워크 업데이트 (20 번 에피소드 마다)
        print("n_episode :{}, score : {:.3f}, n_buffer : {}, eps : {:.1f}%".format(n_epi, score, memory.size(), epsilon*100))                
        
        if (score/print_interval) > 50:
            break

        score = 1.0


# In[ ]:


q_target(torch.tensor(np.array([1,1,1,1,1,1])))

 torch.FloatTensor


# In[307]:


class Stock:
    
    def __init__(self, df):
        self.actions = [0, 1]
        self.count = 0        
        self.sample_data = df
        self.buy_dt = random.choice(df.index[7:-21]).strftime('%Y-%m-%d') # 매수일
        
    def reset(self):         
        self.state = collect_data(self.buy_dt)
        
    def step(self, action):
        return self.state

stock = Stock(df)
stock.reset()
stock.state.shape


# In[372]:


random.randint(0, 2)


# In[392]:


q


# In[ ]:


dir(q_target.parameters)


# In[16]:


s_prime, r, done, _, info  = env.step(1)
s_prime


# In[7]:


q.sample_action(torch.from_numpy(s).float(), epsilon)     


# In[15]:


env.step(1)


# In[19]:


env.reset()[0]


# In[409]:


random.randint(0, 1)


# In[638]:


import gym
import numpy as np
import matplotlib.pyplot as plt
from gym.envs.registration import register

register(
    id='FrozenLake-v3',
    entry_point = 'gym.envs.toy_text:FrozenLakeEnv',
    kwargs={'map_name':'4x4',
           'is_slippery':False}
)


# In[647]:


env = gym.make('FrozenLake-v3')
env.reset()
# action = env.action_space.sample()
# print(action)
env.step(1)
new_state, reward, done, _, _ = env.step(action)
print(new_state)
print(reward)





# In[628]:


env.step(action)


# In[630]:


c = (0, 0.0, False, False, {'prob': 1.0})
c[1]


# In[3]:


import FinanceDataReader as fdr
import datetime
# today_dt = datetime.datetime.today().strftime('%Y-%m-%d') # 오늘날짜를 'YYYY-MM-DD' 형태로 변경하여 저장
today_dt = '2022-09-26'
prev_dt = fdr.DataReader('005930', end = today_dt).index[-1].strftime('%Y-%m-%d') # today_dt 의 전 영업일을 찾아 'YYYY-MM-DD' 로 저장
print(today_dt, prev_dt)


# In[8]:


fdr.DataReader('005930', end = today_dt).tail(5).index[-2]


# In[11]:


today_dt ='2022-10-11'
prev_dt = fdr.DataReader('005930', end = today_dt).index[-2].strftime('%Y-%m-%d') # today_dt 의 전 영업일을 찾아 'YYYY-MM-DD' 로 저장
print(today_dt, prev_dt)


# In[12]:


fdr.DataReader('005930', end = today_dt).tail(5)


# In[ ]:




