import pandas as pd


def analyze_subgroups(
    path="results/s_learner_predictions.csv"
):
    df = pd.read_csv(path)

    df["score_group"] = pd.cut(
        df["previous_score"],
        bins=[0, 50, 70, 100],
        labels=["Low", "Medium", "High"]
    )

    result = (
        df.groupby(
            "score_group",
            observed=True
        )
        .agg(
            learners=("learner_id", "count"),
            average_uplift=("estimated_uplift", "mean"),
            average_outcome=("outcome", "mean")
        )
        .reset_index()
    )

    return result


if __name__ == "__main__":

    result = analyze_subgroups()

    print("Subgroup analysis completed!")

    print("\nSubgroup Results:")
    print(result.to_string(index=False))

    result.to_csv(
        "results/subgroup_analysis.csv",
        index=False
    )

    print("\nSubgroup analysis saved successfully!")