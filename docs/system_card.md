\# Uplift Modeling Platform — System Card



\## 1. System Overview



\### System Name



\*\*Uplift Modeling Platform for Personalized Learning Intervention Allocation\*\*



\### System Version



```text id="v6m2qa"

v1.0

```



\### System Type



End-to-end machine-learning decision-support platform.



The system combines:



\* Simulated learner data

\* Treatment-control analysis

\* Uplift modeling

\* Policy evaluation

\* Subgroup analysis

\* Recommendation generation

\* REST API

\* Interactive dashboard

\* Audit logging

\* Prediction monitoring

\* Docker-based deployment



\---



\# 2. System Objective



The primary objective is to identify learners who are estimated to have a larger benefit from an educational intervention.



The system focuses on the difference between:



```text id="w7j4pr"

Expected outcome with intervention

\-

Expected outcome without intervention

```



This differs from simply identifying learners with low predicted performance.



A learner with a low predicted outcome is not necessarily a learner who is expected to benefit most from intervention.



\---



\# 3. Intended Users



Potential system users include:



\* Academic advisors

\* Student-support teams

\* Learning coordinators

\* Educational administrators

\* Data science teams



The system is designed to support human decision-making.



\---



\# 4. High-Level Architecture



```text id="8q2k1m"

&#x20;                +----------------------+

&#x20;                |   Learner Dataset    |

&#x20;                +----------+-----------+

&#x20;                           |

&#x20;                           v

&#x20;                +----------------------+

&#x20;                | Data Validation      |

&#x20;                +----------+-----------+

&#x20;                           |

&#x20;                           v

&#x20;                +----------------------+

&#x20;                | Feature Processing   |

&#x20;                +----------+-----------+

&#x20;                           |

&#x20;                           v

&#x20;             +-------------+-------------+

&#x20;             |                           |

&#x20;             v                           v

&#x20;     +---------------+           +---------------+

&#x20;     |  T-Learner    |           |  S-Learner    |

&#x20;     +-------+-------+           +-------+-------+

&#x20;             |                           |

&#x20;             +-------------+-------------+

&#x20;                           |

&#x20;                           v

&#x20;                +----------------------+

&#x20;                | Uplift Estimation    |

&#x20;                +----------+-----------+

&#x20;                           |

&#x20;                           v

&#x20;                +----------------------+

&#x20;                | Policy Evaluation    |

&#x20;                +----------+-----------+

&#x20;                           |

&#x20;                           v

&#x20;                +----------------------+

&#x20;                | Recommendation       |

&#x20;                | Engine                |

&#x20;                +----------+-----------+

&#x20;                           |

&#x20;               +-----------+-----------+

&#x20;               |                       |

&#x20;               v                       v

&#x20;       +---------------+       +---------------+

&#x20;       | FastAPI       |       | Streamlit     |

&#x20;       | Prediction    |       | Dashboard     |

&#x20;       +-------+-------+       +-------+-------+

&#x20;               |                       |

&#x20;               +-----------+-----------+

&#x20;                           |

&#x20;                           v

&#x20;                +----------------------+

&#x20;                | Audit Logging        |

&#x20;                | \& Monitoring         |

&#x20;                +----------------------+

```



\---



\# 5. Main System Components



\## 5.1 Data Generation



File:



```text id="p6fr3y"

src/generate\_data.py

```



Generates the simulated learner dataset.



Output:



```text id="7k8bpa"

data/learners.csv

```



\---



\## 5.2 Data Loading



File:



```text id="w4kz7m"

src/data\_loader.py

```



Responsible for loading learner data for downstream processing.



\---



\## 5.3 Data Validation



File:



```text id="3m0x9q"

src/data\_validation.py

```



Checks:



\* Required columns

\* Empty dataset

\* Missing values

\* Treatment values

\* Dataset structure



\---



\## 5.4 Baseline Model



File:



```text id="v5d7n2"

src/baseline\_model.py

```



Uses Random Forest Regression as a conventional predictive baseline.



Result:



```text id="k4w9zp"

MSE = 4.5004

```



\---



\## 5.5 T-Learner



Files:



```text id="n6q2yc"

src/t\_learner.py

src/t\_learner\_evaluation.py

```



Uses separate models for treatment and control outcomes.



\---



\## 5.6 S-Learner



Files:



```text id="q3p8zr"

src/s\_learner.py

src/s\_learner\_qini.py

```



Uses a single model with treatment included as an input variable.



\---



\## 5.7 Recommendation Engine



File:



```text id="a7v2kd"

src/recommendation\_engine.py

```



Uses the current S-Learner uplift estimate.



Threshold:



```text id="z4m6tx"

5.0629

```



Decision:



```text id="j1s8bw"

Uplift >= 5.0629

&#x20;       ↓

Recommend Intervention

```



\---



\# 6. API Layer



The API is implemented using FastAPI.



File:



```text id="k2f9qm"

app/main.py

```



The API provides:



```text id="x7b3nv"

GET /

POST /predict

```



\---



\## 6.1 Root Endpoint



Endpoint:



```text id="p9z2fw"

GET /

```



Purpose:



Health/status check for the service.



\---



\## 6.2 Prediction Endpoint



Endpoint:



```text id="r6c4ya"

POST /predict

```



The endpoint accepts learner attributes and returns predicted control outcome, predicted treatment outcome, uplift and recommendation.



\---



\# 7. API Data Flow



```text id="n3h8qs"

Client

&#x20; |

&#x20; v

FastAPI

&#x20; |

&#x20; v

Input Validation

&#x20; |

&#x20; v

Feature Preparation

&#x20; |

&#x20; v

Treatment Prediction

&#x20; |

&#x20; v

Control Prediction

&#x20; |

&#x20; v

Uplift Calculation

&#x20; |

&#x20; v

Recommendation Threshold

&#x20; |

&#x20; v

Audit Log

&#x20; |

&#x20; v

API Response

```



\---



\# 8. Input Validation



The API validates:



\* Age

\* Study hours

\* Attendance rate

\* Previous score

\* Assignment completion



Example constraints:



```text id="g2f7km"

age: 18–100

study\_hours: 0–24

attendance\_rate: 0–100

previous\_score: 0–100

assignments\_completed: 0–10

```



Invalid values are rejected using HTTP validation responses.



Example:



```text id="t9q5cx"

attendance\_rate = 150

```



Result:



```text id="n1r7vh"

HTTP 422

```



\---



\# 9. Dashboard



The dashboard is implemented using Streamlit.



File:



```text id="c8x4sm"

app/dashboard.py

```



Dashboard functionality includes:



\* Learner input

\* API prediction

\* Predicted control outcome

\* Predicted treatment outcome

\* Estimated uplift

\* Intervention recommendation

\* Recommendation summary

\* Uplift distribution

\* Qini curve



\---



\# 10. Dashboard Architecture



```text id="s5j2kd"

User

&#x20; |

&#x20; v

Streamlit Dashboard

&#x20; |

&#x20; | HTTP Request

&#x20; v

FastAPI

&#x20; |

&#x20; v

Uplift Model

&#x20; |

&#x20; v

Prediction

&#x20; |

&#x20; v

FastAPI Response

&#x20; |

&#x20; v

Streamlit Display

```



Inside Docker Compose, the dashboard communicates with:



```text id="q9b4mw"

http://api:8000/predict

```



\---



\# 11. Deployment Architecture



The platform uses Docker Compose.



Services:



```text id="w3k8xp"

API Container

Dashboard Container

```



\## API



Container:



```text id="z7v2hr"

mds02-uplift-api

```



Host port:



```text id="m6q4ws"

8000

```



\## Dashboard



Container:



```text id="f4y8nk"

mds02-uplift-dashboard

```



Host port:



```text id="d2c7vz"

8502

```



\---



\# 12. Docker Architecture



```text id="h5r3qa"

&#x20;                Docker Compose

&#x20;                     |

&#x20;            +--------+--------+

&#x20;            |                 |

&#x20;            v                 v

&#x20;      +-----------+     +-----------+

&#x20;      | API       |     | Dashboard |

&#x20;      | FastAPI   |     | Streamlit |

&#x20;      +-----+-----+     +-----+-----+

&#x20;            |                 |

&#x20;            +--------+--------+

&#x20;                     |

&#x20;                     v

&#x20;               Project Files

&#x20;                     |

&#x20;                     v

&#x20;             Results / Models

```



The API service also mounts the host `results` directory so that prediction audit logs remain available outside the container.



\---



\# 13. Audit Logging



Prediction requests are recorded in:



```text id="r2m6fv"

results/audit\_log.jsonl

```



Each prediction can include information such as:



\* Input learner attributes

\* Estimated uplift

\* Recommendation

\* Model version

\* Timestamp



Audit logging provides traceability for prediction activity.



\---



\# 14. Monitoring



Monitoring script:



```text id="v8c1px"

src/monitoring.py

```



Current monitored metrics include:



\* Total predictions

\* Average estimated uplift

\* Minimum estimated uplift

\* Maximum estimated uplift

\* Number of recommendations

\* Number of non-recommendations



Current snapshot:



```text id="k6d9rx"

Total Predictions: 14

Average Estimated Uplift: 5.7840

Minimum Estimated Uplift: 3.0886

Maximum Estimated Uplift: 6.2474

Recommend Intervention: 11

No Intervention: 3

```



Report:



```text id="q7n4mz"

results/monitoring\_report.txt

```



\---



\# 15. Model Evaluation



The system includes several evaluation methods.



\## Baseline



Treatment-control difference:



```text id="p5y2vk"

4.18

```



Random Forest baseline:



```text id="x9c6qs"

MSE = 4.5004

```



\## T-Learner



Mean estimated uplift:



```text id="w8m3zr"

4.2988

```



\## S-Learner



Mean estimated uplift:



```text id="b2k7fv"

4.3112

```



\## Qini



T-Learner:



```text id="d6p4yx"

58632.65

```



S-Learner:



```text id="n8w5cq"

60035.09

```



Random reference:



```text id="s4j9mp"

60651.61

```



These results are based on the current evaluation split.



\---



\# 16. Subgroup Monitoring



The system evaluates estimated uplift and recommendation rates across learner groups.



Current recommendation rates:



```text id="a9q2kc"

Low:    15.73%

Medium: 34.18%

High:   24.34%

```



Maximum difference:



```text id="h3m7vz"

18.45 percentage points

```



These differences are monitored as an audit signal.



They do not automatically establish a fairness violation.



\---



\# 17. Security Architecture



Security controls include:



\* API input validation

\* Dataset validation

\* Error handling

\* Audit logging

\* No secrets committed to source code

\* Docker isolation

\* Threat-model documentation

\* Basic privacy audit

\* Dependency-based deployment



The system also considers:



\* Unauthorized access

\* Input manipulation

\* Data poisoning

\* Model manipulation

\* Log tampering

\* API abuse

\* Denial-of-service risk

\* Privacy leakage

\* Dependency vulnerabilities



\---



\# 18. Threat Boundaries



Important trust boundaries are:



```text id="u6p4qa"

User

&#x20; |

&#x20; | Untrusted Input

&#x20; v

API

&#x20; |

&#x20; | Validated Input

&#x20; v

Model

&#x20; |

&#x20; v

Prediction

&#x20; |

&#x20; v

Audit Log

```



The API boundary is therefore an important security control point.



\---



\# 19. Failure Handling



The system handles several failure conditions.



\### Invalid API Input



Rejected using validation.



\### Missing Dataset Columns



Validation reports missing columns.



\### Missing Values



Validation reports affected columns.



\### Invalid Treatment Values



Validation rejects unexpected treatment values.



\### Empty Dataset



Validation rejects the dataset.



\### Internal API Error



The API logs internal details while avoiding unnecessary exposure of internal exception information to the client.



\---



\# 20. Privacy Design



The current project uses simulated learner records.



No real student dataset is required for the prototype.



Privacy controls include:



\* Avoiding real student identifiers

\* Basic automated privacy audit

\* Limited input attributes

\* Audit logging

\* Documentation of privacy limitations



A production system would require stronger controls such as:



\* Authentication

\* Authorization

\* Encryption

\* Data retention policies

\* Access logging

\* Formal privacy impact assessment



\---



\# 21. Human-in-the-Loop Design



The platform does not directly execute an intervention.



Instead:



```text id="b8r5qs"

Model Prediction

&#x20;     ↓

Recommendation

&#x20;     ↓

Human Review

&#x20;     ↓

Contextual Decision

&#x20;     ↓

Possible Intervention

```



The human reviewer can consider information that is not available to the model.



This reduces the risk of treating a model recommendation as an automatic decision.



\---



\# 22. Responsible AI Considerations



Important responsible-AI considerations include:



\### Fairness



Subgroup recommendation rates are monitored.



\### Transparency



The system exposes model outputs and evaluation metrics.



\### Human Oversight



Recommendations require human review.



\### Privacy



The current dataset is simulated and does not contain real student records.



\### Explainability



Feature importance and uplift-related analyses are available.



\### Error Analysis



Qini evaluation, calibration analysis and subgroup analysis are performed.



\### Limitations



The system documents its simulation, ranking and generalization limitations.



\---



\# 23. Data Leakage Prevention



The evaluation workflow separates training and testing data.



The uplift evaluation uses a held-out test set.



The project also explicitly considers leakage as a threat in the threat model.



Future real-world deployment should additionally verify:



\* Temporal leakage

\* Post-treatment features

\* Duplicate learners

\* Cross-period contamination

\* Label leakage



\---



\# 24. Reproducibility



The system includes:



```text id="c4m8yz"

Source Code

Requirements

Dockerfile

Docker Compose

Model Artifacts

Dataset Generator

Evaluation Scripts

Automated Tests

Documentation

```



The fixed random state:



```text id="z5n2hr"

42

```



is used for reproducibility where applicable.



\---



\# 25. Automated Testing



The project uses pytest.



Current result:



```text id="q8v3mx"

4 passed in 0.93s

```



Tests cover important functionality such as:



\* Data validation

\* Recommendation logic

\* Core system behavior



Additional robustness tests were executed separately.



\---



\# 26. Robustness Testing



The following failure cases were tested:



| Test              | Expected Result    |

| ----------------- | ------------------ |

| Missing feature   | Validation failure |

| Invalid treatment | Validation failure |

| Missing value     | Validation failure |

| Empty dataset     | Validation failure |

| Invalid API range | HTTP 422           |



All tested invalid cases produced the expected validation behavior.



\---



\# 27. Operational Workflow



The complete system workflow is:



```text id="m7c5rx"

1\. Data Intake

&#x20;      ↓

2\. Data Validation

&#x20;      ↓

3\. Feature Preparation

&#x20;      ↓

4\. Model Training

&#x20;      ↓

5\. Uplift Estimation

&#x20;      ↓

6\. Model Evaluation

&#x20;      ↓

7\. Policy Evaluation

&#x20;      ↓

8\. Recommendation Generation

&#x20;      ↓

9\. API Deployment

&#x20;      ↓

10\. Dashboard Interaction

&#x20;      ↓

11\. Audit Logging

&#x20;      ↓

12\. Monitoring

&#x20;      ↓

13\. Human Review

```



\---



\# 28. Current System Status



| Component              | Status           |

| ---------------------- | ---------------- |

| Simulated dataset      | Complete         |

| Baseline analysis      | Complete         |

| Random Forest baseline | Complete         |

| T-Learner              | Complete         |

| S-Learner              | Complete         |

| Uplift evaluation      | Complete         |

| Qini analysis          | Complete         |

| Policy evaluation      | Complete         |

| Subgroup analysis      | Complete         |

| Recommendation engine  | Complete         |

| API                    | Complete         |

| Dashboard              | Complete         |

| Docker deployment      | Complete         |

| Audit logging          | Complete         |

| Monitoring             | Complete         |

| Robustness testing     | Complete         |

| Privacy audit          | Complete         |

| Model Card             | Complete         |

| System Card            | Current document |



\---



\# 29. Known Limitations



The current system has several limitations.



\### Simulated Dataset



The system has not yet been validated on real learner intervention data.



\### Limited Evaluation Splits



The primary evaluation is based on a held-out test split.



\### Uplift Ranking



The current Qini analysis shows that the T-Learner result is below the random reference on the evaluation split.



\### Causal Interpretation



Predicted uplift should not automatically be interpreted as a confirmed causal effect in a real-world environment.



\### Production Security



The prototype does not yet implement full enterprise authentication and authorization.



\### Monitoring



Current monitoring is basic and does not yet include complete production-grade drift detection.



\---



\# 30. Future System Improvements



Planned improvements include:



1\. Real-world or approved benchmark dataset evaluation

2\. Cross-validation

3\. Hyperparameter optimization

4\. Additional uplift algorithms

5\. Causal inference methods

6\. Advanced fairness metrics

7\. Model drift detection

8\. API authentication

9\. Role-based access control

10\. CI/CD pipeline

11\. Dependency vulnerability scanning

12\. Load testing

13\. Production-grade observability

14\. Intervention-cost-aware policy optimization



\---



\# 31. System-Level Acceptance Criteria



The prototype satisfies the following major requirements:



\* End-to-end working workflow

\* Treatment-control data design

\* Uplift modeling

\* Baseline comparison

\* Qini/uplift evaluation

\* Policy evaluation

\* Subgroup analysis

\* Recommendation dashboard

\* API/data validation

\* Automated tests

\* Robustness testing

\* Privacy audit

\* Security/threat analysis

\* Docker deployment

\* Audit logging

\* Monitoring

\* Human oversight

\* Model documentation

\* System documentation



The remaining improvements are primarily focused on stronger validation, production hardening and real-world experimentation.



\---



\# 32. System Card Summary



The MDS-02 Uplift Modeling Platform is an end-to-end prototype for personalized learning intervention allocation.



It combines machine learning, uplift modeling, policy analysis, API deployment, dashboard visualization and operational monitoring.



The system is explicitly designed as a \*\*decision-support platform with human oversight\*\*.



The current experimental results demonstrate technical feasibility while also identifying limitations in uplift ranking, generalization, fairness assessment and causal interpretation.



Further validation is required before any real-world educational deployment.



