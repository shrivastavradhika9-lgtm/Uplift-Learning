import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


FEATURES = [
    "age",
    "study_hours",
    "attendance_rate",
    "previous_score",
    "assignments_completed"
]


def train_t_learner(train_df):
    X = train_df[FEATURES]
    treatment = train_df["treatment"]
    outcome = train_df["outcome"]

    X_control = X[treatment == 0]
    y_control = outcome[treatment == 0]

    X_treatment = X[treatment == 1]
    y_treatment = outcome[treatment == 1]

    control_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    treatment_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    control_model.fit(X_control, y_control)
    treatment_model.fit(X_treatment, y_treatment)

    return control_model, treatment_model


def predict_uplift(
    test_df,
    control_model,
    treatment_model
):
    X_test = test_df[FEATURES]

    predicted_control = control_model.predict(X_test)
    predicted_treatment = treatment_model.predict(X_test)

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

    control_model, treatment_model = train_t_learner(
        train_df
    )

    result = predict_uplift(
        test_df,
        control_model,
        treatment_model
    )

    print("T-Learner evaluation completed!")

    print("\nTest set shape:", result.shape)

    print("\nEstimated uplift summary:")
    print(result["estimated_uplift"].describe())

    result.to_csv(
        "results/test_uplift_predictions.csv",
        index=False
    )

    print("\nTest uplift predictions saved successfully!")