# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 20:38:22 2021

@author: Marco

ATP TENNIS APP
"""
import pandas as pd
from sklearn import preprocessing
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import dash_table

#To display the dataframes nicely in the console
pd.set_option('display.max_columns', 15)
pd.set_option('display.max_rows', 10)

#Getting the raw url for each data file
url_09 = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2009.csv"
url_10 = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2010.csv"
url_11 = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2011.csv"
url_12 = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2012.csv"
url_13 = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2013.csv"
url_14 = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2014.csv"
url_15 = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2015.csv"
url_16 = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2016.csv"
url_17 = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2017.csv"
url_18 = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2018.csv"
url_19 = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2019.csv"

#Create a dataframe from each url
atp_09 = pd.read_csv(url_09)
atp_10 = pd.read_csv(url_10)
atp_11 = pd.read_csv(url_11)
atp_12 = pd.read_csv(url_12)
atp_13 = pd.read_csv(url_13)
atp_14 = pd.read_csv(url_14)
atp_15 = pd.read_csv(url_15)
atp_16 = pd.read_csv(url_16)
atp_17 = pd.read_csv(url_17)
atp_18 = pd.read_csv(url_18)
atp_19 = pd.read_csv(url_19)

atp_list = [atp_09, atp_10, atp_11, atp_12, atp_13,
            atp_14, atp_15, atp_16, atp_17, atp_19]

#Concatenate all the dataframes into a big data frame
atp = pd.concat(atp_list)

#Remove columns with very high number of NaN
atp = atp.drop(columns = ["winner_seed","winner_entry", 
               "loser_seed", "loser_entry",
               "minutes"])

#Remove rows with NaNs
atp = atp.dropna()

atp_df = atp.copy()

#create a data frame only for losers
df_loser = atp_df[['tourney_id', 'tourney_name', 'surface', 'draw_size', 
                       'tourney_level','tourney_date', 'match_num',
                       'loser_id', 'loser_name', 'loser_hand',
                       'loser_ioc', 'loser_age', 'score', 'best_of', 
                       'round', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn',
                       'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 
                       'l_bpFaced','loser_rank', 'loser_rank_points',
                        "loser_ht"]].copy()
df_loser["result"] = 0
df_loser = df_loser.rename(columns={'loser_id': "id",
                         'loser_name': "name",
                         'loser_hand': "hand",
                         'loser_ioc': "ioc",
                         'loser_age': "age",
                         'l_ace': "ace",
                         'l_df': "df",
                         'l_svpt': "svpt",
                         'l_1stIn': '1stIn',
                         'l_1stWon': '1stWon',
                         'l_2ndWon': '2ndWon',
                         'l_SvGms': 'SvGms',
                         'l_bpSaved': 'bpSaved',
                         'l_bpFaced': 'bpFaced',
                         'loser_rank': 'rank',
                         'loser_rank_points': 'rank_points',
                         "loser_ht": "height"})

#create a dataframe only for winners
df_winner = atp_df[['tourney_id', 'tourney_name', 'surface', 'draw_size', 
                       'tourney_level','tourney_date', 'match_num',
                       'winner_id', 'winner_name', 'winner_hand',
                       'winner_ioc', 'winner_age', 'score', 'best_of', 
                       'round', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 
                       'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 
                       'w_bpFaced','winner_rank', 'winner_rank_points',
                       "winner_ht"]].copy()
df_winner["result"] = 1
df_winner = df_winner.rename(columns={'winner_id': "id",
                         'winner_name': "name",
                         'winner_hand': "hand",
                         'winner_ioc': "ioc",
                         'winner_age': "age",
                         'w_ace': "ace",
                         'w_df': "df",
                         'w_svpt': "svpt",
                         'w_1stIn': '1stIn',
                         'w_1stWon': '1stWon',
                         'w_2ndWon': '2ndWon',
                         'w_SvGms': 'SvGms',
                         'w_bpSaved': 'bpSaved',
                         'w_bpFaced': 'bpFaced',
                         'winner_rank': 'rank',
                         'winner_rank_points': 'rank_points',
                         "winner_ht": "height"})

atp_results = df_winner.append(df_loser)

#create a copy of dataframe
atp_standardised = atp_results.copy()

#filter the columns i am interested in
atp_standardised = atp_standardised[['id', 'name','ioc', 'age', 'height', 
                                     'ace', 'df', 'svpt', '1stIn', '1stWon',
                                     '2ndWon', 'SvGms', 'bpSaved', 'bpFaced']]

#from preprocessing I use the StandardScaler() class
#the standardscaler() converts data to mean zero and unit variance
scaler = preprocessing.StandardScaler()

#Apply the function .fit_transform() from the class
atp_standardised.iloc[:, 5:] = scaler.fit_transform(
    atp_standardised.iloc[:, 5:].to_numpy())

#Create a dataframe with average performance for each player
atp_player = atp_standardised.groupby("name", as_index = False).mean()
#add the country of each player
atp_player = atp_player.merge(atp_standardised[["name","ioc"]].drop_duplicates(), 
                              on='name', how='left')
#reorder column order
atp_player = atp_player[["id", "name", "ioc", "age", "height",
                         'ace', 'df', 'svpt', '1stIn', '1stWon',
                       '2ndWon', 'SvGms', 'bpSaved', 'bpFaced']]

#collect individual characteristics and number of matches available
player_info = atp_player[["name","ioc","age","height"]].copy()
n_matches = atp_standardised.groupby("name")["id"].count().to_frame()
player_info = pd.merge(left=player_info,
                      right=n_matches,
                      on="name")
player_info = player_info.rename(columns={"id": "n_matches"})
player_info["age"] = player_info["age"].round(2)


##GET THE NUMBER OF GAMES A PLAYER WON EVERY YEAR
#Convert an integer to datetime
atp_results["tourney_date"] = pd.to_datetime(atp_results["tourney_date"], 
                                             format="%Y%m%d")
#Extract the year to groupby
atp_results["year"] = pd.DatetimeIndex(atp_results["tourney_date"]).year

#Individual n of matches won per year
yearly_performance = atp_results.groupby(["name", "year"], as_index = False)["result"].sum()


#~~~~~~~~~~~~~

app = dash.Dash(__name__)

#I may need to remove this line when running on local
server = app.server

colors = {
    'background': '#D5F0E7',
    'text': '#111111'
}

app.layout = html.Div(style={'backgroundColor': colors['background'],
                             'font-family': 'sans-serif'}, 
                      children=[
    html.Div([html.H1(
        children='ATP Player performance',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-family': 'sans-serif'
        }
    ),

    html.H2(children='Average players performance between 2009 and 2019 ATP seasons.', 
             style={
        'textAlign': 'center',
        'color': colors['text'],
        'font-family': 'sans-serif'
    })]),
    
       html.Div([html.Label("Select two players:"),
           dcc.Dropdown(
            id = 'player_one_dropdown',
            options=[
                {'label':i, 'value':i} for i in atp_player["name"].unique()
            ],
            #value='MTL'
            placeholder="Select player one",
            multi = False,
        ),
        dcc.Dropdown(
            id = 'player_two_dropdown',
            options=[
                {'label':i, 'value':i} for i in atp_player["name"].unique()
            ],
            #value='MTL'
            placeholder="Select player two",
            multi = False,
        ),

    dcc.Graph(
        id='players_polar_graph'
    )
  ], style={'width': '48%', 'display': 'inline-block'}),
       
       html.Div([
           dash_table.DataTable(id = "table_players"),
           html.Br(),
           dcc.Graph(id='players_longitudinal')
           ], 
           style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
])


@app.callback(
    Output(component_id='players_polar_graph', component_property='figure'),
    Output(component_id='table_players', component_property='data'), 
    Output(component_id='table_players', component_property='columns'),
    Input(component_id='player_one_dropdown', component_property='value'),
    Input(component_id='player_two_dropdown', component_property='value'))
    
def update_graph(player_name_1, player_name_2):
    
    player_1 = atp_player[atp_player["name"] == player_name_1].iloc[:,5:]
    player_2 = atp_player[atp_player["name"] == player_name_2].iloc[:,5:]
    
    selected_players = player_info[(player_info["name"] == player_name_1) |
                (player_info["name"] == player_name_2)]
    sel_players = selected_players.T
    sel_players = sel_players.rename_axis("id").reset_index()
    new_header = sel_players.iloc[0]
    sel_players = sel_players[1:]
    sel_players.columns = new_header
    columns = [{"name": col, "id": col} for col in sel_players.columns]
    data = sel_players.to_dict(orient="records")

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r = player_1.values.flatten(),
        theta = player_1.columns,
        mode = 'lines+markers',
        name = atp_standardised[atp_standardised["name"] == player_name_1]["name"].unique()[0],
        line_color = 'peru'
        #marker = dict(size=15, color="peru")
        ))
    fig.add_trace(go.Scatterpolar(
        r = player_2.values.flatten(),
        theta = player_2.columns,
        mode = 'lines+markers',
        name = atp_standardised[atp_standardised["name"] == player_name_2]["name"].unique()[0],
        line_color = 'darkviolet'
        #marker = dict(size=15, color="darkviolet")
        ))
    fig.update_layout(showlegend=True,
                  polar = dict(
               radialaxis_range = [atp_player.describe().loc["min"][3:].min(),
                                 atp_player.describe().loc["max"][3:].max()]),
                  paper_bgcolor = colors["background"],
                  margin=dict(l=20, r=20, t=20, b=20))
    
    return fig, data, columns

@app.callback(
    Output(component_id='players_longitudinal',component_property='figure'),
    Input(component_id='player_one_dropdown', component_property='value'),
    Input(component_id='player_two_dropdown', component_property='value'))

def update_linechart(player_name_1, player_name_2):
    
    pl2 = yearly_performance[yearly_performance["name"] == player_name_1]
    pl3 = yearly_performance[yearly_performance["name"] == player_name_2]
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=pl2["year"], y=pl2["result"],
                    mode='lines+markers+text',
                    name=pl2["name"].unique()[0],
                    line_color = "peru",
                     text = pl2["result"],
                     textposition = "middle left",
                     textfont = dict(
                         family = "sans serif",
                         size = 12,
                         color = "peru")))

    fig1.add_trace(go.Scatter(x=pl3["year"], y=pl3["result"],
                    mode='lines+markers+text',
                    name=pl3["name"].unique()[0],
                    line_color = "darkviolet",
                    text = pl3["result"],
                    textposition = "middle left",
                    textfont=dict(
        family="sans serif",
        size=12,
        color="darkviolet"
    )))

    fig1.update_layout(
    #title='Yearly player performance',
    xaxis=dict(
        title='Year',
        tickmode='linear',
        tickangle = -90),
    yaxis = dict(
        title = "Number of matches won (n)"),
    #legend = dict(
    #    title = "Players:"),
    showlegend = False,
    paper_bgcolor = colors["background"],
    margin = dict(l=20, r=20, t=20, b=20),
    height=372
    )
    return fig1

if __name__ == '__main__':
    app.run_server(use_reloader = False)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


