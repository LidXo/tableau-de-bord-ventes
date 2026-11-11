import pandas as pd

# Chargement des données
df = pd.read_csv("data/processed/superstore_cleaned.csv")

# Calcul des indicateurs
chiffre_affaires = df["Sales"].sum()
nombre_commandes = df["Order ID"].nunique()
quantites_vendues = df["Quantity"].sum()
profit_total = df["Profit"].sum()

marge = (profit_total / chiffre_affaires) * 100
panier_moyen = chiffre_affaires / nombre_commandes

# Affichage
print("===== KPI COMMERCIAUX =====")
print(f"Chiffre d'affaires : {chiffre_affaires:,.2f} $")
print(f"Nombre de commandes : {nombre_commandes:,}")
print(f"Quantités vendues : {quantites_vendues:,}")
print(f"Profit total : {profit_total:,.2f} $")
print(f"Marge bénéficiaire : {marge:.2f} %")
print(f"Panier moyen : {panier_moyen:,.2f} $")

