
import streamlit as st
import plotly.express as px
import pandas as pd

from src.data_processing import process_data
from src.kpi import calculate_kpis
from src.analytics import (
    monthly_sales_analysis,
    product_sales_analysis,
    customer_sales_analysis,
    country_sales_analysis
)


# ============================================================
# 1. CONFIGURATION DE LA PAGE
# ============================================================

st.set_page_config(
    page_title="Tableau de bord décisionnel des ventes",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# 2. FONCTIONS UTILITAIRES
# ============================================================

@st.cache_data
def charger_donnees():
    """Charge et prépare les données commerciales."""
    return process_data()


def formater_montant(valeur):
    """Formate un montant avec deux décimales."""
    return f"{valeur:,.2f}".replace(",", " ")


def afficher_tableau(donnees):
    """Affiche un tableau avec les montants arrondis."""
    st.dataframe(
        donnees.round(2),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 3. CHARGEMENT DES DONNÉES
# ============================================================

try:
    df = charger_donnees()
except Exception as erreur:
    st.error(f"Erreur lors du chargement des données : {erreur}")
    st.stop()


# ============================================================
# 4. EN-TÊTE
# ============================================================

st.title("Tableau de bord décisionnel des ventes")

st.markdown(
    """
    Application de suivi et d'analyse des performances commerciales
    à partir du jeu de données **Online Retail**.
    """
)

st.caption(
    "Source : UCI Machine Learning Repository — Online Retail"
)


# ============================================================
# 5. FILTRES
# ============================================================

st.sidebar.title("Filtres")

date_min = df["InvoiceDate"].min().date()
date_max = df["InvoiceDate"].max().date()

periode = st.sidebar.date_input(
    "Période d'analyse",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max
)

if isinstance(periode, (tuple, list)):
    if len(periode) == 2:
        date_debut, date_fin = periode
    elif len(periode) == 1:
        date_debut = date_fin = periode[0]
    else:
        date_debut, date_fin = date_min, date_max
else:
    date_debut = date_fin = periode


pays_disponibles = sorted(df["Country"].dropna().unique())

pays_selectionnes = st.sidebar.multiselect(
    "Pays",
    options=pays_disponibles,
    default=pays_disponibles
)


# Application des filtres

df_filtre = df.loc[
    df["InvoiceDate"].dt.date.between(date_debut, date_fin)
].copy()

df_filtre = df_filtre.loc[
    df_filtre["Country"].isin(pays_selectionnes)
].copy()


st.sidebar.markdown("---")
st.sidebar.caption(
    f"{len(df_filtre):,} transactions sélectionnées".replace(",", " ")
)


if df_filtre.empty:
    st.warning(
        "Aucune transaction ne correspond aux filtres sélectionnés."
    )
    st.stop()


# ============================================================
# 6. CALCUL DES INDICATEURS
# ============================================================

kpis = calculate_kpis(df_filtre)

valeurs_kpi = dict(
    zip(kpis["Indicateur"], kpis["Valeur"])
)

nombre_transactions = len(df_filtre)


# ============================================================
# 7. ORGANISATION EN ONGLETS
# ============================================================

tab_vue, tab_produits, tab_clients, tab_geographie, tab_donnees = st.tabs(
    [
        "Vue générale",
        "Produits",
        "Clients",
        "Géographie",
        "Données"
    ]
)


# ============================================================
# 8. ONGLET VUE GÉNÉRALE
# ============================================================

with tab_vue:

    st.subheader("Vue d'ensemble")

    st.caption(
        f"Période : {date_debut.strftime('%d/%m/%Y')} "
        f"au {date_fin.strftime('%d/%m/%Y')}"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Transactions",
            f"{nombre_transactions:,}".replace(",", " ")
        )

    with col2:
        st.metric(
            "Factures de vente",
            f"{valeurs_kpi['Factures de vente']:,.0f}".replace(",", " ")
        )

    st.markdown("---")

    st.subheader("Indicateurs clés de performance")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "CA brut",
            formater_montant(valeurs_kpi["CA brut"])
        )

    with col2:
        st.metric(
            "Annulations commerciales",
            formater_montant(
                valeurs_kpi["Annulations commerciales"]
            )
        )

    with col3:
        st.metric(
            "CA net provisoire",
            formater_montant(
                valeurs_kpi["CA net provisoire"]
            )
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
            "Clients identifiés",
            f"{valeurs_kpi['Clients identifiés']:,.0f}".replace(",", " ")
        )

    with col5:
        st.metric(
            "Panier moyen brut",
            formater_montant(valeurs_kpi["Panier moyen brut"])
        )

    with col6:
        st.metric(
            "Taux de déduction des annulations",
            f"{valeurs_kpi['Taux de déduction des annulations']:.2f} %"
        )

    st.markdown("---")

    st.subheader("Évolution mensuelle des ventes")

    analyse_mensuelle = monthly_sales_analysis(df_filtre)

    if not analyse_mensuelle.empty:

        fig_mensuel = px.line(
            analyse_mensuelle,
            x="AnneeMois",
            y=["CA_brut", "Annulations", "CA_net"],
            markers=True,
            title="Évolution mensuelle du chiffre d'affaires",
            labels={
                "AnneeMois": "Mois",
                "value": "Montant",
                "variable": "Indicateur"
            }
        )

        fig_mensuel.update_layout(
            hovermode="x unified",
            legend_title="Indicateurs",
            xaxis_title="Période",
            yaxis_title="Montant"
        )

        st.plotly_chart(
            fig_mensuel,
            use_container_width=True
        )

        with st.expander("Consulter les données mensuelles"):
            afficher_tableau(analyse_mensuelle)

    else:
        st.info("Aucune donnée mensuelle disponible.")


# ============================================================
# 9. ONGLET PRODUITS
# ============================================================

with tab_produits:

    st.subheader("Analyse des performances par produit")

    analyse_produits = product_sales_analysis(df_filtre)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top 10 par CA net")

        top_produits_ca = (
            analyse_produits
            .sort_values("CA_net", ascending=False)
            .head(10)
            .copy()
        )

        top_produits_ca["Produit"] = (
            top_produits_ca["StockCode"].astype(str)
            + " - "
            + top_produits_ca["Description"].fillna(
                "Description indisponible"
            )
        )

        fig_produits_ca = px.bar(
            top_produits_ca.sort_values("CA_net"),
            x="CA_net",
            y="Produit",
            orientation="h",
            labels={
                "CA_net": "CA net provisoire",
                "Produit": "Produit"
            }
        )

        st.plotly_chart(
            fig_produits_ca,
            use_container_width=True
        )

    with col2:
        st.markdown("#### Top 10 par quantité vendue")

        top_produits_quantite = (
            analyse_produits
            .sort_values("Quantite_vendue", ascending=False)
            .head(10)
            .copy()
        )

        top_produits_quantite["Produit"] = (
            top_produits_quantite["StockCode"].astype(str)
            + " - "
            + top_produits_quantite["Description"].fillna(
                "Description indisponible"
            )
        )

        fig_produits_quantite = px.bar(
            top_produits_quantite.sort_values("Quantite_vendue"),
            x="Quantite_vendue",
            y="Produit",
            orientation="h",
            labels={
                "Quantite_vendue": "Quantité vendue",
                "Produit": "Produit"
            }
        )

        st.plotly_chart(
            fig_produits_quantite,
            use_container_width=True
        )

    with st.expander("Consulter toutes les performances des produits"):

        afficher_tableau(
            analyse_produits[
                [
                    "StockCode",
                    "Description",
                    "CA_brut",
                    "Annulations",
                    "CA_net",
                    "Quantite_vendue"
                ]
            ]
        )


# ============================================================
# 10. ONGLET CLIENTS
# ============================================================

with tab_clients:

    st.subheader("Analyse des performances par client")

    analyse_clients = customer_sales_analysis(df_filtre)

    top_clients = (
        analyse_clients
        .sort_values("CA_net", ascending=False)
        .head(10)
        .copy()
    )

    top_clients["Client"] = (
        top_clients["CustomerID"]
        .astype("Int64")
        .astype(str)
    )

    fig_clients = px.bar(
        top_clients.sort_values("CA_net"),
        x="CA_net",
        y="Client",
        orientation="h",
        labels={
            "CA_net": "CA net provisoire",
            "Client": "Identifiant client"
        },
        title="Top 10 des clients par CA net provisoire"
    )

    st.plotly_chart(
        fig_clients,
        use_container_width=True
    )

    with st.expander("Consulter les performances des clients"):

        afficher_tableau(
            top_clients[
                [
                    "CustomerID",
                    "CA_brut",
                    "Annulations",
                    "CA_net",
                    "nombre_factures",
                    "quantite_vendue"
                ]
            ]
        )


# ============================================================
# 11. ONGLET GÉOGRAPHIE
# ============================================================

with tab_geographie:

    st.subheader("Analyse des performances géographiques")

    analyse_pays = country_sales_analysis(df_filtre)

    top_pays = (
        analyse_pays
        .sort_values("CA_net", ascending=False)
        .head(10)
        .copy()
    )

    fig_pays = px.bar(
        top_pays.sort_values("CA_net"),
        x="CA_net",
        y="Country",
        orientation="h",
        labels={
            "CA_net": "CA net provisoire",
            "Country": "Pays"
        },
        title="Top 10 des pays par CA net provisoire"
    )

    st.plotly_chart(
        fig_pays,
        use_container_width=True
    )

    with st.expander("Consulter les performances de tous les pays"):

        afficher_tableau(
            analyse_pays[
                [
                    "Country",
                    "CA_brut",
                    "Annulations",
                    "CA_net",
                    "nombre_factures",
                    "nombre_clients",
                    "quantite_vendue"
                ]
            ]
        )


# ============================================================
# 12. ONGLET DONNÉES ET MÉTHODOLOGIE
# ============================================================

with tab_donnees:

    st.subheader("Informations sur les données")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Lignes sélectionnées",
            f"{len(df_filtre):,}".replace(",", " ")
        )

    with col2:
        st.metric(
            "Colonnes",
            len(df_filtre.columns)
        )

    with col3:
        st.metric(
            "Pays sélectionnés",
            df_filtre["Country"].nunique()
        )

    st.markdown("---")

    st.markdown("#### Aperçu des transactions")

    st.dataframe(
        df_filtre.head(100),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Les 100 premières lignes des transactions filtrées sont affichées."
    )

    st.markdown("---")

    st.markdown("#### Précautions méthodologiques")

    st.warning(
        """
        **Le CA net présenté est provisoire.**

        - Les annulations commerciales sont déduites du CA brut.
        - Les frais de plateforme et opérations manuelles sont exclus
          des ventes de marchandises.
        - Les ajustements comptables et mouvements non commerciaux
          sont également exclus.
        - Les doublons exacts sont conservés dans le scénario principal
          faute d'identifiant unique permettant de prouver leur nature.
        - Les transactions sans CustomerID peuvent contribuer au CA global,
          mais ne sont pas attribuées à un client identifié.
        - Les coûts d'achat et charges de l'entreprise ne sont pas disponibles :
          le bénéfice ne peut donc pas être calculé.
        """
    )


# ============================================================
# 13. PIED DE PAGE
# ============================================================

st.markdown("---")

st.caption(
    "Projet académique — Tableau de bord décisionnel des ventes "
    "| Python · Pandas · Streamlit · Plotly"
)



