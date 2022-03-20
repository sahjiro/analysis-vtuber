#! /Users/constance/Desktop/REDEV/envREDEV

# Import des bibliothèques
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Import des bases de données
dataframe_channelFR = pd.read_csv('../dataframe_list_channel_FR_all.csv')
dataframe_channelFR['name'] = [x.split()[0] for x in dataframe_channelFR["name"]]
dataframe_list_video = pd.read_csv('../dataframe_list_video_FR_all.csv')
dataframe_list_video['channelTitle'] = [x.split()[0] for x in dataframe_list_video["channelTitle"]]
dataframe_videogames = pd.read_csv('../jeux_twitch.csv')

# Mise en forme de la page
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# Sélection du VTuber
options = []
name_vtuber = [x.split()[0] for x in dataframe_channelFR["name"]]
for i in range (len(name_vtuber)):
    options.append({"label" : name_vtuber[i], "value" : name_vtuber[i]})

app = dash.Dash("REDEV", external_stylesheets=[dbc.themes.DARKLY])

# Colonne de gauche :
# Première ligne:
# Contient les informations sur le VTuber
# - photo de profil
# - nombre d'abonnés
# - Date de création de la chaîne

# Deuxième ligne :
# - Graphique ratio Live/VOD
# - jeux joués

# Colonne de droite :
# Première ligne : tendance

# Deuxième ligne : Liens sociaux

app.layout = html.Div(
    id='VTuber-body',
    className='dash-bootstrap',
    children=[
        html.H4(className='dash-bootstrap', children='Bienvenue'),
        html.Div(
            id='VTuber-control-tabs',
            className='dash-bootstrap',
            children=[
                dcc.Tabs(
                    id='VTuber-tabs', value='accueil', children=[
                    dcc.Tab(
                        label='Accueil',
                        value='accueil',
                        className="dash-bootstrap",
                        children=dbc.Row([dbc.Col(
                            html.Div(className='dash-bootstrap', children=[
                                html.P("Cette plateforme vous offre un outil de visualisation des données sur les VTubers français. L'application a été développée en Python avec Dash."),
                                html.P("Le VTubing est un phénomène récent qui a doucement commencé en 2016 au Japon et a réellement commencé à prendre de l'ampleur en 2018 avant de s'installer en France. Nous pouvons voir ci-dessous l'évolution au cours du temps du nombre de VTuber dans le monde."),
                                html.P("Dans la partie 'Général', une analyse globale sur les VTubers est faite. Elle montre entre autres des classements entre les VTubers selon différents critères."),
                                html.P("Dans l'onglet 'VTuber', il est possible de choisir un VTuber spécifique et d'avoir une analyse ainsi qu'une fiche récapitulative.")
                            ])
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="evolution",
                                className="dash-bootstrap"
                            )
                        )])
                    ),
                    dcc.Tab(
                        label='General',
                        value='general',
                        className="dash-bootstrap",
                        children=[
                            dbc.Row([
                                dbc.Col(
                                    dcc.Graph(
                                    id="classement_abonnes",
                                    className="dash-bootstrap"
                                    )
                                ),
                                dbc.Col(
                                    dcc.Graph(
                                    id="classement_videos",
                                    className="dash-bootstrap"
                                    )
                                )
                            ]
                        ),
                        dbc.Row(
                            dcc.Graph(
                                id="nombre_vues_videos",
                                className="dash-bootstrap"
                            ),
                        ),
                        dbc.Row(
                            dcc.Graph(
                                id="duree_video",
                                className="dash-bootstrap"
                            )
                        )
                    ]
                    ),
                    dcc.Tab(
                        label='VTuber',
                        value='vtuber',
                        className="dash-bootstrap",
                        children=[
                            dbc.Row(
                                
                            ),
                            # 1ère ligne
                            dbc.Row(
                                dcc.Dropdown(
                                    id="vtuber",
                                    options=options,
                                    placeholder="Choisir un VTuber",
                                    className="dash-bootstrap"
                                )
                            ),
                            # 2ème ligne avec 2 colonnes
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
                            dbc.Row([
                                html.H5("Tendance des jours de publication"),
                                dcc.Graph(
                                    id="tendance_des_jours", 
                                    className="dash-bootstrap"
                                )
                            ])
                        ]
                    )]
                )
            ] 
        )
    ]
)
    

@app.callback(
    [Output(component_id='evolution', component_property='figure'),
    Output(component_id='classement_abonnes', component_property='figure'),
    Output(component_id='classement_videos', component_property='figure'),
    Output(component_id='nombre_vues_videos', component_property='figure'),
    Output(component_id='duree_video', component_property='figure'),
    Output(component_id='games_played', component_property='figure'),
    Output(component_id='live_vod', component_property='figure'),
    Output(component_id='tendance_des_jours', component_property='figure')],
    Input(component_id='vtuber', component_property='value')
)

def update_graph(vtuber):
    # Filtering video database
    df_video = dataframe_list_video.copy()
    df_video['channelTitle'] = [x.split()[0] for x in df_video["channelTitle"]]
    df_video = df_video[df_video["channelTitle"]==vtuber]
    channel = dataframe_channelFR[dataframe_channelFR['name']==vtuber]

    # fig : evolution au cours du temps
    nombre_VT = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 16000] 
    dates = [ 
        datetime(2018, 3, 19),
        datetime(2018, 4, 27),
        datetime(2018, 5, 28),
        datetime(2018, 7, 10),
        datetime(2018, 9, 12),
        datetime(2018, 12, 19),
        datetime(2019, 2, 21),
        datetime(2019, 5, 6),
        datetime(2019, 9, 5),
        datetime(2020, 1, 15), 
        datetime(2020, 5, 24),
        datetime(2020, 8, 17),
        datetime(2020, 11, 10),
        datetime(2021, 10, 19)
    ]
    fig = go.Figure([go.Scatter(x=dates, y=nombre_VT)])
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)',
    )
    fig["layout"]["yaxis"]["title"] = "Nombre de VTubers"
    fig["layout"]["xaxis"]["title"] = 'date'
    fig["layout"]["title"]["font"]["color"] = "#a9a9a9"
    fig["layout"]["xaxis"]["tickfont"]["color"] = "#fff8dc"
    fig["layout"]["yaxis"]["tickfont"]["color"] = "#fff8dc"

    # fig 1 : classement en fonction du nombre d'abonnés 
    ranking_per_subscriber = dataframe_channelFR.sort_values(by='subscriberCount')[-20:]
    fig1 = px.bar(ranking_per_subscriber, x='name', y='subscriberCount', title="Classement des VTubers selon leur nombre d'abonnés")
    fig1.update_layout(
        template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)',
    )
    fig1["layout"]["yaxis"]["title"] = "Nombre d'abonnés"
    fig1["layout"]["xaxis"]["title"] = 'Nom du VTuber'
    fig1["layout"]["title"]["font"]["color"] = "#a9a9a9"
    fig1["layout"]["xaxis"]["tickfont"]["color"] = "#fff8dc"
    fig1["layout"]["yaxis"]["tickfont"]["color"] = "#fff8dc"

    # fig : classement en fonction du nombre de vidéos
    ranking_per_nbVideos = dataframe_channelFR.sort_values(by='videoCount')[-20:]
    fig_ranking_videos = px.bar(ranking_per_nbVideos, x='name', y='subscriberCount', title="Classement des VTubers selon leur nombre de vidéos")
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

    # fig 2 : nombre de vues moyen par vidéos par VTuber
    ranking_per_videosViews = dataframe_list_video.loc[dataframe_list_video.channelTitle.isin(ranking_per_subscriber.name)].sort_values(by='viewCount')
    msk = ranking_per_videosViews['viewCount'] < 25000
    fig2 = px.box(ranking_per_videosViews[msk], x='channelTitle', y='viewCount', title="Nombre de vues moyen par vidéos pour chaque VTuber")
    fig2.update_layout(
        template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)',
    )
    fig2["layout"]["yaxis"]["title"] = 'Nombre de vues'
    fig2["layout"]["xaxis"]["title"] = 'Nom du VTuber'

    # fig 3 : durée moyenne d'une vidéo par VTuber
    dataframe_select = dataframe_list_video.loc[dataframe_list_video.channelTitle.isin(ranking_per_subscriber.name)]
    duration_int = [int(x.split(":")[0])*3600 + int(x.split(":")[1])*60 + int(x.split(":")[2]) for x in dataframe_select.duration_time]
    fig3 = px.box(dataframe_select, x='channelTitle', y=duration_int, title="Durée moyenne d'une vidéo en seconde par VTuber")
    fig3.update_layout(
        template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)',
    )
    fig3["layout"]["yaxis"]["title"] = 'Durée (secondes)'
    fig3["layout"]["xaxis"]["title"] = 'Nom du VTuber'

    # fig 4 : ratio entre les vidéos live et les VOD
    labels = ['Live','VOD']
    values = [sum(df_video['live']), len(df_video['live'])-sum(df_video['live'])]
    fig4 = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig4.update_layout(
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
    videogames_played_clean = videogames_played_clean.sort_values(by='occurence', ascending = False)
    labels = videogames_played_clean['jeu video'].values
    values = videogames_played_clean['occurence'].values
    fig5 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig5.update_layout(
        template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)',
    )

    # fig 6 : tendance des jours de publication
    fig6 = px.histogram(df_video, x='publication_weekday', category_orders=dict(day=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']))
    fig6.update_layout(
        template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)',
    )
    fig6["layout"]["xaxis"]["title"] = 'Jour de la semaine'
    
    return fig, fig1, fig_ranking_videos, fig2, fig3, fig5, fig4, fig6


if __name__ == '__main__':
    app.run_server(debug=True)