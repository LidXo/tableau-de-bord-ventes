import pandas as pd


def analyser_ventes_temporelles(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule le chiffre d'affaires et le profit par mois."""

    df = df.copy()

    df["Order Date"] = pd.to_datetime(df["Order Date"])

    df["Année"] = df["Order Date"].dt.year
    df["Mois"] = df["Order Date"].dt.month

    analyse = (
        df.groupby(["Année", "Mois"])
        .agg(
            chiffre_affaires=("Sales", "sum"),
            profit_total=("Profit", "sum"),
            nombre_commandes=("Order ID", "nunique")
        )
        .reset_index()
    )

    return analyse



def analyser_ventes_par_categorie(df: pd.DataFrame) -> pd.DataFrame:
    """Analyse les performances commerciales par catégorie."""

    analyse = (
        df.groupby("Category")
        .agg(
            chiffre_affaires=("Sales", "sum"),
            profit_total=("Profit", "sum"),
            quantite_totale=("Quantity", "sum"),
            nombre_commandes=("Order ID", "nunique")
        )
        .reset_index()
    )

    analyse["marge_beneficiaire"] = (
        analyse["profit_total"] / analyse["chiffre_affaires"]
    ) * 100

    return analyse.sort_values(
        by="chiffre_affaires",
        ascending=False
    )



def analyser_ventes_par_region(df: pd.DataFrame) -> pd.DataFrame:
    """Analyse les performances commerciales par région."""

    analyse = (
        df.groupby("Region")
        .agg(
            chiffre_affaires=("Sales", "sum"),
            profit_total=("Profit", "sum"),
            quantite_totale=("Quantity", "sum"),
            nombre_commandes=("Order ID", "nunique")
        )
        .reset_index()
    )

    analyse["marge_beneficiaire"] = (
        analyse["profit_total"] / analyse["chiffre_affaires"]
    ) * 100

    return analyse.sort_values(
        by="chiffre_affaires",
        ascending=False
    )



def analyser_ventes_par_segment(df: pd.DataFrame) -> pd.DataFrame:
    """Analyse les performances commerciales par segment client."""

    analyse = (
        df.groupby("Segment")
        .agg(
            chiffre_affaires=("Sales", "sum"),
            profit_total=("Profit", "sum"),
            quantite_totale=("Quantity", "sum"),
            nombre_commandes=("Order ID", "nunique")
        )
        .reset_index()
    )

    analyse["marge_beneficiaire"] = (
        analyse["profit_total"] / analyse["chiffre_affaires"]
    ) * 100

    return analyse.sort_values(
        by="chiffre_affaires",
        ascending=False
    )



def analyser_ventes_par_sous_categorie(df: pd.DataFrame) -> pd.DataFrame:
    """Analyse les performances commerciales par sous-catégorie."""

    analyse = (
        df.groupby("Sub-Category")
        .agg(
            chiffre_affaires=("Sales", "sum"),
            profit_total=("Profit", "sum"),
            quantite_totale=("Quantity", "sum"),
            nombre_commandes=("Order ID", "nunique")
        )
        .reset_index()
    )

    analyse["marge_beneficiaire"] = (
        analyse["profit_total"] / analyse["chiffre_affaires"]
    ) * 100

    return analyse.sort_values(
        by="chiffre_affaires",
        ascending=False
    )





def analyser_rentabilite_produits(df: pd.DataFrame) -> pd.DataFrame:
    """Classe les produits selon leur profit total."""

    analyse = (
        df.groupby("Product Name")
        .agg(
            chiffre_affaires=("Sales", "sum"),
            profit_total=("Profit", "sum"),
            quantite_totale=("Quantity", "sum")
        )
        .reset_index()
    )

    return analyse.sort_values(
        by="profit_total",
        ascending=False
    )



