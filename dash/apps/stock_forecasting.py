# import pandas_datareader.data as web
import datetime
import pandas as pd

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output,State
import pathlib

# from fbprophet import Prophet
import plotly.offline as py
import datetime
# import json
# from fbprophet.serialize import model_to_json, model_from_json


from app import app


# Data scraping
# https://pandas-datareader.readthedocs.io/en/latest/remote_data.html#remote-data-stooq
# start = datetime.datetime(2020,1,1)
# end=datetime.datetime(2020,12,3)
# df=web.DataReader(['AMZN','GOOGL','FB'], 'stooq',start=start,end=end)
# df=df.stack().reset_index()
# # df.unstack().reset_index()
# print(df.head())
# df.to_csv("stock.csv",index=False)

PATH=pathlib.Path(__file__).parent
DATA_PATH=PATH.joinpath("../datasets").resolve()


df=pd.read_csv(DATA_PATH.joinpath("stock.csv"))
df['year_month']=pd.to_datetime(df['Date']).dt.strftime('%Y-%m')


#layout
layout=dbc.Container([

	# navigation
	dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("World GDP Analysis", active=True,href="/apps/world_gdp_analysis")),
        dbc.NavItem(dbc.NavLink("Stock Market Analysis", active=True,href="/apps/stock_forecasting")),
        dbc.NavItem(dbc.NavLink("Tweets Analysis", active=True,href="/apps/tweet_analysis")),
        dbc.NavItem(dbc.NavLink("Topic Modeling", active=True, href="/apps/topic_modeling"))
    ], 
    brand="Stock Market Forecasting",
    brand_href="/apps/home",
    color="primary",
    dark=True,
    style={'margin-bottom': '5px'}
	),#end navigation

# prompts row
	dbc.Row([
		# start sidebar
		dbc.Col([

			dcc.Dropdown(id='my-dpdn', multi=False, value='AMZN',
			options=[{'label':x,'value':x} for x in sorted(df['Symbols'].unique())],
			style={'margin-bottom': '15px'}),

			dbc.Select(
			id="forecasting-frequency",value='6', options=[
	        {"label": "1", "value": "1"},
	        {"label": "2", "value": "2"},
	        {"label": "3",  "value": "3"},
	        {"label": "4", "value": "4"},
	        {"label": "5", "value": "5"},
	        {"label": "6",  "value": "6"},
	        {"label": "7", "value": "7"},
	        {"label": "8", "value": "8"},
	        {"label": "9",  "value": "9"},
	        {"label": "10", "value": "10"},
	        {"label": "11", "value": "11"},
	        {"label": "12", "value": "12"},
	        {"label": "13",  "value": "13"},
	        {"label": "14", "value": "14"},
	        {"label": "15", "value": "15"},
	        {"label": "16",  "value": "16"},
	        {"label": "17", "value": "17"},
	        {"label": "18", "value": "18"},
	        {"label": "19",  "value": "19"},
	        {"label": "20", "value": "20"},
	        {"label": "21", "value": "21"},
	        {"label": "22", "value": "22"},
	        {"label": "23",  "value": "23"},
	        {"label": "24", "value": "24"}
	        ],style={'margin-bottom': '5px'}	          
	          ),

			dcc.Dropdown(id='my-dpdn2',multi=True, value=df['Symbols'].unique(),
			options=[{'label':x,'value':x} for x in sorted(df['Symbols'].unique())],
			style={'margin-bottom': '10px'}),

			dcc.Dropdown(id='year-dropdown', multi=True, 
				value=df['year_month'].unique(),
			options=[{'label':x,'value':x} for x in sorted(df['year_month'].unique())],
			style={'margin-bottom': '10px'}),

			dcc.RadioItems(id='xlog_multi_type', 
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'},
                style={'margin-bottom': '2px'})
		],
		md=3,
		style={'margin-bottom': '2px','margin-top': '2px','margin-left': '0px','border-style': 'solid','border-color': 'green'}
		),
		# end sidebar
	dbc.Col([
		dcc.Graph(id='line-fig', figure={})
		], md=9)
	], no_gutters=True,
	style={'height': '400px','margin-bottom': '1px'}),

# row 2 start
	dbc.Row([
		dbc.Col([
			dcc.Graph(id='line-fig2',figure={})
			]),
		dbc.Col([
			dcc.Graph(id='stackedbar-fig',figure={})
			]),
		], no_gutters=True,
		style={'height': '400px','margin-bottom': '2px'}),
	#row 2 end

	# row 3 start
	dbc.Row([
		dbc.Col([
			# dcc.Graph(id='forecasting_table',figure={})
			], md=0),
		dbc.Col([
			dcc.Graph(id='forecasting_graph_table',figure={})
			], md=12),
		dbc.Col([
			# dcc.Graph(id='forecasting_graph',figure={})
			], md=0),
		], no_gutters=True,
		style={'margin-bottom': '2px'}
		),
	#row 3 end

# row 1 start
dbc.Row([
	dbc.Col([
	
		]),
	], no_gutters=True),
# row 1 end

	  # footer
 		dbc.Row(
            [
                dbc.Col(html.Div("@galaxydataanalytics "),
                	style={
            'margin-top': '2px',
            'text-align':'center',
            'backgroundColor': 'rgba(120,120,120,0.2)'
            },
                 md=12)
            ]
        ),
        #end footer


	],
	fluid=True
	)


@app.callback(
Output('line-fig' , 'figure'),
Input('my-dpdn', 'value'),
Input('year-dropdown', 'value')
)
def update_graph(stock_slctd,date_selected):
	dff=df[df['Symbols'].isin([stock_slctd]) & df['year_month'].isin(date_selected)]
	fig=go.Figure()
	fig.add_trace(go.Scatter(x=dff['Date'], y=dff['High'], name='High',line = dict(color='green'))) #dash='dash' to add line style
	fig.add_trace(go.Scatter(x=dff['Date'], y=dff['Low'], name='Low',line = dict(color='firebrick')))
	fig.add_trace(go.Scatter(x=dff['Date'], y=dff['Open'], name='Open',line = dict(color='orange')))
	fig.add_trace(go.Scatter(x=dff['Date'], y=dff['Close'], name='Close',line = dict(color='royalblue')))
	fig.update_xaxes(rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        			])
    				)
				)
	fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=0,b=0,l=0,r=0),height=400,
		title={'text': stock_slctd,'y':0.75,'x':0.4,'xanchor': 'center','yanchor': 'middle'})
	
	return fig

@app.callback(
Output('line-fig2' , 'figure'),
Input('my-dpdn2', 'value'),
Input('xlog_multi_type', 'value'),
Input('year-dropdown', 'value'),
prevent_initial_call=False)
def update_multi_graph(multi_stock_slctd,xlog_multi_type,date_selected):
	dff=df[df['Symbols'].isin(multi_stock_slctd) & df['year_month'].isin(date_selected)]	
	figln=px.line(dff,x='Date', y='High',color='Symbols',height=400)
	figln.update_yaxes(type='linear' if xlog_multi_type == 'Linear' else 'log')
	figln.update_xaxes(rangeslider_visible=False,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        			])
    				)
				)
	figln.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=0,b=0,l=0,r=0))
	return figln

	# 
@app.callback(
Output('stackedbar-fig' , 'figure'),
Input('my-dpdn2', 'value'),
Input('year-dropdown', 'value'),
Input('xlog_multi_type', 'value'),
prevent_initial_call=False)
def update_stackedbar_graph(multi_stock_slctd,date_selected,xlog_multi_type):
	stock_stacked_df=pd.DataFrame(df.groupby(['year_month','Symbols'],as_index=False)['High'].mean()) #.sort_values(by=['gdpPercap'], ascending=True)
	dff=stock_stacked_df[stock_stacked_df['Symbols'].isin(multi_stock_slctd) & stock_stacked_df['year_month'].isin(date_selected)]	
	stacked_barchart=px.bar(dff,x='year_month',y='High',color='Symbols',text='High',height=400)
	stacked_barchart.update_yaxes(type='linear' if xlog_multi_type == 'Linear' else 'log')
	stacked_barchart.update_xaxes(rangeslider_visible=False,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        			])
    				)
				)
	stacked_barchart.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=0,b=0,l=0,r=0)) #use barmode='stack' when stacking,

	return stacked_barchart

