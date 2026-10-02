#  Uplift Modeling Platform for Personalized Learning Intervention Allocation

## 1. Project Overview

This project develops an end-to-end uplift modeling platform for personalized learning intervention allocation.

The main objective is to identify learners who are more likely to benefit from an intervention, rather than simply identifying learners who have a high or low probability of achieving a particular outcome.

The system uses treatment-control data and uplift modeling techniques to estimate the difference between:

* Expected outcome if a learner receives an intervention
* Expected outcome if the same learner does not receive an intervention

This estimated difference is called **uplift**.

The system provides a recommendation of whether an intervention should be considered for an individual learner.

---

## 2. Problem Statement

In educational environments, intervention resources such as mentoring, additional classes, personalized study plans, or academic support are limited.

A learner with poor academic performance is not necessarily the learner who will benefit most from an intervention.

Therefore, the problem is to identify learners for whom an intervention is expected to produce a meaningful additional benefit.

Traditional predictive models generally estimate an outcome such as academic performance. They do not directly estimate the difference caused by an intervention.

This project addresses this problem using uplift modeling.

---

## 3. Project Objective

The objectives of the project are:

1. Generate and use realistic treatment-control learner data.
2. Perform data validation and preprocessing.
3. Establish a simple baseline for comparison.
4. Implement uplift modeling using T-Learner and S-Learner approaches.
5. Estimate individual-level treatment uplift.
6. Evaluate uplift using uplift curves and Qini analysis.
7. Evaluate intervention policies using estimated policy values.
8. Perform subgroup analysis and recommendation-rate analysis.
9. Analyse uncertainty using confidence intervals.
10. Perform feature importance and calibration analysis.
11. Build a recommendation engine.
12. Provide predictions through a FastAPI service.
13. Build an interactive Streamlit dashboard.
14. Containerize the application using Docker.
15. Maintain prediction audit logs and monitoring reports.
16. Perform input validation, robustness checks and privacy-oriented checks.
17. Provide automated tests and reproducible project artifacts.

---

## 4. Dataset

The project uses a safely simulated learner dataset.

The dataset contains 3,000 learner records and the following variables:

| Feature               | Description                      |
| --------------------- | -------------------------------- |
| learner_id            | Unique learner identifier        |
| age                   | Learner age                      |
| study_hours           | Study hours                      |
| attendance_rate       | Attendance percentage            |
| previous_score        | Previous academic score          |
| assignments_completed | Number of completed assignments  |
| treatment             | Treatment/intervention indicator |
| outcome               | Observed learner outcome         |

The treatment variable contains two groups:

* `0` = Control / No intervention
* `1` = Treatment / Intervention

The simulated data contains heterogeneous treatment effects so that different learner profiles can have different estimated uplift values.

---

## 5. Baseline

A simple treatment-control comparison was established as the initial baseline.

Observed average outcome:

* Control group: approximately 11.14
* Treatment group: approximately 15.32
* Difference: approximately 4.18

This baseline provides a simple reference point before applying individual-level uplift modeling.

The baseline is not treated as proof that intervention causes the observed difference because the project requires careful treatment-effect analysis.

---

## 6. Machine Learning Approach

### T-Learner

The T-Learner trains two separate models:

* One model for the control group
* One model for the treatment group

For a learner:

`Estimated Uplift = Predicted Treatment Outcome - Predicted Control Outcome`

Random Forest regressors were used for the two models.

On the evaluation test split:

* Observed treatment effect: approximately 4.07
* Mean estimated uplift: approximately 4.30
* Correlation between estimated and simulated true effects: approximately 0.41

---

### S-Learner

The S-Learner uses a single model and includes treatment as an input feature.

The treatment variable allows the model to estimate outcomes under different treatment conditions.

On the evaluation test split:

* Mean estimated uplift: approximately 4.31
* Correlation with simulated true effects: approximately 0.42

The S-Learner and T-Learner are evaluated using the same project evaluation framework rather than selecting a model only from a single metric.

---

## 7. Uplift Evaluation

The project evaluates uplift using:

* Uplift curves
* Qini curves
* Qini area
* Policy evaluation
* Treatment-effect estimates
* Confidence intervals
* Subgroup analysis
* Calibration analysis

The current T-Learner Qini area on the evaluation test set was approximately:

`58632.65`

The corresponding random reference area was approximately:

`60651.61`

Therefore, the current result indicates that the implemented uplift ranking requires further improvement before it can be considered reliable for operational intervention allocation.

The result is treated as an experimental finding and limitation rather than as evidence of a universally poor model.

---

## 8. Recommendation Engine

The recommendation engine uses the estimated S-Learner uplift values.

A threshold based on the 75th percentile of estimated uplift was used:

`UPLIFT_THRESHOLD = 5.0629`

Learners with estimated uplift at or above this threshold are assigned:

`Recommend Intervention`

Other learners are assigned:

`No Intervention`

This creates an intervention-targeting policy rather than automatically recommending intervention for every learner.

The recommendation is a model-generated decision support signal and should not replace appropriate human review.

---

## 9. Subgroup Analysis

Subgroup analysis was performed using previous-score groups:

* Low
* Medium
* High

Average estimated uplift:

| Group  | Average Estimated Uplift |
| ------ | -----------------------: |
| Low    |                   4.1378 |
| Medium |                   4.4651 |
| High   |                   4.3144 |

Recommendation rates were also analysed:

| Group  | Recommended | Recommendation Rate |
| ------ | ----------: | ------------------: |
| Low    |    28 / 178 |              15.73% |
| Medium |    67 / 196 |              34.18% |
| High   |    55 / 226 |              24.34% |

The maximum recommendation-rate difference was approximately 18.45 percentage points.

This is an audit finding that requires further investigation. It is not by itself a conclusion that the system is fair or unfair.

---

## 10. Confidence Interval

The observed treatment effect on the evaluation test split was approximately:

`4.0706`

The estimated 95% confidence interval was:

`[3.5367, 4.6045]`

This provides an uncertainty range around the observed treatment-control difference.

---

## 11. Feature Importance

The Random Forest model produced the following predictive feature importance values:

| Feature               | Importance |
| --------------------- | ---------: |
| assignments_completed |     0.3746 |
| treatment             |     0.2786 |
| previous_score        |     0.1152 |
| study_hours           |     0.1068 |
| attendance_rate       |     0.0838 |
| age                   |     0.0410 |

These values represent predictive model importance.

They should not be interpreted as causal importance.

---

## 12. Calibration Analysis

A simulation-based calibration analysis was performed by comparing predicted uplift groups with simulated true treatment effects.

The analysis showed that prediction error varies across uplift groups.

This analysis is simulation-based and is therefore treated as an experimental diagnostic rather than evidence of real-world calibration performance.

---

## 13. Data Validation and Robustness

Automated validation checks include:

* Required-column validation
* Empty dataset detection
* Missing-value detection
* Treatment-value validation
* Input range validation
* Invalid input rejection

Robustness tests successfully detected:

1. Missing `study_hours`
2. Invalid treatment value
3. Missing `previous_score`
4. Empty dataset

FastAPI input validation also rejects invalid values such as attendance rates outside the allowed range.

---

## 14. Privacy and Security

The project uses simulated data rather than real student records.

An automated privacy-oriented audit checks the dataset for obvious identifiers or sensitive-looking columns.

The current dataset contains:

* learner_id
* age
* study_hours
* attendance_rate
* previous_score
* assignments_completed
* treatment
* outcome

The privacy audit is an automated column-level check and does not constitute a complete privacy assessment.

The application also avoids exposing internal prediction errors through the API response.

---

## 15. API

A FastAPI service provides prediction functionality.

Main endpoint:

`POST /predict`

Input fields:

* age
* study_hours
* attendance_rate
* previous_score
* assignments_completed

The API returns:

* predicted control outcome
* predicted treatment outcome
* estimated uplift
* intervention recommendation
* model version

An audit record is generated for predictions.

---

## 16. Dashboard

A Streamlit dashboard provides:

* Learner input form
* Uplift prediction
* Intervention recommendation
* Recommendation summary
* Uplift distribution
* Qini curve visualization

The dashboard communicates with the FastAPI service through the Docker Compose network.

---

## 17. Docker Deployment

The project is containerized using Docker.

Docker Compose runs two services:

### API

FastAPI prediction service.

### Dashboard

Streamlit user interface.

The services communicate using the internal Docker Compose service name.

The dashboard is exposed on:

`http://localhost:8502`

The API is exposed on:

`http://localhost:8000`

---

## 18. Monitoring and Audit Logging

Prediction requests are stored in:

`results/audit_log.jsonl`

The monitoring script calculates:

* Total predictions
* Average estimated uplift
* Minimum estimated uplift
* Maximum estimated uplift
* Number of intervention recommendations
* Number of non-recommendations

The monitoring output is saved to:

`results/monitoring_report.txt`

Current recorded monitoring data contains 14 predictions.

---

## 19. Automated Testing

The project uses Pytest for automated testing.

Current test result:

`4 passed`

Tests cover important data and application behavior.

Additional robustness testing is performed through dedicated validation scripts.

---

## 20. Human Oversight

The system is designed as a decision-support platform.

A model recommendation should not automatically determine a learner's access to educational support.

Human review is required before operational intervention decisions.

Potential concerns such as model uncertainty, subgroup differences, incorrect predictions and changing learner circumstances should be considered before action.

---

## 21. Current Limitations

The current prototype has several limitations:

1. The dataset is simulated rather than collected from real learners.
2. The current Qini evaluation does not demonstrate a strong uplift-ranking result.
3. The current treatment effect is generated using a simulation mechanism.
4. Subgroup recommendation-rate differences require further investigation.
5. Calibration analysis is simulation-based.
6. The model has not yet been validated on external educational datasets.
7. Real-world intervention costs and capacity constraints are not fully modeled.
8. Long-term learner outcomes are not currently available.
9. The recommendation threshold requires further validation.

These limitations will be considered when interpreting project results.

---

## 22. End-to-End Workflow

The complete system workflow is:

`Learner Data`

↓

`Data Validation`

↓

`Feature Processing`

↓

`Treatment-Control Modeling`

↓

`T-Learner / S-Learner`

↓

`Individual Uplift Estimation`

↓

`Uplift & Qini Evaluation`

↓

`Policy Evaluation`

↓

`Subgroup / Fairness Audit`

↓

`Recommendation Engine`

↓

`FastAPI`

↓

`Streamlit Dashboard`

↓

`User Action / Human Review`

↓

`Audit Logging`

↓

`Monitoring`

---

## 23. Technology Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn
* FastAPI
* Pydantic
* Streamlit
* Pytest
* Docker
* Docker Compose
* Joblib

---

## 24. Project Status

The current prototype includes:

* Simulated treatment-control dataset
* Baseline analysis
* T-Learner
* S-Learner
* Uplift evaluation
* Qini evaluation
* Policy evaluation
* Subgroup analysis
* Fairness audit
* Confidence interval analysis
* Feature importance
* Calibration analysis
* Data validation
* Robustness testing
* Privacy audit
* Automated tests
* FastAPI API
* Streamlit dashboard
* Docker deployment
* Docker Compose integration
* Audit logging
* Monitoring report

The next project phase focuses on completing the formal documentation, experiment evidence, architecture diagrams, threat model, model/system card, deployment evidence and final demonstration package.
