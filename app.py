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
# global articles_df
global dfff



def aggregate_fun(df,agg):
    df['Total Articles Read'] = len(df['article_id'].unique())
    df['Total Sessions'] = df['t_sessions'].sum()
    df['Total Users'] = df['t_users'].sum()
    df['Total Views'] = df['t_visits'].sum()
    return df[[agg,'Total Sessions','Total Articles Read','Total Users','Total Views']]




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css','https://codepen.io/chriddyp/pen/brPBPO.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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
    html.Div([html.Label('Domain Selected',className = 'two columns'),dcc.Dropdown(id='filter_domain', multi=True,className = 'ten columns')],className='row'),
    html.Div([html.Label('Category Selected',className = 'two columns'),dcc.Dropdown(id='filter_category', multi=True,className = 'ten columns')],className='row'),
    html.Div([html.Label('Geolocation Selected',className = 'two columns'),dcc.Dropdown(id='filter_geo', multi=True,className = 'ten columns')],className='row'),
    html.Div([html.Label('Traffic Source Selected',className = 'two columns'),dcc.Dropdown(id='filter_source', multi=True,className = 'ten columns')],className='row'),

    #Filter Hidden Data\
    html.Div(id='filters',style = {'display': 'none'}),
    html.Button(id='filter_button',n_clicks = 0, children = 'Filter Data'),
    #Over ALL Traffic
    html.Div([ dcc.Graph(id = 'Overall Traffic',className = 'twelve columns')],className='row')
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
    dfff = pd.merge(df_main,pd.read_csv('Tables/articles+shared.csv',dtype={'article_id':str}),how='inner',on='article_id',indicator=True)
    dfff = dfff[(dfff['da_traffic'] >= date_start) & (dfff['da_traffic'] <= date_end)]
    return 0


#Filters
#Domain

@app.callback(
    dash.dependencies.Output(component_id='filter_domain', component_property='options'),
    [dash.dependencies.Input(component_id='meaww_filter', component_property='value'),
     dash.dependencies.Input(component_id='data_frame', component_property='data-*')] )
def filter_domain(meaww_filter,data_frame):
    global dfff
    domain = list(dfff['domain'].unique())
    domain.append('All')
    dd = [{'label': i, 'value': i} for i in domain]
    if meaww_filter == 'meaww':
        return [d for d in dd if d.get('label') != 'meaww']
    else:
        return dd
#Domain Initial Value
@app.callback(
    dash.dependencies.Output(component_id = 'filter_domain', component_property = 'value'),
    [dash.dependencies.Input(component_id = 'filter_domain', component_property = 'options'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*')])
def set_domain_value(filter_domain, data_frame):
        return ['All']


#CATEGORY
@app.callback(
    dash.dependencies.Output(component_id = 'filter_category', component_property = 'options'),
    [dash.dependencies.Input(component_id = 'meaww_filter', component_property = 'value'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*')])
def filter_category(meaww_filter, data_frame):
    global dfff
    category = list(dfff['category'].unique())
    category.append('All')
    cc = [{'label': i, 'value': i} for i in category]
    if meaww_filter == 'meaww':
        return [c for c in cc if c.get('label') != 'meaww']
    else:
        return cc
@app.callback(
    dash.dependencies.Output('filter_category', 'value'),
    [dash.dependencies.Input('filter_category', 'options'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*')])
def set_category_value(filter_category, data_frame):
        return ['All']


#Geolocation
@app.callback(
    dash.dependencies.Output(component_id = 'filter_geo', component_property = 'options'),
    [dash.dependencies.Input(component_id = 'meaww_filter', component_property = 'value'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*')])

def filter_geo(meaww_filter, data_frame):
    global dfff
    geo = list(dfff['geolocation'].unique())
    geo.append('All')
    gg = [{'label': i, 'value': i} for i in geo]
    return gg
@app.callback(
    dash.dependencies.Output(component_id = 'filter_geo', component_property = 'value'),
    [dash.dependencies.Input(component_id = 'filter_geo', component_property = 'options'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*')])
def set_geo_value(filter_geo, data_frame):
        return ['All']


#Traffic Source
@app.callback(
    dash.dependencies.Output(component_id = 'filter_source', component_property = 'options'),
    [dash.dependencies.Input(component_id = 'meaww_filter', component_property = 'value'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*')])
def filter_source(meaww_filter, data_frame):
    global dfff
    ts = list(dfff['traffic_source'].unique())
    ts.append('All')
    tss = [{'label': i, 'value': i} for i in ts]
    return tss
@app.callback(
    dash.dependencies.Output(component_id = 'filter_source', component_property = 'value'),
    [dash.dependencies.Input(component_id = 'filter_source', component_property = 'options'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*')])
def set_source_value(filter_source, data_frame):
        return ['All']

#Combining Filters
@app.callback(
    dash.dependencies.Output(component_id='filters', component_property='data-*'),
    [dash.dependencies.Input(component_id='filter_button', component_property='n_clicks')],
    [dash.dependencies.State(component_id='filter_domain', component_property='value'),
     dash.dependencies.State(component_id='filter_category', component_property='value'),
     dash.dependencies.State(component_id='filter_geo', component_property='value'),
     dash.dependencies.State(component_id='filter_source', component_property='value')])

def combine_filters(filter_button,filter_domain,filter_category,filter_geo,filter_source):
    fil_ter = { 'domain':filter_domain, 'category':filter_category, 'geolocation':filter_geo, 'traffic_source':filter_source }
    # print fil_ter
    return fil_ter


#Traffic Graph
@app.callback(
    dash.dependencies.Output(component_id = 'Overall Traffic', component_property = 'figure'),
    [dash.dependencies.Input(component_id = 'date_start', component_property = 'date'),
     dash.dependencies.Input(component_id = 'date_end', component_property = 'date'),
     dash.dependencies.Input(component_id = 'meaww_filter', component_property = 'value'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*'),
     dash.dependencies.Input(component_id = 'filters', component_property = 'data-*')])

def Date_Graph(date_start, date_end, meaww_filter, data_frame, filters):
    print filters
    global dfff
    traffic = dfff
    if meaww_filter == 'meaww':
        traffic = traffic[traffic['domain']!='meaww']
    if filters != {u'category': None, u'geolocation': None, u'domain': None, u'traffic_source': None}:
        for key,values in filters.iteritems():
            if values != ['All'] and values != []:
                traffic = traffic[traffic[key].isin(values)]
    traffic = traffic.groupby('da_traffic').apply(aggregate_fun,'da_traffic').drop_duplicates()
    traffic = traffic.sort_values(by = 'da_traffic', ascending = True)
    traffic = traffic[(traffic['da_traffic'] >= str(date_start)) & (traffic['da_traffic'] <= str(date_end))]
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
    fig = {'data': data,'layout':layout}
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)
