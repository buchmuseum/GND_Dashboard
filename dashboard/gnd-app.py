import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk

st.sidebar.header("Satzart wählen")
satzart = st.sidebar.selectbox(
    "Über welche GND-Satzart möchten Sie etwas erfahren?",
    ("Tp - Personen", "Tb - Körperschaften", "Tg - Geografika", "Ts - Sachbegriffe", "Tu - Werke")
)

def ramon():
    df = pd.read_csv('./wirkungsorte-top50.csv')
    df.drop(columns=['id'], inplace=True)
    
    graph_count = alt.Chart(df).mark_bar().encode(x=alt.X('name:N', sort='y'), y='count', tooltip=['name', 'count'])
    st.altair_chart(graph_count, use_container_width=True)

    INITIAL_VIEW_STATE = pdk.ViewState(
    latitude=50.67877877706058,
    longitude=8.129981238464392,
    zoom=4.5,
    max_zoom=16,
    bearing=0
    )

    scatterplotlayer = pdk.Layer(
    "ScatterplotLayer",
    df,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_min_pixels=1,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position='[lon, lat]',
    get_radius="count",
    get_fill_color=[255, 140, 0],
    get_line_color=[0, 0, 0],
)

    st.pydeck_chart(pdk.Deck(
    scatterplotlayer,
    initial_view_state=INITIAL_VIEW_STATE,
    map_provider="mapbox",
    map_style=pdk.map_styles.LIGHT,
    api_keys={'mapbox':'pk.eyJ1IjoiYXduZGxyIiwiYSI6ImNrbWt0OWtxOTE0ZW4ycHFvOGNjb2FwcXgifQ.lv0Ikqq0rIYB6wgkMzrx6Q'},
    tooltip={"html": "<b>{name}</b><br \>Wirkungsort von {count} Personen"}))

    

if satzart == "Tp - Personen":
    #hier werden dann alle widgets als einzelne funktionen aufgerufen, die zur jeweiligen Kategorie gehören sollen
    
    ramon()
elif satzart == 'Tb - Körperschaften':
    st.write('körperschaften')