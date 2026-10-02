import pandas as pd


SENSITIVE_COLUMN_KEYWORDS = [
    "name",
    "email",
    "phone",
    "mobile",
    "address",
    "password",
    "aadhaar",
    "pan",
    "dob"
]


def privacy_audit(path="data/learners.csv"):

    df = pd.read_csv(path)

    flagged_columns = []

    for column in df.columns:
        column_lower = column.lower()

        for keyword in SENSITIVE_COLUMN_KEYWORDS:
            if keyword in column_lower:
                flagged_columns.append(column)
                break

    return df, flagged_columns


if __name__ == "__main__":

    df, flagged_columns = privacy_audit()

    print("Privacy audit completed!")
    print("\nDataset shape:", df.shape)

    if flagged_columns:
        print("\nPotential sensitive columns:")
        for column in flagged_columns:
            print("-", column)
    else:
        print("\nNo obvious sensitive/PII columns detected.")

    print("\nColumns checked:")
    print(df.columns.tolist())