
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


def charger_donnees():
    return pd.read_csv("data/processed/superstore_cleaned.csv")


def test_calculer_kpi():
    df = charger_donnees()
    kpi = calculer_kpi(df)

    assert kpi["chiffre_affaires"] > 0
    assert kpi["nombre_commandes"] == df["Order ID"].nunique()
    assert kpi["quantites_vendues"] == df["Quantity"].sum()
    assert kpi["profit_total"] == df["Profit"].sum()
    assert kpi["marge"] > 0
    assert kpi["panier_moyen"] > 0


def test_analyser_ventes_temporelles():
    df = charger_donnees()
    resultat = analyser_ventes_temporelles(df)

    assert not resultat.empty
    assert len(resultat) == 48
    assert "chiffre_affaires" in resultat.columns


def test_analyser_ventes_par_categorie():
    resultat = analyser_ventes_par_categorie(charger_donnees())

    assert not resultat.empty
    assert len(resultat) == 3
    assert "chiffre_affaires" in resultat.columns


def test_analyser_ventes_par_region():
    resultat = analyser_ventes_par_region(charger_donnees())

    assert not resultat.empty
    assert len(resultat) == 4


def test_analyser_ventes_par_segment():
    resultat = analyser_ventes_par_segment(charger_donnees())

    assert not resultat.empty
    assert len(resultat) == 3


def test_analyser_ventes_par_sous_categorie():
    resultat = analyser_ventes_par_sous_categorie(charger_donnees())

    assert not resultat.empty
    assert len(resultat) == 17


def test_analyser_rentabilite_produits():
    resultat = analyser_rentabilite_produits(charger_donnees())

    assert not resultat.empty
    assert "profit_total" in resultat.columns
    assert "Product Name" in resultat.columns



