import pandas as pd
import numpy as np


t_learner = pd.read_csv(
    "results/qini_curve.csv"
)

s_learner = pd.read_csv(
    "results/s_learner_qini_curve.csv"
)


t_area = np.trapezoid(
    t_learner["qini_gain"],
    t_learner["target_percentage"]
)

s_area = np.trapezoid(
    s_learner["qini_gain"],
    s_learner["target_percentage"]
)


print("Qini Area Comparison")
print("--------------------")

print(
    "T-Learner Qini Area:",
    round(t_area, 2)
)

print(
    "S-Learner Qini Area:",
    round(s_area, 2)
)

print(
    "Difference (S - T):",
    round(s_area - t_area, 2)
)