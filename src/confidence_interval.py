import pandas as pd
import numpy as np


def calculate_confidence_interval(
    path="results/test_uplift_predictions.csv"
):
    df = pd.read_csv(path)

    treatment = df.loc[
        df["treatment"] == 1,
        "outcome"
    ]

    control = df.loc[
        df["treatment"] == 0,
        "outcome"
    ]

    treatment_mean = treatment.mean()
    control_mean = control.mean()

    effect = treatment_mean - control_mean

    treatment_se = (
        treatment.std(ddof=1)
        / np.sqrt(len(treatment))
    )

    control_se = (
        control.std(ddof=1)
        / np.sqrt(len(control))
    )

    standard_error = np.sqrt(
        treatment_se ** 2
        + control_se ** 2
    )

    margin = 1.96 * standard_error

    lower = effect - margin
    upper = effect + margin

    return effect, lower, upper


if __name__ == "__main__":

    effect, lower, upper = (
        calculate_confidence_interval()
    )

    print("95% Confidence Interval")
    print("------------------------")

    print(
        "Observed Treatment Effect:",
        round(effect, 4)
    )

    print(
        "Lower Bound:",
        round(lower, 4)
    )

    print(
        "Upper Bound:",
        round(upper, 4)
    )

    print(
        "\n95% CI:",
        f"[{lower:.4f}, {upper:.4f}]"
    )
