
import numpy as np
import pandas as pd

from src.data_loader import load_data


def process_data():
    """
    Charge les données brutes et prépare les transactions
    pour les analyses commerciales.

    Returns
    -------
    pandas.DataFrame
        Données enrichies avec le montant et le type de transaction.
    """

    # 1. Charger les données brutes
    df = load_data()

    # 2. Créer une copie pour préserver les données originales
    df_travail = df.copy()

    # 3. Calculer le montant de chaque ligne
    df_travail["LineAmount"] = (
        df_travail["Quantity"] * df_travail["UnitPrice"]
    )

    # 4. Identifier les différents types de transactions
    df_travail["IsCancellation"] = (
        df_travail["InvoiceNo"].astype(str).str.startswith("C")
    )

    df_travail["IsPlatformFee"] = (
        df_travail["StockCode"].astype(str) == "AMAZONFEE"
    )

    df_travail["IsManualOperation"] = (
        df_travail["StockCode"].astype(str) == "M"
    )

    # 5. Définir les règles de classification
    conditions = [
        df_travail["UnitPrice"] < 0,
        df_travail["IsPlatformFee"],
        df_travail["IsManualOperation"],
        (
            (df_travail["Quantity"] < 0)
            & (~df_travail["IsCancellation"])
        ),
        df_travail["UnitPrice"] == 0,
        df_travail["IsCancellation"]
    ]

    categories = [
        "AJUSTEMENT_COMPTABLE",
        "FRAIS_PLATEFORME",
        "OPERATION_MANUELLE",
        "MOUVEMENT_NON_COMMERCIAL",
        "PRIX_NUL",
        "ANNULATION_COMMERCIALE"
    ]

    # 6. Attribuer une catégorie à chaque transaction
    df_travail["TransactionType"] = np.select(
        conditions,
        categories,
        default="VENTE_STANDARD"
    )

    return df_travail




