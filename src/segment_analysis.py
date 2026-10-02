import pandas as pd


def analyze_segments():
    df = pd.read_csv("data/learners.csv")

    df["score_group"] = pd.cut(
        df["previous_score"],
        bins=[0, 50, 70, 100],
        labels=["Low", "Medium", "High"]
    )

    means = (
        df.groupby(
            ["score_group", "treatment"],
            observed=True
        )["outcome"]
        .mean()
        .unstack()
    )

    means["treatment_effect"] = means[1] - means[0]

    print("Segment-wise treatment effect:")
    print(means)

    means.to_csv("results/segment_treatment_effect.csv")


if __name__ == "__main__":
    analyze_segments()