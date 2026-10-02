import pandas as pd


def generate_recommendations(
    path="results/s_learner_predictions.csv"
):
    df = pd.read_csv(path)

    threshold = df["estimated_uplift"].quantile(0.75)

    df["recommendation"] = df["estimated_uplift"].apply(
        lambda x:
        "Recommend Intervention"
        if x >= threshold
        else "No Intervention"
    )

    df["priority"] = df["estimated_uplift"].apply(
        lambda x:
        "High"
        if x >= threshold
        else "Standard"
    )

    result = df[
        [
            "learner_id",
            "estimated_uplift",
            "recommendation",
            "priority"
        ]
    ].sort_values(
        "estimated_uplift",
        ascending=False
    )

    return result, threshold


if __name__ == "__main__":

    result, threshold = generate_recommendations()

    print("Recommendation engine completed!")

    print(
        "\nIntervention threshold:",
        round(threshold, 4)
    )

    print("\nRecommendation counts:")
    print(result["recommendation"].value_counts())

    print("\nTop 10 recommendations:")
    print(result.head(10).to_string(index=False))

    result.to_csv(
        "results/learner_recommendations.csv",
        index=False
    )

    print(
        "\nRecommendations saved successfully!"
    )