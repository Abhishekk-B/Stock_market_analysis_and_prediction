import requests
import pandas as pd
import numpy as np


class dataFetch():
    STOCK_ENDPOINT = "https://www.alphavantage.co/query"
    STOCK_API_KEY = "KD5KC7HVRTWK1VPB"
    
    
    def __init__(self) -> None:
        pass        

    def fetchingData(self,name):
        self.name=name
        stock_params = {
        "function": "TIME_SERIES_DAILY",
        "outputsize":"full",
        "symbol": self.name,
        "apikey": dataFetch.STOCK_API_KEY,
        }
        print(stock_params)
        fetch="https://www.alphavantage.co/query"
        response = requests.get(dataFetch.STOCK_ENDPOINT, params=stock_params)
        data = response.json()["Time Series (Daily)"]
        df=pd.DataFrame(data).T
        df.rename(columns={"1. open":"open", "2. high":"high","3. low":"low","4. close":"close","5. volume":"volume"},inplace=True)
        df['date'] = df.index
        df.index = np.arange(1, len(df) + 1)
        return df


