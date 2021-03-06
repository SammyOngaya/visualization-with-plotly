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
import dash_daq as daq #pip install dash-daq
import geopandas
import json
# import dash_leaflet as dl
# import dash_leaflet.express as dlx
import pathlib

from app import app
from app import server

PATH=pathlib.Path(__file__).parent
DATA_PATH=PATH.joinpath("../datasets").resolve()
df=pd.read_csv(DATA_PATH.joinpath("tweets.csv"))

with open(DATA_PATH.joinpath("countries.geojson")) as response:
    country_geojson = json.load(response)

number_of_tweets=df['name'].count()
favourites_count=round(df['favourites_count'].sum()/1000000,2)
unique_users_count=df['name'].nunique()
sentiment_polarity=round(df['sentiment_polarity'].mean(),2)
sentiment_subjectivity=round(df['sentiment_subjectivity'].mean(),2)

# card definition
number_of_tweets_card = [
    dbc.CardBody(
        [
            html.H1(number_of_tweets, className="card-title"),
            html.P("Tweets Count",
                className="card-text",
            ),
        ],
        style={'text-align': 'center'}
    ),
]

favourites_count_card = [
    dbc.CardBody(
        [
            html.H1(favourites_count, className="card-title"),
            html.P(
                "Tweets Likes (Mn)",
                className="card-text",
            ),
        ],
        style={'text-align': 'center'}
    ),
]

unique_users_count_card = [
    dbc.CardBody(
        [
            html.H1(unique_users_count, className="card-title"),
            html.P(
                "Unique Users Tweeted",
                className="card-text",
            ),
        ],
        style={'text-align': 'center'}
    ),
]

sentiment_polarity_card = [
    dbc.CardBody(
        [
            html.H1(sentiment_polarity, className="card-title"),
            html.P(
                "Avg. Sentiment Polarity",
                className="card-text",
            ),
        ],
        style={'text-align': 'center'}
    ),
]
#end card definition


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
    brand="Tweet Analysis",
    brand_href="/apps/home",
    color="primary",
    dark=True,
    style={'margin-bottom': '5px'}
	),#end navigation

# prompts row
	dbc.Row([
		# start sidebar
		dbc.Col([

			dcc.Dropdown(id='country-promptn', multi=False, value='', placeholder='Select Region...',
			# options=[{'label':x,'value':x} for x in sorted(df['Symbols'].unique())],
			style={'margin-bottom': '15px'}),

			dcc.Dropdown(id='user-prompt', multi=False, value='', placeholder='Select Users...',
			# options=[{'label':x,'value':x} for x in sorted(df['Symbols'].unique())],
			style={'margin-bottom': '15px'}),
			dcc.DatePickerRange(
			    id='calendar_prompt',
			    start_date_placeholder_text=min(df['created_at']),
			    end_date_placeholder_text='Select end date',
			    min_date_allowed=datetime.date(2021,1,20),
        		max_date_allowed=max(df['created_at']),
			    display_format='YYYY-MM-DD'
			),
			
   			daq.Gauge( id='sentiment-polarity-gauge', label="Sentiment Polarity", 
				color={"gradient":True,"ranges":{"red":[-1.00,0.03],"blue":[0.03,0.50],"green":[0.50,1.00]}},
				showCurrentValue=True,
				max=1,min=-1,
				value=sentiment_polarity,style={'width':'150px','float':'right','padding-right': '120px'})
		],
		md=3,
		style={'margin-bottom': '2px','margin-top': '2px','margin-left': '0px','border-style': 'ridge','border-color': 'green'}
		),
		# end sidebar
	dbc.Col([
		html.Div(dbc.Row([
			html.Div(dbc.Card(number_of_tweets_card, color="info", inverse=True)),
			html.Div(dbc.Card(favourites_count_card, color="info", inverse=True),style={'padding-left': '50px'}),
			html.Div(dbc.Card(unique_users_count_card, color="info", inverse=True),style={'padding-left': '50px'}),
			html.Div(dbc.Card(sentiment_polarity_card, color="info", inverse=True),style={'padding-left': '50px'})
			]),
			style={'padding-left': '20px'}
			),
		html.Hr(),
			html.Div([
			daq.Gauge( id='sentiment-subjectivity-gauge', label="Sentiment Subjectivity", 
				color={"gradient":True,"ranges":{"red":[-1.00,0.03],"blue":[0.03,0.50],"green":[0.50,1.00]}},
				showCurrentValue=True,
				max=1,min=-1,
				value=sentiment_subjectivity,style={'width':'150px','float':'left','padding-left': '80px'}),
			dcc.Graph(id='sent-polar', figure={},style={'width':'700px','float':'right'})
			]),
			
		])
	], no_gutters=True,
	style={'margin-bottom': '1px'}),
html.Hr(),
# row 2 start

	# row 3 start
	dbc.Row([
		dbc.Col([
			], md=0),
		dbc.Col([
			dcc.Graph(id='sent-pol-region-user-bar',figure={})
			], md=12),
		dbc.Col([
			], md=0),
		], no_gutters=True,
		style={'margin-bottom': '2px'}
		),
	#row 3 end

	# row 3 start
	dbc.Row([
		dbc.Col([
			dcc.Graph(id='sentiment-polarity-geo',figure={})
			], md=6),
		dbc.Col([
				 
			], md=0),
		dbc.Col([
			dcc.Graph(id='sentiment-subjectivity-geo',figure={})
			], md=6),
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
Output('sent-polar' , 'figure'),
Input('calendar_prompt','value'),
 prevent_initial_call=False)
def update_sentiment_polarity_line_graph(date_selected):
	# dff=df[df['created_at'].isin([date_selected])]
	dff=df[(df['created_at'] > min(df['created_at'])) & (df['created_at'] <= max(df['created_at']))]
	fig=go.Figure()
	fig.add_trace(go.Scatter(x=dff['created_at'], y=dff['sentiment_polarity'], name='Polarity',line = dict(color='skyblue'))) 
	fig.update_layout(dict(autosize=True,margin=dict(t=0,b=0,l=0,r=0),xaxis=dict(title = 'Period', ticklen=2, zeroline=False)))
	# fig.update_yaxes(type='linear' if xlog_multi_type == 'Linear' else 'log')
	return fig

@app.callback(
Output('sent-pol-region-user-bar' , 'figure'),
Input('calendar_prompt','value'),
 prevent_initial_call=False)
def update_sent_pol_region_bar_graph(date_selected):
	df_new=df.dropna(subset=['name', 'location'], how='any')
	regional_avg_sentiment_df=pd.DataFrame(df_new.groupby(['location'],as_index=False)['sentiment_polarity'].mean()).head(50)
	regional_avg_sentiment_df=regional_avg_sentiment_df[(regional_avg_sentiment_df['sentiment_polarity'] != 0.000)]
	user_avg_sentiment_df=pd.DataFrame(df_new.groupby(['name'],as_index=False)['sentiment_polarity'].mean()).head(50)
	user_avg_sentiment_df=user_avg_sentiment_df[(user_avg_sentiment_df['sentiment_polarity'] != 0.000)]
	# dff=regional_avg_sentiment_df[regional_avg_sentiment_df['location'].isin([region])]
	fig = make_subplots(rows=1, cols=2,shared_xaxes=False,shared_yaxes=True,vertical_spacing=0.03,specs=[[{"type": "bar"},{"type": "bar"}]],
	    column_width=[50, 50],horizontal_spacing=0.015)
	fig.add_trace(go.Bar(name='Region',x=regional_avg_sentiment_df['location'].str[:20],y=regional_avg_sentiment_df['sentiment_polarity'],marker=dict(color="skyblue"), showlegend=True),row=1, col=1)
	fig.add_trace(go.Bar(name='User',x=user_avg_sentiment_df["name"].str[:20],y=user_avg_sentiment_df["sentiment_polarity"], marker=dict(color="teal"), showlegend=True),row=1, col=2)
	fig.update_layout(dict(autosize=True,margin=dict(t=0,b=0,l=0,r=0),xaxis=dict(ticklen=2, zeroline=False),legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),))
	return fig

@app.callback(
Output('sentiment-polarity-geo' , 'figure'),
Input('calendar_prompt','value'),
 prevent_initial_call=False)
def update_sentiment_polarity_geo(date_selected):
	sentiment_polarity_geo_data_df=df.dropna(subset=['name', 'location'], how='any')
	sentiment_polarity_geo_data_df=pd.DataFrame(sentiment_polarity_geo_data_df.groupby(['location'],as_index=False)['sentiment_polarity'].mean())
	sentiment_polarity_geo_data_df.columns = ['ADMIN', 'sentiment_polarity']
	sentiment_polarity_geo_df = geopandas.GeoDataFrame.from_features(country_geojson["features"]).merge(sentiment_polarity_geo_data_df, on="ADMIN").set_index("ADMIN")
	sentiment_polarity_geo_df.rename(columns={'Admin': 'location'}, inplace=True)
	fig = px.choropleth_mapbox(sentiment_polarity_geo_df,
                           geojson=sentiment_polarity_geo_df.geometry,
                           locations=sentiment_polarity_geo_df.index,
                           color="sentiment_polarity",
#                            center={"lat": 45.5517, "lon": -73.7073},
                           mapbox_style="carto-positron",
                           zoom=0.5)
	fig.update_layout(dict(autosize=True,margin=dict(t=0,b=0,l=0,r=0),xaxis=dict(ticklen=2, zeroline=False),legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),))
	return fig


@app.callback(
Output('sentiment-subjectivity-geo' , 'figure'),
Input('calendar_prompt','value'),
 prevent_initial_call=False)
def update_sentiment_subjectivity_geo(date_selected):
	sentiment_subjectivity_geo_data_df=df.dropna(subset=['name', 'location'], how='any')
	sentiment_subjectivity_geo_data_df=pd.DataFrame(sentiment_subjectivity_geo_data_df.groupby(['location'],as_index=False)['sentiment_subjectivity'].mean())
	sentiment_subjectivity_geo_data_df.columns = ['ADMIN', 'sentiment_subjectivity']
	sentiment_subjectivity_geo_df = geopandas.GeoDataFrame.from_features(country_geojson["features"]).merge(sentiment_subjectivity_geo_data_df, on="ADMIN").set_index("ADMIN")
	sentiment_subjectivity_geo_df.rename(columns={'Admin': 'location'}, inplace=True)
	fig = px.choropleth_mapbox(sentiment_subjectivity_geo_df,
                           geojson=sentiment_subjectivity_geo_df.geometry,
                           locations=sentiment_subjectivity_geo_df.index,
                           color="sentiment_subjectivity",
#                            center={"lat": 45.5517, "lon": -73.7073},
                           mapbox_style="carto-positron",
                           zoom=0.75)
	fig.update_layout(dict(autosize=True,margin=dict(t=0,b=0,l=0,r=0),xaxis=dict(ticklen=2, zeroline=False),legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),))
	return fig