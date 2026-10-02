from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
import json
from pathlib import Path
import logging
from src.config import UPLIFT_THRESHOLD

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


app = FastAPI(
    title="MDS-02 Uplift Modeling API",
    version="1.0.0"
)


FEATURES = [
    "age",
    "study_hours",
    "attendance_rate",
    "previous_score",
    "assignments_completed"
]


from pydantic import BaseModel, Field

class LearnerInput(BaseModel):
    age: int = Field(ge=18, le=100)
    study_hours: float = Field(ge=0, le=24)
    attendance_rate: float = Field(ge=0, le=100)
    previous_score: float = Field(ge=0, le=100)
    assignments_completed: int = Field(ge=0, le=10)


def train_models():

    df = pd.read_csv("data/learners.csv")

    X = df[FEATURES]
    treatment = df["treatment"]
    outcome = df["outcome"]

    control_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    treatment_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    control_model.fit(
        X[treatment == 0],
        outcome[treatment == 0]
    )

    treatment_model.fit(
        X[treatment == 1],
        outcome[treatment == 1]
    )

    return control_model, treatment_model

def save_audit_log(learner, predicted_control, predicted_treatment,
                   estimated_uplift, recommendation):

    log_file = Path("results/audit_log.jsonl")

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "input": learner.model_dump(),
        "predicted_control": round(float(predicted_control), 4),
        "predicted_treatment": round(float(predicted_treatment), 4),
        "estimated_uplift": round(float(estimated_uplift), 4),
        "recommendation": recommendation
    }

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

control_model, treatment_model = train_models()


@app.get("/")
def root():

    return {
        "message": "MDS-02 Uplift Modeling API is running",
        "version": "1.0.0"
    }


@app.post("/predict")
def predict(learner: LearnerInput):

    try:
        input_data = pd.DataFrame([learner.model_dump()])

        predicted_control = control_model.predict(input_data)[0]
        predicted_treatment = treatment_model.predict(input_data)[0]

        estimated_uplift = predicted_treatment - predicted_control

        recommendation = (
            "Recommend Intervention"
            if estimated_uplift >= UPLIFT_THRESHOLD
            else "No Intervention"
        )

        save_audit_log(
            learner,
            predicted_control,
            predicted_treatment,
            estimated_uplift,
            recommendation
        )

        logger.info(
            "Prediction completed successfully. Uplift=%.4f",
            estimated_uplift
        )

        return {
            "predicted_control": round(float(predicted_control), 4),
            "predicted_treatment": round(float(predicted_treatment), 4),
            "estimated_uplift": round(float(estimated_uplift), 4),
            "recommendation": recommendation
        }

    except Exception as e:

        logger.exception("Prediction failed")

        return {
            "error": "Prediction could not be completed",
            "message": "An internal prediction error occurred."
        }