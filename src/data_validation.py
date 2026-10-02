import pandas as pd


REQUIRED_COLUMNS = [
    "learner_id",
    "age",
    "study_hours",
    "attendance_rate",
    "previous_score",
    "assignments_completed",
    "treatment",
    "outcome"
]


def validate_data(df):

    errors = []

    # Check required columns
    missing_columns = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        errors.append(
            f"Missing columns: {missing_columns}"
        )

    # Check empty dataset
    if df.empty:
        errors.append(
            "Dataset is empty"
        )

    # Check treatment values
    if "treatment" in df.columns:
        invalid_treatment = set(
            df["treatment"].dropna().unique()
        ) - {0, 1}

        if invalid_treatment:
            errors.append(
                f"Invalid treatment values: "
                f"{invalid_treatment}"
            )

    # Check missing values
    if df.isnull().any().any():
        missing = (
            df.isnull()
            .sum()
            .loc[lambda x: x > 0]
            .to_dict()
        )

        errors.append(
            f"Missing values found: {missing}"
        )

    if errors:
        return False, errors

    return True, ["Data validation passed"]


if __name__ == "__main__":

    df = pd.read_csv(
        "data/learners.csv"
    )

    valid, messages = validate_data(df)

    print("Data Validation Result:")
    print("-----------------------")

    if valid:
        print("VALID")
    else:
        print("INVALID")

    for message in messages:
        print("-", message)