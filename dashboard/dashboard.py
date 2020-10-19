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
#external_stylesheets = ['./bWLwgP.css']
#external_stylesheets = ['/Users/Alfredo/twitter-nlp/dashboard/skeleton.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



header = html.H2(children="Análisis Término Búsqueda PROPTECH")

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

# Radar Chart
df = pd.read_csv('../csv/hashtags.csv')
df.sort_values(by=['Freq'],ascending=False, inplace=True)

df = df[1:] # Elimina primer regsitro que coincide con el término de búsqueda
#chart5 = px.line_polar(df.head(25), r=df.Freq.head(25), theta=df.Hashtag.head(25), line_close=True)
chart5 = px.line_polar(df.head(25), r='Freq', theta='Hashtag', line_close=True)

chart5.update_layout(
    title="Hashtags más utilizados"
)
chart5.update_traces(fill='toself')

graph5 = dcc.Graph(
        id='graph5',
        figure=chart5,
        className="six columns"
    )

# Tree Map
chart6 = px.treemap(df.head(25), path=['Hashtag'], values='Freq')

chart6.update_layout(
    title="Hashtags más utilizados"
)

graph6 = dcc.Graph(
        id='graph6',
        figure=chart6,
        className="six columns"
    )

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')

#chart_table1 = go.Figure(data=[go.Table(
#    header=dict(values=list(df.columns),
#                fill_color='paleturquoise',
#                align='left'),
#    cells=dict(values=[df.Rank, df.State, df.Postal, df.Population],
#               fill_color='lavender',
#               align='left'))
#])

# ---------------------- Tweets más Retuiteados

df = pd.read_csv('../csv/retweeted.csv')
df.sort_values(by=['Freq'],ascending=False, inplace=True)

# Convierte URL en hyperlinks a la URL

def convert(row):
    #print(row)
    return '<a href="https://twitter.com/i/web/status/{}">{}</a>'.format(row['Id'],  row['Tweet'])

df['Tweet'] = df.apply(convert, axis=1)

chart_table_retweeted = go.Figure(data=[go.Table(
    columnwidth = [400,80],
    #header=dict(values=list(df.columns)),
    header=dict(values=['Tweet','Freq']),
    cells=dict(values=[df.Tweet, df.Freq], align=['left', 'center'])
)]
)

chart_table_retweeted.update_layout(
    title="Tweets más retuiteados"
)

table_retweeted= dcc.Graph(
        id='chart_table_retweeted',
        figure=chart_table_retweeted,
        className="six columns"
    )

# ---------------------- Hashtags más utilizados

df = pd.read_csv('../csv/hashtags.csv')
df.sort_values(by=['Freq'],ascending=False, inplace=True)

chart_table_hashtags = go.Figure(data=[go.Table(
    columnwidth = [400,80],
    header=dict(values=list(df.columns)),
    cells=dict(values=[df.Hashtag, df.Freq], align=['left', 'center'])
)]
)

chart_table_hashtags.update_layout(
    title="Hashtags más utilizados"
)

table_hashtags= dcc.Graph(
        id='chart_table_hashtags',
        figure=chart_table_hashtags,
        className="six columns"
    )
    
# ---------------------- Usuarios más activos

df = pd.read_csv('../csv/users.csv')
df.sort_values(by=['Freq'],ascending=False, inplace=True)

chart_table_users = go.Figure(data=[go.Table(
    columnwidth = [400,80],
    header=dict(values=list(df.columns)),
    cells=dict(values=[df.User, df.Freq], align=['left', 'center'])
)]
)

chart_table_users.update_layout(
    title="Usuarios más activos"
)

table_users= dcc.Graph(
        id='chart_table_users',
        figure=chart_table_users,
        className="six columns"
    )

# ---------------------- Usuarios más retuiteados

df = pd.read_csv('../csv/retweeted_users.csv')
df.sort_values(by=['Freq'],ascending=False, inplace=True)

chart_table_retweeted_users = go.Figure(data=[go.Table(
    columnwidth = [400,80],
    header=dict(values=list(df.columns)),
    cells=dict(values=[df.User, df.Freq], align=['left', 'center'])
)]
)

chart_table_retweeted_users.update_layout(
    title="Usuarios más retuiteados"
)

table_retweeted_users= dcc.Graph(
        id='chart_table_retweeted_users',
        figure=chart_table_retweeted_users,
        className="six columns"
    )

# ---------------------- Usuarios más mencionados

df = pd.read_csv('../csv/mentions.csv')
df.sort_values(by=['Freq'],ascending=False, inplace=True)

chart_table_mentions = go.Figure(data=[go.Table(
    columnwidth = [400,80],
    header=dict(values=list(df.columns)),
    cells=dict(values=[df.Mentioned, df.Freq], align=['left', 'center'])
)]
)

chart_table_mentions.update_layout(
    title="Usuarios más mencionados"
)

table_mentions= dcc.Graph(
        id='chart_table_mentions',
        figure=chart_table_mentions,
        className="six columns"
    )

# ---------------------- Palabras más mencionadas

df = pd.read_csv('../csv/words.csv')
df.sort_values(by=['Freq'],ascending=False, inplace=True)

chart_table_words = go.Figure(data=[go.Table(
    columnwidth = [400,80],
    header=dict(values=list(df.columns)),
    cells=dict(values=[df.Word, df.Freq], align=['left', 'center'])
)]
)

chart_table_words.update_layout(
    title="Palabras más mencionadas"
)

table_words= dcc.Graph(
        id='chart_table_words',
        figure=chart_table_words,
        className="six columns"
    )

# ---------------------- URL's más mencionadas

df = pd.read_csv('../csv/urls.csv')
df.sort_values(by=['Freq'],ascending=False, inplace=True)

# Convierte URL en hyperlinks a la URL

def convert(row):
    #print(row)
    return '<a href="{}">{}</a>'.format(row['URL'],  row['URL'])

df['URL'] = df.apply(convert, axis=1)

chart_table_urls = go.Figure(data=[go.Table(
    columnwidth = [400,80],
    header=dict(values=list(df.columns)),
    cells=dict(values=[df.URL, df.Freq], align=['left', 'center'])
)]
)

chart_table_urls.update_layout(
    title="URL's más mencionadas"
)

table_urls= dcc.Graph(
        id='chart_table_urls',
        figure=chart_table_urls,
        className="six columns"
    )

# ---------------------- Localizaciones más utilizadas

df = pd.read_csv('../csv/locations.csv')
df.fillna(value={'Location':'No Informada'}, inplace=True)
df.sort_values(by=['Freq'],ascending=False, inplace=True)

chart_table_locations = go.Figure(data=[go.Table(
    columnwidth = [400,80],
    header=dict(values=list(df.columns)),
    cells=dict(values=[df.Location, df.Freq], align=['left', 'center'])
)]
)

chart_table_locations.update_layout(
    title="Localizaciones más habituales"
)

table_locations= dcc.Graph(
        id='chart_table_locations',
        figure=chart_table_locations,
        className="six columns"
    )


# Generación presentación HTML

row1 = html.Div(children=[graph5, graph6])

row2 = html.Div(children=[table_retweeted, table_hashtags])

row3 = html.Div(children=[table_retweeted_users, table_users])

row4 = html.Div(children=[table_mentions, table_words])

row5 = html.Div(children=[table_urls, table_locations])

layout = html.Div(children=[header, row1, row2, row3, row4, row5], style={"text-align": "center"})

app.layout = layout

if __name__ == "__main__":
    app.run_server(debug=True)