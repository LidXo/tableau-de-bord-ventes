
from pathlib import Path
from io import BytesIO
from urllib.request import Request, urlopen
from zipfile import ZipFile

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_DATA_PATH = (
    PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"
)

UCI_DATA_URL = (
    "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
)


def load_data_from_uci():
    """
    Télécharge le jeu de données Online Retail depuis UCI
    et charge le fichier Excel directement en mémoire.
    """

    request = Request(
        UCI_DATA_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urlopen(request, timeout=120) as response:
        zip_content = response.read()

    with ZipFile(BytesIO(zip_content)) as archive:

        excel_files = [
            name for name in archive.namelist()
            if name.lower().endswith(".xlsx")
        ]

        if not excel_files:
            raise FileNotFoundError(
                "Aucun fichier Excel trouvé dans l'archive UCI."
            )

        with archive.open(excel_files[0]) as excel_file:
            return pd.read_excel(BytesIO(excel_file.read()))


def load_data(file_path=DEFAULT_DATA_PATH):
    """
    Charge les données localement si le fichier existe.
    Sinon, télécharge les données depuis UCI.
    """

    path = Path(file_path)

    if path.exists():
        return pd.read_excel(path)

    if path == DEFAULT_DATA_PATH:
        return load_data_from_uci()

    raise FileNotFoundError(
        f"Fichier de données introuvable : {path}"
    )
