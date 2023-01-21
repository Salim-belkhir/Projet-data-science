# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# Install the required packages if you don't have them
#"""
#!pip install dash
#!pip install dash-bootstrap-components
#!pip install pandas
#!pip install plotly
#!pip install kaleido
#!pip install folium
#!pip install seaborn
#!pip install matplotlib
#"""

import json
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# Import necessary libraries
import matplotlib.pyplot as plt
import seaborn as sns
import folium # for maps
import plotly.graph_objects as go
import kaleido


# Chargement des données

df_resultPro_all = pd.read_csv('data/df_result_all.csv', sep=',',low_memory=False)
df_resultPro = pd.read_csv('data/df_result.csv', sep=',',low_memory=False)
df_resultGen_all = pd.read_csv('data/df_result_allGen.csv', sep=',',low_memory=False)
df_resultGen = pd.read_csv('data/df_result_Gen.csv', sep=',',low_memory=False)
df_proportion_etablissement = pd.read_csv('data/df_proportion_etablissement.csv', sep=',',low_memory=False)
df_proportion_etablissement_filtered = pd.read_csv('data/df_proportion_etablissement_filtered.csv', sep=',',low_memory=False)
df_unique_labellisation = pd.read_csv('data/df_unique_labellisation.csv', sep=',',low_memory=False)
df_labels_numeriques = pd.read_csv('data/df_labels_numeriques.csv', sep=',',low_memory=False)
df_lycee_gen = pd.read_csv('data/df_lycee_gen.csv', sep=',',low_memory=False) 
df_lycees_professionels = pd.read_csv('data/df_lycees_professionels.csv', sep=',',low_memory=False)
df_lycee_all = pd.read_csv('data/df_lycee_all.csv', sep=',',low_memory=False)
df2M = pd.read_csv('data/df2M.csv', sep=',',low_memory=False)
dflabels = pd.read_csv('data/dflabels.csv', sep=',',low_memory=False)
dfIPSM = pd.read_csv('data/dfIPSM.csv', sep=',',low_memory=False)
dfIPSALL = pd.read_csv('data/dfIPSALL.csv', sep=',',low_memory=False)
dflabels_IPS = pd.read_csv('data/dflabels_IPS.csv', sep=',',low_memory=False)



external_stylesheets = [
    {
        "rel": "stylesheet",
    },
]



# Creation d'un instance de l'application et la relie a la feuille de style et Bootstrap
app = Dash("Forme Scolaire Analyse", external_stylesheets=[dbc.themes.BOOTSTRAP])

# Titre de l'application
app.title = "Forme Scolaire Analyse"

# Définition du layout de l'application
app.layout = html.Div(
    children=[
        html.Div(
            children=[
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
                                                {"label": "Etat Des Lieux Générale", "value": 1},
                                                {"label": "Lycée Professionel", "value": 2},
                                                {"label": "Lycée Générale et Technologique", "value": 3},
                                                {"label": "Collège", "value": 4},
                                            ],
                                            value=2,
                                        ),
                                        html.Div(id="output"),
                                    ],
                                    className="radio-group",
                                )
                            ],
                            className="data",
                        ),
                    ],
                    className="parametre",
                    id="parametre",
                ),
                dbc.Card
                (
                    [
                        dbc.CardHeader(
                            dbc.Tabs(
                                [

                                ],
                                id="card-tabs",
                                active_tab="tab-1",
                            ),
                            className="card-header",
                        ),
                        dbc.CardBody
                        (
                            [
                                html.Div
                                (
                                    children=[
                                        html.Div(
                                            children=[],
                                            className="counts",
                                            id="counts",
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
                                )
                            ],
                            className="card-body",
                        ),
                    ], className="right-side-content",
                )
            ],
            className="content-container",
        )
    ],
    className="main-container",
)


# Callback pour le choix des onglets en fonction du choix de l'utilisateur
@app.callback(Output("card-tabs", "children"), [Input("radios", "value")])
def tabs(value):
    if value == 1:
        return [
            dbc.Tab(label="Proportion", tab_id="tab-1", label_style={"color": "#0DCAF0"}),
            dbc.Tab(label="Carte", tab_id="tab-2",label_style={"color": "#0DCAF0"}),
        ]
    elif value == 2:
        return [
            dbc.Tab(label="Analyse Générale", tab_id="tab-1", label_style={"color": "#0DCAF0"}),
            dbc.Tab(label="Taux De Réussite", tab_id="tab-2",label_style={"color": "#0DCAF0"}),
            dbc.Tab(label="Valeur Ajoutée", tab_id="tab-3",label_style={"color": "#0DCAF0"}),
            dbc.Tab(label="Taux De Réussite Attendu", tab_id="tab-4", label_style={"color": "#0DCAF0"}),
        ]
    elif value == 3:
        return [
            dbc.Tab(label="Analyse Générale", tab_id="tab-1", label_style={"color": "#0DCAF0"}),
            dbc.Tab(label="Taux De Réussite", tab_id="tab-2",label_style={"color": "#0DCAF0"}),
            dbc.Tab(label="Valeur Ajoutée", tab_id="tab-3",label_style={"color": "#0DCAF0"}),
            dbc.Tab(label="Taux De Réussite Attendu", tab_id="tab-4", label_style={"color": "#0DCAF0"}),
        ]
    elif value == 4:
        return [
            dbc.Tab(label="Analyse Générale Sur Les Proportions", tab_id="tab-1", label_style={"color": "#0DCAF0"}),
            dbc.Tab(label="Labélisation", tab_id="tab-2",label_style={"color": "#0DCAF0"}),
            dbc.Tab(label="Indice De Position Sociale", tab_id="tab-3",label_style={"color": "#0DCAF0"}),
        ]



# Callback pour le choix des données à représenté en fonction du choix de l'utilisateur
@app.callback(Output("graph", "children"), [Input("card-tabs", "active_tab")], [Input("radios", "value")])
def data_choice2(value, value2):
    content = ""
    if (value == "tab-1" or value == "tab-3" or value == "tab-4") and value2 == 1:
        
        # La répartition des Ecole, lycce et collège en Occitanie
        fig1 = px.pie(df_proportion_etablissement, values='effectif', names="type etablissement")
        fig1.update_layout(
            autosize=False,
            width=500,
            height=250,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="La proportion de chaque type d'établissementé scolaire en Occitanie",
            title_font_size=13,
            paper_bgcolor="#FFF7E9",
        )

        # La proportion des lycées labelisés et non labelisés en Occitanie
        fig2 = px.pie(df_unique_labellisation, values='effectif', names="labelise",)
        fig2.update_layout(
            autosize=False,
            width=500,
            height=250,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="La proportion des lycées labelisés et non labelisés en Occitanie",
            title_font_size=13,
            paper_bgcolor="#FFF7E9",
        )

        #transform the label to numeric
        df_labels_numeriques["label"] = pd.to_numeric(df_labels_numeriques["label"])
        #transform the annee to numeric
        df_labels_numeriques["annee"] = pd.to_numeric(df_labels_numeriques["annee"])
        #sorted by label ascending
        df_labels_numeriques.sort_values(by=["label","annee"],inplace=True)
        # re transform label in df_labels_numeriques_temp to str so it can be discrete 
        df_labels_numeriques["label"] = df_labels_numeriques["label"].apply(str)
        # re transform annee to str so it can be discrete value
        df_labels_numeriques["annee"] = df_labels_numeriques["annee"].apply(str)
        
        #Plot un histogram de la distribution des labels
        fig3 = px.histogram(df_labels_numeriques, x="label", nbins=10, color="label",facet_col="annee" )
        fig3.update_layout(
            autosize=False,
            width=500,
            height=300,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="Distribution des Labels par année",
            title_font_size=13,
            paper_bgcolor="#FFF7E9",
        )

        # les lycées polyvalents et non polyvalents
        df_lycee_polyvalent = pd.merge(df_lycee_gen, df_lycees_professionels, left_on="UAI", right_on="UAI",how="inner")

        #calcul des proportions
        nbre_lycee_all = df_lycee_all["UAI"].nunique()
        nbre_lycee_polyvalent = df_lycee_polyvalent["UAI"].nunique()
        nbre_lycee_non_polyvalent = nbre_lycee_all - nbre_lycee_polyvalent

        #camamber data parameters
        labels = ['lycées polyvalents', 'lycées non polyvalents']
        values = [nbre_lycee_polyvalent,nbre_lycee_non_polyvalent]

        # Affichage du camamber data pour les lycées polyvalents et non polyvalents
        fig4 = go.Figure(data=[go.Pie(labels=labels, values=values, title = "La proportions des Lycées polyvalents et non polyvalents")])
        fig4.update_layout(
            autosize=False,
            width=400,
            height=250,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title_font_size=13,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )

        #calcul du nombre des lycées profess non polyvalents
        nbre_lycee_pro_polyvalent_inclus = df_lycees_professionels['UAI'].nunique()
        nbre_lycee_pro_uniques = nbre_lycee_pro_polyvalent_inclus - nbre_lycee_polyvalent
        #calcul du nombre des lycées générales non polyvalents
        nbre_lycee_gen_polyvalent_inclus = df_lycee_gen["UAI"].nunique()
        nbre_lycee_gen_uniques = nbre_lycee_gen_polyvalent_inclus - nbre_lycee_polyvalent

        #camamber data parametres pour les lycées polyvalents, professionels et générales
        labels=["Nbr lycées générales et technologiques","Nbr lycées professionels",
            "Nbr lycées polyvalents"]
        values=[nbre_lycee_gen_uniques,nbre_lycee_pro_uniques,nbre_lycee_polyvalent]

        # Affichage du camamber data pour les lycées polyvalents, professionels et générales
        fig5 = go.Figure(data=[go.Pie(labels=labels, values=values, title = "La proportions des Lycées polyvalents, professionels , générales et technologiques")])
        fig5.update_layout(
            autosize=False,
            width=500,
            height=250,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title_font_size=13,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )


        content = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig1),
                ], className="columns"),
                
                html.Div([
                    dcc.Graph(figure=fig2),
                ], className="columns"),
            ],
             className="row1"),

            html.Div([
                html.Div([
                    dcc.Graph(figure=fig3),
                ], className="columns"),
            ],
             className="row2"),

            html.Div([
                html.Div([
                    dcc.Graph(figure=fig4),
                ], className="columns"),
                
                html.Div([
                    dcc.Graph(figure=fig5),
                ], className="columns"),
            ],
                className="row3"),
        ], className="container")
        return content
    elif value == "tab-2" and value2 == 1:
        # Creation DE LA MAP
        m = folium.Map(location=[43.9310426514, 2.15075998953], zoom_start=6)
        #adding the markers to the map
        with open('data/fr-en-occitanie-label-numerique-lycee.geojson') as f:
            labels_numeriques_geoGson = json.load(f)
        for feature in labels_numeriques_geoGson['features']:
            label = feature['properties']['label']
            annee = feature['properties']['annee']
            localite = feature['properties']['localite']
            departement = feature['properties']['departement']
            nom_etablissement = feature['properties']['nom_etablissement']
            position = feature['properties']['position']
            rne = feature['properties']['rne']
            folium.Marker(position, popup=f'Label: {label}, Annee: {annee}, Localite:{localite}, Departement: {departement}, Nom_etablissement:{nom_etablissement}, RNE: {rne}').add_to(m)

        #transform the label to numeric
        df_labels_numeriques["label"] = pd.to_numeric(df_labels_numeriques["label"])
        #create df_labels_numeriques sorted by label ascending
        df_labels_numeriques_temp = df_labels_numeriques.sort_values(by="label")
        # re transform label in df_labels_numeriques_temp to str so it can be discrete value
        df_labels_numeriques_temp["label"] = df_labels_numeriques_temp["label"].apply(str)
        #plot map
        fig1 = px.scatter_mapbox(df_labels_numeriques_temp, lat="latitude",lon="longitude", color="label",
        color_discrete_map={'1' : 'blue', '2' : 'orange', '3' :"red"}, size_max=100, zoom=7,mapbox_style='stamen-terrain')
        fig1.update_layout(
            autosize=False,
            width=1000,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title_font_size=13,
            paper_bgcolor="#FFF7E9",
        )

        content = html.Div([
            html.Div([
                html.Div([  
                    html.H4("Les positions géographiques des lycées labelisés en Occitanie"),
                    html.Iframe(id='map', srcDoc=m._repr_html_(), width='1000px', height='400px')
                ], className="columns"),
            ],
            className="row1"),
            html.Div([
                html.Div([
                    html.H4("La distribution des labels en Occitanie"),
                    dcc.Graph(figure=fig1),
                ], className="columns"),
            ],
            className="row2"),
        ], className="container")
        return content

    if value == "tab-1" and value2 == 2:
        # La proportion de lycées professionnels labelisés 
        nbre_lycee_professionnel = df_resultPro_all['code_etablissement'].nunique()
        nbre_lycee_professionel_labelise = df_resultPro_all['rne'].nunique()
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
        df_resultPro["annee_x"] = df_resultPro["annee_x"].astype(str)
        df_resultPro["rne"] = df_resultPro["rne"].astype(str)
        df_proportion_lycee_labelise_annee = df_resultPro.groupby("annee_x")["rne"].nunique()
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
        df_resultPro_all["annee_y"] = df_resultPro_all["annee_y"].astype(str)
        df_resultPro_all["code_etablissement"] = df_resultPro_all["code_etablissement"].astype(str)
        df_proportion_lycee_non_labelise_annee = df_resultPro_all.query("label_true == False").groupby("annee_y")["code_etablissement"].nunique()
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
        
        content = html.Div([
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
        ], className="container")
        return content

    elif value == "tab-2" and value2 == 2:
        # transform label to numeric
        df_resultPro["label"] = pd.to_numeric(df_resultPro["label"])
        #sort label by ascending order
        df_resultPro.sort_values(by="label",inplace=True)
        # re transform label to str so it can be a discrete value for visualisations (discrete value)
        df_resultPro["label"] = df_resultPro["label"].apply(str)
        
        #plotting a histogram
        #fig5 = px.histogram(df_resultPro[df_resultPro["resultat_apres_label"] == True], x="label", y="taux_brut_de_reussite_total_secteurs", nbins=10, histfunc="avg", color="label")
        #fig5.update_layout(
        #    autosize=False,
        #    width=500,
        #    height=250,
        #    margin=dict(l=0, r=0, b=0, t=35, pad=0), 
        #    title="La moyenne des taux bruts de réussites des lycee après obtention de leurs labels (tous secteurs) selon les labels",    
        #    paper_bgcolor="#FFF7E9", 
        #)

        fig6 = px.box(df_resultPro, x="departement_y",y="taux_brut_de_reussite_total_secteurs", color="departement_y",
        facet_row="resultat_apres_label",
        labels={"resultat_apres_label" : "Labélisation","taux_brut_de_reussite_total_secteurs" : "Taux de réussite", "departement_y" : "Département"})
        fig6.update_layout(
            autosize=False,
            width=1000,
            height=500,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="La moyenne des taux de réussites selon les départements - avant et après obtention labels",
            # change the size of the title
            title_font_size=15,    
            paper_bgcolor="#FFF7E9", 
        )


        fig7 = px.box(df_resultPro, x="resultat_apres_label", y="taux_brut_de_reussite_total_secteurs",
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
        df_resultPro_all.sort_values(by="resultat_apres_label",ascending=False,inplace=True)

        fig8 = px.box(df_resultPro_all, x="resultat_apres_label", y="taux_brut_de_reussite_total_secteurs",
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

        df_resultPro_all["annee_y"] = pd.to_numeric(df_resultPro_all["annee_y"])
        #sort label by ascending order of year and result after label
        df_resultPro_all.sort_values(by=["annee_y"],inplace=True)

        # re transform label to str so it can be a discrete value for visualisations (discrete value)
        df_resultPro_all["annee_y"] = df_resultPro_all["annee_y"].apply(str)
        #plotting a boxplot
        fig5 = px.box(df_resultPro_all, x="annee_y",
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

        content = html.Div([            
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
        ], className="container")
        return content
    elif value == "tab-3" and value2 == 2:
        fig9 = px.histogram(df_resultPro, x="resultat_apres_label", y="va_reu_total", nbins=10, histfunc="avg", color="resultat_apres_label", labels={"va_reu_total" : "Valeur ajoutée", "resultat_apres_label" : "Résultat Avec/ Sans label"})
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

        df_resultPro_all.sort_values(by="resultat_apres_label",ascending=False,inplace=True)
        fig10 = px.box(df_resultPro_all, x="resultat_apres_label", y="va_reu_total",
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

        fig13 = px.histogram(df_resultPro, x="departement_y", y="va_reu_total", nbins=10,
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
        content = html.Div([
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
        ], className="container")
        return content
    elif value == "tab-4" and value2 == 2:
        fig11 = px.box(df_resultPro, x="resultat_apres_label",y="taux_reussite_attendu_france_total_secteurs",
        color="resultat_apres_label",
        labels={"taux_reussite_attendu_france_total_secteurs" :"Taux de réussite attendu", "resultat_apres_label" : "Résultat Avec/ Sans label"})
        fig11.update_layout(
            autosize=False,
            width=500,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="La variance du taux de réussite attendu avant et après obtention label",
            # change the size of the title
            title_font_size=13,    
            legend_font_size=10,
            paper_bgcolor="#FFF7E9", 
        )

        fig12 = px.box(df_resultPro_all, x="resultat_apres_label",y="taux_reussite_attendu_france_total_secteurs",color="resultat_apres_label",
        labels={"taux_reussite_attendu_france_total_secteurs" :"Taux de réussite attendu", "resultat_apres_label" : "Résultat Avec/ Sans label"})
        fig12.update_layout(
            autosize=False,
            width=500,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0), 
            title="La variance du taux de réussite attendu sans et avec labels",
            # change the size of the title
            title_font_size=13,    
            legend_font_size=10,
            paper_bgcolor="#FFF7E9", 
        )
        content = html.Div([
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

    if value == "tab-1" and value2 == 3:
        nbre_lycee_professionnel = df_resultGen_all['UAI'].nunique()
        nbre_lycee_professionel_labelise = df_resultGen_all['rne'].nunique()
        nbre_lycee_professionnel_non_labelise = nbre_lycee_professionnel - nbre_lycee_professionel_labelise
        values = [nbre_lycee_professionnel_non_labelise,nbre_lycee_professionel_labelise]
        labels = ['Non Labelisé', 'Labelisé']
        fig1 = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig1.update_layout(
            autosize=False,
            width=520,
            height=250,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="La proportions des Lycées labelisés parmis les d'enseignement général et technologique",
            # change the size of the title
            title_font_size=12,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )

        # La variation du nombre des lycées labelisés selon les années
        
    
        df_resultGen["annee_x"] = df_resultGen["annee_x"].astype(str)
        df_resultGen["rne"] = df_resultGen["rne"].astype(str)
        df_proportion_lycee_labelise_annee = df_resultGen.groupby("annee_x")["rne"].nunique()
        df_proportion_lycee_labelise_annee = df_proportion_lycee_labelise_annee.reset_index()
        
        #plotting a histogram 
        fig2 = px.histogram(df_proportion_lycee_labelise_annee, x="annee_x", y="rne",
                        color="annee_x",
                        labels={"rne" :"Nombre des lycées labelisés", "annee_x" : "Années"})
        fig2.update_layout(
            autosize=False,
            width=500,
            height=300,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="La variation du nombre des lycées labelisés selon les années",
            # change the size of the title
            title_font_size=13,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )

        # La variation du nombre des lycées non labelisés selon les années
        df_proportion_lycee_non_labelise_annee = df_resultGen_all.query("label_true == False").groupby("annee_y")["UAI"].nunique()
        df_proportion_lycee_non_labelise_annee = df_proportion_lycee_non_labelise_annee.reset_index()
        df_proportion_lycee_non_labelise_annee["annee_y"] = df_proportion_lycee_non_labelise_annee["annee_y"].apply(str)
        

        #plotting a histogram 
        fig3 = px.histogram(df_proportion_lycee_non_labelise_annee, x="annee_y", y="UAI",
                        color="annee_y",
                            labels={"UAI" :"Nombre des lycées non labelisés", "annee_y" : "Année"})
        fig3.update_layout(
            autosize=False,
            width=500,
            height=300,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="La variation du nombre des lycées non labelisés selon les années",
            # change the size of the title
            title_font_size=13,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )

        content = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig1),
                ], className="columns"),
            ], className="row1"),

            html.Div([
                html.Div([
                    dcc.Graph(figure=fig2),
                ], className="columns"),
                html.Div([
                    dcc.Graph(figure=fig3),
                ], className="columns"),
            ], className="row2"),

        ], className="container")
        return content
    elif value == "tab-2" and value2 == 3:
        fig1 = px.box(df_resultGen, x="departement_y", y="taux_reussite_toutes_series",
             color="departement_y",
                       facet_row="resultat_apres_label",
                      labels={"departement_y" :"Département", "taux_reussite_toutes_series" : "Taux de réussite", "resultat_apres_label" : "Labelisation"})
        fig1.update_layout(
            autosize=False,
            width=1000,
            height=500,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="La moyenne des taux de réussites selon les départements - avant et après obtention labels",
            # change the size of the title
            title_font_size=15,
            paper_bgcolor="#FFF7E9",
        )

        
        df_resultGen_all.sort_values(by="resultat_apres_label",ascending=False,inplace=True)
        df_resultGen.sort_values(by="resultat_apres_label",ascending=False,inplace=True)
        
        # Trier selon le taux de réussite des lycées labelisés 
        fig2 = px.box(df_resultGen, x="resultat_apres_label", y="taux_reussite_toutes_series", color="resultat_apres_label",
                      labels={"resultat_apres_label" :"Labelisation", "taux_reussite_toutes_series" : "Taux de réussite"})
        fig2.update_layout(
            autosize=False,
            width=500,
            height=300,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="La moyenne des taux de réussites avant et après obtention labels",
            # change the size of the title
            title_font_size=13,
            paper_bgcolor="#FFF7E9",
        )

        fig3 = px.box(df_resultGen_all, x="resultat_apres_label", y="taux_reussite_toutes_series",
             color="resultat_apres_label", labels={"resultat_apres_label" :"Labelisation", "taux_reussite_toutes_series" : "Taux de réussite"})
        fig3.update_layout(
            autosize=False,
            width=500,
            height=300,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="La variance des taux de réussites sans et avec labels",
            # change the size of the title
            title_font_size=13,
            paper_bgcolor="#FFF7E9",
        )

        df_resultGen_all["annee_y"] = pd.to_numeric(df_resultGen_all["annee_y"])
        
        #sort label by ascending order
        df_resultGen_all.sort_values(by="annee_y",inplace=True)

        # re transform label to str so it can be a discrete value for visualisations (discrete value)
        df_resultGen_all["annee_y"] = df_resultGen_all["annee_y"].apply(str)

        #plotting a bocplot 
        fig4 = px.box(df_resultGen_all, x="annee_y", y="taux_reussite_toutes_series",
                    color="resultat_apres_label", labels={"annee_y" :"Année", "taux_reussite_toutes_series" : "Taux de réussite", "resultat_apres_label" : "Labelisation"})
        fig4.update_layout(title_text="La moyenne des taux de réussites sans et avec labels par année")
        fig4.update_layout(
            autosize=False,
            width=1000,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="La moyenne des taux de réussites sans et avec labels par année",
            # change the size of the title
            title_font_size=15,
            paper_bgcolor="#FFF7E9",
        )


        content = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig1),
                ], className="columns"),
            ], className="row1"),

            html.Div([
                html.Div([
                    dcc.Graph(figure=fig2),
                ], className="columns"),
                html.Div([
                    dcc.Graph(figure=fig3),
                ], className="columns"),
            ], className="row2"),

            html.Div([
                html.Div([
                    dcc.Graph(figure=fig4),
                ], className="columns"),
            ], className="row3"),
            
        ], className="container")
        return content            
    elif value == "tab-3" and value2 == 3:
        df_resultGen.sort_values(by="resultat_apres_label",ascending=False,inplace=True)
        
        fig1 = px.histogram(df_resultGen, x="resultat_apres_label", y="va_taux_reussite_toutes_series", nbins=10, histfunc="avg", color="resultat_apres_label", labels={"resultat_apres_label" :"Labelisation", "va_taux_reussite_toutes_series" : "Valeur ajoutée"})
        fig1.update_layout(
            autosize=False,
            width=500,
            height=300,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="La moyenne des valeurs ajoutés de réussites (toutes séries) avant et après obtention labels",
            # change the size of the title
            title_font_size=12,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )

        df_resultGen_all.sort_values(by="resultat_apres_label",ascending=False,inplace=True)


        fig2 = px.box(df_resultGen_all, x="resultat_apres_label", y="va_taux_reussite_toutes_series",
             color="resultat_apres_label",
             labels={"resultat_apres_label" :"Labelisation", "va_taux_reussite_toutes_series" : "Valeur ajoutée"})
        fig2.update_layout(
            autosize=False,
            width=500,
            height=300,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="La variance des valeurs ajoutés de réussites (toutes séries) sans et avec labels",
            # change the size of the title
            title_font_size=13,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )

        fig3 = px.histogram(df_resultGen, x="departement_y", y="va_taux_reussite_toutes_series", nbins=10, histfunc="avg", color="departement_y", facet_row="resultat_apres_label", labels={"departement_y" :"Département", "va_taux_reussite_toutes_series" : "Valeur ajoutée", "resultat_apres_label" : "Labelisation"})
        fig3.update_layout(
            autosize=False,
            width=1000,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="La moyenne des valeurs ajoutés de réussites selon les départements avant et après obtention labels",
            # change the size of the title
            title_font_size=15,
            paper_bgcolor="#FFF7E9",
        )

        content = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig1),
                ], className="columns"),
                html.Div([
                    dcc.Graph(figure=fig2),
                ], className="columns"),
            ], className="row1"),

            html.Div([
                html.Div([
                    dcc.Graph(figure=fig3),
                ], className="columns"),
            ], className="row2"),

        ], className="container")
        return content
    elif value == "tab-4" and value2 == 3:
        fig1 = px.box(df_resultGen, x="resultat_apres_label", y="taux_reussite_attendu_toutes_series", color="resultat_apres_label",
                    labels={"resultat_apres_label" :"Labelisation", "taux_reussite_attendu_toutes_series" : "Taux de réussite attendu"})
        fig1.update_layout(
            autosize=False,
            width=500,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="La variance du taux de réussite attendu avant et après obtention labels",
            # change the size of the title
            title_font_size=13,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )

        

        fig2 = px.box(df_resultGen_all, x="resultat_apres_label", y="taux_reussite_attendu_toutes_series", color="resultat_apres_label",
                    labels={"resultat_apres_label" :"Labelisation", "taux_reussite_attendu_toutes_series" : "Taux de réussite attendu"})
        fig2.update_layout(
            autosize=False,
            width=500,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="La variance du taux de réussite attendu sans et avec labels",
            # change the size of the title
            title_font_size=13,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )

        content = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig1),
                ], className="columns"),
                html.Div([
                    dcc.Graph(figure=fig2),
                ], className="columns"),
            ], className="row1"),

        ], className="container")
        return content
    if (value == "tab-1" or value == "tab-4")  and value2 == 4:
        df2M["année"] = df2M["année"].astype(str)
        fig1 = px.histogram(df2M, x="année", y="admis", color="année", labels={"année" :"Année", "admis" : "Nombre d'admis"})
        fig1.update_layout(
            autosize=False,
            width=500,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="Distribution du nombre d'admis en fonction de l'année pour l'académie de Montpellier",
            # change the size of the title
            title_font_size=11,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )

        # Total d'inscrits pour toutes les séries
        fig2 = px.histogram(df2M, x="année", y="inscrits", color="année",labels={"année" :"Année", "inscrits" : "Nombre d'inscrits"})
        fig2.update_layout(
            autosize=False,
            width=500,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="Distribution du nombre d'inscrits en fonction de l'année pour l'académie de Montpellier",
            # change the size of the title
            title_font_size=11,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )

        fig3 = px.histogram(df2M, x="année", y="inscrits", color="série", facet_col="série",labels={"année" :"Année", "inscrits" : "Nombre d'inscrits"})
        fig3.update_layout(
            autosize=False,
            width=1000,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="Distribution du nombre d'inscrits en fonction de l'année et de la série pour l'académie de Montpellier",
            # change the size of the title
            title_font_size=11,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )        
        
        content = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig1),
                ], className="columns"),

                html.Div([
                    dcc.Graph(figure=fig2),
                ], className="columns"),

            ], className="row1"),

            html.Div([
                html.Div([
                    dcc.Graph(figure=fig3),
                ], className="columns"),
            ], className="row2"),

        ], className="container")
        return content
    elif value =="tab-2" and value2 == 4:      
        dflabels["Label"] = dflabels["Label"].apply(str)
        dflabels["Département"] = dflabels["Département"].apply(str)
        dflabels["Année"] = dflabels["Année"].apply(str)
        fig1 = px.histogram(dflabels, x="Année", y="Label", color="Année", facet_col="Label")
        fig1.update_layout(
            autosize=False,
            width=1000,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="Distribution du nombre de labels en fonction de l'année pour les collèges de l'académie de Montpellier",
            # change the size of the title
            title_font_size=11,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )
        
        # Compte du nombre de collèges dont le RNE est unique ayant un label de 1
        nblabels1 = dflabels.query("Label == '1'")["RNE"].nunique()
        # Compte du nombre de collèges dont le RNE est unique ayant un label de 2
        nblabels2 = dflabels.query("Label == '2'")["RNE"].nunique()
        # Compte du nombre de collèges dont le RNE est unique ayant un label de 3
        nblabels3 = dflabels.query("Label == '3'")["RNE"].nunique()
        labelvals = [nblabels1, nblabels2, nblabels3]
        labelnames = ['Label 1', 'Label 2', 'Label 3']
        fig2 = px.pie(values=labelvals, names=labelnames, labels={"values" : "Nombre de collèges", "names" : "Labels"})
        fig2.update_layout(
            autosize=False,
            width=500,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="Distribution du nombre de labels pour les collèges de l'académie de Montpellier",
            # change the size of the title
            title_font_size=11,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )


        content = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig1),
                ], className="columns"),
            ], className="row1"),
            
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig2),
                ], className="columns"),
            ], className="row2"),

        ], className="container")
        return content
    elif value =="tab-3" and value2 == 4:
        # IPS moyen en fct du département
        fig1 = px.histogram(dfIPSM, x="Département", y="IPS", color="Département", histfunc="avg", labels={"Département" :"Département", "IPS" : "IPS moyen"})
        fig1.update_layout(
            autosize=False,
            width=500,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="Distribution de l'IPS moyen en fonction du département pour les collèges de l'académie de Montpellier",
            # change the size of the title
            title_font_size=12,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )

        # IPS moyen en fct du département
        fig2 = px.histogram(dfIPSALL, x="Académie", y="IPS", color="Académie", histfunc="avg",labels={"Académie" :"Académie", "IPS" : "IPS moyen"})
        fig2.update_layout(
            autosize=False,
            width=500,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="Distribution de l'IPS moyen en fonction de l'académie pour les collèges en 2021",
            # change the size of the title
            title_font_size=12,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )

        dflabels_IPS["Label"] = dflabels_IPS["Label"].apply(str)
        fig3 = px.histogram(dflabels_IPS, x="Label", y="IPS", color="Label", histfunc="avg", labels={"Label" :"Label", "IPS" : "IPS moyen"})
        fig3.update_layout(
            autosize=False,
            width=500,
            height=400,
            margin=dict(l=0, r=0, b=0, t=35, pad=0),
            title="Distribution de l'IPS moyen en fonction du label pour les collèges de l'académie de Montpellier en 2021",
            # change the size of the title
            title_font_size=12,
            legend_font_size=10,
            paper_bgcolor="#FFF7E9",
        )

        content = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig1),
                ], className="columns"),
            ], className="row1"),

            html.Div([
                html.Div([
                    dcc.Graph(figure=fig2),
                ], className="columns"),

                html.Div([
                    dcc.Graph(figure=fig3),
                ], className="columns"),
            ], className="row2"),

        ], className="container")
        return content
        

    



# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
