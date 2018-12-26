import pandas as pd
import numpy as np
import ipywidgets as widgets
import plotly.plotly as py
import plotly
from datetime import datetime as dt
import plotly.graph_objs as go
from IPython.display import display
plotly.tools.set_credentials_file(username='varunpratap', api_key='FTfaaNI30HlESU7X8HIb')


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
global articles_df
global dfff
# import plotly.graph_objs as go
# import pandas as pd


def fun(df):
    df['Total Articles Read'] = len(df['article_id'].unique())
    df['Total Sessions'] = df['t_sessions'].sum()
    df['Total Users'] = df['t_users'].sum()
    df['Total Views'] = df['t_visits'].sum()
    return df[['da_traffic','Total Sessions','Total Articles Read','Total Users','Total Views']]




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
articles_df = pd.read_csv('Tables/articles+shared.csv',dtype={'article_id':str})
dfff = pd.DataFrame()



app.layout = html.Div([
    #Data Hidden Div
    html.Div(id='data_frame',style = {'display': 'none'}),
    #Header
    html.Div(
        [
            html.H4(children = 'Analytics Dashboard', className = 'nine columns', style={'float':'left'}),
            html.Img(src='https://pubninja.com/assets/images/logo.png',className='three columns',style={'height':'15%','width':'15%','float':'right','position':'relative','background-color':'black','margin':'10px'})
        ],className = 'row'),
    # Date Select
    html.Div([
        html.Div(
            [
                html.Label('Select Date Range'),
                dcc.DatePickerSingle(
                    id='date_start',
                    date=dt(2018, 11, 01)),
                    # style= {'float':'right'}),
                dcc.DatePickerSingle(
                    id='date_end',
                    date=dt(2018, 12, 11)
                    # style= {'float':'right'}
                    )
            ],className='nine columns',style={'float':'left'}),
        html.Div(
            [
                html.Label('**Exclude Meaww'),
                dcc.RadioItems(
                    id='meaww_filter',
                    options=[
                        {'label': 'Yes', 'value': 'meaww'},
                        {'label': 'No', 'value': ''}
                    ],
                    value='',
                    labelStyle={'display': 'inline-block'}
                    )
            ],className='three columns',style={'float':'right','width': '12%'})
    ],className='row'),


    #Domain List
    html.Div([html.Label('Domain Selected',className = 'two columns'),dcc.Dropdown(id='domain_list', multi=True,className = 'ten columns')],className='row'),

    #Over ALL Traffic
    html.Div([ dcc.Graph(id = 'Overall Traffic',className = 'twelve columns')],className='row'),

    #First Pie
    # html.Div([ dcc.Graph(id = 'Overall Traffic',className = 'twelve columns')],className='row')

])


#Data Set
@app.callback(
dash.dependencies.Output(component_id='data_frame', component_property='data-*'),
[dash.dependencies.Input(component_id='date_start', component_property='date'),
 dash.dependencies.Input(component_id='date_end', component_property='date')])

def read_data(date_start,date_end):
    #Read data from Csv/Table.
    df_main = pd.DataFrame(columns=['da_traffic', 'article_id', 'geolocation', 'traffic_source', 'tab', 't_visits', 't_users', 't_sessions'])
    if (int(date_end[5:7])-int(date_start[5:7])) > 0:
        for i in range(int(date_start[5:7]),int(date_end[5:7])+1):
            temp_df = pd.read_csv('Tables/Normalise Dump/'+str(i)+'.csv',dtype={'article_id':str})
            df_main = pd.concat([temp_df,df_main])
    else:
        df_main = pd.read_csv('Tables/Normalise Dump/'+date_end[5:7]+'.csv',dtype={'article_id':str})
    #initalizing dataframe.
    global dfff
    dfff = pd.merge(df_main,articles_df,how='inner',on='article_id',indicator=True)
    dfff = dfff[(dfff['da_traffic'] >= date_start) & (dfff['da_traffic'] <= date_end)]
    return 0


#Domain List
@app.callback(
    dash.dependencies.Output(component_id='domain_list', component_property='options'),
    [dash.dependencies.Input(component_id='meaww_filter', component_property='value')] )

def Domain_list(meaww_filter):
    domain = list(articles_df['domain'].unique())
    domain.append('All')
    dd = [{'label': i, 'value': i} for i in domain]
    if meaww_filter == 'meaww':
        return [d for d in dd if d.get('label') != 'meaww']
    else:
        return dd

#Domain Initial Value
@app.callback(
    dash.dependencies.Output('domain_list', 'value'),
    [dash.dependencies.Input('domain_list', 'options')])
def set_domain_value(domain_list):
        return ['All']


#Traffic Graph
@app.callback(
    dash.dependencies.Output(component_id='Overall Traffic', component_property='figure'),
    [dash.dependencies.Input(component_id='date_start', component_property='date'),
     dash.dependencies.Input(component_id='date_end', component_property='date'),
     dash.dependencies.Input(component_id='meaww_filter', component_property='value'),
     dash.dependencies.Input(component_id='data_frame', component_property='data-*'),
     dash.dependencies.Input(component_id='domain_list', component_property='value')])

def Date_Graph(date_start,date_end,meaww_filter,data_frame,domain_list):
    global dfff
    traffic = dfff
    if meaww_filter == 'meaww':
        traffic = traffic[traffic['domain']!='meaww']
    if domain_list != ['All']:
        traffic = traffic[traffic['domain'].isin(domain_list)]
    print list(traffic)
    traffic = traffic.groupby('da_traffic').apply(fun).drop_duplicates()
    traffic = traffic.sort_values(by='da_traffic',ascending=True)
    traffic = traffic[(traffic['da_traffic']>=str(date_start)) & (traffic['da_traffic']<=str(date_end))]
    trace1 = go.Scatter(x=traffic['da_traffic'], y=traffic['Total Sessions'],name='Total Sessions',yaxis='y2')
    trace2 = go.Scatter(x=traffic['da_traffic'], y=traffic['Total Users'],name='Total Users',yaxis='y2')
    trace3 = go.Scatter(x=traffic['da_traffic'], y=traffic['Total Views'],name='Total Views',yaxis='y2')
    trace4 = go.Bar(x=traffic['da_traffic'], y=traffic['Total Articles Read'],name='Articles',
                    marker=dict(color='rgb(255,182,193)'),
    #                 marker=dict(color='rgb(255,182,193)',line=dict(color='rgb(8,48,107)',width=1.5)),
                opacity=0.6)
    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(title='PubNinJa Traffic',
                       yaxis=dict(title='Articles Read'),
                       yaxis2=dict(title='Number of Sessions\Views\Users',
                       titlefont=dict(color='rgb(148, 103, 189)'),
                       tickfont=dict(color='rgb(148, 103, 189)'),
                       overlaying='y',
                       side='right')
                      )
    # py.iplot(data,layout=layout)
    # fig = go.Figure(data=data, layout=layout)
    fig = {'data': data,'layout':layout}
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
