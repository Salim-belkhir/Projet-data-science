# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# get the data from the Data folder
labelNumLycee = pd.read_csv('data/fr-en-occitanie-label-numerique-lycee.csv', sep=';')
labelNumCollege = pd.read_csv('data/fr-en-occitanie-ac-montpellier-label-numerique-college.csv', sep=';')
annuaireEducation = pd.read_csv('data/fr-en-annuaire-education.csv', sep=';')
collegeEffective = pd.read_csv('data/fr-en-college-effectifs-niveau-sexe-lv.csv', sep=';')
resultatLyceeGenerale = pd.read_csv('data/fr-en-indicateurs-de-resultat-des-lycees-denseignement-general-et-technologique.csv', sep=';')
resultatLyceePro = pd.read_csv('data/fr-en-indicateurs-de-resultat-des-lycees-denseignement-professionnels.csv', sep=';') 
indicateurCollege = pd.read_csv('data/od-indicateurs-2d-colleges-tne.csv', sep=';')
etic2 = pd.read_csv('data/fr-en-etic_2d.csv', sep=';')

# copy the dataToUse
dataToUse = labelNumLycee.copy()


external_stylesheets = [
    {
        "rel": "stylesheet",
    },
]

# create an instance of the Dash class
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

fig = px.bar(labelNumLycee, x="Niveau de Label", y="RNE", color="Niveau de Label")

# create the layout
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                # affficher l'image qui se retrouve dans le dossier assets
                html.Img(src=app.get_asset_url("polytech.png"),className="header-emoji"),
                html.Div(children=[  
                        html.H1(
                            children="Forme Scolaire Analyse", className="header-title"
                        ),
                        html.P(
                            children="Analyser l'impact de la forme scolaire sur la réussite des élèves en fonction du numérique, de l'interstructure et de l'indice de position sociale.",
                            className="header-description",
                        ),
                    ], className="header"
                )
            ],
            className="header-container",
        ), 
        html.Div(
            children=
            [       
                html.Div(
                    children=["parametre displayed here"],
                    className="parametre",
                ),
                html.Div
                (
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    [
                                        dbc.RadioItems(
                                            id="radios",
                                            className="btn-group",
                                            inputClassName="btn-check",
                                            labelClassName="btn btn-outline-info",
                                            labelCheckedClassName="active",
                                            options=[
                                                {"label": "Lycée Professionel", "value": 1},
                                                {"label": "Lycée Genérale et Technologique", "value": 2},
                                                {"label": "Collège", "value": 3},
                                                {"label": "Ecole", "value": 4},
                                            ],
                                            value=1,
                                        ),
                                        html.Div(id="output"),
                                    ],
                                    className="radio-group",
                                )
                            ],
                            className="data",
                        ),

                        html.Div(
                            children=[
                                html.Div(
                                    children=["counts displayed here"],
                                    className="counts",
                                ),
                                html.Div(
                                    children=[
                                       # html.Div(
                                       #     children=dcc.Graph(id="graph", figure=fig),
                                       #     className="card",  
                                       # ),
                                    ],
                                    className="graph",
                                ),
                            ],
                            className="graphics",
                        ),
                    ],
                    className="right-side-content",
                ),
            ],
            className="content-container",
        )
    ],
    className="main-container",
)
     
@app.callback(Output("output", "children"), [Input("radios", "value")])
def data_choice(value):
    if value == 1:
        dataToUse = labelNumLycee.copy()
    return f"Selected value: {value}"


# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
