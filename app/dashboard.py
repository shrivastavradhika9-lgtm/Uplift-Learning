import streamlit as st
import requests
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Uplift Platform",
    page_icon="📊",
    layout="centered"
)

st.title("Uplift Modeling Platform")
st.write("Personalized Learning Intervention Recommendation")

st.subheader("Learner Information")

age = st.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=22
)

study_hours = st.number_input(
    "Study Hours",
    min_value=0.0,
    max_value=24.0,
    value=6.5
)

attendance_rate = st.number_input(
    "Attendance Rate (%)",
    min_value=0.0,
    max_value=100.0,
    value=85.0
)

previous_score = st.number_input(
    "Previous Score",
    min_value=0.0,
    max_value=100.0,
    value=65.0
)

assignments_completed = st.number_input(
    "Assignments Completed",
    min_value=0,
    max_value=10,
    value=8
)

st.divider()

st.subheader("Learner Recommendation Summary")

import pandas as pd

try:
    recommendations = pd.read_csv(
        "results/learner_recommendations.csv"
    )

    total_learners = len(recommendations)

    recommended = (
        recommendations["recommendation"]
        == "Recommend Intervention"
    ).sum()

    no_intervention = (
        recommendations["recommendation"]
        == "No Intervention"
    ).sum()

    average_uplift = recommendations[
        "estimated_uplift"
    ].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Learners", total_learners)
    col2.metric("Recommend Intervention", recommended)
    col3.metric("No Intervention", no_intervention)
    col4.metric(
        "Average Estimated Uplift",
        f"{average_uplift:.2f}"
    )

except Exception:
    st.warning(
        "Recommendation summary is currently unavailable."
    )
st.divider()

st.subheader("Estimated Uplift Distribution")

fig, ax = plt.subplots()

st.divider()

st.subheader("Qini Gain Curve")

qini = pd.read_csv("results/qini_curve.csv")

fig_qini, ax_qini = plt.subplots()

ax_qini.plot(
    qini["target_percentage"],
    qini["qini_gain"],
    label="T-Learner Qini Curve"
)

ax_qini.plot(
    qini["target_percentage"],
    qini["random_baseline"],
    linestyle="--",
    label="Random Baseline"
)

ax_qini.set_xlabel("Learners Targeted (%)")
ax_qini.set_ylabel("Cumulative Qini Gain")
ax_qini.set_title("Qini Gain Curve vs Random Baseline")
ax_qini.legend()

st.pyplot(fig_qini)

ax.hist(
    recommendations["estimated_uplift"],
    bins=20
)

ax.set_xlabel("Estimated Uplift")
ax.set_ylabel("Number of Learners")
ax.set_title("Distribution of Estimated Uplift")

st.pyplot(fig)

if st.button("Predict Intervention"):

    data = {
        "age": age,
        "study_hours": study_hours,
        "attendance_rate": attendance_rate,
        "previous_score": previous_score,
        "assignments_completed": assignments_completed
    }

    try:
        response = requests.post(
            "http://api:8000/predict",
            json=data
        )

        if response.status_code == 200:

            result = response.json()

            st.subheader("Prediction Result")

            st.metric(
                "Predicted Outcome - No Intervention",
                result["predicted_control"]
            )

            st.metric(
                "Predicted Outcome - Intervention",
                result["predicted_treatment"]
            )

            st.metric(
                "Estimated Uplift",
                result["estimated_uplift"]
            )

            st.write(
                "**Recommendation:**",
                result["recommendation"]
            )
            
            st.info(
                f"The intervention is predicted to change the learner's "
    		f"outcome by approximately "
    		f"{result['estimated_uplift']:.2f} points."
	   )
        else:
            st.error(
                f"API Error: {response.status_code}"
            )

    except requests.exceptions.ConnectionError:
        st.error(
            "Could not connect to FastAPI. "
            "Make sure the API server is running."
        )