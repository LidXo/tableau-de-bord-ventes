
import pandas as pd


def calculate_kpis(df):
    """
    Calcule les principaux indicateurs commerciaux.

    Parameters
    ----------
    df : pandas.DataFrame
        Données préparées par data_processing.py.

    Returns
    -------
    pandas.DataFrame
        Tableau contenant les indicateurs commerciaux.
    """

    # 1. Vérifier la présence des colonnes nécessaires
    colonnes_requises = [
        "InvoiceNo",
        "StockCode",
        "CustomerID",
        "Quantity",
        "LineAmount",
        "TransactionType"
    ]

    for colonne in colonnes_requises:
        if colonne not in df.columns:
            raise ValueError(
                f"Colonne manquante dans les données : {colonne}"
            )

    # 2. Isoler les ventes standards
    df_ventes = df.loc[
        df["TransactionType"] == "VENTE_STANDARD"
    ].copy()

    # 3. Isoler les annulations commerciales
    df_annulations = df.loc[
        df["TransactionType"] == "ANNULATION_COMMERCIALE"
    ].copy()

    # 4. Calculer le chiffre d'affaires brut
    ca_brut = df_ventes["LineAmount"].sum()

    # 5. Calculer le montant des annulations
    montant_annulations = df_annulations["LineAmount"].sum()

    # 6. Calculer le chiffre d'affaires net provisoire
    ca_net = ca_brut + montant_annulations

    # 7. Compter les factures de vente
    nombre_factures = df_ventes["InvoiceNo"].nunique()

    # 8. Compter les factures d'annulation
    nombre_factures_annulees = (
        df_annulations["InvoiceNo"].nunique()
    )

    # 9. Calculer les quantités vendues
    quantite_vendue = df_ventes["Quantity"].sum()

    # 10. Compter les clients identifiés
    nombre_clients = df_ventes["CustomerID"].nunique()

    # 11. Calculer le panier moyen brut
    panier_moyen = (
        ca_brut / nombre_factures
        if nombre_factures > 0
        else 0
    )

    # 12. Calculer le taux de déduction des annulations
    taux_annulations = (
        abs(montant_annulations) / ca_brut * 100
        if ca_brut > 0
        else 0
    )

    # 13. Exclure les frais de livraison des références produits
    df_marchandises = df_ventes.loc[
        ~df_ventes["StockCode"].astype(str).isin(["DOT", "POST"])
    ]

    nombre_produits = df_marchandises["StockCode"].nunique()

    # 14. Construire le tableau des indicateurs
    indicateurs = {
        "Indicateur": [
            "CA brut",
            "Annulations commerciales",
            "CA net provisoire",
            "Factures de vente",
            "Factures d'annulation",
            "Quantités vendues",
            "Clients identifiés",
            "Panier moyen brut",
            "Taux de déduction des annulations",
            "Références de marchandises vendues"
        ],
        "Valeur": [
            round(ca_brut, 2),
            round(montant_annulations, 2),
            round(ca_net, 2),
            nombre_factures,
            nombre_factures_annulees,
            quantite_vendue,
            nombre_clients,
            round(panier_moyen, 2),
            round(taux_annulations, 2),
            nombre_produits
        ]
    }

    return pd.DataFrame(indicateurs)



