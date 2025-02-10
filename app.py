import panel as pn
from datetime import datetime
import math
import numpy as np
import pandas as pd
import panel as pn
pn.extension("tabulator")
import hvplot.pandas
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json

url1 = "https://raw.githubusercontent.com/Teekaynium/ZimStock-Project/refs/heads/main/archive-single-file/close_price.json"
url2 = "https://raw.githubusercontent.com/Teekaynium/ZimStock-Project/refs/heads/main/archive-single-file/vol_traded.json"
close_resp = requests.get(url1)
vol_resp = requests.get(url2)

voljson = json.loads(vol_resp.text)
closejson = json.loads(close_resp.text)

def json_convert(data):    

    df = pd.DataFrame(data["data"],data["index"],data["columns"])
    return df

close_price = json_convert(closejson)
close_price = close_price.astype(float)

vol_traded = json_convert(voljson)
vol_traded = vol_traded.astype(float)  


def drop_duplicates(df):
    """converts iso date str to %Y-%m-%d datetime"""
    # creating an empty list to place shortened date
    d_f = df.copy()
    d = []
    # for loop to slice date to just year-month-date
    for x in df.index:
    
        v = x[:10]
        d.append(v)

    # creating an empty list to place string transformed to datetime object
    dates = []
    
    # for loop to convert each date entry into datetime object
    for i in d:
        new_date = datetime.strptime(i,'%Y-%m-%d').date()
        dates.append(new_date)
        
    # adding a column of converted dates to the df
    d_f["dates"] = d
    # dropping duplicate days
    d_f = d_f.drop_duplicates()
    # sorting values in ascending order by date
    d_f = d_f.sort_values(by = ["dates"])
    # setting dates column to index
    d_f.index = d_f["dates"]
    # removing dates column
    d_f = d_f.drop(columns = ["dates"], axis = 1)

        
    return d_f

vol_tradd = drop_duplicates(vol_traded)

def convert_date(df):
    """converts iso date str to %Y-%m-%d datetime"""
    # creating an empty list to place shortened date
    d_f = df.copy()
    d = []
    # for loop to slice date to just year-month-date
    for x in df.index:
    
        v = x[:10]
        d.append(v)

    # creating an empty list to place string transformed to datetime object
    dates = []
    
    # for loop to convert each date entry into datetime object
    for i in d:
        new_date = datetime.strptime(i,'%Y-%m-%d').date()
        dates.append(new_date)

    # adding a column of converted dates to the df
    d_f["dates"] = dates
    d_f.index = d_f["dates"]

    # removing dates column
    d_f = d_f.drop(columns = ["dates"], axis = 1)
    return d_f


def get_returns(start_date, end_date,df):
    """ this function turns a df of security price to returns"""
    # calculating percentage difference between successive days
    returns_df = drop_duplicates(df).loc[start_date: end_date].pct_change()*100
    # removing the first line of new df
    returns_df = returns_df[1:]
    return returns_df

def compare_returns(start_date, end_date,df):
    """ this function gives a statistical overview of the df, 
    i.e., calculates average returns, volatility, variance, sharp ratios"""

    # calling get_returns function
    returns = get_returns(start_date[:10], end_date[:10],df)
    # calculating daily stdev of each asset's return for current period
    stdev_ret = returns.std()
    # calculating variance of each asset's return for current period
    var_ret = returns.var()

    # calculating average daily return
    ave_ret = returns.mean()
    # calculating annualised return for the asset
    P_stdev = stdev_ret*np.sqrt(250)
    # calculating annualised return for the period
    period_ret = (((1+ave_ret/100)**(250))-1)*100
    # calculating daily sharp ratio
    Dsharp = ave_ret/stdev_ret
    # calculating sharp ratio for the period
    Psharp = period_ret/P_stdev
    ss = df.iloc[0]
    sss = df.iloc[-1]
    d__f = pd.concat([ave_ret, period_ret, var_ret,stdev_ret, P_stdev,Dsharp, Psharp], axis = 1)
    d__f.columns = ["Average Daily Return", "Annualised Return","Variance", "Daily Standard Dev",
                    "Annualised Standard Dev", "Daily Sharp Ratio", "Annual Sharp Ratio"]
    return d__f.round(2)

table1 = compare_returns(close_price.index[0],close_price.index[-1],close_price).T

close2 = convert_date(close_price)
idf = close2.interactive()
vol2 = convert_date(vol_traded)
idfv = vol2.interactive()


def price_graph(df, col):

    if df[col].iloc[0]> df[col].iloc[-1]:
        x = "red"  
    elif df[col].iloc[0] == df[col].iloc[-1]:
        x = "orange"
    else:
        x = "green"
    graph = df.hvplot(x = "dates",
                      y = col,line_width = 2,title = col,
                      bgcolor = "lightgray",
                      c = x).opts(xticks = 20,
                                  xrotation = 45,axiswise = True,
                                  ylabel = "Security Price (ZiG$-cents)",
                                  width = 600, margin = (0,25))
    return graph

close_variable_widget = pn.widgets.Select(name="variable",
                                    value="Econet Wireless Zimbabwe Limited",
                                    options=list(close2.columns))

bound_close = pn.bind(
    price_graph, col=close_variable_widget, df = close2)

widgets = pn.Column(close_variable_widget,sizing_mode="stretch_height", width=300)
pn.Column(widgets, bound_close)

def vol_graph(df, col):
    graph = df.hvplot(x = "dates",
                  y = col,line_width = 2,title = col,
                     bgcolor = "lightblue",c = "black").opts(ylabel = "Volume of trades",
                                                             xticks = 20,xrotation = 45,
                                                             axiswise = True, 
                                                             width = 600, margin = (0,25))
    return graph

vol_variable_widget = pn.widgets.Select(name="variable",
                                    value="Econet Wireless Zimbabwe Limited",
                                    options=list(vol2.columns))
bound_vol = pn.bind(
    vol_graph, col=close_variable_widget, df = vol2)
bound_vol

def table(df,col):
    new_df = pd.DataFrame(df[col])
    stats_table = pn.widgets.Tabulator(new_df,
                                       layout = "fit_columns",
                                       name="Table",header_align='center',
                                       text_align={'index': 'center', col: 'center'},
                                       widths=200
)
    return stats_table

table_variable_widget = pn.widgets.Select(name="variable",
                                    value="Econet Wireless Zimbabwe Limited",
                                    options=list(table1.columns))

bound_table = pn.bind(table, col=close_variable_widget, df = table1)
bound_table

# Instantiate the template with widgets displayed in the sidebar
template = pn.template.FastListTemplate(
    title="Zim Stocks Analysis",
    sidebar=[pn.pane.Markdown("# Zimbabwe Stock Exchange Data"),
             pn.pane.Markdown("### This dashboard provides insight into the movements of the Zimbabwe Equity market. The dashboard contains data on stock prices, traded volumes and offers a brief financial statistical analysis."),
             pn.pane.Markdown("# Choose Stock Below:"),
             widgets], 
    main = [pn.Row(pn.Column(bound_close,bound_vol),bound_table)],
    accent_base_color = "#88d8b0",
    header_background = "#88d8b0",
)
    
# Append a layout to the main area, to demonstrate the list-like API

template.servable();


