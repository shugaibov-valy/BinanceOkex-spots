#!/usr/bin/env python
# coding: utf-8

# In[139]:


import bs4
import requests


# In[140]:


headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/69.0'})


# ## Binance

# In[141]:



url = "https://api.binance.com/api/v1/ticker/24hr"
data = requests.get(url).json()

binance_dict = {}
for currency in data:
        name = currency['symbol']
        price = currency['lastPrice']
        volume = currency['volume']
        binance_dict[name] = [price, volume]    # binance_dict[name] = {цена, объем} 


# ## Okex

# In[142]:


url = "https://okex.com/api/spot/v3/instruments/ticker/"
response = requests.get(url)
data = response.json()
okex_dict = {}
for currency in data:
    name = currency['instrument_id'].replace('-', '')  # убираем '-'
    price = currency['ask']
    volume = currency['base_volume_24h']
    okex_dict[name] = [price, volume]     # okex_dict[name] = {цена, объем}


# In[143]:


ls1 = list(binance_dict.keys())   # списки названий инструментов каждой биржы
ls2 = list(okex_dict.keys())


# In[144]:


all_names = set(ls1 + ls2)   # все неповторяющиеся названия интструментов


# ### DataFrame создаем

# In[145]:


import pandas as pd
import numpy as np
unify_name = pd.Series([name for name in all_names])
binance_name = pd.Series([f'{price}$/{volume}' for name in all_names for price, volume in [binance_dict.get(name, ['-', '-'])]])
okex_name = pd.Series([f'{price}$/{volume}' for name in all_names for price, volume in [okex_dict.get(name, ['-', '-'])]])

### Сливаем все Серии вместе
Data = pd.DataFrame([unify_name, binance_name, okex_name]).T
Data.columns = ['unify_name', 'binance_name', 'okex_name']


# In[146]:


Data.sort_values(by='unify_name', ignore_index=True)  ### сортировка по Unify_name


# In[ ]:




