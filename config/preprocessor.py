from pathlib import Path

import pandas as pd
from data.dataset import Dataset

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split


RAW_PATH = Path("data/raw/nasa.csv")
CLEAN_PATH = Path("data/processed/nasa_clean.csv")

TARGET_COL = "Hazardous"

NUMERIC_FEATURES = [
    "Absolute Magnitude",
    "Est Dia in KM(min)",
    "Est Dia in KM(max)",
    "Relative Velocity km per sec",
    "Miss Dist.(Astronomical)",
    "Orbit Uncertainity",
    "Minimum Orbit Intersection",
    "Jupiter Tisserand Invariant",
    "Eccentricity",
    "Semi Major Axis",
    "Inclination",
    "Orbital Period",
    "Perihelion Distance",
    "Aphelion Dist",
    "Mean Anomaly",
    "Mean Motion",
]

DROP_COLS = [
    "Neo Reference ID",
    "Name",

    "Est Dia in M(min)",
    "Est Dia in M(max)",
    "Est Dia in Miles(min)",
    "Est Dia in Miles(max)",
    "Est Dia in Feet(min)",
    "Est Dia in Feet(max)",

    "Relative Velocity km per hr",
    "Miles per hour",

    "Miss Dist.(lunar)",
    "Miss Dist.(kilometers)",
    "Miss Dist.(miles)",

    "Close Approach Date",
    "Epoch Date Close Approach",

    "Orbiting Body",
    "Orbit ID",
    "Orbit Determination Date",
    "Epoch Osculation",
    "Equinox",
    "Asc Node Longitude",
    "Perihelion Arg",
    "Perihelion Time",
]


def build_clean_dataset():
    ds = Dataset(RAW_PATH)
    df = ds.getDataset()

    print("Raw shape:", df.shape)

    # Normalizzazione target a 0/1
    df[TARGET_COL] = df[TARGET_COL].astype(str).str.lower().map({
        "true": 1,
        "false": 0
    }).fillna(df[TARGET_COL])

    df[TARGET_COL] = df[TARGET_COL].astype(int)

    # Drop colonne inutili
    cols_to_drop = [c for c in DROP_COLS if c in df.columns]
    df = df.drop(columns=cols_to_drop)

    # Teniamo solo feature previste + target
    keep_cols = [c for c in NUMERIC_FEATURES if c in df.columns] + [TARGET_COL]
    df = df[keep_cols]

    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)

    print("Clean shape:", df.shape)
    print("Hazardous distribution:")
    print(df[TARGET_COL].value_counts(normalize=True))


def load_clean_dataset() -> pd.DataFrame:
    ds = Dataset(CLEAN_PATH)
    return ds.getDataset()


def build_preprocessor() -> ColumnTransformer:
    num_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, NUMERIC_FEATURES)
        ],
        remainder="drop"
    )

    return preprocessor


def prepare_train_test_raw(test_size: float = 0.2, random_state: int = 42):
    df = load_clean_dataset()

    X_raw = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]

    print("\nShape X_raw:", X_raw.shape)
    print("Distribuzione y complessiva:")
    print(y.value_counts().to_string())

    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X_raw,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    print("\nDistribuzione y_train:")
    print(y_train.value_counts().to_string())
    print("\nDistribuzione y_test:")
    print(y_test.value_counts().to_string())

    return X_train_raw, X_test_raw, y_train, y_test