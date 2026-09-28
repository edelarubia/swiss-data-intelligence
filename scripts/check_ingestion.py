from pathlib import Path

from src.data.ingestion import load_dataset


# -------------------------------------------------------------------------
# Dataset selection
# -------------------------------------------------------------------------
# Uncomment the dataset that you want to test and keep the others commented.


# CSV test: occupied dwellings
"""
DATASET_PATH = Path(
    "data/raw/bfs/housing/occupied-dwellings-by-occupancy-status-and-canton/"
    "OCCUPIED_DWELLINGS_BY_OCCUPANCY_STATUS_AND_CANTON_2019_2024.csv"
)
ENCODING = None
"""


# Excel test: canton geographic lookup
"""
DATASET_PATH = Path(
    "data/raw/bfs/reference/GEO_CANTON_LOOKUP.xlsx"
)
ENCODING = None
"""


# PX test: detailed population dataset
"""
DATASET_PATH = Path(
    "data/raw/bfs/demographics/"
    "BFS_PERMANENT_AND_NON_PERMANENT_RESIDENT_POPULATION_BY_CANTON.px"
)
ENCODING = None
"""


# CSV Latin-1 test: population by canton, sex, marital status and age.
# This BFS demographic export requires an explicit Latin-1 encoding.
DATASET_PATH = Path(
    "data/raw/bfs/demographics/"
    "population-by-canton-sex-marital-status-age/"
    "POPULATION_BY_CANTON_SEX_MARITAL_STATUS_AGE_2019_2024.csv"
)
ENCODING = "latin1"


# -------------------------------------------------------------------------
# Ingestion test
# -------------------------------------------------------------------------

# Load the selected dataset through the reusable ingestion component.
df = load_dataset(
    DATASET_PATH,
    encoding=ENCODING,
)


# -------------------------------------------------------------------------
# Basic inspection
# -------------------------------------------------------------------------

# Display basic information to verify that the dataset was parsed correctly.
print(f"Dataset: {DATASET_PATH.name}")
print(f"Shape: {df.shape}")

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst rows:")
print(df.head())


# -------------------------------------------------------------------------
# Validation for the current Latin-1 demographic CSV
# -------------------------------------------------------------------------

# Validate the expected structure of the demographic dataset.
# These assertions confirm that the file was not only opened successfully,
# but also parsed into the expected rows and columns.
assert df.shape == (3024, 107), (
    f"Unexpected shape: {df.shape}. Expected (3024, 107)."
)

assert "Year" in df.columns, "Expected column 'Year' was not found."
assert "Canton" in df.columns, "Expected column 'Canton' was not found."
assert "Age - total" in df.columns, "Expected column 'Age - total' was not found."

print("\nLatin-1 CSV ingestion: OK")