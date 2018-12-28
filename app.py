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
global dfff,temp_df


def aggregate_fun(df,agg):
    df['Total Articles Read'] = len(df['article_id'].unique())
    df['Total Sessions'] = df['t_sessions'].sum()
    df['Total Users'] = df['t_users'].sum()
    df['Total Views'] = df['t_visits'].sum()
    return df[[agg,'Total Sessions','Total Articles Read','Total Users','Total Views']]



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css','https://codepen.io/chriddyp/pen/brPBPO.css','https://raw.githubusercontent.com/varunsingh1996/pubninja-analytics/master/dashboard_style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dfff = pd.DataFrame()


app.layout = html.Div([
    #Data Hidden Div
    html.Div(id='data_frame',style = {'display': 'none'}),
    #Header
    html.Div([
            html.Div(
                [
                    html.H4(children = 'Analytics Dashboard', className = 'nine columns', style={'float':'left'}),
                    html.Img(src='https://pubninja.com/assets/images/logo.png',className='three columns',style={'height':'15%','width':'15%','float':'right','position':'relative','background-color':'black','margin':'10px'})
                ],className = 'row'),
            # Date Select
            html.Div([
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
                    ],className='three columns',style={'float':'left'}),
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
                    ],className='four columns',style={'float':'right','width': '23.666667%'})
            ],className = 'row')
        ],className = 'top-nav', style = {'position': 'fixed','top': '0','height': 'inherit', 'width': '100%', 'background-color': 'black','color':'white' ,'zIndex': 9999999999}),
    #body
    html.Div([
        #Filter List
        html.Div([
            html.H4('Filters'),
            html.Hr(),html.Label('Domain Selected',style = {}),dcc.Dropdown(id='filter_domain', multi=True,style={'color':'black'}),
            html.Label('Category Selected'),dcc.Dropdown(id='filter_category', multi=True, style={'color':'black'}),
            html.Label('Geolocation Selected'),dcc.Dropdown(id='filter_geo', multi=True, style={'color':'black'}),
            html.Label('Traffic Source Selected'),dcc.Dropdown(id='filter_source', multi=True, style={'color':'black'}),
            html.Br(),
            html.Button(id='filter_button',n_clicks = 0, children = 'Filter Data', style = {'background-color':'white'}),
            #Filter Hidden Data
            html.Div(id='filters',style = {'display': 'none'})
            ],className = 'three columns', style = {'padding': '0 5px','position': 'fixed', 'width': ' 250px','height':'100vh','left': '8px','right': '0px','overflow-y': 'scroll','background-color': '#411b09','color':'white','top':'146px'}),

        html.Div([
            #Over All Counts
            html.Div(id = 'overall_count',className = 'row', style = {'text-align':'center','color':'white'}),
            html.Br(),
            #Over ALL Traffic
            html.Div([ dcc.Graph(id = 'Overall Traffic')],className = 'twelve columns', style = {'margin-top': '40px'}),
            #Articles Shared
            html.Div([ dcc.Graph(id = 'article_shared')],className = 'twelve columns', style = {'margin-top': '40px'}),
            #Domain Traffic
            html.Div([ dcc.Graph(id = 'domain_traffic')],className = 'twelve columns', style = {'margin-top': '40px'}),
            #Category Traffic
            html.Div([dcc.Graph(id = 'category_traffic')],className = 'twelve columns',style={'margin-top': '40px'}),
            #Source and Geolocation Traffic
            html.Div([
                #Geolocation
                html.Div([dcc.Graph(id = 'geo_traffic')],className = 'six columns',style={'float': 'left'}),
                #Source
                html.Div([dcc.Graph(id = 'source_traffic')],className = 'six columns',style={'float': 'right'})
            ],className = 'twelve columns',style = {'margin-top': '40px'}),
            #Articles Updates
            html.Div([dcc.Graph(id = 'articles_update')],className = 'twelve columns',style={'margin-top': '40px'})

            ],className = 'nine columns',style = {'top': '138px', 'padding':'10px 30px', 'float': 'left', 'overflow-y': 'scroll','left': '240px',
            'height':'100vh','background-color': '#411b09','z-index':'-1','opacity':'1', 'position': 'relative'})
        ],className = 'row')

    #First Pie
    # html.Div([ dcc.Graph(id = 'Overall Traffic',className = 'twelve columns')],className='row')

],className = 'row', style = {'width': '100%'})


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
    global articles_df
    articles_df = pd.read_csv('Tables/articles+shared.csv')
    global dfff
    dfff = pd.merge(df_main,pd.read_csv('Tables/articles+shared.csv',dtype={'article_id':str}),how='inner',on='article_id',indicator=True)
    dfff = dfff[(dfff['da_traffic'] >= date_start) & (dfff['da_traffic'] <= date_end)]
    print 'dataframe changed'
    return 0


#Filters
#Domain

@app.callback(
    dash.dependencies.Output(component_id='filter_domain', component_property='options'),
    [dash.dependencies.Input(component_id='meaww_filter', component_property='value'),
     dash.dependencies.Input(component_id='data_frame', component_property='data-*')])
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
        print 'domain value set to ALL'
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
    dash.dependencies.Output(component_id = 'filter_category', component_property = 'value'),
    [dash.dependencies.Input(component_id = 'filter_category', component_property = 'options'),
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
    dash.dependencies.Output(component_id = 'filters', component_property = 'data-*'),
    [dash.dependencies.Input(component_id = 'filter_button', component_property = 'n_clicks'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*')],
    [dash.dependencies.State(component_id = 'filter_domain', component_property = 'value'),
     dash.dependencies.State(component_id = 'filter_category', component_property = 'value'),
     dash.dependencies.State(component_id = 'filter_geo', component_property = 'value'),
     dash.dependencies.State(component_id = 'filter_source', component_property = 'value')])

def combine_filters(filter_button, data_frame, filter_domain, filter_category, filter_geo, filter_source):
    fil_ter = { 'domain':filter_domain, 'category':filter_category, 'geolocation':filter_geo, 'traffic_source':filter_source }
    print 'combine filters called'
    return fil_ter

#Count Overall
@app.callback(
    dash.dependencies.Output(component_id = 'overall_count', component_property = 'children'),
    [dash.dependencies.Input(component_id = 'date_start', component_property = 'date'),
     dash.dependencies.Input(component_id = 'date_end', component_property = 'date'),
     dash.dependencies.Input(component_id = 'meaww_filter', component_property = 'value'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*'),
     dash.dependencies.Input(component_id = 'filters', component_property = 'data-*')])

def count_overall(date_start, date_end, meaww_filter, data_frame, filters):
    print 'Count Overall Called'
    print filters
    global dfff
    traffic = dfff
    if meaww_filter == 'meaww':
        traffic = traffic[traffic['domain']!='meaww']
    if filters != {u'category': None, u'geolocation': None, u'domain': None, u'traffic_source': None}:
        for key,values in filters.iteritems():
            if values != ['All'] and values != [] and values != None:
                traffic = traffic[traffic[key].isin(values)]
    total_session = traffic['t_sessions'].sum()
    total_articles_read = len(traffic['article_id'].unique())
    total_articles_shared = len(list(traffic[(traffic['min'] >= date_start) & (traffic['min'] <= date_end)]['article_id'].unique()))
    return [html.Div([html.H6('Sessions'),
                  html.H2(total_session,style = {'background-color':'white','height':'100%', 'border-radius': '20%', 'color':'#1bd51b'})
            ],className = 'four columns'),
            html.Div([html.H6('Articles Read'),
                  html.H2(total_articles_read,style = {'background-color':'white','height':'100%', 'border-radius': '20%', 'color':'#ab3a04'})
            ],className = 'four columns'),
            html.Div([html.H6('Articles Shared'),
                  html.H2(total_articles_shared,style = {'background-color':'white','height':'100%', 'border-radius': '20%', 'color':'#ff91a4'})
            ],className = 'four columns')]

#Traffic Graph
@app.callback(
    dash.dependencies.Output(component_id = 'Overall Traffic', component_property = 'figure'),
    [dash.dependencies.Input(component_id = 'date_start', component_property = 'date'),
     dash.dependencies.Input(component_id = 'date_end', component_property = 'date'),
     dash.dependencies.Input(component_id = 'meaww_filter', component_property = 'value'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*'),
     dash.dependencies.Input(component_id = 'filters', component_property = 'data-*')])

def Date_Graph(date_start, date_end, meaww_filter, data_frame, filters):
    print 'Date Graph function called with below filters'
    print filters
    global dfff
    traffic = dfff
    if meaww_filter == 'meaww':
        traffic = traffic[traffic['domain']!='meaww']
    if filters != {u'category': None, u'geolocation': None, u'domain': None, u'traffic_source': None}:
        for key,values in filters.iteritems():
            if values != ['All'] and values != [] and values != None:
                traffic = traffic[traffic[key].isin(values)]
    global temp_df
    temp_df = traffic
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
    layout = go.Layout(title='PubNinJa Over All Traffic',
                       yaxis=dict(title='Articles Read'),
                       yaxis2=dict(title='Number of Sessions\Views\Users',
                       titlefont=dict(color='rgb(148, 103, 189)'),
                       tickfont=dict(color='rgb(148, 103, 189)'),
                       overlaying='y',
                       side='right')
                      )
    fig = {'data': data,'layout':layout}
    return fig

#Articles Shared Graph
@app.callback(
    dash.dependencies.Output(component_id = 'article_shared', component_property = 'figure'),
    [dash.dependencies.Input(component_id = 'date_start', component_property = 'date'),
     dash.dependencies.Input(component_id = 'date_end', component_property = 'date'),
     dash.dependencies.Input(component_id = 'meaww_filter', component_property = 'value'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*'),
     dash.dependencies.Input(component_id = 'filters', component_property = 'data-*')])

def Article_Shared_Graph(date_start, date_end, meaww_filter, data_frame, filters):
    print 'Article_Shared_Graph function called with below filters'
    print filters
    global dfff
    traffic = dfff
    if meaww_filter == 'meaww':
        traffic = traffic[traffic['domain']!='meaww']
    if filters != {u'category': None, u'geolocation': None, u'domain': None, u'traffic_source': None}:
        for key,values in filters.iteritems():
            if values != ['All'] and values != [] and values != None:
                traffic = traffic[traffic[key].isin(values)]
    global temp_df
    temp_df = traffic
    traffic = traffic[(traffic['min'] >= date_start) & (traffic['min'] <= date_end)]
    print "this is column list of articles graph traffic"
    print list(traffic)
    traffic = traffic[['domain','category','min','article_id']].drop_duplicates().groupby(['domain','category','min']).count().reset_index()
    traffic.columns = ['domain','category','Date','Articles Shared']
    final = []
    ffff = pd.pivot_table(traffic,index="Date",columns="category", values='Articles Shared').reset_index()
    ffff = ffff.sort_values(by='Date',ascending = True)
    value_li = list(ffff)
    for i in value_li[1:]:
        temp = go.Bar( x=ffff['Date'], y=ffff[i], name=i, opacity=0.6)
        final.append(temp)
    layout = go.Layout(title='PubNinJa Articles Shared',
                       yaxis=dict(title='Number of Articles Shared'),
                       barmode='stack')
    fig = {'data': final,'layout':layout}
    return fig


#Domain Traffic
@app.callback(
    dash.dependencies.Output(component_id = 'domain_traffic', component_property = 'figure'),
    [dash.dependencies.Input(component_id = 'date_start', component_property = 'date'),
     dash.dependencies.Input(component_id = 'date_end', component_property = 'date'),
     dash.dependencies.Input(component_id = 'meaww_filter', component_property = 'value'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*'),
     dash.dependencies.Input(component_id = 'filters', component_property = 'data-*')])

def Domain_Traffic_Graph(date_start, date_end, meaww_filter, data_frame, filters):
    print 'Domain_Traffic_Graph function called with below filters'
    print filters
    global dfff
    traffic = dfff
    if meaww_filter == 'meaww':
        traffic = traffic[traffic['domain']!='meaww']
    if filters != {u'category': None, u'geolocation': None, u'domain': None, u'traffic_source': None}:
        for key,values in filters.iteritems():
            if values != ['All'] and values != [] and values != None:
                traffic = traffic[traffic[key].isin(values)]
    global temp_df
    temp_df = traffic
    shared_articles = traffic[(traffic['min'] >= date_start) & (traffic['min'] <= date_end)]
    shared_articles = shared_articles[['domain','min']].drop_duplicates().groupby(['domain']).count().reset_index()
    traffic = traffic.groupby('domain').apply(aggregate_fun,'domain').drop_duplicates()
    traffic = traffic[['domain','Total Sessions','Total Users','Total Articles Read']]
    traffic = pd.merge(traffic, shared_articles, on = 'domain', how = 'left')
    traffic.columns = ['domain','Sessions','Users','Articles Read','Articles Shared']
    print "this is column list of Domain_Traffic_Graph traffic"
    print list(traffic)
    data = []
    annotations = []
    label_data = ['Sessions','Users','Articles Read','Articles Shared']
    graph_data = [[{'x': [0.00, 0.21],'y': [0, 1]},[ 0.05,0]],
                 [{'x': [0.24, 0.45],'y': [0, 1]},[0.30,0]],
                 [{'x': [0.49, 0.71],'y': [0, 1]},[0.69,0]],
                 [{'x': [0.75, 0.96],'y': [0, 1]},[0.94,0]]]
    for i in range(0,len(label_data)):
        temp_dict = {
              "labels": list(traffic['domain']),
              "values": list(traffic[label_data[i]]),
              "domain": graph_data[i][0],
              "name": label_data[i],
              "hoverinfo":"label+percent+name+value",
              "textinfo":"none",
              "hole": .4,
              "type": "pie"
            }
        temp_annotation = {"font": {"size": 15},"showarrow": False,"text": label_data[i],"x":graph_data[i][1][0],"y":graph_data[i][1][1]}
        data.append(temp_dict)
        annotations.append(temp_annotation)
    layout = {
            "title":"Domain Traffic",
            "annotations": annotations
        }
    fig = { 'data':data,'layout':layout}
    # print fig
    return fig


#Category Traffic
@app.callback(
    dash.dependencies.Output(component_id = 'category_traffic', component_property = 'figure'),
    [dash.dependencies.Input(component_id = 'date_start', component_property = 'date'),
     dash.dependencies.Input(component_id = 'date_end', component_property = 'date'),
     dash.dependencies.Input(component_id = 'meaww_filter', component_property = 'value'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*'),
     dash.dependencies.Input(component_id = 'filters', component_property = 'data-*')])

def Category_Traffic_Graph(date_start, date_end, meaww_filter, data_frame, filters):
    print 'Categiry_Traffic_Graph function called with below filters'
    print filters
    global dfff
    traffic = dfff
    if meaww_filter == 'meaww':
        traffic = traffic[traffic['domain']!='meaww']
    if filters != {u'category': None, u'geolocation': None, u'domain': None, u'traffic_source': None}:
        for key,values in filters.iteritems():
            if values != ['All'] and values != [] and values != None:
                traffic = traffic[traffic[key].isin(values)]
    global temp_df
    temp_df = traffic
    shared_articles = traffic[(traffic['min'] >= date_start) & (traffic['min'] <= date_end)]
    shared_articles = shared_articles[['category','min']].drop_duplicates().groupby(['category']).count().reset_index()
    traffic = traffic.groupby('category').apply(aggregate_fun,'category').drop_duplicates()
    traffic = traffic[['category','Total Sessions','Total Users','Total Articles Read']]
    traffic = pd.merge(traffic, shared_articles, on = 'category', how = 'left')
    traffic.columns = ['category','Sessions','Users','Articles Read','Articles Shared']
    data = []
    location = [{'x': [0, .48],'y': [0, .49]},
                {'x': [.52, 1],'y': [0, .49]},
                {'x': [0, .48],'y': [.51, 1]},
                {'x': [.52, 1],'y': [.51, 1]}]
    label_data = ['domain','Sessions','Users','Articles Read','Articles Shared']
    for i in range(0,4):
        temp_data = {
                'labels':list(traffic['category']),
                'values':list(traffic[label_data[i+1]]) ,
                'type': 'pie',
                'name': label_data[i+1],
                'domain': location[i],
                'hoverinfo':'label+percent+name+value',
                'textinfo':'none'
            }
        data.append(temp_data)
    fig = {'data':data,
        'layout': {'title': 'Category Traffic', 'showlegend' : True, 'legend' : dict(orientation="h")}}
    return fig


#Geo Traffic
@app.callback(
    dash.dependencies.Output(component_id = 'geo_traffic', component_property = 'figure'),
    [dash.dependencies.Input(component_id = 'date_start', component_property = 'date'),
     dash.dependencies.Input(component_id = 'date_end', component_property = 'date'),
     dash.dependencies.Input(component_id = 'meaww_filter', component_property = 'value'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*'),
     dash.dependencies.Input(component_id = 'filters', component_property = 'data-*')])

def Geo_Traffic_Graph(date_start, date_end, meaww_filter, data_frame, filters):
    print 'Geo_Traffic_Graph function called with below filters'
    print filters
    global dfff
    traffic = dfff
    if meaww_filter == 'meaww':
        traffic = traffic[traffic['domain']!='meaww']
    if filters != {u'category': None, u'geolocation': None, u'domain': None, u'traffic_source': None}:
        for key,values in filters.iteritems():
            if values != ['All'] and values != [] and values != None:
                traffic = traffic[traffic[key].isin(values)]
    global temp_df
    temp_df = traffic
    traffic = dfff
    traffic = traffic[['geolocation','t_sessions']].drop_duplicates().groupby(['geolocation']).sum().reset_index()
    return {"data": [{
                "values": list(traffic['t_sessions']),
                "labels": list(traffic['geolocation']),
                'domain': {'x': [0, 1],'y': [0, 1]},
                "name": "Traffic Geolocation",
                "hoverinfo":"label+percent+name+value",
                "textinfo":"none",
                "hole": .5,
                "type": "pie"
                }],
            "layout": {"title":"Traffic Geolocation", "legend":dict(orientation="h"), "annotations":[{"font": {"size": 10},"showarrow": False,"text": 'Traffic Geolocation',"x": 0.5,"y":0.5 }]}}

#source Traffic
@app.callback(
    dash.dependencies.Output(component_id = 'source_traffic', component_property = 'figure'),
    [dash.dependencies.Input(component_id = 'date_start', component_property = 'date'),
     dash.dependencies.Input(component_id = 'date_end', component_property = 'date'),
     dash.dependencies.Input(component_id = 'meaww_filter', component_property = 'value'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*'),
     dash.dependencies.Input(component_id = 'filters', component_property = 'data-*')])

def Source_Traffic_Graph(date_start, date_end, meaww_filter, data_frame, filters):
    print 'Source_Traffic_Graph function called with below filters'
    print filters
    global dfff
    traffic = dfff
    if meaww_filter == 'meaww':
        traffic = traffic[traffic['domain']!='meaww']
    if filters != {u'category': None, u'geolocation': None, u'domain': None, u'traffic_source': None}:
        for key,values in filters.iteritems():
            if values != ['All'] and values != [] and values != None:
                traffic = traffic[traffic[key].isin(values)]
    global temp_df
    temp_df = traffic
    traffic = dfff
    traffic = traffic[['traffic_source','t_sessions']].drop_duplicates().groupby(['traffic_source']).sum().reset_index()
    return {"data": [{
                "values": list(traffic['t_sessions']),
                "labels": list(traffic['traffic_source']),
                'domain': {'x': [0, 1],'y': [0, 1]},
                "name": "Traffic Source",
                "hoverinfo":"label+percent+name+value",
                "textinfo":"none",
                "hole": .5,
                "type": "pie"
                }],
            "layout": {"title":"Traffic Source",
                    #    "legend":dict(orientation="h"),
                       "annotations":[{"font": {"size": 10},"showarrow": False,"text": 'Traffic Source',"x": 0.5,"y":0.5 }]}}



#source Traffic
@app.callback(
    dash.dependencies.Output(component_id = 'articles_update', component_property = 'figure'),
    [dash.dependencies.Input(component_id = 'date_start', component_property = 'date'),
     dash.dependencies.Input(component_id = 'date_end', component_property = 'date'),
     dash.dependencies.Input(component_id = 'meaww_filter', component_property = 'value'),
     dash.dependencies.Input(component_id = 'data_frame', component_property = 'data-*'),
     dash.dependencies.Input(component_id = 'filters', component_property = 'data-*')])

def Articles_Update(date_start, date_end, meaww_filter, data_frame, filters):
    print 'Source_Traffic_Graph function called with below filters'
    print filters
    global articles_df
    traffic = articles_df
    if meaww_filter == 'meaww':
        traffic = traffic[traffic['domain']!='meaww']
    if filters != {u'category': None, u'geolocation': None, u'domain': None, u'traffic_source': None}:
        for key,values in filters.iteritems():
            if values != ['All'] and values != [] and values != None and key != 'traffic_source':
                traffic = traffic[traffic[key].isin(values)]
    def artice_status_fun(so,traffic):
        temp_df = articles_df[(articles_df[so] >= date_start) & (articles_df[so] <= date_end)]
        temp_df = temp_df[[so,'article_id']].drop_duplicates()
        temp_df[so] = pd.to_datetime(temp_df[so], format='%Y/%m/%d')
        temp_df[so] = temp_df[so].dt.date
        temp_df = temp_df.groupby(so).count().reset_index()
        temp_df.columns = ['Date',so]
        return temp_df
    dfs = [artice_status_fun('dateadded',traffic),artice_status_fun('approval_date',traffic),artice_status_fun('live_date',traffic),artice_status_fun('min',traffic)]
    traffic = reduce(lambda left,right: pd.merge(left,right,on='Date',how='outer'), dfs)
    traffic.columns = ['Date','Added','Approved','Live','Shared']
    trace1 = go.Scatter(x=traffic['Date'], y=traffic['Added'],name='Added')
    trace2 = go.Scatter(x=traffic['Date'], y=traffic['Approved'],name='Approved')
    trace3 = go.Scatter(x=traffic['Date'], y=traffic['Live'],name='Live')
    trace4 = go.Scatter(x=traffic['Date'], y=traffic['Shared'],name='Shared')
    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(title='Article Update',
                       yaxis=dict(title='Number of Articles'))
    fig = {'data': data,'layout':layout}
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
