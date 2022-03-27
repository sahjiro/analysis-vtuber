#! /Users/constance/Desktop/REDEV/envREDEV

# Import des bibliothèques
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from app import app

# Import des bases de données
dataframe_channelFR = pd.read_csv('../data/dataframe_list_channel_FR_all.csv')
dataframe_channelFR['name'] = [x.split()[0] for x in dataframe_channelFR["name"]]
dataframe_list_video = pd.read_csv('../data/dataframe_list_video_FR_all.csv')
dataframe_list_video['channelTitle'] = [x.split()[0] for x in dataframe_list_video["channelTitle"]]
dataframe_videogames = pd.read_csv('../data/jeux_twitch.csv')
dataframe_channelFR_Twitch = pd.read_csv('../data/json_id_streamer.csv')
dataframe_list_video_Twitch = pd.read_csv('../data/json_video_streamer.csv')

# Sélection du VTuber
options = []
name_vtuber = [x.split()[0] for x in dataframe_channelFR["name"]]
for i in range (len(name_vtuber)):
    options.append({"label" : name_vtuber[i], "value" : name_vtuber[i]})

def get_vtuber_photo(vtuber):
    url = dataframe_channelFR[dataframe_channelFR["name"]==vtuber]['thumbnail'].values[0]
    return url

def vtuber_information(vtuber):
    channel = dataframe_channelFR[dataframe_channelFR['name']==vtuber]
    if vtuber in list(dataframe_channelFR_Twitch['display_name']):
        channel_twitch = dataframe_channelFR_Twitch[dataframe_channelFR_Twitch['display_name']==vtuber]
        return html.Div(
            [
                html.H4(vtuber),
                html.P("Date de création", style={'color':'#858282'}),
                html.P("Youtube : "+ str(channel.creation.values[0]) + " - Twitch : " + str(channel_twitch['date creat'].values[0])),
                html.P("Nombre d'abonnés: ", style={'color':'#858282'}), 
                html.P("Youtube : " + str(channel.subscriberCount.values[0])+ " - Twitch : " + str(channel_twitch['nb abo'].values[0])),
                html.P("Nombre de vidéos: ", style={'color':'#858282'}), 
                html.P("Youtube : " + str(channel.videoCount.values[0])+ " - Twitch : " + str(channel_twitch['nb vod'].values[0])),
                html.P("Nombre de vues cumulées: ", style={'color':'#858282'}),
                html.P("Youtube : " + str(channel.viewCount.values[0])+ " - Twitch : " + str(channel_twitch['nb vu cumul'].values[0]))
            ]
        )
    else:
        return html.Div(
            [
                html.H4(vtuber),
                html.P("Date de création: " + str(channel.creation.values[0])),
                html.P("Nombre d'abonnés: " + str(channel.subscriberCount.values[0])),
                html.P("Nombre de vidéos: " + str(channel.videoCount.values[0])),
                html.P("Nombre de vues cumulées: " + str(channel.viewCount.values[0]))
            ]
        )

def layout():
    return [
        dbc.Row(
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            children=[
                                dbc.CardHeader("Choisir un VTuber ici"),
                                dcc.Dropdown(
                                    id="vtuber",
                                    options=options,
                                    value="Selph1ne",
                                    clearable=True,
                                    searchable=True
                                ),
                                dbc.Row([
                                    dbc.Col(
                                        html.Img(
                                        id="vtuber-name-card",
                                        style={
                                            "padding-top": "5%",
                                            "height": "300px",
                                            "width": "300px"
                                        })   
                                    ),
                                    dbc.Col(
                                        html.Div(
                                        id="profile-about-section",
                                        style={
                                            "padding-left": "5%",
                                            "padding-top": "10%",
                                        })
                                    )
                                ])
                            ]
                        )
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            children=[
                                dbc.CardHeader("Tendance des jours de publication sur les réseaux"),
                                dcc.Graph(
                                    id="tendance_des_jours",
                                    className="dash-bootstrap"
                                )
                            ]
                        )
                    )
                )
            ]
        ),
        dbc.Row(
            dbc.Card(
                dbc.CardBody(
                    children=[
                        dbc.Row([
                            dbc.Col([
                                html.H5('Proportion des jeux joués'),
                                dcc.Graph(
                                    id="games_played", 
                                    className="dash-bootstrap"
                                )
                            ]),
                            dbc.Col([
                                html.H5('Ratio live / VOD'),
                                dcc.Graph(
                                    id="live_vod",
                                    className="dash-bootstrap"
                                )   
                            ])
                        ]),
                    ]
                )
            )
        )
]

@app.callback(Output("vtuber-name-card", "src"), [Input("vtuber", "value")])
def get_vtuber_name_card(vtuber):
    if vtuber is not None:
        return get_vtuber_photo(vtuber)
    else:
        raise PreventUpdate

@app.callback(
    Output("profile-about-section", "children"), [Input("vtuber", "value")]
)
def get_driver_profile_section(vtuber):
    if vtuber is not None:
        return vtuber_information(vtuber)
    else:
        raise PreventUpdate

@app.callback(
    [Output(component_id='tendance_des_jours', component_property='figure'),
    Output(component_id='games_played', component_property='figure'),
    Output(component_id='live_vod', component_property='figure')],
    Input(component_id='vtuber', component_property='value')
)
def update_vtuber_graphs(vtuber):
    # sous-sélection de la dataframe
    df_video = dataframe_list_video.copy()
    df_video['channelTitle'] = [x.split()[0] for x in df_video["channelTitle"]]
    df_video = df_video[df_video["channelTitle"]==vtuber]

    # fig : tendance des jours de publication Youtube
    if vtuber in list(dataframe_channelFR_Twitch['display_name']):
        df_video_twitch = dataframe_list_video_Twitch.copy()
        df_video_twitch = df_video_twitch[df_video_twitch["user_name"]==vtuber]
        fig_publi_trend = go.Figure()
        fig_publi_trend.add_trace(go.Histogram(x=df_video['publication_weekday'], name="Youtube", marker_color='#375a7f'))
        fig_publi_trend.add_trace(go.Histogram(x=df_video_twitch['publication_weekday'], name="Twitch", marker_color='#f4a62a'))
    else:
        fig_publi_trend = px.histogram(df_video, x='publication_weekday', category_orders=dict(day=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']), color_discrete_sequence=px.colors.qualitative.Set3)
    fig_publi_trend.update_layout(
        template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)',
    )
    fig_publi_trend["layout"]["xaxis"]["title"] = 'Jour de la semaine'
    fig_publi_trend["layout"]["yaxis"]["title"] = 'Nombre de vidéos'

    # fig : ratio entre les vidéos live et les VOD
    labels = ['Live','VOD']
    values = [sum(df_video['live']), len(df_video['live'])-sum(df_video['live'])]
    fig_ratio = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=px.colors.qualitative.Set3)])
    fig_ratio.update_layout(
        template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)',
    )

    # fig 5 : proportion de jeux joues
    videogames_played = {
        "jeu video" : dataframe_videogames.name.unique(),
        "occurence" : np.zeros(dataframe_videogames.name.unique().shape)
    }
    dataframe_videogames_played = pd.DataFrame.from_dict(data=videogames_played, orient='index').transpose()
    for i in df_video.index:
        try:
            description = df_video["description"][i]
            for j in range (len(dataframe_videogames_played["jeu video"])):
                c = dataframe_videogames_played["jeu video"][j]
                if description.find(c) != -1 :
                    dataframe_videogames_played["occurence"].values[j] += 1
        except:
            pass

    videogames_played_clean = dataframe_videogames_played[dataframe_videogames_played['occurence']!=0]
    videogames_played_clean = videogames_played_clean.sort_values(by='occurence', ascending = False)[:10]
    labels = videogames_played_clean['jeu video'].values
    values = videogames_played_clean['occurence'].values
    fig_videogames = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, marker_colors=px.colors.qualitative.Set3)])
    fig_videogames.update_layout(
        template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)',
    )

    return fig_publi_trend, fig_videogames, fig_ratio
