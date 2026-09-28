from pathlib import Path

import pandas as pd
from pyaxis import pyaxis

EXCEL_EXTENSIONS = {".xls", ".xlsx"}


def load_dataset(
    file_path: str | Path,
    encoding: str | None = None,
) -> pd.DataFrame:
    """
    Load a dataset into a pandas DataFrame.

    Supported formats:
        - CSV
        - XLS
        - XLSX
        - PX (PC-Axis)

    Parameters
    ----------
    file_path:
        Path to the dataset.

    encoding:
        Optional text encoding used when reading CSV files.
        If not provided, pandas uses its default UTF-8 encoding.
    """
    path = Path(file_path)

    # Fail early if the requested dataset does not exist.
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    # Normalize the extension so that format detection is case-insensitive.
    file_ext = path.suffix.lower()

    if file_ext in EXCEL_EXTENSIONS:
        df = pd.read_excel(path)

    elif file_ext == ".csv":
        # Automatically detect the CSV delimiter because BFS exports may use
        # different separators depending on the source.
        #
        # The encoding can be explicitly provided for datasets that are not
        # stored as UTF-8, such as some BFS demographic exports.
        df = pd.read_csv(
            path,
            sep=None,
            engine="python",
            encoding=encoding,
        )

    elif file_ext == ".px":
        df = pyaxis.parse(
            str(path),
            encoding="utf-8",
        )["DATA"]

    else:
        raise ValueError(
            f"Unsupported file format: {file_ext}. "
            "Supported formats: .csv, .xls, .xlsx and .px"
        )

    return df