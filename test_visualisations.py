import pandas as pd

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

df = pd.read_csv("data/processed/superstore_cleaned.csv")

graphiques = {
    "evolution_ventes": graphique_evolution_ventes(
        analyser_ventes_temporelles(df)
    ),
    "ventes_par_categorie": graphique_ventes_par_categorie(
        analyser_ventes_par_categorie(df)
    ),
    "ventes_par_region": graphique_ventes_par_region(
        analyser_ventes_par_region(df)
    ),
    "ventes_par_segment": graphique_ventes_par_segment(
        analyser_ventes_par_segment(df)
    ),
    "ventes_par_sous_categorie": graphique_ventes_par_sous_categorie(
        analyser_ventes_par_sous_categorie(df)
    ),
    "rentabilite_produits": graphique_rentabilite_produits(
        analyser_rentabilite_produits(df)
    )
}

for nom, fig in graphiques.items():
    fig.write_html(f"reports/{nom}.html")
    print(f"[OK] {nom}.html")

print(f"\n{len(graphiques)} graphiques générés avec succès.")
