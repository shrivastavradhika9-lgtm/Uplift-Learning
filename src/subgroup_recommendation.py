import pandas as pd


def analyze_recommendations(
    path="results/learner_recommendations.csv"
):
    recommendations = pd.read_csv(path)

    predictions = pd.read_csv(
        "results/s_learner_predictions.csv"
    )

    df = predictions[
        [
            "learner_id",
            "previous_score"
        ]
    ].merge(
        recommendations[
            [
                "learner_id",
                "recommendation",
                "priority"
            ]
        ],
        on="learner_id"
    )

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
            recommended=("recommendation",
                          lambda x:
                          (x == "Recommend Intervention").sum())
        )
        .reset_index()
    )

    result["recommendation_rate"] = (
        result["recommended"]
        / result["learners"]
        * 100
    )

    return result


if __name__ == "__main__":

    result = analyze_recommendations()

    print("Subgroup recommendation analysis completed!")

    print("\nRecommendation by subgroup:")
    print(result.to_string(index=False))

    result.to_csv(
        "results/subgroup_recommendation.csv",
        index=False
    )

    print(
        "\nSubgroup recommendation analysis saved successfully!"
    )