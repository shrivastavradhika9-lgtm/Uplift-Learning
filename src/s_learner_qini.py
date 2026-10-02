import pandas as pd


def calculate_qini(
    path="results/s_learner_predictions.csv"
):
    df = pd.read_csv(path)

    df = df.sort_values(
        "estimated_uplift",
        ascending=False
    ).reset_index(drop=True)

    cumulative_treatment = 0.0
    cumulative_control = 0.0

    treatment_count = 0
    control_count = 0

    results = []

    for i, row in df.iterrows():

        if row["treatment"] == 1:
            cumulative_treatment += row["outcome"]
            treatment_count += 1
        else:
            cumulative_control += row["outcome"]
            control_count += 1

        if treatment_count > 0 and control_count > 0:
            qini_gain = (
                cumulative_treatment
                - cumulative_control
                * (treatment_count / control_count)
            )
        else:
            qini_gain = 0.0

        results.append({
            "rank": i + 1,
            "target_percentage": (
                (i + 1) / len(df) * 100
            ),
            "qini_gain": qini_gain
        })

    return pd.DataFrame(results)


if __name__ == "__main__":

    result = calculate_qini()

    print("S-Learner Qini evaluation completed!")

    print("\nQini Gain Summary:")
    print(result["qini_gain"].describe())

    result.to_csv(
        "results/s_learner_qini_curve.csv",
        index=False
    )

    print("\nS-Learner Qini curve saved successfully!")

    print("\nSample:")
    print(
        result.iloc[
            [59, 119, 179, 299, 359, 599]
        ].to_string(index=False)
    )