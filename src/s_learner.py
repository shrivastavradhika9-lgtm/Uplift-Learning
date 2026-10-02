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


def train_s_learner(train_df):

    X = train_df[FEATURES]
    y = train_df["outcome"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model


def predict_uplift(test_df, model):

    X_control = test_df[FEATURES].copy()
    X_treatment = test_df[FEATURES].copy()

    X_control["treatment"] = 0
    X_treatment["treatment"] = 1

    predicted_control = model.predict(X_control)
    predicted_treatment = model.predict(X_treatment)

    uplift = predicted_treatment - predicted_control

    result = test_df.copy()

    result["predicted_control"] = predicted_control
    result["predicted_treatment"] = predicted_treatment
    result["estimated_uplift"] = uplift

    return result


if __name__ == "__main__":

    df = pd.read_csv("data/learners.csv")

    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        stratify=df["treatment"]
    )

    model = train_s_learner(train_df)

    result = predict_uplift(
        test_df,
        model
    )

    print("S-Learner trained successfully!")

    print("\nEstimated uplift summary:")
    print(
        result["estimated_uplift"].describe()
    )

    result.to_csv(
        "results/s_learner_predictions.csv",
        index=False
    )

    print("\nS-Learner predictions saved successfully!")