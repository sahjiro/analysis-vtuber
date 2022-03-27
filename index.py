#! /Users/constance/Desktop/REDEV/envREDEV

# Import des bibliothèques
import base64
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pages import accueil, page_general, page_vtuber
from app import app

server = app.server

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dbc.Navbar(
            children=[
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.NavbarBrand(
                                    "Analyse sur les VTubers francophones", class_name="dash-bootstrap",
                                    style={"padding-left": "10%"}
                                )
                            ),
                        ],
                        class_name="dash-bootstrap",
                        align="center",
                    ),
                    className="dash-bootstrap"
                ),
                dbc.Row(
                    children=[
                        dbc.Col(dbc.NavLink("Accueil", href=app.get_relative_path("/"), class_name="dash-bootstrap", active='exact')),
                        dbc.Col(dbc.NavLink("Général", href=app.get_relative_path("/general"), class_name="dash-bootstrap", active='exact')),
                        dbc.Col(dbc.NavLink("Vtuber", href=app.get_relative_path("/vtuber"), class_name="dash-bootstrap", active='exact'))
                    ],
                    class_name="dash-bootstrap",
                    style={"paddingLeft": "480px"}
                ),
            ],
            class_name="dash-bootstrap",
            color="primary",
            dark=True,
            sticky='top'
        ),
        html.Div(id="page-content", className="dash-bootstrap"),
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page_content(pathname):
    path = app.strip_relative_path(pathname)
    if not path:
        return accueil.layout()
    elif path == "general":
        return page_general.layout()
    elif path == "vtuber":
        return page_vtuber.layout()
    else:
        return "404"


if __name__ == "__main__":
    app.run_server(debug=True)