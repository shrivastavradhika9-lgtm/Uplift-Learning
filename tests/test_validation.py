import pandas as pd
from src.data_validation import validate_data


def test_valid_data():

    df = pd.read_csv(
        "data/learners.csv"
    )

    valid, messages = validate_data(df)

    assert valid is True
    assert "Data validation passed" in messages


def test_missing_column():

    df = pd.read_csv(
        "data/learners.csv"
    )

    df = df.drop(
        columns=["study_hours"]
    )

    valid, messages = validate_data(df)

    assert valid is False
    assert any(
        "Missing columns" in message
        for message in messages
    )


def test_invalid_treatment():

    df = pd.read_csv(
        "data/learners.csv"
    )

    df.loc[0, "treatment"] = 5

    valid, messages = validate_data(df)

    assert valid is False
    assert any(
        "Invalid treatment values" in message
        for message in messages
    )


def test_empty_data():

    df = pd.read_csv(
        "data/learners.csv"
    )

    df = df.iloc[0:0]

    valid, messages = validate_data(df)

    assert valid is False
    assert "Dataset is empty" in messages