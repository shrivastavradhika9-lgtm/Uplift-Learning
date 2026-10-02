import pandas as pd


def calibration_analysis(
    path="results/s_learner_predictions.csv"
):
    df = pd.read_csv(path)

    df["true_effect"] = (
        2
        + 0.15 * df["study_hours"]
        + 0.02 * df["attendance_rate"]
    )

    df["uplift_bin"] = pd.qcut(
        df["estimated_uplift"],
        q=5,
        labels=[
            "Q1 Lowest",
            "Q2",
            "Q3",
            "Q4",
            "Q5 Highest"
        ],
        duplicates="drop"
    )

    result = (
        df.groupby(
            "uplift_bin",
            observed=True
        )
        .agg(
            learners=("learner_id", "count"),
            mean_predicted_uplift=(
                "estimated_uplift",
                "mean"
            ),
            mean_true_effect=(
                "true_effect",
                "mean"
            )
        )
        .reset_index()
    )

    result["calibration_error"] = (
        result["mean_predicted_uplift"]
        - result["mean_true_effect"]
    )

    return result


if __name__ == "__main__":

    result = calibration_analysis()

    print("Calibration analysis completed!")

    print("\nCalibration Results:")
    print(
        result.to_string(index=False)
    )

    result.to_csv(
        "results/calibration_analysis.csv",
        index=False
    )

    print(
        "\nCalibration analysis saved successfully!"
    )