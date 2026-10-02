import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("results/qini_curve.csv")

total_qini = df["qini_gain"].iloc[-1]

df["random_baseline"] = (
    df["target_percentage"] / 100
) * total_qini


plt.figure(figsize=(8, 5))

plt.plot(
    df["target_percentage"],
    df["qini_gain"],
    label="T-Learner Qini Curve"
)

plt.plot(
    df["target_percentage"],
    df["random_baseline"],
    linestyle="--",
    label="Random Baseline"
)

plt.xlabel("Learners Targeted (%)")
plt.ylabel("Cumulative Qini Gain")
plt.title("Qini Gain Curve vs Random Baseline")

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "results/qini_curve_comparison.png",
    dpi=150
)

plt.show()

print("Qini comparison graph saved successfully!")