import pandas as pd


def evaluate_policy(
    path="results/s_learner_predictions.csv"
):
    df = pd.read_csv(path)

    df = df.sort_values(
        "estimated_uplift",
        ascending=False
    ).reset_index(drop=True)

    results = []

    # Treat Nobody
    nobody_value = df["predicted_control"].mean()

    results.append({
        "policy": "Treat Nobody",
        "target_percentage": 0,
        "predicted_policy_value": nobody_value
    })

    # Treat Everyone
    everyone_value = df["predicted_treatment"].mean()

    results.append({
        "policy": "Treat Everyone",
        "target_percentage": 100,
        "predicted_policy_value": everyone_value
    })

    # Target selected percentages
    for percentage in [10, 25, 50]:

        n = int(len(df) * percentage / 100)

        selected = df.iloc[:n]
        not_selected = df.iloc[n:]

        policy_value = (
            selected["predicted_treatment"].sum()
            + not_selected["predicted_control"].sum()
        ) / len(df)

        results.append({
            "policy": f"Target Top {percentage}%",
            "target_percentage": percentage,
            "predicted_policy_value": policy_value
        })

    return pd.DataFrame(results)


if __name__ == "__main__":

    result = evaluate_policy()

    print("Policy evaluation completed!")
    print("\nPolicy Results:")
    print(result.to_string(index=False))

    result.to_csv(
        "results/policy_evaluation.csv",
        index=False
    )

    print("\nPolicy evaluation saved successfully!")