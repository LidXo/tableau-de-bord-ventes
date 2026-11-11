import sys
from pathlib import Path

RACINE_PROJET = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE_PROJET))


import streamlit as st
import pandas as pd

from src.kpi import calculer_kpi

from src.analytics import (
    analyser_ventes_temporelles,
    analyser_ventes_par_categorie,
    analyser_ventes_par_region,
    analyser_ventes_par_segment,
    analyser_ventes_par_sous_categorie,
    analyser_rentabilite_produits
)

from src.visualizations import (
    graphique_evolution_ventes,
    graphique_ventes_par_categorie,
    graphique_ventes_par_region,
    graphique_ventes_par_segment,
    graphique_ventes_par_sous_categorie,
    graphique_rentabilite_produits
)


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Tableau de bord des ventes",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Tableau de bord décisionnel des ventes")
st.markdown(
    "Analyse des performances commerciales, "
    "de la rentabilité et de l'évolution des ventes."
)


# --------------------------------------------------
# CHARGEMENT DES DONNÉES
# --------------------------------------------------

@st.cache_data
def charger_donnees():
    df = pd.read_csv("data/processed/superstore_cleaned.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])
    return df


df = charger_donnees()


# --------------------------------------------------
# FILTRES
# --------------------------------------------------

st.sidebar.header("Filtres")

date_min = df["Order Date"].min().date()
date_max = df["Order Date"].max().date()

periode = st.sidebar.date_input(
    "Période des commandes",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max
)

regions = st.sidebar.multiselect(
    "Région",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Catégorie",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

segments = st.sidebar.multiselect(
    "Segment client",
    options=sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)


# --------------------------------------------------
# APPLICATION DES FILTRES
# --------------------------------------------------

df_filtre = df.copy()

if len(periode) == 2:
    date_debut, date_fin = periode

    df_filtre = df_filtre[
        (df_filtre["Order Date"].dt.date >= date_debut)
        & (df_filtre["Order Date"].dt.date <= date_fin)
    ]

df_filtre = df_filtre[
    df_filtre["Region"].isin(regions)
    & df_filtre["Category"].isin(categories)
    & df_filtre["Segment"].isin(segments)
]


if df_filtre.empty:
    st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
    st.stop()


# --------------------------------------------------
# KPI COMMERCIAUX
# --------------------------------------------------

st.header("Indicateurs clés de performance")

kpi = calculer_kpi(df_filtre)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Chiffre d'affaires",
    f"{kpi['chiffre_affaires']:,.2f} $"
)

col2.metric(
    "Nombre de commandes",
    f"{kpi['nombre_commandes']:,}"
)

col3.metric(
    "Quantités vendues",
    f"{kpi['quantites_vendues']:,}"
)

col4, col5, col6 = st.columns(3)

col4.metric(
    "Profit total",
    f"{kpi['profit_total']:,.2f} $"
)

col5.metric(
    "Marge bénéficiaire",
    f"{kpi['marge']:.2f} %"
)

col6.metric(
    "Panier moyen",
    f"{kpi['panier_moyen']:,.2f} $"
)


# --------------------------------------------------
# ANALYSES ET VISUALISATIONS
# --------------------------------------------------

st.divider()
st.header("Analyse des performances commerciales")

# Évolution temporelle
st.subheader("Évolution mensuelle des ventes")

donnees_temporelles = analyser_ventes_temporelles(df_filtre)
fig_evolution = graphique_evolution_ventes(donnees_temporelles)
st.plotly_chart(fig_evolution, use_container_width=True)


# Catégories et régions
col1, col2 = st.columns(2)

with col1:
    st.subheader("Chiffre d'affaires par catégorie")
    donnees_categories = analyser_ventes_par_categorie(df_filtre)
    fig_categories = graphique_ventes_par_categorie(donnees_categories)
    st.plotly_chart(fig_categories, use_container_width=True)

with col2:
    st.subheader("Chiffre d'affaires par région")
    donnees_regions = analyser_ventes_par_region(df_filtre)
    fig_regions = graphique_ventes_par_region(donnees_regions)
    st.plotly_chart(fig_regions, use_container_width=True)


# Segments et sous-catégories
col1, col2 = st.columns(2)

with col1:
    st.subheader("Répartition par segment client")
    donnees_segments = analyser_ventes_par_segment(df_filtre)
    fig_segments = graphique_ventes_par_segment(donnees_segments)
    st.plotly_chart(fig_segments, use_container_width=True)

with col2:
    st.subheader("Performance par sous-catégorie")
    donnees_sous_categories = analyser_ventes_par_sous_categorie(df_filtre)
    fig_sous_categories = graphique_ventes_par_sous_categorie(
        donnees_sous_categories
    )
    st.plotly_chart(fig_sous_categories, use_container_width=True)


# Rentabilité des produits
st.subheader("Produits les plus et les moins rentables")

donnees_produits = analyser_rentabilite_produits(df_filtre)
fig_produits = graphique_rentabilite_produits(donnees_produits)

st.plotly_chart(fig_produits, use_container_width=True)


# --------------------------------------------------
# INFORMATIONS SUR LES DONNÉES
# --------------------------------------------------

st.divider()

st.caption(
    f"Données affichées : {len(df_filtre):,} lignes "
    f"sur {len(df):,} lignes disponibles."
)



