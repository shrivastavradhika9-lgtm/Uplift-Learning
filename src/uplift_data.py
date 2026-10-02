import pandas as pd


FEATURES = [
    "age",
    "study_hours",
    "attendance_rate",
    "previous_score",
    "assignments_completed"
]


def prepare_uplift_data(path="data/learners.csv"):
    df = pd.read_csv(path)

    X = df[FEATURES]
    treatment = df["treatment"]
    outcome = df["outcome"]

    return X, treatment, outcome


if __name__ == "__main__":
    X, treatment, outcome = prepare_uplift_data()

    print("Uplift data prepared successfully!")
    print("Features shape:", X.shape)
    print("Treatment shape:", treatment.shape)
    print("Outcome shape:", outcome.shape)
    print("\nFeatures:")
    print(X.columns.tolist())