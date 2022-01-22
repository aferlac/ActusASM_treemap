#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

df = pd.read_csv('./joueur_actuASM_saison.csv', index_col=0)

# Configuration de la page
st.set_page_config(page_title=" 14 saisons d'actus sur www.asm-rugby.com - A.Ferlac ",
                   layout='centered',
                   initial_sidebar_state='auto')

col1, col2 = st.columns(2)
choix1 = col1.radio(
     'De quelle zone voulez-vous le nombre de citations ?',
     ('du texte', 'du titre'))

liste_saisons = ['2008-2009','2009-2010','2010-2011','2011-2012','2012-2013',
                 '2013-2014','2014-2015','2015-2016','2016-2017','2017-2018',
                 '2018-2019','2019-2020','2020-2021','2021-2022',
                ]
start_saison, end_saison = col2.select_slider(
     'Selectionnez la plage des saisons',
     options=liste_saisons,
     value=('2008-2009', '2021-2022'))
start_index, end_index = liste_saisons.index(start_saison), liste_saisons.index(end_saison)+1
choix_saison = liste_saisons[start_index:end_index]

df1 = df[df['saison']==choix_saison[0]]
for s in np.arange(1, len(choix_saison)):
    df1=pd.concat([df1,df[df['saison']==choix_saison[s]]],axis=0)

dict_joueur_color={'(?)':'lightgrey'}
liste_joueur=list(df['joueur'].unique())
for j in range(len(liste_joueur)):
    joueur=liste_joueur[j]
    color = 'gold' if j%2==0 else 'darkblue'
    dict_joueur_color[joueur]=color

fig1 = px.treemap(data_frame=df1,
                 path=[px.Constant("ASM Clermont Auvergne"),'saison','joueur'],
                 values='occurence_texte',
                 labels={'occurence_texte':'Nombre de citation'},
                 color='joueur',
                 color_discrete_map=dict_joueur_color,
                 title='Citations dans le texte',
)
fig1.update_layout(margin = dict(t=50, l=25, r=25, b=25))

fig2 = px.treemap(data_frame=df1,
                 path=[px.Constant("ASM Clermont Auvergne"),'saison','joueur'],
                 values='occurence_titre',
                 labels={'occurence_titre':'Nombre de citation'},
                 color='joueur',
                 color_discrete_map=dict_joueur_color,
                 title='Citations dans le titre',
)
fig2.update_layout(margin = dict(t=50, l=25, r=25, b=25))

if choix1 == 'du titre':
    st.write(fig2)
else:
    st.write(fig1)

st.write('---')
st.write('''Cette application a été construite sous Python avec les librairies Streamlit, Pandas et Plotly.\n
Les données ont été scrappées et traitées sous Python avec les librairies Request, Beautifulsoup, nlkt, re, numpy et pandas.\n
A. FERLAC - Janvier 2022.''')
st.write('---')
