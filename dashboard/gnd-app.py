import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk
import os
import glob

path = os.path.dirname(__file__)

st.sidebar.header("Satzart wählen")
satzart = st.sidebar.selectbox(
    "Über welche GND-Satzart möchten Sie etwas erfahren?",
    ('alle', "Tp - Personen", "Tb - Körperschaften", "Tg - Geografika", "Ts - Sachbegriffe", "Tu - Werke", "Tf - Veranstaltungen")
)
st.sidebar.info('Diese Widgets wurden von der Python Community in der Deutschen Nationalbibliothek geschrieben. Das sind die GitHub-User niko2342, ramonvoges, a-wendler sowie Christian Baumann.')

def ramon():
    df = pd.read_csv(f'{path}/wirkungsorte-top50.csv')
    df.drop(columns=['id'], inplace=True)
    df.rename(columns={'name': 'Name', 'count': 'Anzahl'}, inplace=True)

    st.header('TOP 10 Wirkungsorte von GND-Personen')
    st.markdown('Von allen Personensätzen (Tp) weisen 782.682 Angaben zum Wirkungsort der jeweiligen Person auf.')

    #Balkendiagramm
    orte_filt = st.slider('Zeige Top ...', min_value=3, max_value=len(df), value=10, step=1)
    graph_count = alt.Chart(df.nlargest(orte_filt, 'Anzahl', keep='all')).mark_bar().encode(alt.X('Name:N', sort='y'), y='Anzahl', tooltip=['Name', 'Anzahl'], color='Name')
    st.altair_chart(graph_count, use_container_width=True)

    #Karte
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
    opacity=0.5,
    stroked=True,
    filled=True,
    radius_min_pixels=1,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position='[lon, lat]',
    get_radius="Anzahl",
    get_fill_color=[255, 140, 0],
    get_line_color=[0, 0, 0],
)

    st.pydeck_chart(pdk.Deck(
    scatterplotlayer,
    initial_view_state=INITIAL_VIEW_STATE,
    map_style=pdk.map_styles.LIGHT,
    tooltip={"html": "<b>{Name}</b><br \>Wirkungsort von {Anzahl} Personen"}))

def wirkungsorte_musik():
    musiker_orte = pd.read_csv('musiker_orte.csv', sep='\t', index_col='idn')
    st.header('Wirkungszentren der Musik 1400-2010')
    st.write('Eine Auswertung der veröffentlichten Titel von Musikern und deren Wirkungszeiten erlaubt Rückschlüsse auf die musikalischen Zentren, wie sie im Bestand der DNB repräsentiert sind.')
    limiter = st.slider('Jahresfilter', min_value=1400, max_value=musiker_orte['jahrzehnt'].max(), value=(1900), step=10)
    #Karte
    INITIAL_VIEW_STATE = pdk.ViewState(
        latitude=50.67877877706058,
        longitude=8.129981238464392,
        zoom=4.5,
        max_zoom=16,
        bearing=0
    )

    COLOR_BREWER_BLUE_SCALE = [
    [240, 249, 232],
    [204, 235, 197],
    [168, 221, 181],
    [123, 204, 196],
    [67, 162, 202],
    [8, 104, 172],
]
    musiker_layer = pdk.Layer(
    "HeatmapLayer",
    musiker_orte.loc[(musiker_orte['jahrzehnt'] == limiter)],
    opacity=0.9,
    intensity=0.8,
    get_position='[lon, lat]',
    color_range=COLOR_BREWER_BLUE_SCALE,
    threshold=0.1,
    aggregation=pdk.types.String("SUM"),
    get_weight="count",
)

    st.pydeck_chart(pdk.Deck(
    musiker_layer,
    initial_view_state=INITIAL_VIEW_STATE,
    map_style=pdk.map_styles.LIGHT))

    st.table(musiker_orte.loc[(musiker_orte['jahrzehnt'] == limiter),['count','name']].nlargest(10, 'count'))

def stat_allgemein():   
    #Gesamt Entity Count
    with open(f"{path}/../stats/gnd_entity_count.csv", "r") as f:
        entities = f'{int(f.read()):,}'
    st.write(f"GND-Entitäten gesamt: {entities.replace(',','.')}")

    #Relationen
    rels = pd.read_csv(f'{path}/../stats/gnd_codes_all.csv', index_col=False)
    st.header('Relationen')
    rels_filt = st.slider('Zeige Top ...', 5, len(rels), 10, 1)
    relation_count = alt.Chart(rels.nlargest(rels_filt, 'count', keep='all')).mark_bar().encode(
        alt.X('code', title='Relationierungs-Code', sort='-y'),
        alt.Y('count', title='Anzahl'),
        alt.Color('code', sort='-y'),
        tooltip=['count'],
    )
    st.altair_chart(relation_count, use_container_width=True)

    with open(f"{path}/../stats/gnd_relation_count.csv", "r") as f:
        relations = f'{int(f.read()):,}'
    st.write(f"Relationen zwischen Entitäten gesamt: {relations.replace(',','.')}")

    #Systematik
    classification = pd.read_csv(f'{path}/../stats/gnd_classification_all.csv', index_col=False)
    st.header('Systematik')
    class_filt = st.slider('Zeige Top ...', 5, len(classification), 10, 1)
    classification_count = alt.Chart(classification.nlargest(class_filt, 'count', keep='all')).mark_bar().encode(
        alt.X('id', title='Notation', sort='-y'),
        alt.Y('count', title='Anzahl'),
        alt.Color('id', sort='-y'),
        tooltip=['count']
    )
    st.altair_chart(classification_count, use_container_width=True)

@st.cache
def load_gnd_top_daten():
    gnd_top_df = pd.DataFrame()
    for file in glob.glob(f'{path}/../stats/title_gnd_top10_*.csv'):
        gnd_top_df = gnd_top_df.append(pd.read_csv(file, index_col=None))
    return gnd_top_df

#main
st.title('GND-Dashboard beta')
st.warning('Die Daten werden noch überarbeitet und sind als vorläufig anzusehen. Die finale Version dieses Dashboards mit aktuellen Daten erscheint am 7. Juni 2021')
st.info('Hier finden Sie statistische Auswertungen der GND und ihrer Verknüpfungen mit den Titeldaten der Deutschen Nationalbibliothek (Stand der Daten: Mai 2021). Wählen Sie links die Satzart, die Sie interessiert, und sie erhaltenden die verfügbaren Auswertungen und Statstiken.')

#Entities nach Typ
df = pd.read_csv(f'{path}/../stats/gnd_entity_types.csv', index_col=False, names=['entity','count'])
df['level'] = df.entity.str[2:3]
df.entity = df.entity.str[:2]

if satzart == 'alle':

    entity_count = alt.Chart(df).mark_bar().encode(
        alt.X('sum(count)', title='Datensätze pro Katalogisierungslevel'),
        alt.Y('entity', title='Satzart'),
        alt.Color('level'),
        tooltip=['count']
    )
    st.header('Entitäten und Katalogisierungslevel')

else:

    entity_count = alt.Chart(df.loc[df['entity'].str.startswith(satzart[:2])]).mark_bar().encode(
        alt.X('sum(count)', title='Datensätze pro Katalogisierungslevel'),
        alt.Y('entity', title='Satzart'),
        alt.Color('level'),
        tooltip=['count']
    )
    st.header(f'Katalogisierungslevel in Satzart {satzart}')
st.altair_chart(entity_count, use_container_width=True)


if satzart == 'alle':
    stat_allgemein()

elif satzart == "Tp - Personen":
    #hier werden dann alle widgets als einzelne funktionen aufgerufen, die zur jeweiligen Kategorie gehören sollen

    ramon()
elif satzart == 'Tb - Körperschaften':
    tb_stat()

elif satzart == "Tg - Geografika":
    wirkungsorte_musik()
    ramon()


st.header('GND in der Deutschen Nationalbibliothek')

#top_diagram mit Satzartfilter
if satzart == 'alle':
    st.header(f'TOP 10 GND-Entitäten in DNB-Titeldaten')
    top_daten = pd.read_csv(f'{path}/../stats/title_gnd_top10.csv', index_col=None)

    gnd_top = alt.Chart(top_daten).mark_bar().encode(
        alt.X('name', title='Entitäten', sort='-y'),
        alt.Y('count', title='Anzahl'),
        alt.Color('name', sort='-y'),
        tooltip=['count'],
    )

else:
    st.header(f'TOP 10 {satzart} in DNB-Titeldaten')
    top_daten = load_gnd_top_daten()

    gnd_top = alt.Chart(top_daten.loc[top_daten['bbg'].str.startswith(satzart[:2], na=False)]).mark_bar().encode(
        alt.X('name', title='Entitäten', sort='-y'),
        alt.Y('count', title='Anzahl'),
        alt.Color('name', sort='-y'),
        tooltip=['count'],
    )
st.altair_chart(gnd_top, use_container_width=True)

#Durchschnittliche Verknüpfungen pro Satzart

if satzart == 'alle':
    #Anzahl GND-Verknüpfungen in DNB-Titeldaten

    with open(f"{path}/../stats/title_gnd_links.csv", "r") as f:
        links = f'{int(f.read()):,}'

    #Anzahl der verknüpften GND-Entitäten in DNB-Titeldaten
    with open(f"{path}/../stats/title_gnd_links_unique.csv", "r") as f:
        uniques = f'{int(f.read()):,}'

    #Durchschnittliche Anzahl an GND-Verknüpfungen pro DNB-Titeldatensatz
    with open(f"{path}/../stats/title_gnd_mean.csv", "r") as f:
        mean = str(round(float(f.read()),2)).replace('.',',')

    st.write(f"{links.replace(',','.')} Verknüpfungen zu {uniques.replace(',','.')} GND-Entitäten in den DNB-Titeldaten. Durchschnittlich {mean} GND-Verknüpfungen pro DNB-Titeldatensatz")
else:
    with open(f"{path}/../stats/title_gnd_mean_{satzart[:2]}.csv", "r") as f:
        mean = str(round(float(f.read()),2)).replace('.',',')
    st.write(f'Durchschnittlich {mean} Verknüpfungen zu {satzart}-Sätzen pro DNB-Titeldatensatz')
