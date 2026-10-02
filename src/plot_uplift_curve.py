import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("results/uplift_curve.csv")

plt.figure(figsize=(8, 5))

plt.plot(
    df["target_percentage"],
    df["observed_effect"],
    marker="o"
)

plt.xlabel("Learners Targeted (%)")
plt.ylabel("Observed Treatment Effect")
plt.title("Uplift Curve")

plt.xticks(df["target_percentage"])
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "results/uplift_curve.png",
    dpi=150
)

plt.show()

print("Uplift curve graph saved successfully!")