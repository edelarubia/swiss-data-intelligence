from pathlib import Path

from src.data.ingestion import load_dataset


""""DATASET_PATH = Path(
    "data/raw/bfs/housing/occupied-dwellings-by-occupancy-status-and-canton/"
    "OCCUPIED_DWELLINGS_BY_OCCUPANCY_STATUS_AND_CANTON_2019_2024.csv"
)"""

""""DATASET_PATH = Path(
    "data/raw/bfs/reference/GEO_CANTON_LOOKUP.xlsx"
)"""

DATASET_PATH = Path(
    "data/raw/bfs/demographics/"
    "BFS_PERMANENT_AND_NON_PERMANENT_RESIDENT_POPULATION_BY_CANTON.px"
)


def main() -> None:
    dataframe = load_dataset(DATASET_PATH)

    print(f"Dataset: {DATASET_PATH.name}")
    print(f"Rows: {dataframe.shape[0]:,}")
    print(f"Columns: {dataframe.shape[1]}")
    print(f"Column names: {dataframe.columns.tolist()}")
    print()
    print(dataframe.head())


if __name__ == "__main__":
    main()