import plotly.express as px
import pandas as pd


def graphique_evolution_ventes(df: pd.DataFrame):
    """Visualise l'évolution mensuelle du chiffre d'affaires."""

    df = df.copy()

    df["periode"] = pd.to_datetime(
        df["Année"].astype(str) + "-" +
        df["Mois"].astype(str) + "-01"
    )

    fig = px.line(
        df,
        x="periode",
        y="chiffre_affaires",
        title="Évolution mensuelle du chiffre d'affaires",
        labels={
            "periode": "Période",
            "chiffre_affaires": "Chiffre d'affaires ($)"
        },
        markers=True
    )

    fig.update_layout(
        xaxis_title="Période",
        yaxis_title="Chiffre d'affaires ($)",
        hovermode="x unified"
    )

    return fig



def graphique_ventes_par_categorie(df: pd.DataFrame):
    """Visualise le chiffre d'affaires par catégorie."""

    fig = px.bar(
        df,
        x="Category",
        y="chiffre_affaires",
        title="Chiffre d'affaires par catégorie de produits",
        labels={
            "Category": "Catégorie",
            "chiffre_affaires": "Chiffre d'affaires ($)"
        },
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Catégorie",
        yaxis_title="Chiffre d'affaires ($)",
        showlegend=False
    )

    return fig



def graphique_ventes_par_region(df: pd.DataFrame):
    """Visualise le chiffre d'affaires par région."""

    fig = px.bar(
        df,
        x="chiffre_affaires",
        y="Region",
        orientation="h",
        title="Chiffre d'affaires par région",
        labels={
            "Region": "Région",
            "chiffre_affaires": "Chiffre d'affaires ($)"
        },
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Chiffre d'affaires ($)",
        yaxis_title="Région",
        yaxis={"categoryorder": "total ascending"},
        showlegend=False
    )

    return fig




def graphique_ventes_par_segment(df: pd.DataFrame):
    """Visualise le chiffre d'affaires par segment client."""

    fig = px.pie(
        df,
        names="Segment",
        values="chiffre_affaires",
        title="Répartition du chiffre d'affaires par segment",
        hole=0.4
    )

    return fig


def graphique_ventes_par_sous_categorie(df: pd.DataFrame):
    """Compare le chiffre d'affaires par sous-catégorie."""

    fig = px.bar(
        df.sort_values("chiffre_affaires"),
        x="chiffre_affaires",
        y="Sub-Category",
        orientation="h",
        title="Chiffre d'affaires par sous-catégorie",
        labels={
            "Sub-Category": "Sous-catégorie",
            "chiffre_affaires": "Chiffre d'affaires ($)"
        }
    )

    return fig


def graphique_rentabilite_produits(df: pd.DataFrame):
    """Compare les 10 produits les plus et les moins rentables."""

    top = df.nlargest(10, "profit_total")
    bottom = df.nsmallest(10, "profit_total")

    resultat = pd.concat([top, bottom]).sort_values("profit_total")

    fig = px.bar(
        resultat,
        x="profit_total",
        y="Product Name",
        orientation="h",
        title="Top 10 des produits rentables et déficitaires",
        labels={
            "Product Name": "Produit",
            "profit_total": "Profit ($)"
        }
    )

    return fig

