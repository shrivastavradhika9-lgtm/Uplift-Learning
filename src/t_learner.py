import pandas as pd

from sklearn.ensemble import RandomForestRegressor


FEATURES = [
    "age",
    "study_hours",
    "attendance_rate",
    "previous_score",
    "assignments_completed"
]


def train_t_learner(path="data/learners.csv"):
    df = pd.read_csv(path)

    X = df[FEATURES]
    treatment = df["treatment"]
    outcome = df["outcome"]

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


def calculate_uplift(
    df,
    control_model,
    treatment_model
):
    X = df[FEATURES]

    predicted_control = control_model.predict(X)
    predicted_treatment = treatment_model.predict(X)

    uplift = predicted_treatment - predicted_control

    result = df.copy()

    result["predicted_control"] = predicted_control
    result["predicted_treatment"] = predicted_treatment
    result["estimated_uplift"] = uplift

    return result


if __name__ == "__main__":
    df = pd.read_csv("data/learners.csv")

    control_model, treatment_model = train_t_learner()

    result = calculate_uplift(
        df,
        control_model,
        treatment_model
    )

    print("T-Learner trained successfully!")

    print("\nSample uplift predictions:")

    print(
        result[
            [
                "learner_id",
                "treatment",
                "predicted_control",
                "predicted_treatment",
                "estimated_uplift"
            ]
        ].head(10)
    )

    result.to_csv(
        "results/uplift_predictions.csv",
        index=False
    )

    print("\nUplift predictions saved successfully!")