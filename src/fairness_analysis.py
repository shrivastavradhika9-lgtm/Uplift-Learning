import pandas as pd


def analyze_fairness(
    path="results/subgroup_recommendation.csv"
):
    df = pd.read_csv(path)

    max_rate = df["recommendation_rate"].max()
    min_rate = df["recommendation_rate"].min()

    rate_difference = max_rate - min_rate

    return df, rate_difference


if __name__ == "__main__":

    df, rate_difference = analyze_fairness()

    print("Fairness analysis completed!")

    print("\nSubgroup recommendation rates:")
    print(
        df[
            [
                "score_group",
                "learners",
                "recommended",
                "recommendation_rate"
            ]
        ].to_string(index=False)
    )

    print(
        "\nMaximum recommendation-rate difference:",
        round(rate_difference, 2),
        "percentage points"
    )

    df.to_csv(
        "results/fairness_analysis.csv",
        index=False
    )

    print("\nFairness analysis saved successfully!")