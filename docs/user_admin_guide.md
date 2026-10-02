#  Uplift Modeling Platform — User and Admin Guide

## 1. Introduction

The Uplift Modeling Platform is a decision-support system for personalized learning intervention allocation.

The platform estimates the potential benefit of an intervention for an individual learner and presents the result through an API and interactive dashboard.

The system contains:

* Uplift modeling
* Recommendation engine
* FastAPI service
* Streamlit dashboard
* Docker deployment
* Prediction audit logging
* Monitoring
* Validation and testing

---

# 2. System Requirements

Recommended environment:

* Windows 10/11
* Python 3.12 or compatible Python version
* Docker Desktop
* Docker Compose
* Internet connection for initial dependency installation

Project directory:

```text
C:\MDS02_Uplift_Learning
```

---

# 3. Project Structure

```text
MDS02_Uplift_Learning/
│
├── app/
│   ├── main.py
│   └── dashboard.py
│
├── data/
│   └── learners.csv
│
├── models/
│   └── baseline_model.joblib
│
├── notebooks/
│
├── results/
│   ├── audit_log.jsonl
│   ├── monitoring_report.txt
│   ├── uplift_curve.png
│   ├── qini_curve.png
│   └── qini_curve_comparison.png
│
├── src/
│   ├── baseline_model.py
│   ├── data_loader.py
│   ├── data_validation.py
│   ├── fairness_analysis.py
│   ├── monitoring.py
│   ├── recommendation_engine.py
│   ├── robustness_check.py
│   ├── s_learner.py
│   ├── t_learner.py
│   └── ...
│
├── tests/
│
├── docs/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .dockerignore
```

---

# 4. Running the Project Locally

Open Command Prompt or PowerShell.

Navigate to the project:

```cmd
cd C:\MDS02_Uplift_Learning
```

Activate the virtual environment if required:

```cmd
venv\Scripts\activate
```

Install dependencies:

```cmd
pip install -r requirements.txt
```

---

# 5. Running the API

Start the FastAPI service:

```cmd
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API becomes available at:

```text
http://localhost:8000
```

API documentation is available through FastAPI's automatic documentation interface.

---

# 6. Checking the API

Open a browser and visit:

```text
http://localhost:8000
```

Expected response:

```json
{
  "message": "MDS-02 Uplift Modeling API is running",
  "version": "1.0.0"
}
```

The exact response may include additional status information depending on the current implementation.

---

# 7. API Documentation

FastAPI provides interactive documentation.

Open:

```text
http://localhost:8000/docs
```

The documentation allows the user to:

* View available endpoints
* Inspect request schemas
* Inspect response schemas
* Send test requests
* View validation errors

---

# 8. Making a Prediction

The prediction endpoint is:

```text
POST /predict
```

Example input:

```json
{
  "age": 22,
  "study_hours": 6.5,
  "attendance_rate": 85,
  "previous_score": 65,
  "assignments_completed": 8
}
```

The API calculates:

```text
Predicted Control Outcome
Predicted Treatment Outcome
Estimated Uplift
Recommendation
Model Version
```

Example output:

```json
{
  "predicted_control": 12.9032,
  "predicted_treatment": 19.1506,
  "estimated_uplift": 6.2474,
  "recommendation": "Recommend Intervention",
  "model_version": "v1"
}
```

---

# 9. Understanding the Prediction

The important value is:

```text
Estimated Uplift
```

The basic calculation is:

```text
Estimated Uplift =
Predicted Treatment Outcome
-
Predicted Control Outcome
```

For example:

```text
Treatment prediction = 19.1506
Control prediction   = 12.9032

Uplift = 19.1506 - 12.9032
       = 6.2474
```

The current recommendation threshold is:

```text
5.0629
```

Therefore, the example produces:

```text
Recommend Intervention
```

The recommendation is a decision-support signal and requires human review.

---

# 10. Running the Streamlit Dashboard

The dashboard can be started with:

```cmd
streamlit run app/dashboard.py --server.port 8501
```

For the Docker deployment used in this project, the dashboard is exposed through host port `8502`.

Open:

```text
http://localhost:8502
```

---

# 11. Using the Dashboard

The dashboard provides learner input fields.

Enter:

* Age
* Study hours
* Attendance rate
* Previous score
* Assignments completed

Then submit the prediction.

The dashboard displays:

* Predicted control outcome
* Predicted treatment outcome
* Estimated uplift
* Recommendation

---

# 12. Dashboard Analytics

The dashboard also provides analytical views such as:

### Uplift Distribution

Shows the distribution of estimated uplift values across learners.

### Qini Curve

Provides an evaluation view of uplift ranking.

### Recommendation Summary

Shows the current distribution of intervention recommendations.

These visualizations are intended for analysis and monitoring.

---

# 13. Running with Docker Compose

Docker Desktop must be running.

Navigate to:

```cmd
cd C:\MDS02_Uplift_Learning
```

Build and start the services:

```cmd
docker compose up -d --build
```

Check running containers:

```cmd
docker ps
```

Expected services:

```text
mds02-uplift-api
mds02-uplift-dashboard
```

---

# 14. Docker URLs

API:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

Dashboard:

```text
http://localhost:8502
```

---

# 15. Stopping the System

To stop the Docker services:

```cmd
docker compose down
```

To restart them:

```cmd
docker compose up -d
```

---

# 16. Checking Container Logs

API logs:

```cmd
docker logs mds02-uplift-api
```

Dashboard logs:

```cmd
docker logs mds02-uplift-dashboard
```

For live API logs:

```cmd
docker logs -f mds02-uplift-api
```

Press:

```text
Ctrl + C
```

to stop following the logs.

---

# 17. Checking Container Status

Run:

```cmd
docker ps
```

A running system should show both containers with an active status.

If a container has stopped, inspect its logs:

```cmd
docker logs <container_name>
```

---

# 18. Monitoring Predictions

Prediction events are stored in:

```text
results/audit_log.jsonl
```

The monitoring script can be executed with:

```cmd
python src\monitoring.py
```

The generated report is stored in:

```text
results\monitoring_report.txt
```

---

# 19. Current Monitoring Metrics

The current monitoring snapshot contains:

```text
Total Predictions: 14

Average Estimated Uplift: 5.7840
Minimum Estimated Uplift: 3.0886
Maximum Estimated Uplift: 6.2474

Recommend Intervention: 11
No Intervention: 3
```

These values represent the current recorded prediction activity and will change as new predictions are made.

---

# 20. Data Validation

Before model processing, the dataset can be validated.

Run:

```cmd
python src\data_validation.py
```

The validation checks:

* Required columns
* Empty dataset
* Missing values
* Treatment values
* Dataset structure

---

# 21. Robustness Testing

Run:

```cmd
python src\robustness_check.py
```

The test suite checks cases including:

* Missing feature
* Invalid treatment value
* Missing value
* Empty dataset

Expected behavior is that invalid input is detected rather than silently processed.

---

# 22. Automated Tests

Run:

```cmd
pytest -q
```

Current result:

```text
4 passed in 0.93s
```

The exact execution time may vary between machines.

---

# 23. Privacy Audit

Run:

```cmd
python src\privacy_audit.py
```

The audit performs a basic check for obvious sensitive or personal-information columns.

This is an automated screening check and is not a complete privacy assessment.

---

# 24. Viewing Generated Results

Important result files are stored in:

```text
results/
```

Examples:

```text
baseline_result.txt
segment_treatment_effect.csv
learner_recommendations.csv
uplift_curve.png
qini_curve.png
qini_curve_comparison.png
audit_log.jsonl
monitoring_report.txt
```

These files support analysis, demonstration and documentation.

---

# 25. Model Artifacts

Model artifacts are stored under:

```text
models/
```

Example:

```text
models/baseline_model.joblib
```

The deployed API trains/loads the required uplift components according to the current implementation.

Model versions should be documented whenever the production artifact changes.

---

# 26. Admin Responsibilities

An administrator or technical maintainer should:

1. Keep dependencies updated.
2. Validate incoming datasets.
3. Monitor API health.
4. Review prediction logs.
5. Monitor model behavior.
6. Review subgroup recommendation rates.
7. Run automated tests after changes.
8. Review security findings.
9. Keep model documentation updated.
10. Maintain reproducible deployment configuration.

---

# 27. Before Updating the Model

Before retraining or replacing a model, perform:

```text
1. Data validation
2. Leakage checks
3. Reproducible train/test split
4. Baseline evaluation
5. Uplift evaluation
6. Qini evaluation
7. Policy evaluation
8. Subgroup analysis
9. Robustness testing
10. Documentation update
```

The new model should not be deployed solely because it produces a different numerical result.

The complete evaluation evidence should be retained.

---

# 28. Updating the Recommendation Threshold

The current threshold is:

```text
5.0629
```

It is defined in:

```text
src/config.py
```

If the threshold is changed, the administrator should:

1. Record the old threshold.
2. Record the new threshold.
3. Re-run policy evaluation.
4. Re-run subgroup analysis.
5. Check recommendation-rate changes.
6. Update documentation.
7. Re-test the API.
8. Record the change in the project history.

---

# 29. Security Guidelines for Administrators

Do not:

* Commit passwords or API keys.
* Store real student personal information unnecessarily.
* Expose the API publicly without authentication and authorization.
* Disable validation to bypass errors.
* Modify model files without recording the change.

Recommended production controls include:

* Authentication
* Authorization
* HTTPS
* Secrets management
* Access logging
* Network restrictions
* Dependency scanning
* Regular backups

---

# 30. Troubleshooting

## Problem: Port 8000 Already in Use

Check the process using the port.

Alternatively, stop the existing API container:

```cmd
docker stop mds02-uplift-api
```

Then restart the services.

---

## Problem: Dashboard Cannot Reach API

When running inside Docker Compose, the dashboard should use:

```text
http://api:8000/predict
```

It should not use:

```text
http://127.0.0.1:8000/predict
```

because `127.0.0.1` inside the dashboard container refers to the dashboard container itself.

---

## Problem: Container Stops Immediately

Check:

```cmd
docker ps -a
```

Then:

```cmd
docker logs mds02-uplift-api
```

or:

```cmd
docker logs mds02-uplift-dashboard
```

The logs should be checked before making configuration changes.

---

## Problem: Validation Error

Check the input ranges.

For example:

```text
attendance_rate must be between 0 and 100
```

Correct the input and submit the request again.

---

# 31. Safe Demonstration Workflow

For a project demonstration:

### Step 1

Start Docker Desktop.

### Step 2

Open Command Prompt:

```cmd
cd C:\MDS02_Uplift_Learning
```

### Step 3

Start the project:

```cmd
docker compose up -d
```

### Step 4

Open API:

```text
http://localhost:8000/docs
```

### Step 5

Open dashboard:

```text
http://localhost:8502
```

### Step 6

Enter a learner profile.

### Step 7

Generate a prediction.

### Step 8

Show:

* Control prediction
* Treatment prediction
* Estimated uplift
* Recommendation

### Step 9

Show the Qini/uplift visualization.

### Step 10

Show monitoring:

```cmd
python src\monitoring.py
```

### Step 11

Show automated tests:

```cmd
pytest -q
```

This demonstrates the complete system rather than only the machine-learning model.

---

# 32. Human Review Procedure

When the system generates:

```text
Recommend Intervention
```

the user should:

1. Review the learner's available contextual information.
2. Consider whether intervention is appropriate.
3. Check for relevant circumstances not represented in the dataset.
4. Make the final decision using appropriate human judgment.
5. Avoid treating the recommendation as an automatic instruction.

The model should not be used to make high-impact educational decisions without appropriate oversight.

---

# 33. Data and Privacy Procedure

For a real deployment:

1. Use approved data sources.
2. Minimize collected data.
3. Avoid unnecessary personal identifiers.
4. Restrict access to authorized users.
5. Define retention periods.
6. Protect data during transmission and storage.
7. Conduct a formal privacy review.
8. Maintain an audit trail.

---

# 34. Production Deployment Considerations

The current Docker deployment is suitable for demonstration and prototype evaluation.

A production deployment would additionally require:

* Authentication
* Authorization
* HTTPS
* Secrets management
* Persistent monitoring
* Centralized logging
* Alerting
* Model registry
* CI/CD
* Automated security scanning
* Backup and recovery
* Scaling strategy
* Formal privacy controls

---

# 35. Quick Command Reference

| Task                 | Command                                             |
| -------------------- | --------------------------------------------------- |
| Go to project        | `cd C:\MDS02_Uplift_Learning`                       |
| Activate venv        | `venv\Scripts\activate`                             |
| Install dependencies | `pip install -r requirements.txt`                   |
| Run API              | `uvicorn app.main:app --host 0.0.0.0 --port 8000`   |
| Run dashboard        | `streamlit run app/dashboard.py --server.port 8501` |
| Start Docker         | `docker compose up -d`                              |
| Build + start        | `docker compose up -d --build`                      |
| Stop Docker          | `docker compose down`                               |
| Container status     | `docker ps`                                         |
| API logs             | `docker logs mds02-uplift-api`                      |
| Dashboard logs       | `docker logs mds02-uplift-dashboard`                |
| Run tests            | `pytest -q`                                         |
| Monitoring           | `python src\monitoring.py`                          |
| Validation           | `python src\data_validation.py`                     |
| Robustness           | `python src\robustness_check.py`                    |
| Privacy audit        | `python src\privacy_audit.py`                       |

---

# 36. User Guide Summary

The normal user workflow is:

```text
Open Dashboard
      ↓
Enter Learner Information
      ↓
Submit Prediction
      ↓
View Control Prediction
      ↓
View Treatment Prediction
      ↓
View Estimated Uplift
      ↓
View Recommendation
      ↓
Human Review
```

---

# 37. Admin Guide Summary

The administrator workflow is:

```text
Start Services
      ↓
Check API Health
      ↓
Check Dashboard
      ↓
Monitor Predictions
      ↓
Review Logs
      ↓
Run Tests
      ↓
Validate Data
      ↓
Review Model Performance
      ↓
Review Subgroups
      ↓
Maintain Documentation
```

---

# 38. Final Note

The MDS-02 Uplift Modeling Platform is a prototype research and decision-support system.

Its current purpose is to demonstrate an end-to-end workflow involving uplift modeling, personalized intervention recommendations, evaluation, deployment and monitoring.

Predictions should be interpreted as model-generated evidence rather than automatic decisions.

Real-world deployment would require independent validation, privacy review, security controls, fairness assessment and appropriate human oversight.
