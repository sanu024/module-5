#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install yfinance')
get_ipython().system('pip install bs4')
get_ipython().system('pip install nbformat')


# In[2]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[3]:


import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# In[4]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[5]:


tesla=yf.Ticker('TSLA')


# In[6]:


tesla_data=tesla.history(period='max')


# In[7]:


tesla_data.reset_index(inplace=True)


# In[8]:


tesla_data.head()


# In[9]:


url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'


# In[10]:


html_data=requests.get(url).text


# In[11]:


html_data=BeautifulSoup(html_data,'html.parser')


# In[32]:


tesla_revenue=pd.DataFrame(columns=['Date','Revenue'])


# In[33]:


for row in html_data.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    tesla_revenue = pd.concat([tesla_revenue,pd.DataFrame({"Date":[date], "Revenue":[revenue]})], ignore_index=True)


# In[34]:


tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"", regex=True)


# In[35]:


tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[36]:


tesla_revenue.tail()


# In[17]:


gamestop=yf.Ticker('GME')


# In[18]:


gme_data=gamestop.history(period='max')


# In[19]:


gme_data.reset_index(inplace=True)


# In[20]:


gme_data.head()


# In[21]:


url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'


# In[22]:


html_data_2=requests.get(url).text


# In[23]:


html_data_2=BeautifulSoup(html_data_2,'html.parser')


# In[24]:


gme_revenue=pd.DataFrame(columns=['Date','Revenue'])


# In[25]:


for row in html_data_2.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    gme_revenue = pd.concat([gme_revenue,pd.DataFrame({"Date":[date], "Revenue":[revenue]})], ignore_index=True)


# In[27]:


gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"", regex=True)


# In[28]:


gme_revenue.dropna(inplace=True)

gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]


# In[29]:


gme_revenue.tail()


# In[37]:


make_graph(tesla_data,tesla_revenue,'Tesla')


# In[31]:


make_graph(gme_data,gme_revenue,'GameStop')


# In[ ]:




