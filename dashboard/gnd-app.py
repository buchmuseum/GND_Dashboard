from matplotlib.pyplot import title
import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk
import os
import glob
from wordcloud import WordCloud
import streamlit_analytics

path = os.path.dirname(__file__)

streamlit_analytics.start_tracking()

@st.cache
def load_gnd_top_daten(typ):
    gnd_top_df = pd.DataFrame()
    for file in glob.glob(f'{path}/../stats/title_gnd_{typ}_*.csv'):
        gnd_top_df = gnd_top_df.append(pd.read_csv(file, index_col=None))
    return gnd_top_df

def sachbegriff_cloud():
    #wordcloud der top 100 sachbegriffe eines auszuwählenden tages der letzten 10 werktage
    st.header('TOP 100 Sachbegriffe pro Tag')
    st.write('Wählen Sie ein Datum aus den letzten 10 Werktagen vor der letzten Aktualisierung der Daten des Dashboards und sehen Sie eine Wordcloud der 100 meistverwendeten GND-Sachbegriffe dieses Tages. Die Größe des Begriffes entspricht der Häufigkeit des Sachbegriffs.')
    files = glob.glob(f'{path}/../stats/*Ts-count.csv')
    daten = [x[-23:-13] for x in files]
    daten.sort()
    daten_filter = st.select_slider('Wählen Sie ein Datum', options=daten, value=daten[-1])

    df = pd.read_csv(f'{path}/../stats/{daten_filter}-Ts-count.csv')
    
    dict = df.to_dict(orient='records')
    worte = {}
    for record in dict:
        worte.update({record['sachbegriff']:record['count']})

    wc = WordCloud(background_color="white", max_words=100, width=2000, height=800, colormap='tab20')
    wc.generate_from_frequencies(worte)
    return st.image(wc.to_array())

def wirkungsorte():
    #ranking und karte der meistverwendeten wirkungsorte aller personen in der gnd
    df = pd.read_csv(f'{path}/wirkungsorte-top50.csv')
    df.drop(columns=['id'], inplace=True)
    df.rename(columns={'name': 'Name', 'count': 'Anzahl'}, inplace=True)

    st.header('TOP Wirkungsorte von GND-Personen')
    st.markdown('Von allen Personensätzen (Tp) weisen 782.682 Angaben zum Wirkungsort der jeweiligen Person auf.')

    #Balkendiagramm
    orte_filt = st.slider('Zeige Top …', min_value=3, max_value=len(df), value=10, step=1)
    graph_count = alt.Chart(df.nlargest(orte_filt, 'Anzahl', keep='all')).mark_bar().encode(
        alt.X('Name:N', sort='y'),
        alt.Y('Anzahl'),
        alt.Color('Name:N', legend=alt.Legend(columns=2)),
        tooltip=[alt.Tooltip('Name:N', title='Ort'), alt.Tooltip('Anzahl:Q', title='Anzahl')]
    )
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
    get_line_color=[0, 0, 0]
)

    st.pydeck_chart(pdk.Deck(
    scatterplotlayer,
    initial_view_state=INITIAL_VIEW_STATE,
    map_style=pdk.map_styles.LIGHT,
    tooltip={"html": "<b>{Name}</b><br \>Wirkungsort von {Anzahl} Personen"}))

def wirkungsorte_musik():
    #nach jahrzehnten zwischen 1400 und 2010 gefilterte auswertung der GND-Musikwerke, Musik-Personen und Wikrungsorte und daraus abgeleitete Zentren der Musikkultur, dargestellt auf einer Karte
    musiker_orte = pd.read_csv(f'{path}/musiker_orte.csv', sep='\t', index_col='idn')
    st.header('Wirkungszentren der Musik 1400–2010')
    st.write('Eine Auswertung der veröffentlichten Titel von Musikern und deren Wirkungszeiten erlaubt Rückschlüsse auf die musikalischen Zentren, wie sie im Bestand der DNB repräsentiert sind.')
    limiter = st.slider('Jahresfilter', min_value=1400, max_value=int(musiker_orte['jahrzehnt'].max()), value=(1900), step=10)
    musik_filt= musiker_orte.loc[(musiker_orte['jahrzehnt'] == limiter)]
    musik_filt['norm']=(musik_filt['count']-musik_filt['count'].min())/(musik_filt['count'].max()-musik_filt['count'].min())
    #Karte
    INITIAL_VIEW_STATE = pdk.ViewState(
        latitude=50.67877877706058,
        longitude=8.129981238464392,
        zoom=4.5,
        max_zoom=16,
        bearing=0
    )

    musiker_scatter = pdk.Layer(
        "ScatterplotLayer",
        musik_filt,
        opacity=0.8,
        get_position='[lon, lat]',
        pickable=True,
        stroked=True,
        filled=True,
        radius_min_pixels=1,
        radius_max_pixels=100,
        radiusscale=100,
        line_width_min_pixels=1,
        get_radius="norm*50000",
        get_fill_color=[50, 168, 92],
        get_line_color=[39, 71, 51]
    )

    st.pydeck_chart(pdk.Deck(
    musiker_scatter,
    initial_view_state=INITIAL_VIEW_STATE,
    map_style=pdk.map_styles.LIGHT,
    tooltip={"html": "<b>{name}</b>"}))
    st.subheader(f'TOP 10 Wirkungszentren der {limiter}er')
    col1, col2 = st.beta_columns(2)
    i = 1
    for index, row in musik_filt.nlargest(10, 'norm').iterrows():
        if i <= 5:
            with col1:
                st.write(f'{i}. {row["name"]}')
        elif i > 5:
            with col2:
                st.write(f'{i}. {row["name"]}')
        i += 1

def gesamt_entity_count():
    #Gesamtzahl der GND-Entitäten
    with open(f"{path}/../stats/gnd_entity_count.csv", "r") as f:
        entities = f'{int(f.read()):,}'
    return st.write(f"GND-Entitäten gesamt: {entities.replace(',','.')}")

def relationen():
    #Top 10 der GND-Relationierungscodes
    rels = pd.read_csv(f'{path}/../stats/gnd_codes_all.csv', index_col=False)
    st.subheader('Relationen')
    st.write('GND-Datensätze können mit anderen Datensätzen verlinkt (»relationiert«) werden. Die Art der Verlinkung wird über einen Relationierungscode beschrieben. Hier sind die am häufigsten verwendeten Relationierungscodes zu sehen. Die Auflösung der wichtigsten Codes gibt es [hier](https://wiki.dnb.de/download/attachments/51283696/Codeliste_ABCnachCode_Webseite_2012-07.pdf).')
    rels_filt = st.slider('Zeige Top ...', 5, len(rels), 10, 1)
    relation_count = alt.Chart(rels.nlargest(rels_filt, 'count', keep='all')).mark_bar().encode(
        alt.X('code', title='Relationierungs-Code', sort='-y'),
        alt.Y('count', title='Anzahl'),
        alt.Color('code', sort='-y', title='Relationierungscode'),
        tooltip=[alt.Tooltip('count', title='Anzahl'), alt.Tooltip('code', title='Code')]
    )
    st.altair_chart(relation_count, use_container_width=True)

    with open(f"{path}/../stats/gnd_relation_count.csv", "r") as f:
        relations = f'{int(f.read()):,}'
    st.write(f"Relationen zwischen Entitäten gesamt: {relations.replace(',','.')}")

def systematik():
    #Ranking der meistverwendeten GND-Systematik-Notationen
    classification = pd.read_csv(f'{path}/../stats/gnd_classification_all.csv', index_col=False)
    st.subheader('Systematik')
    st.write('Die Entitäten der GND können in eine Systematik eingeordnet werden. Die Liste der möglichen Notationen gibt es [hier](http://www.dnb.de/gndsyst).')
    class_filt = st.slider('Zeige Top …', 5, len(classification), 10, 1)
    classification_count = alt.Chart(classification.nlargest(class_filt, 'count', keep='all')).mark_bar().encode(
        alt.X('id', title='Notation', sort='-y'),
        alt.Y('count', title='Anzahl'),
        alt.Color('name', sort='-y', title="Bezeichnung"),
        tooltip=[alt.Tooltip('id', title='Notation'), alt.Tooltip('name', title='Bezeichnung'), alt.Tooltip('count', title='Anzahl')]
    )
    return st.altair_chart(classification_count, use_container_width=True)

def systematik_ts():
    #Ranking der Systematik von Ts-Sätzen
    classification_ts = pd.read_csv(f'{path}/../stats/gnd_classification_Ts_all.csv', index_col=False)
    st.subheader('Systematik der Sachbegriffe')
    st.write('Die Entitäten der GND können in eine Systematik eingeordnet werden. Hier sind die Systematik-Notationen der Sachbegriffe (Ts) aufgetragen. Die Liste der möglichen Notationen gibt es [hier](http://www.dnb.de/gndsyst).')
    class_ts_filt = st.slider('Zeige TOP …', min_value=5, max_value=len(classification_ts), value=10, step=1)
    classification_ts_count = alt.Chart(classification_ts.nlargest(class_ts_filt, 'count', keep='all')).mark_bar().encode(
        alt.X('id:N', title='Notation', sort='-y'),
        alt.Y('count:Q', title='Anzahl'),
        alt.Color('name:N', sort='-y', title='Bezeichnung'),
        tooltip = [alt.Tooltip('id', title='Notation'), alt.Tooltip('name', title='Bezeichnung'), alt.Tooltip('count', title='Anzahl')]
    )
    return st.altair_chart(classification_ts_count, use_container_width=True)

def zeitverlauf():
    #zeitverlauf der erstellung der GND-Sätze ab Januar 1972
    created_at = pd.read_csv(f'{path}/../stats/gnd_created_at.csv', index_col='created_at', parse_dates=True, header=0, names=['created_at', 'count'])
    
    st.subheader('Zeitverlauf der GND-Datensatzerstellung')
    st.write('Auf einer Zeitleiste wird die Anzahl der monatlich erstellten GND-Sätze aufgetragen. Die ersten Sätze stammen aus dem Januar 1972')
    created_filt = st.slider('Zeitraum', 1972, 2021, (1972,2021), 1)
    created = alt.Chart(created_at[f'{created_filt[0]}':f'{created_filt[1]}'].reset_index()).mark_line().encode(
        alt.X('created_at:T', title='Erstelldatum'),
        alt.Y('count:Q', title='Sätze pro Monat'),
        tooltip=['count']
    )
    return st.altair_chart(created, use_container_width=True)

def entities():
    #GND-Entitäten nach Satzart und Katalogisierungslevel
    df = pd.read_csv(f'{path}/../stats/gnd_entity_types.csv', index_col=False, names=['entity','count'])
    df['level'] = df.entity.str[2:3]
    df.entity = df.entity.str[:2]

    if satzart == 'alle':

        entity_count = alt.Chart(df).mark_bar().encode(
            alt.X('sum(count)', title='Datensätze pro Katalogisierungslevel'),
            alt.Y('entity', title='Satzart'),
            alt.Color('level', title='Katalogisierungslevel'),
            tooltip=[alt.Tooltip('entity', title='Satzart'), alt.Tooltip( 'level', title='Katalogisierungslevel'), alt.Tooltip('count', title='Anzahl')]
        )
        st.subheader('Entitäten und Katalogisierungslevel')

    else:

        entity_count = alt.Chart(df.loc[df['entity'].str.startswith(satzart[:2])]).mark_bar().encode(
            alt.X('sum(count)', title='Datensätze pro Katalogisierungslevel'),
            alt.Y('entity', title='Satzart'),
            alt.Color('level', title='Katalogisierungslevel'),
            tooltip=[alt.Tooltip( 'level', title='Katalogisierungslevel'), alt.Tooltip('count', title='Anzahl')]
        )
        st.subheader(f'Katalogisierungslevel in Satzart {satzart}')
    st.write('Alle GND-Entitäten können in verschiedenen Katalogisierungsleveln (1-7) angelegt werden. Je niedriger das Katalogisierungslevel, desto verlässlicher die Daten, weil Sie dann von qualifizierten Personen erstellt bzw. überprüft wurden.')
    return st.altair_chart(entity_count, use_container_width=True)

def newcomer():
    #TOP 10 der Entitäten, die in den letzten 365 Tagen erstellt wurden
    if satzart == 'alle':
        st.subheader(f'TOP 10 GND-Newcomer')
        st.write('TOP 10 der GND-Entitäten, die in den letzten 365 Tagen angelegt wurden.')
        newcomer_daten = pd.read_csv(f'{path}/../stats/title_gnd_newcomer_top10.csv', index_col=None)

        newcomer = alt.Chart(newcomer_daten).mark_bar().encode(
            alt.X('gnd_id', title='Entitäten', sort='-y'),
            alt.Y('count', title='Anzahl'),
            alt.Color('name', sort='-y', title='Entität'),
            tooltip=[alt.Tooltip('name:N', title='Entität'), alt.Tooltip('bbg:N', title='Satzart'), alt.Tooltip('gnd_id:N', title='IDN'), alt.Tooltip('count:Q', title='Anzahl')]
        )

    else:
        st.subheader(f'TOP 10 {satzart} GND-Newcomer')
        st.write(f'TOP 10 der {satzart} Sätze, die in den letzten 365 Tagen angelegt wurden.')
        newcomer_daten = load_gnd_top_daten('newcomer_top10')

        newcomer = alt.Chart(newcomer_daten.loc[newcomer_daten['bbg'].str.startswith(satzart[:2], na=False)]).mark_bar().encode(
            alt.X('gnd_id:O', title='Entitäten', sort='-y'),
            alt.Y('count', title='Anzahl'),
            alt.Color('name', sort='-y', title='Entität'),
            tooltip=[alt.Tooltip('name:N', title='Entität'), alt.Tooltip('gnd_id:N', title='IDN'), alt.Tooltip('count:Q', title='Anzahl')]
        )
    st.altair_chart(newcomer, use_container_width=True)

def gnd_top():
    #TOP 10 GND-Entitäten in DNB-Titeldaten, nach Satzart gefiltert
    if satzart == 'alle':
        st.subheader(f'TOP 10 GND-Entitäten in DNB-Titeldaten')
        top_daten = pd.read_csv(f'{path}/../stats/title_gnd_top10.csv', index_col=None)

        gnd_top = alt.Chart(top_daten).mark_bar().encode(
            alt.X('gnd_id:N', title='Entitäten', sort='-y'),
            alt.Y('count:Q', title='Anzahl'),
            alt.Color('name:N', sort='-y', title='Entität'),
            tooltip=[alt.Tooltip('name:N', title='Entität'), alt.Tooltip('gnd_id:N', title='IDN'), alt.Tooltip('bbg:N', title='Satzart'), alt.Tooltip('count:Q', title='Anzahl')]
        )

    else:
        st.subheader(f'TOP 10 {satzart} in DNB-Titeldaten')
        top_daten = load_gnd_top_daten('top10')

        gnd_top = alt.Chart(top_daten.loc[top_daten['bbg'].str.startswith(satzart[:2], na=False)]).mark_bar().encode(
            alt.X('gnd_id:N', title='Entitäten', sort='-y'),
            alt.Y('count:Q', title='Anzahl'),
            alt.Color('name:N', sort='-y', title='Entität'),
            tooltip=[alt.Tooltip('name:N', title='Entität'), alt.Tooltip('gnd_id:N', title='IDN'), alt.Tooltip('count:Q', title='Anzahl')]
        )
    st.write('Verknüpfungen, die maschinell erzeugt wurden, aus Fremddaten stammen oder verwaist sind, wurden nicht in die Auswertung einbezogen. Eine detaillierte Auflistung der ausgewerteten Felder ist im [GitHub-Repository](https://git.io/JG5vN) dieses Dashboards dokumentiert.')
    st.altair_chart(gnd_top, use_container_width=True)

def dnb_links():
    #GND-Verknüpfungen in DNB Titeldaten
    if satzart == 'alle':
        #Anzahl GND-Verknüpfungen in DNB-Titeldaten
        with open(f"{path}/../stats/title_gnd_links.csv", "r") as f:
            links = f'{int(f.read()):,}'
        
        #GND-Entitäten maschinell verknüpft
        with open(f"{path}/../stats/title_gnd_links_auto.csv", "r") as f:
            auto_entites = int(f.read())

        #GND-Entitäten aus Fremddaten
        with open(f"{path}/../stats/title_gnd_links_ext.csv", "r") as f:
            fremd_entities = int(f.read())

        #Anzahl der intellktuell verknüpften GND-Entitäten in DNB-Titeldaten
        with open(f"{path}/../stats/title_gnd_links_unique.csv", "r") as f:
            uniques = int(f.read())
            uniques_str = f'{uniques:,}'

        #Durchschnittliche Anzahl an GND-Verknüpfungen pro DNB-Titeldatensatz
        with open(f"{path}/../stats/title_gnd_mean.csv", "r") as f:
            mean = str(round(float(f.read()),2)).replace('.',',')

        st.write(f"{links.replace(',','.')} intellektuell vergebene Verknüpfungen zu {uniques_str.replace(',','.')} GND-Entitäten in den DNB-Titeldaten. Durchschnittlich {mean} GND-Verknüpfungen pro DNB-Titeldatensatz")

        entity_df = pd.DataFrame.from_dict({"intellektuell verknüpfte Entitäten": uniques, "Entitäten aus automatischen Prozessen": auto_entites, "Entitäten aus Fremddaten": fremd_entities}, orient = "index").reset_index()
        entity_df = entity_df.rename(columns={"index":"Datenart", 0:"Anzahl"})
        st.subheader('Datenherkunft der GND-Entitäten in DNB-Titeldaten')
        st.write('Weniger als ein Drittel der GND-Entitäten in DNB-Titeldaten wurde in intellektuellen Erschließungsprozessen vergeben. Jeweils ca. ein weiteres Drittel wurde in maschinellen Erschließungsprozessen vergeben, ca. ein Drittel stammt aus Fremddaten.')
        entities = alt.Chart(entity_df).mark_bar().encode(
            alt.X('sum(Datenart):N', title='Datenart'),
            alt.Y('sum(Anzahl):Q', title='Anzahl'),
            color='Datenart',
            tooltip='Anzahl:N'
        )
        st.altair_chart(entities, use_container_width=True)

        
    else:
        with open(f"{path}/../stats/title_gnd_mean_{satzart[:2]}.csv", "r") as f:
            mean = str(round(float(f.read()),2)).replace('.',',')
        st.write(f'Durchschnittlich {mean} Verknüpfungen zu {satzart}-Sätzen pro DNB-Titeldatensatz')

#main
st.title('GND-Dashboard')

#infoebereich oben
with st.beta_container():
    st.info('Hier finden Sie statistische Auswertungen der GND und ihrer Verknüpfungen mit den Titeldaten der Deutschen Nationalbibliothek (Stand der Daten: Juli 2021). Wählen Sie links die Satzart, die Sie interessiert, und Sie erhalten die verfügbaren Auswertungen und Statstiken. Verwenden Sie einen auf Chromium basierenden Browser.')
    with st.beta_expander("Methodik und Datenherkunft"):
        st.markdown('''
Datengrundlage ist ein Gesamtabzug der Daten der Gemeinsamen Normadatei (GND) sowie der Titeldaten der Deutschen Nationalbibliothek (DNB) inkl. Zeitschriftendatenbank (ZDB), sofern sich Exemplare der Zeitschrift im Bestand der DNB befinden. In den Titeldaten ist auch der Tonträger- und Notenbestand des Deutschen Musikarchivs (DMA) sowie der Buch- und Objektbestand des Deutschen Buch- und Schriftmuseums (DBSM) nachgewiesen.

Der Gesamtabzug liegt im OCLC-Format PICA+ vor. Die Daten werden mithilfe des Pica-Parsers [pica.rs](https://github.com/deutsche-nationalbibliothek/pica-rs) gefiltert. Dieses Tool produziert aus dem sehr großen Gesamtabzug (~ 31 GB) kleinere CSV-Dateien, die mit Python weiterverarbeitet werden.

Das Dashboard ist mit dem Python-Framework [Streamlit](https://streamlit.io/) geschrieben. Die Skripte sowie die gefilterten CSV-Rohdaten sind auf [Github](https://github.com/buchmuseum/GND_Dashboard) zu finden. Die Diagramme wurden mit [Altair](https://altair-viz.github.io/index.html) erstellt, die Karten mit [Deck GL](https://deck.gl/) (via [Pydeck](https://deckgl.readthedocs.io/en/latest/#)), die Wordcloud mit [wordcloud](https://amueller.github.io/word_cloud/index.html).

Für grundlegende Zugriffsstatistik verwenden wir [streamlit-analytics](https://pypi.org/project/streamlit-analytics/). Dabei werden keine personenbezogenen Daten gespeichert.

Alle Skripte und Daten stehen unter CC0 Lizenz und können frei weitergenutzt werden.

Die Daten werden monatlich aktualisiert.
''')

#sidebar mit satzartenfilter
st.sidebar.header("Satzart wählen")
satzart = st.sidebar.selectbox(
    "Über welche GND-Satzart möchten Sie etwas erfahren?",
    ('alle', "Tp - Personen", "Tb - Körperschaften", "Tg - Geografika", "Ts - Sachbegriffe", "Tu - Werke", "Tf - Veranstaltungen")
)
st.sidebar.info('Diese Widgets haben die GitHub-User [niko2342](https://github.com/niko2342/), [ramonvoges](https://github.com/ramonvoges), [a-wendler](https://github.com/a-wendler/) sowie Christian Baumann geschrieben. Sie gehören zur Python Community der Deutschen Nationalbibliothek.')

gnd_allgemein = st.beta_container()
with gnd_allgemein:
    st.header('GND Statistik allgemein')
    #allgemeine statistiken in abhängigkeit der satzart
    if satzart == 'alle':
        gesamt_entity_count()
        entities()
        newcomer()
        zeitverlauf()
        relationen()
        systematik()
    else:
        entities()
        newcomer()
    
    #besondere widgets für einzelne satzarten
    if satzart == "Tp - Personen":
        wirkungsorte()
    elif satzart == "Tg - Geografika":
        wirkungsorte_musik()
        wirkungsorte()
    elif satzart == "Ts - Sachbegriffe":
        sachbegriff_cloud()
        systematik_ts()

dnb = st.beta_container()
with dnb:
    st.header('GND in der Deutschen Nationalbibliothek')
    gnd_top()
    dnb_links()

streamlit_analytics.stop_tracking()