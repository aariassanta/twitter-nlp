import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import re


@st.cache
def get_hashtags():
    df = pd.read_csv('./csv/hashtags.csv')
    df.sort_values(by=['Freq'], ascending=False, inplace=True)
    df = df[1:]  # Elimina primer regsitro que coincide con el término de búsqueda
    return df

df_hashtags = get_hashtags()
NHashtags = str(len(df_hashtags))

def get_last_updated():
    df = pd.read_csv('./csv/last_updated.csv')
    #df.sort_values(by=['last_updated'], ascending=False, inplace=True)
    #df = df[1:]  # Elimina primer regsitro que coincide con el término de búsqueda
    last_updated = df['last_updated'].iloc[0]
    return last_updated

last_updated = get_last_updated()

def get_users():
    df = pd.read_csv('./csv/users.csv')
    df.sort_values(by=['Freq'], ascending=False, inplace=True)
    return df

df_users = get_users()
NUsers = str(len(df_users))

def get_retweeted_users():
    df = pd.read_csv('./csv/retweeted_users.csv')
    df.sort_values(by=['Freq'], ascending=False, inplace=True)
    return df

df_retweeted_users = get_retweeted_users()
NRetweeted_users = str(len(df_retweeted_users))

def get_mentions():
    df = pd.read_csv('./csv/mentions.csv')
    df.sort_values(by=['Freq'], ascending=False, inplace=True)
    return df

df_mentions = get_mentions()
NMentions = str(len(df_mentions))

def get_retweets():
    df = pd.read_csv('./csv/retweeted.csv')
    df.sort_values(by=['Freq'], ascending=False, inplace=True)
    return df

df_retweeted = get_retweets()
NRetweeted = str(len(df_retweeted))

st.markdown(
    """<head>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
  <title>COVID-19 Dashboard | Hetav Desai</title>
  <style>
  body{
      background-color: #fff;
      font-size: 40px;
  }
  </style>
</head>""", unsafe_allow_html=True
)

st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
  <h1 style="margin: auto; width: 100%;">Twitter <font color="red">PROPTECH</font> Term Interactive Dashboard</h1>
  <h2></h2><p style="margin: auto; font-weight: bold; text-align: center; width: 100%;">Data Source: Twitter Stream</p>
  <h2></h2><p style="margin: auto; font-weight: 400; text-align: center; width: 100%;">Last Updated: <font color="red">''' + last_updated + '''</font></p>
  <h2></h2><p style="margin: auto; font-weight: 400; text-align: center; width: 100%;">( Best viewed on Desktop. Use Landscape mode for Mobile View. )</p>
  <h2>______</h2>
</div>

''', unsafe_allow_html=True)

st.title('')
st.title('Seleccionar # Top Registros a visualizar')

NTop = [10,15,25]
Top = st.selectbox('', NTop, 0)

def modifica_tabla_html(tabla):
    df_html = tabla.head(Top).reset_index(drop=True).to_html(index='True', classes="table-hover") # Utiliza Clase table-hover de Bootstrap
    df_html = df_html.replace("dataframe", "")  # Elimina clase por defecto dataframe
    df_html = df_html.replace('border="1"', 'border="2"')  # Incrementa tamaño línea borde tabla
    df_html = df_html.replace("<table", '<table style="font-size:15px; text-align: center; width: 100%" ') # Cambia tamaño fuente a 15px
    #df_html = df_html.replace("<th>Hashtag", '<th style="text-align: center">Hashtag ') # Cambia alineación a header Hashtag
    df_html = df_html.replace("<th>"+ tabla.columns[0], '<th style="text-align: center">'+ tabla.columns[0]) # Cambia alineación a header Columna 1
    df_html = df_html.replace("<th>"+ tabla.columns[1], '<th style="text-align: center">'+ tabla.columns[1]) # Cambia alineación a header Columna 2
    return df_html


def modifica_tabla_retweeted(tabla):
    tabla = tabla [['Id','Tweet','Freq']] # reordena columnas de tabla 
    tabla['Tweet'] = '<a href=' + 'https://twitter.com/i/web/status/' + tabla['Id'] + ' ' + 'target="_blank"' + '><div>' + tabla['Tweet'] + '</div></a>' # Añade url link a Tweet
    tabla.drop('Id',axis='columns', inplace=True)
    df_html = tabla.head(Top).reset_index(drop=True).to_html(index='True', classes="table-hover", escape=False) # Utiliza Clase table-hover de Bootstrap
    df_html = df_html.replace("dataframe", "")  # Elimina clase por defecto dataframe
    df_html = df_html.replace('border="1"', 'border="2"')  # Incrementa tamaño línea borde tabla
    df_html = df_html.replace("<table", '<table style="font-size:15px; text-align: center; width: 100%" ') # Cambia tamaño fuente a 15px
    #df_html = df_html.replace("<th>Hashtag", '<th style="text-align: center">Hashtag ') # Cambia alineación a header Hashtag
    df_html = df_html.replace("<th>"+ tabla.columns[0], '<th style="text-align: center">'+ tabla.columns[0]) # Cambia alineación a header Columna 1
    df_html = df_html.replace("<th>"+ tabla.columns[1], '<th style="text-align: center">'+ tabla.columns[1]) # Cambia alineación a header Columna 2

    return df_html

# --------------------------------------------------------------------------------
# Análisis Hashtags
# --------------------------------------------------------------------------------

st.markdown(" ")

st.markdown(
    '''
    <div class='jumbotron text-center' style='background-color: #fff; padding:0px; margin:0px'>
    <br>
        <p style="margin: auto; font-weight: 500; text-align: center; width: 100%; font-size: 50px">Análisis Hashtags</p>
        <h2></h2><p style="margin: auto; font-weight: 400; text-align: center; width: 100%;">Generación de una tabla con la frecuencia de aparición de los hashtags</p>
    </div>
    ''',
    unsafe_allow_html=True
)

#<font color="red">This is some text!</font> 

st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
  <h2></h2><p style="margin: auto; font-weight: bold; text-align: center; width: 100%;"> <font color="red">''' + NHashtags + '''</font>  Hashtags detectados, de los cuales, los ''' + str(Top) + ''' primeros se representan en la siguiente tabla, en orden, e indicando el número de repeticiones  </p>
</div>
''', unsafe_allow_html=True)

st.write(modifica_tabla_html(df_hashtags), unsafe_allow_html=True)

st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
    <h2>______</h2>
</div>
''', unsafe_allow_html=True)

# --------------------------------------------------------------------------------
# Análisis Usuarios
# --------------------------------------------------------------------------------

st.markdown(" ")

st.markdown(
    '''
    <div class='jumbotron text-center' style='background-color: #fff; padding:0px; margin:0px'>
    <br>
        <p style="margin: auto; font-weight: 500; text-align: center; width: 100%; font-size: 50px">Análisis Usuarios</p>
        <h2></h2><p style="margin: auto; font-weight: 400; text-align: center; width: 100%;">Genera 2 tablas con los usuarios más activos y los más retuiteados</p>
    </div>
    ''',
    unsafe_allow_html=True
)

st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
  <h2></h2><p style="margin: auto; font-weight: bold; text-align: center; width: 100%;"> <font color="red">''' + NUsers + '''</font>  Usuarios únicos detectados, de los cuales, los ''' + str(Top) + ''' primeros se representan en la siguiente tabla, en orden, e indicando el número de twits generados</p>
</div>
''', unsafe_allow_html=True)


st.write(modifica_tabla_html(df_users), unsafe_allow_html=True)

#----------

st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
  <h2></h2><p style="margin: auto; font-weight: bold; text-align: center; width: 100%;"> <font color="red">''' + NRetweeted_users + '''</font>  Usuarios retuiteados detectados, de los cuales, los ''' + str(Top) + ''' primeros se representan en la siguiente tabla, en orden, e indicando el número de twits generados</p>
</div>
''', unsafe_allow_html=True)


st.write(modifica_tabla_html(df_retweeted_users), unsafe_allow_html=True)

#----------

st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
  <h2></h2><p style="margin: auto; font-weight: bold; text-align: center; width: 100%;"> <font color="red">''' + NMentions + '''</font>  Usuarios mencionados, de los cuales, los ''' + str(Top) + ''' primeros se representan en la siguiente tabla, en orden, e indicando el número de twits generados</p>
</div>
''', unsafe_allow_html=True)

st.write(modifica_tabla_html(df_mentions), unsafe_allow_html=True)

st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
    <h2>______</h2>
</div>
''', unsafe_allow_html=True)


# --------------------------------------------------------------------------------
# Análisis Retweets
# --------------------------------------------------------------------------------

st.markdown(" ")

st.markdown(
    '''
    <div class='jumbotron text-center' style='background-color: #fff; padding:0px; margin:0px'>
    <br>
        <p style="margin: auto; font-weight: 500; text-align: center; width: 100%; font-size: 50px">Análisis Retweets</p>
        <h2></h2><p style="margin: auto; font-weight: 400; text-align: center; width: 100%;">Generación de una tabla con los tweets más retuiteados y su frecuencia de aparición</p>
    </div>
    ''',
    unsafe_allow_html=True
)

#<font color="red">This is some text!</font> 

st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
  <h2></h2><p style="margin: auto; font-weight: bold; text-align: center; width: 100%;"> <font color="red">''' + NRetweeted + '''</font>  Tweets retuiteados, de los cuales, los ''' + str(Top) + ''' primeros se representan en la siguiente tabla, en orden, e indicando el número de repeticiones  </p>
</div>
''', unsafe_allow_html=True)

st.write(modifica_tabla_retweeted(df_retweeted), unsafe_allow_html=True)

st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
    <h2>______</h2>
</div>
''', unsafe_allow_html=True)

# --------------------------------------------------------------------------------
# Análisis 
# --------------------------------------------------------------------------------

values = st.slider("# TOP Hashtags representados", 1, 50, (1, 10))

st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
  <h1 style="margin: auto; width: 100%;">Twitter PROPTECH Term Interactive Dashboard</h1>
  <h2></h2><p style="margin: auto; font-weight: bold; text-align: center; width: 100%;">Data Source: Twitter Stream</p>
  <h2></h2><p style="margin: auto; font-weight: 400; text-align: center; width: 100%;">Last Updated: ''' + last_updated + '''</p>
  <h2></h2><p style="margin: auto; font-weight: 400; text-align: center; width: 100%;">( Best viewed on Desktop. Use Landscape mode for Mobile View. )</p>
  <h2>______</h2><br><br><p style="margin: auto; font-weight: 500; text-align: center; width: 100%; font-size: 50px">World Stats</p>
</div>
<div class="jumbotron text-center" style='padding: 0px'>
  <div class="row" style="background-color: #fff;width: 100%; margin: auto;">
    <div class="col-sm-4">
      <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: #000'>Total Confirmed</p>
      <p style='text-align: center; font-size: 15px; color: #000'>[''' + " " + " " + ''']</p>
      <p style='text-align: center; font-size: 35px; font-weight: bold; color: #000'>''' + " " + '''</p>
    </div>
    <div class="col-sm-4" style='background-color: #fff; border-radius: 5px'>
      <p style='text-align: center; font-weight: 400 ; color: #000'>Total Deaths</p>
      <p style='text-align: center; font-size: 15px; color: #e73631'>[''' + " " + " " + ''']</p>
      <p style='text-align: center; font-size: 35px; font-weight: bold; color: #e73631'>''' + " " + '''</p>
    </div>
    <div class="col-sm-4">
      <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: #000'>Total Recovered</p>
      <p style='text-align: center; font-size: 15px; color: #70a82c'>[''' + " " + " " + ''']</p>
      <p style='text-align: center; font-size: 35px; font-weight: bold; color: #70a82c'>''' + " " + '''</p>
    </div>
  </div>
</div>

<div class="twitter-tweet twitter-tweet-rendered" style="width: 50%; margin: 10px auto; display: flex; max-width: 550px;">
    <div class="col-4">
        <iframe id="twitter-widget-1" scrolling="no" frameborder="0" allowtransparency="true" allowfullscreen="true" class="" style="position: static; visibility: visible; width: 550px; height: 290px; display: block; flex-grow: 1;" title="Twitter Tweet" src="https://platform.twitter.com/embed/index.html?dnt=false&amp;embedId=twitter-widget-1&amp;frame=false&amp;hideCard=false&amp;hideThread=false&amp;id=1319658846160408584&amp;lang=en&amp;origin=https%3A%2F%2Fdeveloper.twitter.com%2Fen%2Fdocs%2Ftwitter-for-websites%2Fembedded-tweets%2Foverview&amp;theme=light&amp;widgetsVersion=ed20a2b%3A1601588405575&amp;width=550px" data-tweet-id="1319658846160408584">
        </iframe>
    </div>
    <div class="col-4">
        <iframe id="twitter-widget-1" scrolling="no" frameborder="0" allowtransparency="true" allowfullscreen="true" class="" style="position: static; visibility: visible; width: 550px; height: 290px; display: block; flex-grow: 1;" title="Twitter Tweet" src="https://platform.twitter.com/embed/index.html?dnt=false&amp;embedId=twitter-widget-1&amp;frame=false&amp;hideCard=false&amp;hideThread=false&amp;id=1319658846160408584&amp;lang=en&amp;origin=https%3A%2F%2Fdeveloper.twitter.com%2Fen%2Fdocs%2Ftwitter-for-websites%2Fembedded-tweets%2Foverview&amp;theme=light&amp;widgetsVersion=ed20a2b%3A1601588405575&amp;width=550px" data-tweet-id="1319658846160408584">
        </iframe>
    </div>
</div>

''', unsafe_allow_html=True)


st.title("Análisis Término Búsqueda Proptech en TWITTER")
st.markdown(
    "Welcome to this in-depth introduction to [Streamlit](www.streamlit.io)! For this exercise, we'll use an Airbnb [dataset](http://data.insideairbnb.com/united-states/ny/new-york-city/2019-09-12/visualisations/listings.csv) containing NYC listings.")
st.header("Customary quote")
st.markdown("> I just love to go home, no matter where I am, the most luxurious hotel suite in the world, I love to go home.\n\n—Michael Caine")
st.header("Airbnb NYC listings: data at a glance")
st.markdown("The first five records of the Airbnb data we downloaded.")


#df = df.style.set_properties(**{'font-size':'25pt',})

st.dataframe(df_hashtags.head(values[1])
             .assign(hack='').set_index('hack'))  # Elimina Columna Index

# st.dataframe(df.head(values[1])\
#    .styles.set_table_styles(styles)) # Elimina Columna Index

st.header("Caching our data")
st.markdown(
    "Streamlit has a handy decorator [`st.cache`](https://streamlit.io/docs/api.html#optimize-performance) to enable data caching.")
st.code("""
#@st.cache
#def get_data():
#    url = "http://data.insideairbnb.com/united-states/ny/new-york-city/2019-09-12/visualisations/listings.csv"
#    return pd.read_csv(url)
#""", language="python")
st.markdown(
    "_To display a code block, pass in the string to display as code to [`st.code`](https://streamlit.io/docs/api.html#streamlit.code)_.")
with st.echo():
    st.markdown(
        "Alternatively, use [`st.echo`](https://streamlit.io/docs/api.html#streamlit.echo).")

st.header("Where are the most expensive properties located?")
st.subheader("On a map")
st.markdown(
    "The following map shows the top 1% most expensive Airbnbs priced at $800 and above.")
#st.map(df.query("price>=800")[["latitude", "longitude"]].dropna(how="any"))
st.subheader("In a table")
st.markdown("Following are the top five most expensive properties.")
#st.write(df.query("price>=800").sort_values("price", ascending=False).head())
st.write(df_hashtags.query("Freq>=25").sort_values("Freq", ascending=False).head(values[1])
         .assign(hack='').set_index('hack'))  # Elimina Columna Index

st.subheader("Selecting a subset of columns")
# st.write(f"Out of the {df.shape[1]} columns, you might want to view only a subset. Streamlit has a [multiselect](https://streamlit.io/docs/api.html#streamlit.multiselect) widget for this.")
#defaultcols = ["name", "host_name", "neighbourhood", "room_type", "price"]
#cols = st.multiselect("Columns", df.columns.tolist(), default=defaultcols)
# st.dataframe(df[cols].head(10))

st.header("Average price by room type")
st.write("You can also display static tables. As opposed to a data frame, with a static table you cannot sorting by clicking a column header.")
# st.table(df.groupby("room_type").price.mean().reset_index()\
#    .round(2).sort_values("price", ascending=False)\
#    .assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y)))

st.table(df_hashtags.sort_values("Freq", ascending=False).head(values[1])
         .assign(hack='').set_index('hack'))  # Elimina Columna Index


st.header("Which host has the most properties listed?")

# df.style.hide_index()

#listingcounts = df.Hashtag.value_counts()
##top_host_1 = df.query('host_id==@listingcounts.index[0]')
##top_host_2 = df.query('host_id==@listingcounts.index[1]')
#top_host_1 = df.query('Hashtag==@listingcounts.index[0]')
#top_host_2 = df.query('Hashtag==@listingcounts.index[1]')
# st.write(f"""**{top_host_1.iloc[0].Hashtag}** is at the top with {listingcounts.iloc[0]} property listings.
# **{top_host_2.iloc[1].Hashtag}** is second with {listingcounts.iloc[1]} listings. Following are randomly chosen
# listings from the two displayed as JSON using [`st.json`](https://streamlit.io/docs/api.html#streamlit.json).""")
#
# st.json({top_host_1.iloc[0].host_name: top_host_1\
#    [["name", "neighbourhood", "room_type", "minimum_nights", "price"]]\
#        .sample(2, random_state=4).to_dict(orient="records"),
#        top_host_2.iloc[0].host_name: top_host_2\
#    [["name", "neighbourhood", "room_type", "minimum_nights", "price"]]\
#        .sample(2, random_state=4).to_dict(orient="records")})

st.header("What is the distribution of property price?")
st.write("""Select a custom price range from the side bar to update the histogram below displayed as a Plotly chart using
[`st.plotly_chart`](https://streamlit.io/docs/api.html#streamlit.plotly_chart).""")

#df['Freq'] = df['Freq'].astype(float)

#values = st.sidebar.slider("Freqrange", float(df.Freq.min()), float(df.Freq.clip(upper=1000.).max()), (50., 300.))


#f = px.histogram(df[df['Freq'].between(values[0],values[1])], x="Freq", nbins=15, title="Freq distribution")
# f.update_xaxes(title="Freq")
#f.update_yaxes(title="No. of Hashtags Mentions")

# Tree Map
#f = px.treemap(df.head(25), path=['Hashtag'], values='Freq', title="Freq distribution")
f = px.treemap(df_hashtags.head(values[1]), path=[
               'Hashtag'], values='Freq', title="Hashtags Frequency distribution")

st.plotly_chart(f)


r = px.line_polar(df_hashtags.head(values[1]), r='Freq',
                  theta='Hashtag', line_close=True)

st.plotly_chart(r)

# st.balloons()

st.header("What is the distribution of availability in various neighborhoods?")
st.write("Using a radio button restricts selection to only one option at a time.")
st.write("💡 Notice how we use a static table below instead of a data frame. \
Unlike a data frame, if content overflows out of the section margin, \
a static table does not automatically hide it inside a scrollable area. \
Instead, the overflowing content remains visible.")
neighborhood = st.radio("Neighborhood", df.neighbourhood_group.unique())
show_exp = st.checkbox("Include expensive listings")
show_exp = " and price<200" if not show_exp else ""


@st.cache
def get_availability(show_exp, neighborhood):
    return df.query(f"""neighbourhood_group==@neighborhood{show_exp}\
        and availability_365>0""").availability_365.describe(
        percentiles=[.1, .25, .5, .75, .9, .99]).to_frame().T


st.table(get_availability(show_exp, neighborhood))
st.write("At 169 days, Brooklyn has the lowest average availability. At 226, Staten Island has the highest average availability.\
    If we include expensive listings (price>=$200), the numbers are 171 and 230 respectively.")
st.markdown(
    "_**Note:** There are 18431 records with `availability_365` 0 (zero), which I've ignored._")

df.query("availability_365>0").groupby("neighbourhood_group")\
    .availability_365.mean().plot.bar(rot=0).set(title="Average availability by neighborhood group",
                                                 xlabel="Neighborhood group", ylabel="Avg. availability (in no. of days)")
st.pyplot()

st.header("Properties by number of reviews")
st.write("Enter a range of numbers in the sidebar to view properties whose review count falls in that range.")
minimum = st.sidebar.number_input("Minimum", min_value=0)
maximum = st.sidebar.number_input("Maximum", min_value=0, value=5)
if minimum > maximum:
    st.error("Please enter a valid range")
else:
    df.query("@minimum<=number_of_reviews<=@maximum").sort_values("number_of_reviews", ascending=False)\
        .head(50)[["name", "number_of_reviews", "neighbourhood", "host_name", "room_type", "price"]]

st.write("486 is the highest number of reviews and two properties have it. Both are in the East Elmhurst \
    neighborhood and are private rooms with prices $65 and $45. \
    In general, listings with >400 reviews are priced below $100. \
    A few are between $100 and $200, and only one is priced above $200.")
st.header("Images")
pics = {
    "Cat": "https://cdn.pixabay.com/photo/2016/09/24/22/20/cat-1692702_960_720.jpg",
    "Puppy": "https://cdn.pixabay.com/photo/2019/03/15/19/19/puppy-4057786_960_720.jpg",
    "Sci-fi city": "https://storage.needpix.com/rsynced_images/science-fiction-2971848_1280.jpg"
}
pic = st.selectbox("Picture choices", list(pics.keys()), 0)
st.image(pics[pic], use_column_width=True, caption=pics[pic])

st.markdown("## Party time!")
st.write("Yay! You're done with this tutorial of Streamlit. Click below to celebrate.")
btn = st.button("Celebrate!")
if btn:
    st.balloons()
