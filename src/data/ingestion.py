from pathlib import Path

import pandas as pd
from pyaxis import pyaxis


EXCEL_EXTENSIONS = {".xls", ".xlsx"}


def load_dataset(file_path: str | Path) -> pd.DataFrame:
    """
    Load a dataset into a pandas DataFrame.

    Supported formats:
        - CSV
        - XLS
        - XLSX
        - PX (PC-Axis)

    Parameters
    ----------
    file_path : str | Path
        Path to the dataset.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    file_ext = path.suffix.lower()

    if file_ext in EXCEL_EXTENSIONS:
        df = pd.read_excel(path)

    elif file_ext == ".csv":
        df = pd.read_csv(
            path,
            sep=None,
            engine="python")

    elif file_ext == ".px":
        px_data = pyaxis.parse(
            str(path),
            encoding="utf-8",
        )
        df = px_data["DATA"]

    else:
        raise ValueError(
            f"Unsupported file format: {file_ext}. "
            "Supported formats: .csv, .xls, .xlsx and .px"
        )

    return df