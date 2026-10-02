import pandas as pd


def calculate_uplift_curve(
    path="results/test_uplift_predictions.csv"
):
    df = pd.read_csv(path)

    # Highest estimated uplift first
    df = df.sort_values(
        "estimated_uplift",
        ascending=False
    ).reset_index(drop=True)

    results = []

    total = len(df)

    for percentage in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:

        n = int(total * percentage / 100)

        selected = df.iloc[:n]

        treatment_outcome = selected.loc[
            selected["treatment"] == 1,
            "outcome"
        ].mean()

        control_outcome = selected.loc[
            selected["treatment"] == 0,
            "outcome"
        ].mean()

        observed_effect = (
            treatment_outcome - control_outcome
        )

        results.append({
            "target_percentage": percentage,
            "learners_targeted": n,
            "treatment_outcome": round(
                treatment_outcome, 4
            ),
            "control_outcome": round(
                control_outcome, 4
            ),
            "observed_effect": round(
                observed_effect, 4
            )
        })

    result_df = pd.DataFrame(results)

    return result_df


if __name__ == "__main__":

    result = calculate_uplift_curve()

    print("Uplift curve calculated successfully!")

    print("\nUplift Curve:")
    print(result.to_string(index=False))

    result.to_csv(
        "results/uplift_curve.csv",
        index=False
    )

    print("\nUplift curve saved successfully!")