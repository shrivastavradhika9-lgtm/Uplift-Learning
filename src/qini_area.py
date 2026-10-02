import pandas as pd
import numpy as np


df = pd.read_csv("results/qini_curve.csv")

x = df["target_percentage"].values
model_gain = df["qini_gain"].values

total_qini = model_gain[-1]

random_gain = (
    x / 100
) * total_qini

model_area = np.trapezoid(
    model_gain,
    x
)

random_area = np.trapezoid(
    random_gain,
    x
)

area_difference = model_area - random_area

print("Qini Area Analysis")
print("------------------")

print("Model Qini Area:",
      round(model_area, 2))

print("Random Baseline Area:",
      round(random_area, 2))

print("Area Difference:",
      round(area_difference, 2))