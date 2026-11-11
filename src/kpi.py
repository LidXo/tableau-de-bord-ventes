import pandas as pd


def calculer_kpi(df: pd.DataFrame) -> dict:
    """Calcule les principaux indicateurs commerciaux."""

    chiffre_affaires = df["Sales"].sum()
    nombre_commandes = df["Order ID"].nunique()
    quantites_vendues = df["Quantity"].sum()
    profit_total = df["Profit"].sum()

    marge = (
        (profit_total / chiffre_affaires) * 100
        if chiffre_affaires != 0 else 0
    )

    panier_moyen = (
        chiffre_affaires / nombre_commandes
        if nombre_commandes != 0 else 0
    )

    return {
        "chiffre_affaires": chiffre_affaires,
        "nombre_commandes": nombre_commandes,
        "quantites_vendues": quantites_vendues,
        "profit_total": profit_total,
        "marge": marge,
        "panier_moyen": panier_moyen
    }


