# Tableau de bord décisionnel des ventes

## 1. Présentation du projet

Ce projet consiste à concevoir et développer un tableau de bord décisionnel permettant d'analyser les performances commerciales à partir du jeu de données **Online Retail**.

L'application permet de suivre les indicateurs clés de performance (KPI), d'étudier l'évolution des ventes et d'identifier les principaux produits, clients et marchés géographiques.

## 2. Objectifs

- Suivre l'évolution du chiffre d'affaires.
- Mesurer l'impact des annulations commerciales.
- Identifier les produits générant le plus de chiffre d'affaires.
- Analyser les performances des clients identifiés.
- Comparer les performances commerciales par pays.
- Faciliter la prise de décision à partir des données.

## 3. Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python | Langage de programmation |
| Pandas | Manipulation et analyse des données |
| Streamlit | Développement de l'application web |
| Plotly | Visualisation interactive |
| Jupyter Notebook | Exploration et préparation des données |
| Git / GitHub | Gestion du code source |

## 4. Source des données

**Jeu de données :** Online Retail.

**Source :** UCI Machine Learning Repository.

Le jeu de données contient 541 909 transactions et 8 colonnes initiales, notamment :

- InvoiceNo : numéro de facture.
- StockCode : référence du produit.
- Description : description du produit.
- Quantity : quantité.
- InvoiceDate : date de facturation.
- UnitPrice : prix unitaire.
- CustomerID : identifiant du client.
- Country : pays.

## 5. Fonctionnalités du tableau de bord

L'application comprend cinq espaces :

1. **Vue générale :** indicateurs clés et évolution mensuelle des ventes.
2. **Produits :** classement des produits par chiffre d'affaires et quantités vendues.
3. **Clients :** analyse des performances des clients identifiés.
4. **Géographie :** analyse des performances commerciales par pays.
5. **Données :** aperçu des transactions et précautions méthodologiques.

Des filtres permettent de sélectionner une période et un ou plusieurs pays.

## 6. Indicateurs clés

Les principaux indicateurs calculés sont :

- Chiffre d'affaires brut.
- Annulations commerciales.
- Chiffre d'affaires net provisoire.
- Nombre de factures de vente.
- Nombre de factures d'annulation.
- Nombre de clients identifiés.
- Panier moyen brut.
- Taux de déduction des annulations.
- Quantités vendues.
- Références de marchandises vendues.

### Résultats de référence

Sur l'ensemble du jeu de données :

| Indicateur | Valeur |
|---|---:|
| CA brut | 10 574 813,18 |
| Annulations commerciales | -514 746,44 |
| CA net provisoire | 10 060 066,74 |
| Factures de vente | 19 866 |
| Clients identifiés | 4 335 |
| Panier moyen brut | 532,31 |
| Taux de déduction des annulations | 4,87 % |

## 7. Architecture du projet

```text
tableau-de-bord-ventes/
│
├── app/
│   └── dashboard.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│
├── notebooks/
│   └── 01_analyse_preparation.ipynb
│
├── screenshots/
│
├── src/
│   ├── data_loader.py
│   ├── data_processing.py
│   ├── kpi.py
│   └── analytics.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## 8. Installation et exécution

### Prérequis

- Python installé.
- Git installé.
- Les dépendances listées dans `requirements.txt`.

### Installation

Cloner le dépôt :

```bash
git clone URL_DU_DEPOT
```

Accéder au répertoire :

```bash
cd tableau-de-bord-ventes
```

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Activer l'environnement sous Windows :

```powershell
.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Placer le fichier `Online Retail.xlsx` dans :

```text
data/raw/Online Retail.xlsx
```

Lancer l'application :

```bash
python -m streamlit run app/dashboard.py
```

## 9. Précautions méthodologiques

Le chiffre d'affaires net présenté est un indicateur provisoire construit à partir des règles de classification des transactions.

- Les annulations commerciales sont déduites du chiffre d'affaires brut.
- Les opérations manuelles, frais de plateforme, ajustements comptables et mouvements non commerciaux sont exclus du calcul des ventes standard.
- Les doublons exacts sont conservés, car leur nature commerciale ne peut pas être établie avec certitude.
- Les transactions sans identifiant client peuvent contribuer au chiffre d'affaires global, mais ne sont pas attribuées à un client identifié.
- Les coûts d'achat et les charges ne sont pas disponibles. Le bénéfice ne peut donc pas être calculé.

## 10. Perspectives d'amélioration

- Ajouter des tests automatisés.
- Améliorer la gestion des erreurs et des données manquantes.
- Ajouter des fonctionnalités d'exportation des résultats.
- Mettre en place un déploiement en ligne.
- Optimiser les performances de traitement des données.

## 11. Statut du projet

Projet fonctionnel : analyse des données, calcul des indicateurs, visualisations interactives et filtres intégrés.

**Technologies principales :** Python, Pandas, Streamlit et Plotly.



