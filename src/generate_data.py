import numpy as np
import pandas as pd

from config import RANDOM_STATE


def generate_dataset(n_samples=3000):
    np.random.seed(RANDOM_STATE)

    data = pd.DataFrame({
        "learner_id": range(1, n_samples + 1),
        "age": np.random.randint(18, 35, n_samples),
        "study_hours": np.round(
            np.random.uniform(1, 10, n_samples), 1
        ),
        "attendance_rate": np.round(
            np.random.uniform(50, 100, n_samples), 1
        ),
        "previous_score": np.round(
            np.random.uniform(30, 95, n_samples), 1
        ),
        "assignments_completed": np.random.randint(
            1, 11, n_samples
        ),
        "treatment": np.random.binomial(
            1, 0.5, n_samples
        )
    })

    # Base learning outcome
    outcome = (
        0.25 * data["study_hours"]
        + 0.03 * data["attendance_rate"]
        + 0.05 * data["previous_score"]
        + 0.8 * data["assignments_completed"]
    )

    # Treatment effect
    treatment_effect = (
        data["treatment"]
        * (
            2
            + 0.15 * data["study_hours"]
            + 0.02 * data["attendance_rate"]
        )
    )

    # Random noise
    noise = np.random.normal(0, 2, n_samples)

    data["outcome"] = np.round(
        outcome + treatment_effect + noise,
        2
    )

    return data


if __name__ == "__main__":
    df = generate_dataset()

    print(df.head())
    print("\nShape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    df.to_csv("data/learners.csv", index=False)
    print("\nDataset saved successfully!")
