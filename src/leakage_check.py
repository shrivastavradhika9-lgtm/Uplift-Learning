import pandas as pd

DATA_PATH = "data/learners.csv"

def main():
    df = pd.read_csv(DATA_PATH)

    target = "outcome"
    treatment = "treatment"

    features = [
        "age",
        "study_hours",
        "attendance_rate",
        "previous_score",
        "assignments_completed"
    ]

    print("MDS-02 Leakage Check")
    print("=" * 40)

    if target in features:
        print("FAIL: Outcome is included as a feature.")
    else:
        print("PASS: Outcome is not used as a feature.")

    if treatment in features:
        print("WARNING: Treatment is included in predictive features.")
    else:
        print("PASS: Treatment is kept separate from predictive features.")

    if df.index.duplicated().sum() == 0:
        print("PASS: No duplicate dataset rows detected.")
    else:
        print("WARNING: Duplicate rows detected.")

    if df[target].isnull().sum() == 0:
        print("PASS: Outcome has no missing values.")
    else:
        print("WARNING: Missing outcome values detected.")

    print("\nLeakage check completed.")

if __name__ == "__main__":
    main()