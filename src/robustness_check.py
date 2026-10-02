import pandas as pd
from data_validation import validate_data


def run_test(name, df):
    valid, messages = validate_data(df)

    print(f"\n{name}")
    print("-" * len(name))

    if valid:
        print("UNEXPECTED: Validation passed")
    else:
        print("EXPECTED: Validation failed")

    for message in messages:
        print("-", message)


if __name__ == "__main__":

    original = pd.read_csv(
        "data/learners.csv"
    )

    # Test 1: Missing column
    missing_column = original.drop(
        columns=["study_hours"]
    )

    run_test(
        "Test 1 - Missing Feature",
        missing_column
    )

    # Test 2: Invalid treatment value
    invalid_treatment = original.copy()

    invalid_treatment.loc[
        0, "treatment"
    ] = 5

    run_test(
        "Test 2 - Invalid Treatment Value",
        invalid_treatment
    )

    # Test 3: Missing value
    missing_value = original.copy()

    missing_value.loc[
        0, "previous_score"
    ] = None

    run_test(
        "Test 3 - Missing Value",
        missing_value
    )

    # Test 4: Empty dataset
    empty_data = original.iloc[0:0]

    run_test(
        "Test 4 - Empty Dataset",
        empty_data
    )