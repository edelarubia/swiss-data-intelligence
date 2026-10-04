from pathlib import Path
from PIL import Image

import altair as alt
import geopandas as gpd
import joblib
import numpy as np
import pandas as pd
import streamlit as st


# Resolve the project root from the location of this file.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Define the processed dataset used by the application.
DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "canton_year_modelling_dataset_2019_2024.csv"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "home_ownership_gradient_boosting.joblib"
)

BOUNDARIES_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "swisstopo"
    / "swissboundaries3d"
    / "swissBOUNDARIES3D_1_5_LV95_LN02.gpkg"
)

CANTON_LOOKUP_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "bfs"
    / "reference"
    / "GEO_CANTON_LOOKUP.xlsx"
)

# Map BFS geographic identifiers to standard Swiss canton abbreviations.
GEO_TO_ABBREVIATION = {
    "CH011": "VD",
    "CH012": "VS",
    "CH013": "GE",
    "CH021": "BE",
    "CH022": "FR",
    "CH023": "SO",
    "CH024": "NE",
    "CH025": "JU",
    "CH031": "BS",
    "CH032": "BL",
    "CH033": "AG",
    "CH040": "ZH",
    "CH051": "GL",
    "CH052": "SH",
    "CH053": "AR",
    "CH054": "AI",
    "CH055": "SG",
    "CH056": "GR",
    "CH057": "TG",
    "CH061": "LU",
    "CH062": "UR",
    "CH063": "SZ",
    "CH064": "OW",
    "CH065": "NW",
    "CH066": "ZG",
    "CH070": "TI",
}

# -------------------------------------------------------------------
# Application configuration
# -------------------------------------------------------------------

FAVICON_PATH = (
    PROJECT_ROOT
    / "app"
    / "assets"
    / "swiss_data_intelligence_icon.png"
)

favicon = Image.open(FAVICON_PATH)

st.set_page_config(
    page_title="Swiss Data Intelligence",
    page_icon="🚀",
    layout="wide",
)

@st.cache_data
def load_data() -> pd.DataFrame:
    """Load the processed canton-year modelling dataset."""
    return pd.read_csv(DATA_PATH)

@st.cache_resource
def load_model():
    """Load the trained model artifact used by the application."""
    return joblib.load(MODEL_PATH)

@st.cache_data
def load_canton_geometries() -> gpd.GeoDataFrame:
    """Load and harmonise Swiss canton geometries with BFS identifiers."""

    # Load the official canton geometries from swisstopo.
    cantons_geo = gpd.read_file(
        BOUNDARIES_PATH,
        layer="tlm_kantonsgebiet",
    )

    # Load the BFS canton reference table used during data preparation.
    canton_lookup = pd.read_excel(
        CANTON_LOOKUP_PATH
    )

    canton_lookup = canton_lookup[
        canton_lookup["CODE"] != "CH"
    ].copy()

    # Harmonise the only naming difference between the two sources.
    cantons_geo["name_bfs"] = cantons_geo["name"].replace(
        {
            "Fribourg": "Freiburg",
        }
    )

    # Add the BFS geographic identifier to the canton geometries.
    cantons_geo = cantons_geo.merge(
        canton_lookup[
            ["CODE", "LABEL_EN"]
        ],
        left_on="name_bfs",
        right_on="LABEL_EN",
        how="left",
        validate="one_to_one",
    )

    cantons_geo = cantons_geo.rename(
        columns={
            "CODE": "GEO",
        }
    )

    # Ensure that all 26 cantons were successfully harmonised.
    assert cantons_geo["GEO"].notna().all()
    assert cantons_geo["GEO"].nunique() == 26

    # Convert the static canton geometries once to WGS84.
    # The cached result can then be reused across Streamlit reruns.
    cantons_geo = cantons_geo.to_crs(
        epsg=4326
    )

    return cantons_geo

@st.cache_data
def prepare_map_data(
    year: int,
    data: pd.DataFrame,
    _geometries: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Prepare canton-level geographic data for the selected year."""

    # Select the statistical observations for the requested year.
    year_data = data[
        data["YEAR"] == year
    ][
        [
            "GEO",
            "CANTON",
            "HOME_OWNERSHIP_RATE",
        ]
    ].copy()

    # Combine statistical observations with the cached canton geometries.
    map_data = _geometries.merge(
        year_data,
        on="GEO",
        how="left",
        validate="one_to_one",
    )

    # Validate the geographic integration.
    assert len(map_data) == 26
    assert map_data[
        "HOME_OWNERSHIP_RATE"
    ].notna().all()

    return map_data

# Configure the Streamlit page.
st.set_page_config(
    page_title="Swiss Data Intelligence",
    page_icon="🇨🇭",
    layout="wide",
)


# Load the processed data.
df = load_data()

# Load the saved model.
model_artifact = load_model()

model = model_artifact["model"]
model_features = model_artifact["features"]

cantons_geo = load_canton_geometries()

#print(
#    f"Model loaded successfully with "
#    f"{len(model_features)} features."
#)
#
#print(model_features)



# -------------------------------------------------------------------
# Application header
# -------------------------------------------------------------------

LOGO_PATH = (
    PROJECT_ROOT
    / "app"
    / "assets"
    / "swiss_data_intelligence_logo.png"
)

# Display the project identity in a centered hero section.
logo_col1, logo_col2, logo_col3 = st.columns(
    [1, 5, 1]
)

with logo_col2:
    st.image(
        LOGO_PATH,
        width="stretch",
    )

st.markdown(
    """
    <p style="
        text-align: center;
        font-size: 1.15rem;
        color: #AAB2BF;
        margin-top: -15px;
        margin-bottom: 30px;
    ">
        Explore Swiss housing patterns through public data,
        interactive analytics and machine learning.
    </p>
    """,
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------
# Dataset overview
# -------------------------------------------------------------------

st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

overview = [
    ("🇨🇭", "Cantons", df["GEO"].nunique()),
    ("📅", "Data coverage", f"{df['YEAR'].min()}-{df['YEAR'].max()}"),
    ("📊", "Observations", len(df)),
]

for column, (icon, label, value) in zip(
    [col1, col2, col3],
    overview,
):
    with column:
        st.markdown(
            f"""
            <div style="text-align:center; padding:10px 0 20px 0;">
                <div style="font-size:1.8rem; margin-bottom:8px;">
                    {icon}
                </div>
                <div style="
                    font-size:0.95rem;
                    color:#AAB2BF;
                    font-weight:600;
                ">
                    {label}
                </div>
                <div style="
                    font-size:2.4rem;
                    font-weight:750;
                    margin-top:4px;
                ">
                    {value}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()


# -------------------------------------------------------------------
# Canton and year selection
# -------------------------------------------------------------------

# Get the available cantons from the modelling dataset.
cantons = sorted(
    df["CANTON"].unique()
)

st.subheader("Explore a canton")

selector_left, selector_center, selector_right = st.columns(
    [1, 4, 1]
)

with selector_center:
    canton_col, year_col = st.columns([2, 1])

    with canton_col:
        selected_canton = st.selectbox(
            "Canton",
            options=cantons,
        )

    # Only show years available for the selected canton.
    available_years = sorted(
        df[
            df["CANTON"] == selected_canton
        ]["YEAR"].unique(),
        reverse=True,
    )

    with year_col:
        selected_year = st.selectbox(
            "Year",
            options=available_years,
        )


# Retrieve the observation corresponding to the selected
# canton and year.
selected_data = df[
    (df["CANTON"] == selected_canton)
    & (df["YEAR"] == selected_year)
].iloc[0]

# -------------------------------------------------------------------
# Model inference
# -------------------------------------------------------------------

# Extract the exact feature set expected by the trained model.
# Keeping the stored feature order prevents inconsistencies between
# model training and application inference.
prediction_input = selected_data[
    model_features
].to_frame().T


# Generate the model estimate for the selected canton-year.
model_estimate = model.predict(
    prediction_input
)[0]


# Calculate the difference between the model estimate and
# the observed home-ownership rate.
estimation_error = (
    model_estimate
    - selected_data["HOME_OWNERSHIP_RATE"]
)

# -------------------------------------------------------------------
# Canton profile
# -------------------------------------------------------------------

# Reconstruct the reference categories omitted from the modelling
# dataset because compositional shares sum to one.
share_age_0_19 = 1 - (
    selected_data["SHARE_AGE_20_39"]
    + selected_data["SHARE_AGE_40_64"]
    + selected_data["SHARE_AGE_65_PLUS"]
)

share_6_plus_households = 1 - (
    selected_data["SHARE_1_PERSON_HOUSEHOLDS"]
    + selected_data["SHARE_2_PERSON_HOUSEHOLDS"]
    + selected_data["SHARE_3_PERSON_HOUSEHOLDS"]
    + selected_data["SHARE_4_PERSON_HOUSEHOLDS"]
    + selected_data["SHARE_5_PERSON_HOUSEHOLDS"]
)


# Prepare complete demographic composition for visualisation.
demographic_profile = pd.DataFrame(
    {
        "Age group": [
            "0-19",
            "20-39",
            "40-64",
            "65+",
        ],
        "Share": [
            share_age_0_19,
            selected_data["SHARE_AGE_20_39"],
            selected_data["SHARE_AGE_40_64"],
            selected_data["SHARE_AGE_65_PLUS"],
        ],
    }
)


# Prepare complete household-size composition for visualisation.
household_profile = pd.DataFrame(
    {
        "Household size": [
            "1 person",
            "2 people",
            "3 people",
            "4 people",
            "5 people",
            "6+ people",
        ],
        "Share": [
            selected_data["SHARE_1_PERSON_HOUSEHOLDS"],
            selected_data["SHARE_2_PERSON_HOUSEHOLDS"],
            selected_data["SHARE_3_PERSON_HOUSEHOLDS"],
            selected_data["SHARE_4_PERSON_HOUSEHOLDS"],
            selected_data["SHARE_5_PERSON_HOUSEHOLDS"],
            share_6_plus_households,
        ],
    }
)


st.subheader("Canton profile")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Demographic structure")

    st.bar_chart(
        demographic_profile,
        x="Age group",
        y="Share",
    )

with col2:
    st.markdown("#### Household composition")

    st.bar_chart(
        household_profile,
        x="Household size",
        y="Share",
    )



# -------------------------------------------------------------------
# Home-ownership evolution
# -------------------------------------------------------------------

st.subheader("Home-ownership evolution")

# Extract the complete time series for the selected canton.
canton_history = (
    df[df["CANTON"] == selected_canton][
        ["YEAR", "HOME_OWNERSHIP_RATE"]
    ]
    .sort_values("YEAR")
    .rename(
        columns={
            "HOME_OWNERSHIP_RATE": selected_canton,
        }
    )
)

# Calculate the unweighted mean across cantons for each year.
# This is a descriptive benchmark, not the official Swiss rate.
cantonal_average = (
    df.groupby("YEAR", as_index=False)["HOME_OWNERSHIP_RATE"]
    .mean()
    .rename(
        columns={
            "HOME_OWNERSHIP_RATE": "Cantonal average",
        }
    )
)

# Combine both time series.
home_ownership_history = canton_history.merge(
    cantonal_average,
    on="YEAR",
    how="left",
)

#st.line_chart(
#    home_ownership_history,
#    x="YEAR",
#    y=[
#        selected_canton,
#        "Cantonal average",
#    ],
#)

# Reshape the data into long format for interactive visualisation.
history_long = home_ownership_history.melt(
    id_vars="YEAR",
    value_vars=[
        selected_canton,
        "Cantonal average",
    ],
    var_name="Series",
    value_name="Home ownership rate",
)


# Calculate a dynamic y-axis range so that relatively small
# temporal changes remain visible.
min_rate = history_long["Home ownership rate"].min()
max_rate = history_long["Home ownership rate"].max()

y_margin = max(
    (max_rate - min_rate) * 0.20,
    1.0,
)


# Create an interactive time-series chart.
history_chart = (
    alt.Chart(history_long)
    .mark_line(
        point=True,
        strokeWidth=3,
    )
    .encode(
        x=alt.X(
            "YEAR:O",
            title="Year",
        ),
        y=alt.Y(
            "Home ownership rate:Q",
            title="Home ownership rate (%)",
            scale=alt.Scale(
                domain=[
                    min_rate - y_margin,
                    max_rate + y_margin,
                ],
                zero=False,
            ),
        ),
        color=alt.Color(
            "Series:N",
            title=None,
        ),
        strokeDash=alt.StrokeDash(
            "Series:N",
            title=None,
        ),
        tooltip=[
            alt.Tooltip(
                "properties.CANTON:N",
                title="Canton",
            ),
            alt.Tooltip(
                "properties.HOME_OWNERSHIP_RATE:Q",
                title="Home ownership",
                format=".1f",
            ),
        ],
    )
    .properties(
        height=400,
    )
    .interactive()
)


st.altair_chart(
    history_chart,
    width="stretch",
)


# Calculate the cantonal average for the selected year.
selected_year_average = df[
    df["YEAR"] == selected_year
]["HOME_OWNERSHIP_RATE"].mean()

# Compare the selected canton with the benchmark.
difference_from_average = (
    selected_data["HOME_OWNERSHIP_RATE"]
    - selected_year_average
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Selected canton",
    f"{selected_data['HOME_OWNERSHIP_RATE']:.1f}%",
)

col2.metric(
    "Cantonal average",
    f"{selected_year_average:.1f}%",
)

col3.metric(
    "Difference",
    f"{difference_from_average:+.1f} pp",
)


# -------------------------------------------------------------------
# Model estimate
# -------------------------------------------------------------------

st.subheader("Model estimate")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Observed",
    f"{selected_data['HOME_OWNERSHIP_RATE']:.1f}%",
)

col2.metric(
    "Model estimate",
    f"{model_estimate:.1f}%",
)

col3.metric(
    "Fitted residual",
    f"{estimation_error:+.1f} pp",
)

# Explain how the displayed estimate should be interpreted.
st.caption(
    "The estimate is generated by the final Gradient Boosting model fitted "
    "on the complete 2019-2024 dataset. The fitted residual is therefore "
    "an in-sample difference and should not be interpreted as an "
    "out-of-sample prediction error."
)

# -------------------------------------------------------------------
# Model performance
# -------------------------------------------------------------------

st.subheader("Model performance")

performance_data = pd.DataFrame(
    {
        "Evaluation scenario": [
            "Unseen cantons (GroupKFold)",
            "New year 2024 (Gradient Boosting)",
            "2024 persistence baseline",
        ],
        "MAE (pp)": [
            6.05,
            2.29,
            1.20,
        ],
        "R²": [
            0.359,
            0.885,
            0.964,
        ],
    }
)

st.dataframe(
    performance_data,
    hide_index=True,
    width="stretch",
)

st.caption(
    "The evaluation scenarios answer different questions. "
    "GroupKFold evaluates generalisation to previously unseen cantons. "
    "The temporal holdout evaluates prediction of a new year for cantons "
    "already represented in training. The persistence baseline uses each "
    "canton's 2023 observed value as its prediction for 2024 and highlights "
    "the strong temporal persistence of the target."
)



# -------------------------------------------------------------------
# Geographic comparison
# -------------------------------------------------------------------

# Add visual separation from the previous section.
st.markdown(
    "<div style='height: 40px;'></div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div style="
    font-size: 2rem;
    font-weight: 750;
    margin-bottom: 25px;
">
    Geographic comparison
</div>
""",
    unsafe_allow_html=True,
)

# Retrieve the standard abbreviation for the selected canton.
selected_abbreviation = GEO_TO_ABBREVIATION[
    selected_data["GEO"]
]

# Build the path to the selected canton's coat of arms.
coat_of_arms_path = (
    PROJECT_ROOT
    / "app"
    / "assets"
    / "canton_coats_of_arms"
    / f"{selected_abbreviation}.png"
)

# Prepare geographic data for the selected year.
home_ownership_map = prepare_map_data(
    selected_year,
    df,
    cantons_geo,
)

# Convert the GeoDataFrame to GeoJSON for Altair.
map_geojson = home_ownership_map.__geo_interface__

# -------------------------------------------------------------------
# Base choropleth
# -------------------------------------------------------------------

base_map = (
    alt.Chart(
        alt.Data(
            values=map_geojson,
            format=alt.DataFormat(
                property="features",
                type="json",
            ),
        )
    )
    .mark_geoshape(
        stroke="#D9E2EC",
        strokeWidth=0.8,
    )
    .encode(
        color=alt.Color(
            "properties.HOME_OWNERSHIP_RATE:Q",
            title="Home ownership (%)",
            scale=alt.Scale(
                scheme="blues",
            ),
        ),
        tooltip=[
            alt.Tooltip(
                "properties.CANTON:N",
                title="Canton",
            ),
            alt.Tooltip(
                "properties.HOME_OWNERSHIP_RATE:Q",
                title="Home ownership",
                format=".1f",
            ),
        ],
    )
)

# -------------------------------------------------------------------
# Selected canton highlight
# -------------------------------------------------------------------

selected_map = home_ownership_map[
    home_ownership_map["GEO"]
    == selected_data["GEO"]
]

selected_geojson = selected_map.__geo_interface__

selected_canton_layer = (
    alt.Chart(
        alt.Data(
            values=selected_geojson,
            format=alt.DataFormat(
                property="features",
                type="json",
            ),
        )
    )
    .mark_geoshape(
        fillOpacity=0,
        stroke="#FF3B30",
        strokeWidth=4,
    )
)

# Combine the choropleth and selected-canton outline.
map_chart = (
    alt.layer(
        base_map,
        selected_canton_layer,
    )
    .project(
        type="identity",
        reflectY=True,
    )
    .properties(
        height=500,
    )
)

# -------------------------------------------------------------------
# Selected canton and interactive map
# -------------------------------------------------------------------

# Create the layout for the selected canton profile and the map.
info_col, map_col = st.columns(
    [1, 3],
    vertical_alignment="center",
)

with info_col:
    # Center the canton coat of arms within the information column.
    image_left, image_center, image_right = st.columns(
        [1, 2, 1]
    )

    with image_center:
        st.image(
            coat_of_arms_path,
            width="stretch",
        )

    # Display the selected canton information.
    st.markdown(
        f"<h2 style='text-align: center;'>{selected_canton}</h2>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<p style='text-align: center; color: #AAB2BF; "
        f"font-size: 1.15rem;'>{selected_year}</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<div style='text-align: center; margin-top: 20px; "
        f"font-size: 3.2rem; font-weight: 750;'>"
        f"{selected_data['HOME_OWNERSHIP_RATE']:.1f}%"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='text-align: center; color: #AAB2BF; "
        "font-size: 1rem;'>Home ownership</p>",
        unsafe_allow_html=True,
    )

with map_col:
    st.altair_chart(
        map_chart,
        width="stretch",
    )