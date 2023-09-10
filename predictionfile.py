import datetime
import pandas as pd
import numpy as np
import sklearn
from sklearn.preprocessing import MinMaxScaler


class stockPrediction():
    fut_inp=None

    def __init__(self,df,model) -> None:
        self.df=df
        self.model=model
        
    def prediction(self,n):
        lst_output=[]
        n_steps=100
        ds=self.df[['EWMA']]
        normalizer = MinMaxScaler(feature_range=(0,1))
        ds_scaled = normalizer.fit_transform(np.array(ds).reshape(-1,1))
        opn=ds_scaled[:100]
        fut_inp = opn.reshape(1,-1)
        tmp_inp = list(fut_inp)
        tmp_inp = tmp_inp[0].tolist()
        i=0
        n=int(n)
        while(i<n):
            if(len(tmp_inp)>n_steps):
                fut_inp = np.array(tmp_inp[1:])
                fut_inp=fut_inp.reshape(1,-1)
                fut_inp = fut_inp.reshape((1, n_steps, 1))
                yhat = self.model.predict(fut_inp, verbose=0)
                tmp_inp.extend(yhat[0].tolist())
                tmp_inp = tmp_inp[1:]
                lst_output.extend(yhat.tolist())
                i=i+1
            else:
                fut_inp = fut_inp.reshape((1, n_steps,1))
                yhat = self.model.predict(fut_inp, verbose=0)
                tmp_inp.extend(yhat[0].tolist())
                lst_output.extend(yhat.tolist())
                i=i+1
        lst_output=[x[0] for x in lst_output]
        return lst_output
    
    def prediction_data(self,days,end_date):
        ds=self.df[['EWMA']].values
        normalizer = MinMaxScaler(feature_range=(0,1))
        normalizer.fit_transform(np.array(ds).reshape(-1,1))
        lst=stockPrediction.prediction(self,n=days)
        lst=normalizer.inverse_transform(np.array(lst).reshape(1,-1))
        lst=list(list(lst)[0])
        test_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        date_generated = pd.bdate_range(test_date, periods=len(lst)).strftime("%Y-%m-%d")
        df1=pd.DataFrame(list(zip(date_generated,lst)),columns=['Date','Prediction'])
        return df1

    