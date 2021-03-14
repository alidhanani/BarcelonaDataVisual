#possible properties
# "properties":{"ID_ANNEX":"01",
# "ANNEXDESCR":"Grup - I",
# "ID_TEMA":"0104",
# "TEMA_DESCR":"Unitats Administratives",
# "ID_CONJUNT":"010412",
# "CONJ_DESCR":"Districtes",
# "ID_SUBCONJ":"01041201",
# "SCONJ_DESC":"Districte",
# "ID_ELEMENT":"0104120101",
# "ELEM_DESCR":"Límit de districte",
# "NIVELL":"ADM_02_PL",
# "NDESCR_CA":"Límit de districte (polígon)",
# "NDESCR_ES":"Límite de distrito (polígono)",
# "NDESCR_EN":"District boundary (polygon)",
# "TERME":"080193",
# "DISTRICTE":"03",
# "BARRI":"-",
# "AEB":"-",
# "SEC_CENS":"-",
# "GRANBARRI":"-",
# "ZUA":"-",
# "AREA_I":"-",
# "LITERAL":"03",
# "PERIMETRE":46711.857,
# "AREA":22879850.05,
# "ORD_REPRES":5,
# "CODI_UA":"03",
# "TIPUS_UA":"DISTRICTE",
# "NOM":"Sants-Montjuïc",
# "WEB1":"http://www.bcn.cat/sants-montjuic",
# "WEB2":"http://www.bcn.cat/estadistica/catala/dades/guiadt03/index.htm",
# "WEB3":"http://www.bcn.cat/estadistica/catala/documents/districtes/03_Sants_Montju%C3%AFc_2017.pdf",
# "DOCUMENTA":null,
# "RANGESCALA":"1-150000",
# "TIPUS_POL":null,"GRUIX_ID":"6",
# "GRUIXDIMEN":70,
# "ESTIL_ID":"0",
# "ESTIL_QGIS":"Sòlid",
# "VALOR1QGIS":"0",
# "VALOR2QGIS":"0",
# "COL_FARCIT":"1",
# "FCOL_DESCR":"Negre",
# "FHEX_COLOR":"#000000",
# "COL_DESCR":"Negre",
# "HEX_COLOR7":"#000000"}},
# {"type":"Polygon","arcs":[[-6,-12,13,14]]




import altair as alt
import streamlit as st
from vega_datasets import data
#https://stackoverflow.com/questions/56396452/how-to-create-a-topojson-geomap-using-altair-library-for-python
#https://github.com/martgnz/bcn-geodata


url = "https://raw.githubusercontent.com/martgnz/bcn-geodata/master/districtes/districtes.json"

source = alt.topo_feature(url, "districtes")

fig = alt.Chart(source).mark_geoshape().encode(
    tooltip='properties.NOM:N'
)
st.write(fig)

