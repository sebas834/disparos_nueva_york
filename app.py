import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import base64

# df = pd.read_csv('Bases/NYPD_Shooting_Incident_Data__Historic_.csv')
# enviar BD a streamlit
# st.write(df)

#--------------------------------------------------------------------------------------------------------------------------------------------------------
# que abarque todo el ancho de la página
st.set_page_config(layout='wide')

# Definir el título del dashboard y su estilo
st.markdown("<h1 style = 'text-align:center;color:cyan;'> 🗽💥Histórico de disparos en New York 💥🗽</h1>", unsafe_allow_html=True)

#--------------------------------------------------------------------------------------------------------------------------------------------------------

#### Tratatamiento de datos #####
#### función que toma una url y hace los cambios necesarios y lo retorna con los cambios

@st.cache(persist = True) #permite que quede la info almacenada si se corre una vez
def load_data(url):
    df = pd.read_csv(url)
    df['OCCUR_DATE'] = pd.to_datetime(df['OCCUR_DATE'])
    df['OCCUR_TIME'] = pd.to_datetime(df['OCCUR_TIME'], format = '%H:%M:%S') # el formato está en ese orden
    df['YEAR'] = df['OCCUR_DATE'].dt.year
    df['HOUR'] = df['OCCUR_TIME'].dt.hour
    df['YEARMONTH'] = df['OCCUR_DATE'].dt.strftime('%Y%m') #se saca año mes Y:2001, y:01
    df.columns = df.columns.map(str.lower)
    return df

# función que permite descargar un DF a la máquina local
def get_table_download_link(df):
    csv = df.to_csv(index = False)
    b64 = base64.b64encode(csv.encode()).decode() # convetir el df en bits
    href = f'<a href="data:file/csv;base64,{b64}" download="datos.csv">Descargar archivo csv</a>'
    return href

#------------------------------------------------------------------------------------------------------------------------------------------------------
df = load_data('Bases/NYPD_Shooting_Incident_Data__Historic_.csv')
#------------------------------------------------------------------------------------------------------------------------------------------------------

############################################################## INDICADORES ########################################################################
c1, c2, c3, c4, c5 = st.columns((1,1,1,1,1))

c1.markdown("<h3 style = 'text-align:left;color:white;'> Top Sexo </h3>", unsafe_allow_html=True)

# porcentaje de cada sexo

# nombre de la categoría que más se repite
top_perp_name = df['perp_sex'].value_counts().index[0]

# porcentaje de la categoría que más se repite
top_perp_num = (round(df['perp_sex'].value_counts()/df['perp_sex'].value_counts().sum(),2)*100)[0]

c1.text('Atacante: ' + str(top_perp_name) + '; ' + str(top_perp_num) + '%')

# nombre de la categoría que más se repite de las víctimas
top_vic_name = df['vic_sex'].value_counts().index[0]

# porcentaje de la categoría que más se repite
top_vic_num = (round(df['vic_sex'].value_counts()/df['vic_sex'].value_counts().sum(),2)*100)[0]

c1.text('Víctima: ' + str(top_vic_name) + '; ' + str(top_vic_num) + '%')

##################################################
# porcentaje de cada raza

c2.markdown("<h3 style = 'text-align:left;color:white;'> Top Raza </h3>", unsafe_allow_html=True)

# nombre de la categoría que más se repite
top_perp_name = df['perp_race'].value_counts().index[0]

# porcentaje de la categoría que más se repite
top_perp_num = (round(df['perp_race'].value_counts()/df['perp_race'].value_counts().sum(),2)*100)[0]

c2.text('Atacante: ' + str(top_perp_name) + '; ' + str(top_perp_num) + '%')

############################
# nombre de la categoría que más se repite
top_vic_name = df['perp_race'].value_counts().index[0]

# porcentaje de la categoría que más se repite
top_vic_num = (round(df['vic_race'].value_counts()/df['vic_race'].value_counts().sum(),2)*100)[0]

c2.text('Víctima: ' + str(top_vic_name) + '; ' + str(top_vic_num) + '%')

#############################################
# porcentaje de cada edad

c3.markdown("<h3 style = 'text-align:left;color:white;'> Top Edad </h3>", unsafe_allow_html=True)

# nombre de la categoría que más se repite
top_perp_name = df['perp_age_group'].value_counts().index[0]

# porcentaje de la categoría que más se repite
top_perp_num = (round(df['perp_age_group'].value_counts()/df['perp_age_group'].value_counts().sum(),2)*100)[0]

c3.text('Atacante: ' + str(top_perp_name) + '; ' + str(top_perp_num) + '%')

############################
# nombre de la categoría que más se repite
top_vic_name = df['vic_age_group'].value_counts().index[0]

# porcentaje de la categoría que más se repite
top_vic_num = (round(df['vic_age_group'].value_counts()/df['vic_age_group'].value_counts().sum(),2)*100)[0]

c3.text('Víctima: ' + str(top_vic_name) + '; ' + str(top_vic_num) + '%')

#############################################
# porcentaje de cada edad

c4.markdown("<h3 style = 'text-align:left;color:white;'> Top Barrio </h3>", unsafe_allow_html=True)

# nombre de la categoría que más se repite
top_perp_name = df['boro'].value_counts().index[0]

# porcentaje de la categoría que más se repite
top_perp_num = (round(df['boro'].value_counts()/df['boro'].value_counts().sum(),2)*100)[0]

c4.text('Nombre: ' + str(top_perp_name) + '; ' + str(top_perp_num) + '%')

#############################################
# porcentaje de cada hora

c5.markdown("<h3 style = 'text-align:left;color:white;'> Top Hora </h3>", unsafe_allow_html=True)

# nombre de la categoría que más se repite
top_perp_name = df['hour'].value_counts().index[0]

# porcentaje de la categoría que más se repite
top_perp_num = (round(df['hour'].value_counts()/df['hour'].value_counts().sum(),2)*100)[0]

c5.text('Nombre: ' + str(top_perp_name) + '; ' + str(top_perp_num) + '%')


########################################################## GRÁFICA MAPAS ############################################
#--------------------------------------------------------------------------------------------------------------------------------------------------------
# dividir en dos columnas
c1, c2 = st.columns((1,1)) # cantidad de espacio que va a ocupar cada columna

# definir lo que contiene la columna 1
c1.markdown("<h3 style = 'text-align:center;color:white;'> ¿Dónde han ocurrido disparos en New York?</h3>", unsafe_allow_html=True)
year = c1.slider('Año en que ocurrió el suceso', df.year.min(), df.year.max())
c1.map(df[df['year'] == year][['latitude','longitude']])

# definir lo que contiene la columna 2
c2.markdown("<h3 style = 'text-align:center;color:white;'> ¿A qué hora ocurren disparon en New York?</h3>", unsafe_allow_html=True)

hour = c2.slider('Hora en la que ocurrió el suceso', df.hour.min(), df.hour.max())
df2 = df[df['hour'] == hour]

# gráfico
c2.write(pdk.Deck( # Código para crear el mapa
    # Set up del mapa
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state={
        'latitude' : df['latitude'].mean(),
        'longitude': df['longitude'].mean(),
        'zoom' : 9.5,
        'pitch': 50
        },

    # Capa con información
    layers = [pdk.Layer(
    'HexagonLayer',  # cómo queremos que nos muestre el gráfico: bolitas, hexágonos...
    data = df2[['latitude','longitude']],
    get_position = ['longitude','latitude'],  #como se llama la latitud y longitud en el DF
    radius = 100,
    extruded = True,   # permite que se eleven las celdas hexagonales dentro del mapa
    elevation_scale = 4, # escala hasta la cual puede estar elevado
    elevation_range = [0,1000])] # los valores entre los cuales se puede elevar
    ))

#--------------------------------------------------------------------------------------------------------------------------------------------------------
################################################ SERIE DE TIEMPO ##################################################
# pongo st porque ya va completo, no en columnas
st.markdown("<h3 style = 'text-align:center;color:white;'> ¿Cómo ha sido la evolución disparos por barrio en New York?</h3>", unsafe_allow_html=True)

df3 = df.groupby(['yearmonth','boro'])[['incident_key']].count().reset_index().rename(columns = {'incident_key':'disparos'})
fig = px.line(df3, x = 'yearmonth',y = 'disparos',color = 'boro', width = 1300, height = 450)

# Editar gráfica
fig.update_layout(
        title_x=0.5,
        template = 'simple_white',
        xaxis_title="<b>Año/mes<b>",
        yaxis_title='<b>Cantidad de incidentes<b>',
        legend_title_text='',
        
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y = 1.02,
            xanchor="right",
            x = 0.8))

# mandar figura a streamlit
st.plotly_chart(fig)

#--------------------------------------------------------------------------------------------------------------------------------------------------------
############################################# 4 GRÁFICOS ##############################################################
# se divide en 4 secciones y cada una con el mismo tamaño
c4, c5, c6, c7 = st.columns((1,1,1,1))

c4.markdown("<h3 style = 'text-align:center;color:white;'> ¿Qué edad tienen los atacantes? </h3>", unsafe_allow_html=True)

# cantidad de veces que un atacante tipo cierta edad
df2 = df.groupby(['perp_age_group'])[['incident_key']].count().reset_index().rename(columns = {'incident_key':'disparos'})
df2['perp_age_group'] = df2['perp_age_group'].replace({'940':'N/A','224':'N/A','1020':'N/A','UNKNOWN':'N/A'})
df2['perp_age_group2'] = df2['perp_age_group'].replace({'<18':'1','18-24':'2','24-44':'3','44-54':'4','65+':'5','N/A':'6'}) # variable nueva donde se reemplaza valores y luego se ordena por esos valores
df2 = df2.sort_values(by = 'perp_age_group2')

fig = px.bar(df2, x = 'disparos', y = 'perp_age_group', orientation = 'h', width = 340, height = 310)

fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        xaxis_title="<b>Atacante<b>",
        yaxis_title='<b>Edades<b>')

c4.plotly_chart(fig)

####################
c5.markdown("<h3 style = 'text-align:center;color:white;'> ¿Qué edad tienen las víctimas? </h3>", unsafe_allow_html=True)

# cantidad de veces que un atacante tipo cierta edad
df2 = df.groupby(['vic_age_group'])[['incident_key']].count().reset_index().rename(columns = {'incident_key':'disparos'})
df2['vic_age_group'] = df2['vic_age_group'].replace({'940':'N/A','224':'N/A','1020':'N/A','UNKNOWN':'N/A'})
df2['perp_age_group2'] = df2['vic_age_group'].replace({'<18':'1','18-24':'2','24-44':'3','44-54':'4','65+':'5','N/A':'6'}) # variable nueva donde se reemplaza valores y luego se ordena por esos valores
df2 = df2.sort_values(by = 'perp_age_group2')

fig = px.bar(df2, x = 'disparos', y = 'vic_age_group', orientation = 'h', width = 340, height = 310)

fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        xaxis_title="<b>Víctima<b>",
        yaxis_title='<b>Edades<b>')

c5.plotly_chart(fig)

####################

c6.markdown("<h3 style = 'text-align:center;color:white;'> ¿Cuál es el sexo del atacante? </h3>", unsafe_allow_html=True)

df2 = df.groupby(['perp_sex'])[['incident_key']].count().reset_index().sort_values('incident_key',ascending = False)

fig = px.pie(df2, values = 'incident_key', names = 'perp_sex', width=300, height=300)

# Editar gráfica

fig.update_traces(marker=dict(colors=['green', 'blue', 'purple']))

fig.update_layout(
        title_x=0.5,
        template = 'simple_white',
        plot_bgcolor='rgba(0,0,0,0)',
        legend_title_text='',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y = -0.4,
            xanchor="center",
            x = 0.5))

c6.plotly_chart(fig)

####################
c7.markdown("<h3 style = 'text-align:center;color:white;'> ¿Cuál es el sexo de la víctima? </h3>", unsafe_allow_html=True)

df2 = df.groupby(['vic_sex'])[['incident_key']].count().reset_index().sort_values('incident_key',ascending = False)

fig = px.pie(df2, values = 'incident_key', names = 'vic_sex', width=300, height=300)

# Editar gráfica

fig.update_traces(marker=dict(colors=['green', 'purple' ,'blue']))

fig.update_layout(
        title_x=0.5,
        template = 'simple_white',
        plot_bgcolor='rgba(0,0,0,0)',
        legend_title_text='',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y = -0.4,
            xanchor="center",
            x = 0.5))

c7.plotly_chart(fig)

####################
######################## EVOLUCIÓN DISPAROS ########################
st.markdown("<h3 style = 'text-align:center;color:white;'> Evolución de disparos por año en las horas con más y menos sucesos </h3>", unsafe_allow_html=True)

df2 = df[df['hour'].isin([23,9])].groupby(['year','hour'])[['incident_key']].count().reset_index()
df2['hour'] = df2['hour'].astype('category')    

fig = px.bar(df2, x='year',y='incident_key',color='hour',barmode='group',width=1150,height=450)

fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        xaxis_title="<b>Año<b>",
        yaxis_title='<b>Cantidad de disparos<b>',
        legend_title = 'Hora')


st.plotly_chart(fig)
# --------------------------
####################  OPCIÓN DE OBSERVAR LA TABLA Y LINK DE DESCARGA ####################
# para que muestre una opción ver o no la tabla 

if st.checkbox('Obtener datos por fecha y barrio', False):
    df2 = df.groupby(['occur_date','boro'])[['incident_key']].count().reset_index().rename(columns={'boro':'Barrio','occur_date':'Fecha','incident_key':'Disparos'})
    df2['Fecha'] = pd.to_datetime(df2['Fecha']).dt.date
    
    fig = go.Figure(data = [go.Table(
        header = dict(values=list(df2.columns), # encabezado
                      fill_color = 'black',
                      line_color = 'darkslategray'),
        
        cells = dict(values = [df2.Fecha, df2.Barrio, df2.Disparos],
                      fill_color = 'darkcyan',
                      line_color = 'lightgrey'))
        ])
    fig.update_layout(width = 500, height = 450)
    
    st.write(fig)
    
    st.markdown(get_table_download_link(df2), unsafe_allow_html = True)
    
        
####################
        
        
        