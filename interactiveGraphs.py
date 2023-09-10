import plotly.graph_objects as go

class InteractiveGraphs():

    def __init__(self) -> None:
        pass

    def basicGraph(self,df,input_df,options):
        fig = go.Figure(data=[go.Candlestick(x=df['stockdate'], open=df["open"], 
                    high=df["high"],low=df["low"], close=df["close"],name='Stock Chart')],layout=dict(
        legend=dict(groupclick="toggleitem"),
        ))
        if 'Simple Moving Average(SMA)' in options:
            fig.add_trace(go.Scatter(x=df['stockdate'], y=df['SMA'],name='SMA',line=dict(color='firebrick', width=2)))
        if 'Exponential Weightage Moving Average(EWMA)' in options:
            fig.add_trace(go.Scatter(x=df['stockdate'], y=df['EWMA'],name='EWMA',line=dict(color='royalblue', width=2)))
        fig.update_xaxes(
            rangeslider_visible=False,
            range=[input_df['start_date'][0],input_df['end_date'][0]],
            rangebreaks=[
                dict(bounds=["sat", "mon"]), 
                dict(values=["2020-12-25", "2021-01-01","2010-07-05"])
            ]
        )

        fig.update_layout(autosize=False,height=600,template="plotly_dark")
        return fig
    
    def prediction_chart(self,df,input_df,n,st,name,i1):
        n=int(n)
        fig = go.Figure(
        layout=dict(
            legend=dict(groupclick="toggleitem"),
        )
        )
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Prediction'],name='Opening price',line=dict(color='green', width=2)))
        
        if i1:
            fig.add_trace(go.Scatter(x=df.iloc[:n]['Date'], y=df.iloc[:n]['Prediction'],name='Prediction price',line=dict(color='orange', width=2)))
            fig.update_xaxes(
            rangeslider_visible=False,
            range=[df.Date.values[-1],df.Date.values[0]],
            rangebreaks=[
                dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
                dict(values=["2020-12-25", "2021-01-01","2010-07-05"])  # hide holidays (Christmas and New Year's, etc)
            ]
        )
        else:
            fig.update_xaxes(
                rangeslider_visible=False,
                range=[input_df['start_date'][0],input_df['end_date'][0]],
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
                    dict(values=["2020-12-25", "2021-01-01","2010-07-05"])  # hide holidays (Christmas and New Year's, etc)
                ]
            )

        fig.update_layout(title=f"{name} stock chart",autosize=True,template="plotly_dark")
        return fig


    
