import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


FEATURES = [
    "age",
    "study_hours",
    "attendance_rate",
    "previous_score",
    "assignments_completed",
    "treatment"
]


def train_model(path="data/learners.csv"):

    df = pd.read_csv(path)

    train_df, _ = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        stratify=df["treatment"]
    )

    X = train_df[FEATURES]
    y = train_df["outcome"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model


if __name__ == "__main__":

    model = train_model()

    result = pd.DataFrame({
        "feature": FEATURES,
        "importance": model.feature_importances_
    })

    result = result.sort_values(
        "importance",
        ascending=False
    )

    print("Feature importance analysis completed!")

    print("\nFeature Importance:")
    print(
        result.to_string(index=False)
    )

    result.to_csv(
        "results/feature_importance.csv",
        index=False
    )

    print(
        "\nFeature importance saved successfully!"
    )
