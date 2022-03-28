#! /Users/constance/Desktop/REDEV/envREDEV

# Import des bibliothèques
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from datetime import datetime
import plotly.express as px


# Quelques données
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

def graph_introduction():
    fig = go.Figure([go.Scatter(x=dates, y=nombre_VT, line=dict(color="#2b9ab6"))])
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
    return fig

def layout():
    return [
        dbc.Row(
            children=[
                dbc.Card(
                    dbc.CardBody(
                        children=[
                            dbc.CardHeader("Bienvenue sur cette page dédiée aux VTubers francophones !"),
                            dbc.Row([
                                dbc.Col(
                                    dcc.Markdown(
                                        """
                                        Cette plateforme vous offre un outil de visualisation des données sur les VTubers français. L'application a été développée en Python avec Dash.
                                        Le VTubing est un phénomène récent qui a doucement commencé en 2016 au Japon et a réellement commencé à prendre de l'ampleur en 2018 avant de s'installer en France. Nous pouvons voir ci-dessous l'évolution au cours du temps du nombre de VTuber dans le monde.
                                        Dans la partie 'Général', une analyse globale sur les VTubers est faite. Elle montre entre autres des classements entre les VTubers selon différents critères.
                                        Dans l'onglet 'VTuber', il est possible de choisir un VTuber spécifique et d'avoir une analyse ainsi qu'une fiche récapitulative.
                                        """,
                                        style={"margin": "0 20px", "padding-top": "10%"}
                                    )
                                ),
                                dbc.Col(
                                    dcc.Graph(
                                        figure=graph_introduction(),
                                        className="dash-bootstrap"
                                    )
                                )
                            ])
                        ]
                    )
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Row(
                    dbc.Card(
                        dbc.CardBody(
                            children=[
                                dbc.CardHeader("Qu'est-ce que le VTubing ?"),
                                dbc.Row(
                                    dcc.Markdown(
                                        """
                                        Les VTubers sont des diffuseurs de divertissement qui utilisent différentes plateformes comme Youtube, Twitch, TikTok, etc… Leurs particularités est qu’ils utilisent des logiciels générant des avatars 2D, 3D qui vont collés aux mouvements des avatars à ceux des VTubers. 

                                        En ce qui concerne le phénomène VTuber, nous pouvons faire un bref historique mettant en avant l'émergence de ce dernier ainsi qu’une description brève de son histoire. Tout commence en 2010, avec la première publication d’un avatar 3D, Super Sonico, mascotte de la chaîne YouTube de visual novels : Nitroplus. Ensuite, en 2011, nous avons Ami Yamato qui met en ligne sa première vidéo dans laquelle un avatar virtuel animé parle à la caméra. Puis en 2014, le lancement du premier programme hebdomadaire de météo en direct avec l’avatar Airi. Finalement, en 2016, nous avons la première youtubeuse virtuelle, Kizuna AI que l’on peut voir Figure 1, qui a atteint une popularité internationale. 

                                        """,
                                        style={"margin": "0 10px"},
                                    )
                                )
                            ]
                        ),
                    )
                ),
                dbc.Row(
                    dbc.Card(
                        dbc.CardBody(
                            children=[
                                dbc.CardHeader("Ressources et bibliographie"),
                                dbc.Row(
                                    dcc.Markdown(
                                        """
                                        Données récupérées par l'API Youtube et l'API Twitch.
                                        
                                        Chiffre du graphique : https://www.animenewsnetwork.com/fr/interest/2021-10-20/une-societe-de-classement-de-donnees-repertorie-pus-de-16-000-youtubeurs-virtuels/.178647
                                        
                                        Github : https://github.com/sahjiro/analysis-vtuber
                                        """,
                                        style={"margin": "0 10px"},
                                    )
                                )
                            ]
                        )
                    )
                ),
            ]
        )
]
