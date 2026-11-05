
import pandas as pd


def monthly_sales_analysis(df):
    """
    Analyse les ventes et les annulations commerciales par mois.

    Parameters
    ----------
    df : pandas.DataFrame
        Données préparées par data_processing.py.

    Returns
    -------
    pandas.DataFrame
        Synthèse mensuelle du CA brut, des annulations
        et du CA net provisoire.
    """

    # 1. Sélectionner les ventes et les annulations commerciales
    categories = [
        "VENTE_STANDARD",
        "ANNULATION_COMMERCIALE"
    ]

    df_ventes = df.loc[
        df["TransactionType"].isin(categories)
    ].copy()

    # 2. Extraire l'année et le mois
    df_ventes["AnneeMois"] = (
        df_ventes["InvoiceDate"]
        .dt.to_period("M")
        .astype(str)
    )

    # 3. Calculer les montants par mois et par type
    analyse = (
        df_ventes.groupby(["AnneeMois", "TransactionType"])
        .agg(
            montant_total=("LineAmount", "sum"),
            nombre_factures=("InvoiceNo", "nunique"),
            quantite_totale=("Quantity", "sum")
        )
        .reset_index()
    )

    # 4. Séparer les ventes et les annulations
    synthese = analyse.pivot(
        index="AnneeMois",
        columns="TransactionType",
        values="montant_total"
    ).fillna(0)

    # 5. Renommer les colonnes
    synthese = synthese.rename(
        columns={
            "VENTE_STANDARD": "CA_brut",
            "ANNULATION_COMMERCIALE": "Annulations"
        }
    )

    # 6. Calculer le CA net provisoire
    synthese["CA_net"] = (
        synthese["CA_brut"] + synthese["Annulations"]
    )

    return synthese.reset_index()





def product_sales_analysis(df):
    """
    Analyse les performances commerciales par produit.

    Calcule le CA brut, les annulations, le CA net
    et les quantités vendues par référence.

    Parameters
    ----------
    df : pandas.DataFrame
        Données préparées par data_processing.py.

    Returns
    -------
    pandas.DataFrame
        Performances commerciales par produit.
    """

    # 1. Conserver les ventes et les annulations commerciales
    categories = [
        "VENTE_STANDARD",
        "ANNULATION_COMMERCIALE"
    ]

    df_commercial = df.loc[
        df["TransactionType"].isin(categories)
    ].copy()

    # 2. Exclure les frais de livraison
    df_marchandises = df_commercial.loc[
        ~df_commercial["StockCode"].astype(str).isin(["DOT", "POST"])
    ].copy()

    # 3. Regrouper les montants par produit et type de transaction
    analyse = (
        df_marchandises.groupby(
            ["StockCode", "TransactionType"]
        )["LineAmount"]
        .sum()
        .unstack(fill_value=0)
    )

    # 4. Garantir la présence des deux colonnes
    analyse = analyse.reindex(
        columns=[
            "VENTE_STANDARD",
            "ANNULATION_COMMERCIALE"
        ],
        fill_value=0
    )

    # 5. Calculer le CA net provisoire
    analyse["CA_net"] = (
        analyse["VENTE_STANDARD"]
        + analyse["ANNULATION_COMMERCIALE"]
    )

    # 6. Calculer les quantités vendues
    quantites = (
        df_marchandises.loc[
            df_marchandises["TransactionType"] == "VENTE_STANDARD"
        ]
        .groupby("StockCode")["Quantity"]
        .sum()
    )

    analyse["Quantite_vendue"] = quantites

    # 7. Récupérer une description par référence
    descriptions = (
        df_marchandises.groupby("StockCode")["Description"]
        .first()
    )

    analyse["Description"] = descriptions

    # 8. Réorganiser les colonnes
    analyse = analyse.reset_index()

    analyse = analyse.rename(
        columns={
            "VENTE_STANDARD": "CA_brut",
            "ANNULATION_COMMERCIALE": "Annulations"
        }
    )

    # 9. Classer les produits par CA net décroissant
    analyse = analyse.sort_values(
        "CA_net",
        ascending=False
    )

    return analyse


def customer_sales_analysis(df):
    """
    Analyse les performances commerciales par client identifié.

    Calcule le CA brut, les annulations, le CA net,
    le nombre de factures et les quantités vendues.
    """

    categories = ["VENTE_STANDARD", "ANNULATION_COMMERCIALE"]

    df_commercial = df.loc[
        df["TransactionType"].isin(categories)
        & df["CustomerID"].notna()
    ].copy()

    analyse = (
        df_commercial.groupby(["CustomerID", "TransactionType"])["LineAmount"]
        .sum()
        .unstack(fill_value=0)
    )

    analyse = analyse.reindex(
        columns=["VENTE_STANDARD", "ANNULATION_COMMERCIALE"],
        fill_value=0
    )

    analyse["CA_net"] = (
        analyse["VENTE_STANDARD"]
        + analyse["ANNULATION_COMMERCIALE"]
    )

    df_ventes = df_commercial.loc[
        df_commercial["TransactionType"] == "VENTE_STANDARD"
    ]

    details = (
        df_ventes.groupby("CustomerID")
        .agg(
            nombre_factures=("InvoiceNo", "nunique"),
            quantite_vendue=("Quantity", "sum")
        )
    )

    analyse = analyse.join(details).fillna({
        "nombre_factures": 0,
        "quantite_vendue": 0
    })

    analyse = analyse.reset_index()

    analyse = analyse.rename(
        columns={
            "VENTE_STANDARD": "CA_brut",
            "ANNULATION_COMMERCIALE": "Annulations"
        }
    )

    analyse = analyse.sort_values(
        "CA_net",
        ascending=False
    )

    return analyse



def country_sales_analysis(df):
    """
    Analyse les performances commerciales par pays.

    Calcule le CA brut, les annulations, le CA net,
    le nombre de factures, les clients identifiés
    et les quantités vendues.
    """

    categories = ["VENTE_STANDARD", "ANNULATION_COMMERCIALE"]

    df_commercial = df.loc[
        df["TransactionType"].isin(categories)
    ].copy()

    # Calcul du CA brut et des annulations par pays
    analyse = (
        df_commercial.groupby(["Country", "TransactionType"])["LineAmount"]
        .sum()
        .unstack(fill_value=0)
    )

    analyse = analyse.reindex(
        columns=["VENTE_STANDARD", "ANNULATION_COMMERCIALE"],
        fill_value=0
    )

    analyse["CA_net"] = (
        analyse["VENTE_STANDARD"]
        + analyse["ANNULATION_COMMERCIALE"]
    )

    # Indicateurs calculés uniquement sur les ventes standard
    df_ventes = df_commercial.loc[
        df_commercial["TransactionType"] == "VENTE_STANDARD"
    ]

    details = (
        df_ventes.groupby("Country")
        .agg(
            nombre_factures=("InvoiceNo", "nunique"),
            nombre_clients=("CustomerID", "nunique"),
            quantite_vendue=("Quantity", "sum")
        )
    )

    analyse = analyse.join(details)

    # Remplacer les valeurs absentes des indicateurs par zéro
    analyse[
        ["nombre_factures", "nombre_clients", "quantite_vendue"]
    ] = analyse[
        ["nombre_factures", "nombre_clients", "quantite_vendue"]
    ].fillna(0)

    analyse = analyse.rename(
        columns={
            "VENTE_STANDARD": "CA_brut",
            "ANNULATION_COMMERCIALE": "Annulations"
        }
    )

    analyse = analyse.reset_index()

    analyse = analyse.sort_values(
        "CA_net",
        ascending=False
    )

    return analyse









