import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
data_path = 'Motor_Vehicle_Collisions_-_Crashes.csv'


st.title('Motor Collisions in New York city')

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(data_path,nrows=nrows,parse_dates=[['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'],inplace=True)
    data.rename(lambda x: str(x).lower(),axis='columns',inplace=True)
    data.rename(columns={'crash_date_crash_time':'date/time'},inplace=True)
    return data

data = load_data(100000)


st.header('Injured point in NYC')
injured_people = st.slider('Number of persons injured in vehicle collisions',0,19)
st.map(data.query('injured_persons == @injured_people')[['latitude','longitude']].dropna())


st.header('Rush hour')
hour = st.slider('Hour point',0,23)
data_rush_hour = data[data['date/time'].dt.hour == hour]
median_point = (np.average(data_rush_hour['latitude']),np.average(data_rush_hour['longitude']))

st.write(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state={
        'latitude' : median_point[0],
        'longitude': median_point[1],
        'zoom' :11,
        'pitch' : 50, 
    },
    layers=[
        pdk.Layer(
        'HexagonLayer',
        data = data_rush_hour[['date/time','latitude','longitude']],
        get_position = ['longitude','latitude'],
        radius = 100,
        extruded = True,
        pickable = True,
        elevation_scale = 4,
        elevation_range = [0,1000],
    ),
    ]
))

st.header('Top 5 dangerous street by type: ')
select = st.selectbox('Type',['Pedestrians','Cyclists','Motorists'])
if select == 'Pedestrians':
    st.write(data.query('injured_pedestrians >= 1')[['on_street_name','injured_pedestrians']].sort_values(by=['injured_pedestrians'],ascending=False).dropna()[:5])
elif select == 'Cyclists':
    st.write(data.query('injured_cyclists >= 1')[['on_street_name','injured_cyclists']].sort_values(by=['injured_cyclists'],ascending=False).dropna()[:5])
else:
    st.write(data.query('injured_motorists >= 1')[['on_street_name','injured_motorists']].sort_values(by=['injured_motorists'],ascending=False).dropna()[:5])

if st.checkbox('Show raw data', False):
    st.subheader('Raw data')
    st.write(data_rush_hour)

