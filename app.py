#! /Users/constance/Desktop/REDEV/envREDEV

# Import des bibliothèques
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True, 
    external_stylesheets=[dbc.themes.DARKLY]
)

app.title = "Etude statistiques des VTubers francophones"