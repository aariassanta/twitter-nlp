import pandas as pd
from sklearn.datasets import load_iris

import plotly.express as px
import plotly.graph_objects as go

import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as table

iris = load_iris() ## It returns simple dictionary like object with all data.

# Creating dataframe of total data
iris_df = pd.DataFrame(data=np.concatenate((iris.data,iris.target.reshape(-1,1)), axis=1), columns=(iris.feature_names+['Flower Type']))
iris_df["Flower Name"] = [iris.target_names[int(i)] for i in iris_df["Flower Type"]]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



header = html.H2(children="IRIS Dataset Analysis")

chart1 = px.scatter(data_frame=iris_df,
           x="sepal length (cm)",
           y="petal length (cm)",
           color="Flower Name",
           size=[1.0]*150,
           title="sepal length (cm) vs petal length (cm) color-encoded by flower type")


graph1 = dcc.Graph(
        id='graph1',
        figure=chart1,
        className="six columns"
    )

chart2 = px.scatter(data_frame=iris_df,
           x="sepal width (cm)",
           y="petal width (cm)",
           color="Flower Name",
           size=[1.0]*150,
           title="sepal width (cm) vs petal width (cm) color-encoded by flower type")


graph2 = dcc.Graph(
        id='graph2',
        figure=chart2,
        className="six columns"
    )

chart3 = px.histogram(data_frame=iris_df,
             x="sepal length (cm)",
             color="Flower Name",
             title="Distributions of sepal length (cm) color-encoded by flower name")

graph3 = dcc.Graph(
        id='graph3',
        figure=chart3,
        className="six columns"
    )

chart4 = px.box(data_frame=iris_df,
           x="Flower Name",
           y="sepal width (cm)",
           color="Flower Name",
           title="concentration of sepal width (cm) by flower types")


graph4 = dcc.Graph(
        id='graph4',
        figure=chart4,
        className="six columns"
    )

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')

#chart_table1 = go.Figure(data=[go.Table(
#    header=dict(values=list(df.columns),
#                fill_color='paleturquoise',
#                align='left'),
#    cells=dict(values=[df.Rank, df.State, df.Postal, df.Population],
#               fill_color='lavender',
#               align='left'))
#])

chart_table1 = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns)),
    cells=dict(values=[df.Rank, df.State, df.Postal, df.Population])
)]
)

chart_table1.update_layout(
    title="Título de Tabla"
)

table1 = dcc.Graph(
        id='chart_table1',
        figure=chart_table1,
        className="six columns"
    )

row1 = html.Div(children=[graph1, graph3])

row2 = html.Div(children=[graph2, table1])

layout = html.Div(children=[header, row1, row2], style={"text-align": "center"})

app.layout = layout

if __name__ == "__main__":
    app.run_server(debug=True)