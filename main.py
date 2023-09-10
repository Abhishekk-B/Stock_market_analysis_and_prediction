from stockDB import databaseAPI
from interactiveGraphs import InteractiveGraphs
from predictionfile import stockPrediction


import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pickle

import streamlit as st
import pandas as pd
from datetime import date

import yfinance as yf
import humanize



gr=InteractiveGraphs()

STOCKNAME='TSLA'
db=databaseAPI()
print(db)


st.set_page_config(page_title="Stock Market Analysis",layout="wide")

st.header("Stock market analysis and prediction")   



def user_input_features():
    stocks = st.sidebar.selectbox('Stock',('TSLA','AAPL'))
    col1,col2=st.sidebar.columns(2)
    with col1:
        d1=st.date_input("Start date", date(2022, 12, 1))
    with col2:
        d2=st.date_input("End date") 
    data = {'stock':[stocks], 
            'start_date':[d1], 
            'end_date':[d2]}   

    features = pd.DataFrame(data)
    return features

input_df = user_input_features()
ticker = yf.Ticker(input_df['stock'].values[0]).info


dic={
    'Exchange':ticker['exchange'],
    'Sector':ticker['sector'],
    'Industry':ticker['industry'],
    'Country':ticker['country'],
    'Previous Close':ticker['previousClose'],
    'Open':ticker['open'],
    'Day Low':ticker['dayLow'],
    'Day High':ticker['dayHigh'],
    'Trailing PE':ticker['trailingPE'],
    'Volume':ticker['volume'],
    'MarketCap':ticker['marketCap'],
    'FiftyTwoWeekLow':ticker['fiftyTwoWeekLow'],
    'FiftyTwoWeekHigh':ticker['fiftyTwoWeekHigh'],
    'FiftyDayAverage':ticker['fiftyDayAverage'],
    'Profit Margins':ticker['profitMargins'],
    'Total Revenue':ticker['totalRevenue']   
}
options = st.sidebar.multiselect('Technical Indicators', ['No Indicator','Simple Moving Average(SMA)','Exponential Weightage Moving Average(EWMA)'],default='No Indicator') 

df_sum=pd.DataFrame(dic,index=['value']).T
df_sum=df_sum.reset_index()
df_sum.rename(columns = {'index':'Parameter'}, inplace = True)

df_sum_left=df_sum[:8]
df_sum_right=df_sum[8:]


st.subheader(input_df['stock'].values[0])
st.write(ticker['longName'])
col1, col2, col3,col4= st.columns(4)
col1.metric("Market Cap", humanize.intword(ticker['totalDebt']))
col2.metric("Previous Close",f"$ {ticker['previousClose']}")
col3.metric("Trailing PE Ratio", round(ticker['trailingPE'],2))
col4.metric("Volume", humanize.intword(ticker['volume']))

  
st.sidebar.subheader("Select number of days")
n_day = ("30", "60")
n=st.sidebar.radio("Days", n_day, 0)

if input_df['stock'].values[0] in ('TSLA','AAPL'):
    STOCKNAME=input_df['stock'].values[0]
    if STOCKNAME =='TSLA':
        filename = 'model_pickle_TSLA'
        loaded_model = pickle.load(open(filename, 'rb'))
    else:
        filename = 'model_pickle_AAPL'
        loaded_model = pickle.load(open(filename, 'rb'))
    try:
        df=db.data_fetchAll(STOCKNAME)
        df1=db.data_fetch(STOCKNAME,input_df['start_date'][0],input_df['end_date'][0])
        print(df.head())
    except:
        db.dataInsertion(STOCKNAME)
        df=db.data_fetchAll(STOCKNAME)
        df1=db.data_fetch(STOCKNAME,input_df['start_date'][0],input_df['end_date'][0])
        print(df1.head())

df_new=df.iloc[::-1]
df_new['SMA']=df_new['open'].rolling(window=10,min_periods=1).mean().astype(float)
df_new['EWMA']=df_new['open'].ewm(alpha=0.3,adjust=False).mean().astype(float)
df_new=df_new.iloc[::-1]
df1=pd.merge(df_new,df1,how='right')



fig=gr.basicGraph(df1,input_df,options)
st.plotly_chart(fig,use_container_width=True)
i1=st.sidebar.button("Predict")

st.header("Key Data")
l1, r1= st.columns(2)

r1.table(df_sum_right)
l1.table(df_sum_left)


def pred_data():
    pred=stockPrediction(df_new,loaded_model)
    pred_data=pred.prediction_data(n,str(input_df['end_date'][0]))
    pred_data=pred_data.iloc[::-1]
    df_temp=df1[['stockdate','EWMA']]
    df_temp=df_temp.rename(columns={'stockdate':'Date','EWMA':'Prediction'})
    frames = [pred_data,df_temp]   
    result = pd.concat(frames) 
    result=result.reset_index(drop=True)
    return result

result =pred_data()

fig=gr.prediction_chart(result,input_df,n,st,STOCKNAME,i1)
st.plotly_chart(fig,use_container_width=True)
if i1:
    st.write(result)







