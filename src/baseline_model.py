import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


def load_data():
    return pd.read_csv("data/learners.csv")


def train_baseline_model(df):
    features = [
        "age",
        "study_hours",
        "attendance_rate",
        "previous_score",
        "assignments_completed",
        "treatment"
    ]

    X = df[features]
    y = df["outcome"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)

    return model, mse


if __name__ == "__main__":
    df = load_data()

    model, mse = train_baseline_model(df)

    print("Baseline model trained successfully!")
    print("MSE:", round(mse, 4))
    joblib.dump(model, "models/baseline_model.joblib")
    print("Baseline model saved successfully!")