
from pathlib import Path
import pandas as pd


# Chemin racine du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Chemin du fichier de données brutes
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"


def load_data(file_path=DEFAULT_DATA_PATH):
    """
    Charge le fichier Excel contenant les données brutes des ventes.

    Parameters
    ----------
    file_path : str ou Path
        Chemin vers le fichier Excel.

    Returns
    -------
    pandas.DataFrame
        Données chargées dans un DataFrame.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Fichier de données introuvable : {path}"
        )

    return pd.read_excel(path)



