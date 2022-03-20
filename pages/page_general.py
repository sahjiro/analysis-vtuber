#! /Users/constance/Desktop/REDEV/envREDEV

# Import des bibliothèques
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Import des bases de données
dataframe_channelFR = pd.read_csv('/Users/constance/Desktop/REDEV/App/data/dataframe_list_channel_FR_all.csv')
dataframe_channelFR['name'] = [x.split()[0] for x in dataframe_channelFR["name"]]
dataframe_list_video = pd.read_csv('/Users/constance/Desktop/REDEV/App/data/dataframe_list_video_FR_all.csv')
dataframe_list_video['channelTitle'] = [x.split()[0] for x in dataframe_list_video["channelTitle"]]
dataframe_videogames = pd.read_csv('/Users/constance/Desktop/REDEV/App/data/jeux_twitch.csv')

# Traitement
ranking_per_subscriber = dataframe_channelFR.sort_values(by='subscriberCount')[-20:]
ranking_per_nb_videos = dataframe_channelFR.sort_values(by='videoCount')[-20:]

def classement_abonnes():
    # fig : classement en fonction du nombre d'abonnés 
    fig_ranking_subs = px.bar(ranking_per_subscriber, x='name', y='subscriberCount', title="Classement des VTubers selon leur nombre d'abonnés", color_discrete_sequence=px.colors.qualitative.Set3)
    fig_ranking_subs.update_layout(
        template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)',
    )
    fig_ranking_subs["layout"]["yaxis"]["title"] = "Nombre d'abonnés"
    fig_ranking_subs["layout"]["xaxis"]["title"] = 'Nom du VTuber'
    fig_ranking_subs["layout"]["title"]["font"]["color"] = "#a9a9a9"
    fig_ranking_subs["layout"]["xaxis"]["tickfont"]["color"] = "#fff8dc"
    fig_ranking_subs["layout"]["yaxis"]["tickfont"]["color"] = "#fff8dc"
    return fig_ranking_subs

def classement_nb_videos():
    # fig : classement en fonction du nombre de vidéos
    fig_ranking_videos = px.bar(ranking_per_nb_videos, x='name', y='videoCount', title="Classement des VTubers selon leur nombre de vidéos", color_discrete_sequence=px.colors.qualitative.Set3)
    fig_ranking_videos.update_layout(
        template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)',
    )
    fig_ranking_videos["layout"]["yaxis"]["title"] = "Nombre d'abonnés"
    fig_ranking_videos["layout"]["xaxis"]["title"] = 'Nom du VTuber'
    fig_ranking_videos["layout"]["title"]["font"]["color"] = "#a9a9a9"
    fig_ranking_videos["layout"]["xaxis"]["tickfont"]["color"] = "#fff8dc"
    fig_ranking_videos["layout"]["yaxis"]["tickfont"]["color"] = "#fff8dc"
    return fig_ranking_videos

def classement_nb_vues():
    # fig 2 : nombre de vues moyen par vidéos par VTuber
    ranking_per_videos_views = dataframe_list_video.loc[dataframe_list_video.channelTitle.isin(ranking_per_subscriber.name)].sort_values(by='viewCount')
    msk = ranking_per_videos_views['viewCount'] < 25000
    fig_nb_vues = px.box(ranking_per_videos_views[msk], x='channelTitle', y='viewCount', color_discrete_sequence=px.colors.qualitative.Set3)
    fig_nb_vues.update_layout(
        template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)',
    )
    fig_nb_vues["layout"]["yaxis"]["title"] = 'Nombre de vues'
    fig_nb_vues["layout"]["xaxis"]["title"] = 'Nom du VTuber'
    return fig_nb_vues

def duree_moyenne():
    # fig 3 : durée moyenne d'une vidéo par VTuber
    dataframe_select = dataframe_list_video.loc[dataframe_list_video.channelTitle.isin(ranking_per_subscriber.name)]
    duration_int = [int(x.split(":")[0])*3600 + int(x.split(":")[1])*60 + int(x.split(":")[2]) for x in dataframe_select.duration_time]
    fig_duree_moyenne = px.box(dataframe_select, x='channelTitle', y=duration_int, color_discrete_sequence=px.colors.qualitative.Set3)
    fig_duree_moyenne.update_layout(
        template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)',
    )
    fig_duree_moyenne["layout"]["yaxis"]["title"] = 'Durée (secondes)'
    fig_duree_moyenne["layout"]["xaxis"]["title"] = 'Nom du VTuber'
    return fig_duree_moyenne

def layout():
    return [
        dbc.Row(
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            children=[
                                dbc.CardHeader("Classement des VTubers les plus connus"),
                                dbc.Row([
                                    dbc.Col([
                                        dcc.Graph(
                                            figure=classement_abonnes(), 
                                            className="dash-bootstrap"
                                        )
                                    ]),
                                    dbc.Col([
                                        dcc.Graph(
                                            figure=classement_nb_videos(),
                                            className="dash-bootstrap"
                                        )   
                                    ])
                                ])
                            ]
                        )
                    )
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Card(
                    dbc.CardBody(
                        children=[
                            dbc.CardHeader("Nombre de vues moyen des vidéos par chaîne de VTuber"),
                            dcc.Graph(
                                figure=classement_nb_vues(),
                                className="dash-bootstrap"
                            )
                        ]
                    )
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Card(
                    dbc.CardBody(
                        children=[
                            dbc.CardHeader("Durée moyenne d'une vidéo par VTuber"),
                            dcc.Graph(
                                figure=duree_moyenne(),
                                className="dash-bootstrap"
                            )
                        ]
                    )
                )
            ]
        )
]