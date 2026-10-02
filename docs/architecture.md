\# MDS-02: Architecture and Data Flow



\## 1. System Architecture



The MDS-02 Uplift Modeling Platform is designed as an end-to-end decision-support system for personalized learning intervention allocation.



The architecture is divided into the following layers:



1\. Data Layer

2\. Validation and Processing Layer

3\. Modeling Layer

4\. Evaluation Layer

5\. Recommendation Layer

6\. API Layer

7\. Dashboard Layer

8\. Monitoring and Audit Layer



\---



\## 2. High-Level Architecture



```text

&#x20;                   ┌──────────────────────┐

&#x20;                   │   Learner Dataset    │

&#x20;                   │  learners.csv        │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Data Validation      │

&#x20;                   │ Missing values       │

&#x20;                   │ Schema checks        │

&#x20;                   │ Treatment checks     │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Feature / Data       │

&#x20;                   │ Processing           │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                ┌─────────────┴─────────────┐

&#x20;                ▼                           ▼

&#x20;       ┌─────────────────┐         ┌─────────────────┐

&#x20;       │   T-Learner     │         │   S-Learner     │

&#x20;       │ Treatment Model  │         │ Single Model    │

&#x20;       │ Control Model    │         │ + Treatment     │

&#x20;       └────────┬────────┘         └────────┬────────┘

&#x20;                │                           │

&#x20;                └─────────────┬─────────────┘

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Uplift Estimation    │

&#x20;                   │ Treatment Outcome    │

&#x20;                   │ - Control Outcome    │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;             ┌────────────────────────────────┐

&#x20;             │ Evaluation \& Analysis          │

&#x20;             │                                │

&#x20;             │ Uplift Curve                   │

&#x20;             │ Qini Curve                     │

&#x20;             │ Policy Evaluation              │

&#x20;             │ Confidence Interval            │

&#x20;             │ Subgroup Analysis              │

&#x20;             │ Calibration                    │

&#x20;             └───────────────┬────────────────┘

&#x20;                             │

&#x20;                             ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Recommendation       │

&#x20;                   │ Engine               │

&#x20;                   │                      │

&#x20;                   │ Recommend /          │

&#x20;                   │ No Intervention      │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ FastAPI Prediction   │

&#x20;                   │ Service              │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Streamlit Dashboard  │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Human Review /       │

&#x20;                   │ User Action          │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Audit Logging \&      │

&#x20;                   │ Monitoring            │

&#x20;                   └──────────────────────┘

```



\---



\## 3. Data Flow



The end-to-end data flow is:



\### Step 1: Data Input



The system receives learner-level data from:



`data/learners.csv`



The dataset contains learner characteristics, treatment assignment and outcome.



\---



\### Step 2: Data Validation



Before modeling, the dataset is checked for:



\* Required columns

\* Empty dataset

\* Missing values

\* Valid treatment values

\* Valid data structure



Invalid data is rejected rather than passed directly to the model.



\---



\### Step 3: Data Processing



Relevant learner characteristics are used as model features.



The treatment variable identifies whether the learner belongs to:



\* Control group

\* Treatment group



The outcome variable represents the observed learner outcome.



\---



\### Step 4: Model Training



Two uplift modeling approaches are implemented.



\#### T-Learner



Two separate Random Forest models are trained:



```text

Control Data ──────> Control Model

&#x20;                        │

&#x20;                        ▼

&#x20;                 Predicted Control

&#x20;                      Outcome



Treatment Data ───> Treatment Model

&#x20;                        │

&#x20;                        ▼

&#x20;                 Predicted Treatment

&#x20;                      Outcome

```



The difference between the two predicted outcomes provides the estimated uplift.



\#### S-Learner



A single model uses treatment as an input feature.



The model estimates outcomes under different treatment conditions and derives the estimated uplift.



\---



\## 4. Uplift Calculation



For an individual learner:



```text

Predicted Treatment Outcome

&#x20;             -

Predicted Control Outcome

&#x20;             =

Estimated Uplift

```



For example, if:



```text

Predicted Treatment Outcome = 19.15

Predicted Control Outcome   = 12.90

```



then:



```text

Estimated Uplift = 19.15 - 12.90

&#x20;                = 6.25

```



A positive uplift indicates that the model estimates a higher outcome under treatment than under control.



\---



\## 5. Recommendation Flow



The recommendation engine uses the estimated uplift.



Current threshold:



```text

UPLIFT\_THRESHOLD = 5.0629

```



Decision logic:



```text

Estimated Uplift >= 5.0629

&#x20;            │

&#x20;         YES ──────────> Recommend Intervention

&#x20;            │

&#x20;         NO

&#x20;            │

&#x20;            └──────────> No Intervention

```



This recommendation is intended as decision support and does not automatically determine a learner's intervention.



\---



\## 6. API Architecture



The FastAPI service acts as the application interface between the dashboard and the prediction models.



```text

Streamlit Dashboard

&#x20;       │

&#x20;       │ HTTP POST /predict

&#x20;       ▼

&#x20;  FastAPI Service

&#x20;       │

&#x20;       ▼

&#x20;Prediction Logic

&#x20;       │

&#x20;       ├── Control Prediction

&#x20;       │

&#x20;       ├── Treatment Prediction

&#x20;       │

&#x20;       └── Uplift Calculation

&#x20;               │

&#x20;               ▼

&#x20;       Recommendation Engine

&#x20;               │

&#x20;               ▼

&#x20;         JSON Response

```



The API validates incoming input using Pydantic.



Example input:



```json

{

&#x20; "age": 22,

&#x20; "study\_hours": 6.5,

&#x20; "attendance\_rate": 85,

&#x20; "previous\_score": 65,

&#x20; "assignments\_completed": 8

}

```



Example response structure:



```json

{

&#x20; "predicted\_control": 12.9032,

&#x20; "predicted\_treatment": 19.1506,

&#x20; "estimated\_uplift": 6.2474,

&#x20; "recommendation": "Recommend Intervention",

&#x20; "model\_version": "v1"

}

```



\---



\## 7. Dashboard Architecture



The Streamlit dashboard provides a user-facing interface.



The dashboard contains:



\* Learner input fields

\* Prediction button

\* Predicted control outcome

\* Predicted treatment outcome

\* Estimated uplift

\* Intervention recommendation

\* Recommendation summary

\* Uplift distribution

\* Qini curve



The dashboard communicates with the API rather than directly exposing the model implementation to the user interface.



\---



\## 8. Docker Architecture



The application is deployed using Docker Compose.



Two containers are used:



```text

┌──────────────────────────────┐

│ Docker Compose               │

│                              │

│  ┌────────────────────────┐  │

│  │ API Container          │  │

│  │ FastAPI                │  │

│  │ Port 8000              │  │

│  └────────────┬───────────┘  │

│               │              │

│               │ HTTP         │

│               ▼              │

│  ┌────────────────────────┐  │

│  │ Dashboard Container     │  │

│  │ Streamlit              │  │

│  │ Port 8501              │  │

│  └────────────────────────┘  │

│                              │

└──────────────────────────────┘

```



On the host machine:



```text

API       → http://localhost:8000

Dashboard → http://localhost:8502

```



The host dashboard port is mapped to the Streamlit container port.



\---



\## 9. Monitoring and Audit Architecture



Each prediction request can generate an audit record.



```text

Prediction Request

&#x20;       │

&#x20;       ▼

FastAPI Prediction

&#x20;       │

&#x20;       ├───────────────> Prediction Response

&#x20;       │

&#x20;       ▼

Audit Log

&#x20;       │

&#x20;       ▼

results/audit\_log.jsonl

&#x20;       │

&#x20;       ▼

Monitoring Script

&#x20;       │

&#x20;       ▼

results/monitoring\_report.txt

```



The monitoring process currently tracks:



\* Number of predictions

\* Average estimated uplift

\* Minimum estimated uplift

\* Maximum estimated uplift

\* Number of intervention recommendations

\* Number of non-interventions



\---



\## 10. Security and Failure Handling



The system includes several defensive mechanisms.



\### Input Validation



FastAPI/Pydantic validates input ranges.



Examples:



```text

age: 18–100

study\_hours: 0–24

attendance\_rate: 0–100

previous\_score: 0–100

assignments\_completed: 0–10

```



Invalid values result in an HTTP validation error.



\### Dataset Validation



The data validation layer checks:



\* Missing columns

\* Missing values

\* Empty datasets

\* Invalid treatment values



\### API Error Handling



Internal prediction errors are logged while the API avoids returning internal implementation details to the user.



\---



\## 11. Human-in-the-Loop Architecture



The system is designed for human oversight.



```text

Model Prediction

&#x20;      │

&#x20;      ▼

Recommendation

&#x20;      │

&#x20;      ▼

Human Review

&#x20;      │

&#x20;      ├── Accept / consider intervention

&#x20;      │

&#x20;      └── Do not intervene / investigate further

```



The model does not independently determine the final educational action.



\---



\## 12. Reproducibility



The project maintains a structured repository:



```text

MDS02\_Uplift\_Learning/

│

├── data/

├── src/

├── models/

├── notebooks/

├── results/

├── app/

├── tests/

├── docs/

├── requirements.txt

├── Dockerfile

├── docker-compose.yml

└── .dockerignore

```



The use of a fixed random state, requirements file and Docker configuration supports repeatable execution.



\---



\## 13. Main Components and Responsibilities



| Component                      | Responsibility                    |

| ------------------------------ | --------------------------------- |

| `data/`                        | Dataset storage                   |

| `src/data\_loader.py`           | Dataset loading                   |

| `src/data\_validation.py`       | Dataset validation                |

| `src/baseline\_model.py`        | Baseline model                    |

| `src/t\_learner.py`             | T-Learner implementation          |

| `src/s\_learner.py`             | S-Learner implementation          |

| `src/qini\_evaluation.py`       | Qini evaluation                   |

| `src/uplift\_curve.py`          | Uplift evaluation                 |

| `src/policy\_evaluation.py`     | Policy analysis                   |

| `src/recommendation\_engine.py` | Intervention recommendations      |

| `src/subgroup\_analysis.py`     | Subgroup analysis                 |

| `src/fairness\_analysis.py`     | Recommendation-rate audit         |

| `src/robustness\_check.py`      | Robustness testing                |

| `src/privacy\_audit.py`         | Privacy-oriented audit            |

| `src/monitoring.py`            | Prediction monitoring             |

| `app/main.py`                  | FastAPI service                   |

| `app/dashboard.py`             | Streamlit dashboard               |

| `tests/`                       | Automated tests                   |

| `results/`                     | Experiment and monitoring outputs |

| `docs/`                        | Project documentation             |



\---



\## 14. Architecture Design Principles



The architecture follows these principles:



1\. \*\*Modularity\*\* — modeling, evaluation, API and dashboard are separated.

2\. \*\*Validation first\*\* — invalid data should be detected before modeling.

3\. \*\*Reproducibility\*\* — experiments and deployment should be repeatable.

4\. \*\*Observability\*\* — predictions generate audit information for monitoring.

5\. \*\*Human oversight\*\* — recommendations support rather than replace human decisions.

6\. \*\*Privacy awareness\*\* — simulated data is used and privacy checks are included.

7\. \*\*Failure handling\*\* — invalid inputs and invalid datasets are explicitly tested.

8\. \*\*Separation of concerns\*\* — UI, API and model logic have separate responsibilities.



\---



\## 15. End-to-End System Flow



The complete architecture can therefore be summarized as:



```text

DATA

&#x20; ↓

VALIDATE

&#x20; ↓

PROCESS

&#x20; ↓

TRAIN / LOAD MODELS

&#x20; ↓

ESTIMATE INDIVIDUAL UPLIFT

&#x20; ↓

EVALUATE

&#x20; ├── Qini

&#x20; ├── Uplift Curve

&#x20; ├── Policy Value

&#x20; ├── Confidence Interval

&#x20; ├── Subgroup Analysis

&#x20; └── Calibration

&#x20; ↓

RECOMMENDATION ENGINE

&#x20; ↓

FASTAPI

&#x20; ↓

STREAMLIT DASHBOARD

&#x20; ↓

HUMAN REVIEW

&#x20; ↓

AUDIT LOG

&#x20; ↓

MONITORING

```



This architecture supports the complete workflow required for the MDS-02 capstone, from treatment-control data intake through uplift estimation, recommendation, user interaction and operational monitoring.



