# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Import necessary libraries
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium # for maps
import plotly.graph_objects as go

# get the data from the Data folder
labelNumLycee = pd.read_csv('data/fr-en-occitanie-label-numerique-lycee.csv', sep=';')
labelNumCollege = pd.read_csv('data/fr-en-occitanie-ac-montpellier-label-numerique-college.csv', sep=';')
annuaireEducation = pd.read_csv('data/fr-en-annuaire-education.csv', sep=';')
collegeEffective = pd.read_csv('data/fr-en-college-effectifs-niveau-sexe-lv.csv', sep=';')
resultatLyceeGenerale = pd.read_csv('data/fr-en-indicateurs-de-resultat-des-lycees-denseignement-general-et-technologique.csv', sep=';')
resultatLyceePro = pd.read_csv('data/fr-en-indicateurs-de-resultat-des-lycees-denseignement-professionnels.csv', sep=';') 
indicateurCollege = pd.read_csv('data/od-indicateurs-2d-colleges-tne.csv', sep=';')
etic2 = pd.read_csv('data/fr-en-etic_2d.csv', sep=';')

df_result_all = pd.read_csv('data/df_result_all.csv', sep=',')
df_result = pd.read_csv('data/df_result.csv', sep=',')
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
                                        html.Div(
                                            id="graph",
                                        ),
                                       
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


@app.callback(Output("graph", "children"), [Input("radios", "value")])
def data_choice(value):
    content = ""
    if value == 1:
        # La proportion de lycées professionnels labelisés 
        nbre_lycee_professionnel = df_result_all['code_etablissement'].nunique()
        nbre_lycee_professionel_labelise = df_result_all['rne'].nunique()
        nbre_lycee_professionnel_non_labelise = nbre_lycee_professionnel - nbre_lycee_professionel_labelise
        values = [nbre_lycee_professionnel_non_labelise,nbre_lycee_professionel_labelise]
        labels = ["Lycées Pro Non Labelisés", "Lycées Pro Labelisés"]
        fig2 = go.Figure(data=[go.Pie(labels=labels, values=values)])
        
        # update the layout of the figure
        fig2.update_layout(
            autosize=False,
            width=500,
            height=250,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="Les proportions des Lycées Pro labelisés pour lequels on connait les résultats",
            title_font_size=13,
            paper_bgcolor="#FFF7E9",
        )

        # La variation du nombre des lycées labelisés selon les années
        # transform the column annee_x and rne to strings
        df_result["annee_x"] = df_result["annee_x"].astype(str)
        df_result["rne"] = df_result["rne"].astype(str)
        df_proportion_lycee_labelise_annee = df_result.groupby("annee_x")["rne"].nunique()
        df_proportion_lycee_labelise_annee = df_proportion_lycee_labelise_annee.reset_index()

        #plotting a histogram 
        fig3 = px.histogram(df_proportion_lycee_labelise_annee, x="annee_x", y="rne",
                        color="annee_x",
                        labels={"rne" : "Nombre de lycee labelisés","annee_x":"Année"}
                        )

        # update the layout of the figure
        fig3.update_layout(
            autosize=False,
            width=500,
            height=300,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="La variation du nombre des lycées labelisés selon les années",  
            title_font_size=15,  
            paper_bgcolor="#FFF7E9", 
        )

        # La variation du nombre des lycées non labelisés selon les années
        # transform the column annee_y and code_etablissement to strings
        df_result_all["annee_y"] = df_result_all["annee_y"].astype(str)
        df_result_all["code_etablissement"] = df_result_all["code_etablissement"].astype(str)
        df_proportion_lycee_non_labelise_annee = df_result_all.query("label_true == False").groupby("annee_y")["code_etablissement"].nunique()
        df_proportion_lycee_non_labelise_annee = df_proportion_lycee_non_labelise_annee.reset_index()

        #plotting a histogram 
        fig4 = px.histogram(df_proportion_lycee_non_labelise_annee, x="annee_y", y="code_etablissement",
                        color="annee_y",
                            labels={"code_etablissement" : "nombre de lycee non labelisés","annee_y":"Année"})
        fig4.update_layout(
            autosize=False,
            width=500,
            height=300,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="La variation du nombre des lycées non labelisés selon les années", 
            title_font_size=15,   
            paper_bgcolor="#FFF7E9", 
        )

        # transform label to numeric
        df_result["label"] = pd.to_numeric(df_result["label"])
        #sort label by ascending order
        df_result.sort_values(by="label",inplace=True)
        # re transform label to str so it can be a discrete value for visualisations (discrete value)
        df_result["label"] = df_result["label"].apply(str)
        
        #plotting a histogram
        #fig5 = px.histogram(df_result[df_result["resultat_apres_label"] == True], x="label", y="taux_brut_de_reussite_total_secteurs", nbins=10, histfunc="avg", color="label")
        #fig5.update_layout(
        #    autosize=False,
        #    width=500,
        #    height=250,
        #    margin=dict(l=0, r=0, b=0, t=35, pad=0), 
        #    title="La moyenne des taux bruts de réussites des lycee après obtention de leurs labels (tous secteurs) selon les labels",    
        #    paper_bgcolor="#FFF7E9", 
        #)

        fig6 = px.box(df_result, x="departement_y",y="taux_brut_de_reussite_total_secteurs", color="departement_y",
        facet_row="resultat_apres_label",
        labels={"resultat_apres_label" : "Labélisation","taux_brut_de_reussite_total_secteurs" : "Taux de réussite", "departement_y" : "Département"})
        fig6.update_layout(
            autosize=False,
            width=1000,
            height=500,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="La moyenne des taux de réussites selon lesdépartements - avant et après obtention labels",
            # change the size of the title
            title_font_size=15,    
            paper_bgcolor="#FFF7E9", 
        )


        fig7 = px.box(df_result, x="resultat_apres_label", y="taux_brut_de_reussite_total_secteurs",
            color="resultat_apres_label",
            labels={"taux_brut_de_reussite_total_secteurs" : "Taux de réussite", "resultat_apres_label" : "Résultat Avant/ Après label"})
        
        fig7.update_layout(
            autosize=False,
            width=500,
            height=250,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="Le taux de réussites avant et après obtention labels",
            title_font_size=15,
            legend_font_size=10,   
            paper_bgcolor="#FFF7E9",


        )

        # sort the column resultat_apres_label by descing order
        df_result_all.sort_values(by="resultat_apres_label",ascending=False,inplace=True)

        fig8 = px.box(df_result_all, x="resultat_apres_label", y="taux_brut_de_reussite_total_secteurs",
            color="resultat_apres_label",
            labels={"taux_brut_de_reussite_total_secteurs" : "Taux de réussite", "resultat_apres_label" : "Résultat Avec/ Sans label"})
            
        fig8.update_layout(
            autosize=False,
            width=500,
            height=250,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="Le taux de réussites sans et avec labels",
            # change the size of the title
            title_font_size=15,   
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )

        df_result_all["annee_y"] = pd.to_numeric(df_result_all["annee_y"])
        #sort label by ascending order of year and result after label
        df_result_all.sort_values(by=["annee_y"],inplace=True)

        # re transform label to str so it can be a discrete value for visualisations (discrete value)
        df_result_all["annee_y"] = df_result_all["annee_y"].apply(str)
        #plotting a boxplot
        fig5 = px.box(df_result_all, x="annee_y",
        y="taux_brut_de_reussite_total_secteurs",
        color="resultat_apres_label",
        labels={"taux_brut_de_reussite_total_secteurs" : "Taux de réussite", "resultat_apres_label" : "Résultat Avec/ Sans label", "annee_y" : "Année"})
        fig5.update_layout(
            autosize=False,
            width=1000,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="La variance du taux de réussites sans et avec labels par année",
            # change the size of the title
            title_font_size=15,    
            paper_bgcolor="#FFF7E9", 
        )

        fig9 = px.histogram(df_result, x="resultat_apres_label", y="va_reu_total", nbins=10, histfunc="avg", color="resultat_apres_label", labels={"va_reu_total" : "Valeur ajoutée", "resultat_apres_label" : "Résultat Avec/ Sans label"})
        fig9.update_layout(
            autosize=False,
            width=500,
            height=250,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="La valeurs ajoutés de réussites avant et après obtention labels",
            # change the size of the title
            title_font_size=13,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9", 
        )

        df_result_all.sort_values(by="resultat_apres_label",ascending=False,inplace=True)
        fig10 = px.box(df_result_all, x="resultat_apres_label", y="va_reu_total",
        color="resultat_apres_label",
        labels={"va_reu_total" : "Valeur ajoutée", "resultat_apres_label" : "Résultat Avec/ Sans label"})
        fig10.update_layout(
            autosize=False,
            width=500,
            height=250,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="La valeurs ajoutés de réussites avec et sans labels",
            # change the size of the title
            title_font_size=13,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9", 
        )

        fig13 = px.histogram(df_result, x="departement_y", y="va_reu_total", nbins=10,
        histfunc="avg", color="departement_y", facet_row="resultat_apres_label",labels={"va_reu_total" : "Val ajoutée", "resultat_apres_label" : "Labélisation", "departement_y" : "Département"})
        fig13.update_layout(
            autosize=False,
            width=1000,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="La moyenne des valeurs ajoutés de réussites selon les départements avant et après obtention labels",
            # change the size of the title
            title_font_size=15,    
            legend_font_size=10,
            paper_bgcolor="#FFF7E9", 
        )


        fig11 = px.box(df_result, x="resultat_apres_label",y="taux_reussite_attendu_france_total_secteurs",
        color="resultat_apres_label",
        labels={"taux_reussite_attendu_france_total_secteurs" :"Taux de réussite attendu", "resultat_apres_label" : "Résultat Avec/ Sans label"})
        fig11.update_layout(
            autosize=False,
            width=500,
            height=250,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="La variance du taux de réussite attendu avant et après obtention label",
            # change the size of the title
            title_font_size=13,    
            legend_font_size=10,
            paper_bgcolor="#FFF7E9", 
        )



        fig12 = px.box(df_result_all, x="resultat_apres_label",y="taux_reussite_attendu_france_total_secteurs",color="resultat_apres_label",
        labels={"taux_reussite_attendu_france_total_secteurs" :"Taux de réussite attendu", "resultat_apres_label" : "Résultat Avec/ Sans label"})
        fig12.update_layout(
            autosize=False,
            width=500,
            height=250,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="La variance du taux de réussite attendu sans et avec labels",
            # change the size of the title
            title_font_size=13,    
            legend_font_size=10,
            paper_bgcolor="#FFF7E9", 
        )

        content = html.Div([
            #html.H1("Analyse des données"),
            #html.Hr(),
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig2),
                ], className="columns"),
            ],
             className="row1"),

            html.Div([
                html.Div([
                    dcc.Graph(figure=fig3),
                ], className="columns"),
                html.Div([
                    dcc.Graph(figure=fig4),
                ], className="columns"),
            ],
             className="row2"),

            html.H3("Taux de réussite"),
            html.Hr(),
            
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig6),
                ], className="columns"),
            ],
             className="row3"),
            
            
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig7),
                ], className="columns"),
                html.Div([
                    dcc.Graph(figure=fig8),
                ], className="columns"),
            ],
             className="row4"),

            html.Div([
                html.Div([
                    dcc.Graph(figure=fig5),
                ], className="columns"),
            ],
             className="row5"), 
            
            html.H3("Valeur ajoutée"),
            html.Hr(),


            html.Div([
                html.Div([
                    dcc.Graph(figure=fig9),
                ], className="columns"),
                html.Div([
                    dcc.Graph(figure=fig10),
                ], className="columns"),
            ], className="row6"),

            html.Div([
                html.Div([
                    dcc.Graph(figure=fig13),
                ], className="columns"),
            ], className="row7"),
            
            html.H3("Taux de réussite attendu en France"),
            html.Hr(),

            html.Div([
                html.Div([
                    dcc.Graph(figure=fig11),
                ], className="columns"),
                html.Div([
                    dcc.Graph(figure=fig12),
                ], className="columns"),
            ], className="row8"),
        ], className="container")

        return content


# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
