# Tableau de bord décisionnel des ventes

## Présentation

Ce projet consiste à développer une application interactive de Business Intelligence permettant d'analyser les performances commerciales d'une entreprise à partir du jeu de données **Sample Superstore**.

L'application permet de suivre les principaux indicateurs de performance (KPI), d'explorer les ventes selon plusieurs dimensions et d'identifier les catégories et produits les plus ou les moins rentables.

## Objectifs

- Calculer les principaux indicateurs commerciaux.
- Analyser l'évolution temporelle du chiffre d'affaires.
- Comparer les performances par catégorie, sous-catégorie, région et segment client.
- Étudier la rentabilité des produits.
- Proposer une interface interactive facilitant l'exploration des données.

## Indicateurs clés de performance

L'application présente six KPI :

| Indicateur | Valeur globale |
|---|---:|
| Chiffre d'affaires | 2 297 200,86 $ |
| Nombre de commandes | 5 009 |
| Quantités vendues | 37 873 |
| Profit total | 286 397,02 $ |
| Marge bénéficiaire | 12,47 % |
| Panier moyen | 458,61 $ |

*Ces valeurs correspondent à l'ensemble du jeu de données, avant application des filtres.*

## Fonctionnalités

- Visualisation de l'évolution mensuelle des ventes.
- Analyse du chiffre d'affaires par catégorie.
- Comparaison des performances régionales.
- Répartition des ventes par segment client.
- Analyse des sous-catégories.
- Identification des produits les plus et les moins rentables.
- Filtres interactifs par période, région, catégorie et segment.

## Technologies utilisées

- **Python** : langage de programmation.
- **Pandas** : manipulation et analyse des données.
- **Streamlit** : développement de l'interface interactive.
- **Plotly** : visualisations interactives.
- **Pytest** : tests automatisés.
- **Git et GitHub** : gestion de versions et hébergement du code.

## Architecture du projet

```text
tableau-de-bord-ventes/
│
├── app/
│   └── dashboard.py
│
├── data/
│   ├── raw/
│   └── processed/
│       └── superstore_cleaned.csv
│
├── notebooks/
│
├── reports/
│   └── graphiques HTML interactifs
│
├── screenshots/
│
├── src/
│   ├── __init__.py
│   ├── kpi.py
│   ├── analytics.py
│   └── visualizations.py
│
├── tests/
│   └── test_analytics.py
│
├── requirements.txt
└── README.md
```

## Installation

### 1. Cloner le dépôt

```bash
git clone URL_DU_DEPOT
cd tableau-de-bord-ventes
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
```

### 3. Activer l'environnement

Sous Windows PowerShell :

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Installer les dépendances

```bash
python -m pip install -r requirements.txt
```

### 5. Lancer l'application

```bash
python -m streamlit run app/dashboard.py
```

## Tests

Pour exécuter les tests automatisés :

```bash
python -m pytest tests/ -v
```

**Résultat actuel : 7 tests réussis.**

## Jeu de données

Le projet utilise le jeu de données Sample Superstore, contenant des informations commerciales telles que les commandes, les clients, les produits, les ventes, les remises et les profits.

Le fichier nettoyé utilisé par l'application est :

`data/processed/superstore_cleaned.csv`

## Auteur

**Lidao ABIYI**

Étudiant en Informatique — IA & Big Data

Orientation professionnelle : Data Engineering.

