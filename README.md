\#  — Uplift Modeling Platform for Personalized Learning Intervention Allocation



\## 1. Project Overview



The \*\* Uplift Modeling Platform\*\* is an end-to-end machine-learning decision-support system designed to identify learners who may have a higher expected benefit from an educational intervention.



The central idea is different from simply predicting which learners are at risk.



A learner may have a low predicted outcome but may not benefit substantially from intervention. Uplift modeling attempts to estimate the difference between the expected outcome under intervention and the expected outcome without intervention.



```text

Estimated Uplift =

Predicted Outcome with Treatment

\-

Predicted Outcome without Treatment

```



The platform combines:



\* Treatment-control data design

\* Feature engineering

\* T-Learner

\* S-Learner

\* Uplift estimation

\* Qini analysis

\* Policy evaluation

\* Subgroup analysis

\* Recommendation engine

\* FastAPI

\* Streamlit

\* Docker Compose

\* Audit logging

\* Monitoring

\* Automated testing

\* Robustness validation

\* Privacy audit

\* Human oversight



\---



\# 2. Problem Statement



Traditional learner-risk prediction focuses mainly on identifying learners who are likely to have poor outcomes.



However:



```text

High Risk ≠ High Expected Intervention Benefit

```



The project therefore investigates whether uplift modeling can provide a more intervention-oriented decision-support signal.



The system estimates:



```text

Potential outcome with intervention

&#x20;             -

Potential outcome without intervention

```



and uses this estimated uplift to generate an intervention recommendation.



\---



\# 3. Project Objectives



The main objectives are:



1\. Design a treatment-control learner dataset.

2\. Perform feature engineering and validation.

3\. Establish a conventional machine-learning baseline.

4\. Implement T-Learner uplift modeling.

5\. Implement S-Learner uplift modeling.

6\. Evaluate uplift using uplift curves and Qini analysis.

7\. Evaluate different intervention policies.

8\. Perform subgroup analysis.

9\. Build an intervention recommendation engine.

10\. Expose predictions through a FastAPI service.

11\. Build an interactive Streamlit dashboard.

12\. Containerize the system using Docker.

13\. Implement prediction audit logging.

14\. Implement operational monitoring.

15\. Perform robustness and privacy checks.

16\. Provide human oversight and responsible-AI documentation.



\---



\# 4. Dataset



The current project uses a \*\*safely simulated learner dataset\*\*.



Dataset size:



```text

3000 learners

8 columns

```



Columns:



```text

learner\_id

age

study\_hours

attendance\_rate

previous\_score

assignments\_completed

treatment

outcome

```



Treatment:



```text

0 = Control

1 = Treatment

```



The dataset was generated programmatically with heterogeneous treatment effects to demonstrate uplift modeling.



No real student records are required for the current prototype.



\---



\# 5. Project Architecture



```text

&#x20;                   Learner Dataset

&#x20;                         |

&#x20;                         v

&#x20;                 Data Validation

&#x20;                         |

&#x20;                         v

&#x20;                 Feature Preparation

&#x20;                         |

&#x20;            +------------+------------+

&#x20;            |                         |

&#x20;            v                         v

&#x20;       T-Learner                 S-Learner

&#x20;            |                         |

&#x20;            +------------+------------+

&#x20;                         |

&#x20;                         v

&#x20;                  Uplift Estimation

&#x20;                         |

&#x20;                         v

&#x20;                  Policy Evaluation

&#x20;                         |

&#x20;                         v

&#x20;               Recommendation Engine

&#x20;                         |

&#x20;             +-----------+-----------+

&#x20;             |                       |

&#x20;             v                       v

&#x20;         FastAPI                Streamlit

&#x20;             |                       |

&#x20;             +-----------+-----------+

&#x20;                         |

&#x20;                         v

&#x20;                Audit + Monitoring

```



Detailed architecture is documented in:



```text

docs/architecture.md

```



\---



\# 6. Technology Stack



| Area                       | Technology               |

| -------------------------- | ------------------------ |

| Language                   | Python                   |

| Data Processing            | Pandas, NumPy            |

| Machine Learning           | Scikit-learn             |

| Uplift Modeling            | T-Learner, S-Learner     |

| API                        | FastAPI                  |

| Dashboard                  | Streamlit                |

| Testing                    | Pytest                   |

| Visualization              | Matplotlib               |

| Containerization           | Docker                   |

| Multi-container Deployment | Docker Compose           |

| Model Serialization        | Joblib                   |

| Monitoring                 | Custom Python monitoring |

| Documentation              | Markdown                 |



\---



\# 7. Project Structure



```text

MDS02\_Uplift\_Learning/

│

├── app/

│   ├── main.py

│   └── dashboard.py

│

├── data/

│   └── learners.csv

│

├── models/

│   └── baseline\_model.joblib

│

├── notebooks/

│

├── results/

│   ├── audit\_log.jsonl

│   ├── monitoring\_report.txt

│   ├── uplift\_curve.png

│   ├── qini\_curve.png

│   └── qini\_curve\_comparison.png

│

├── src/

│   ├── baseline\_model.py

│   ├── calibration\_analysis.py

│   ├── confidence\_interval.py

│   ├── data\_loader.py

│   ├── data\_validation.py

│   ├── fairness\_analysis.py

│   ├── feature\_importance.py

│   ├── monitoring.py

│   ├── privacy\_audit.py

│   ├── qini\_evaluation.py

│   ├── recommendation\_engine.py

│   ├── robustness\_check.py

│   ├── s\_learner.py

│   ├── s\_learner\_qini.py

│   ├── subgroup\_analysis.py

│   ├── subgroup\_recommendation.py

│   ├── t\_learner.py

│   ├── t\_learner\_evaluation.py

│   ├── uplift\_curve.py

│   ├── uplift\_data.py

│   └── \_\_init\_\_.py

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



\---



\# 8. Baseline Results



A simple treatment-control comparison produced:



| Group     | Average Outcome |

| --------- | --------------: |

| Control   |           11.14 |

| Treatment |           15.32 |



Observed difference:



```text

4.18

```



A Random Forest predictive baseline produced:



```text

MSE = 4.5004

```



The baseline provides a reference point before applying uplift modeling.



\---



\# 9. T-Learner



The T-Learner trains separate models for the treatment and control groups.



```text

Treatment Model → Predicted Y(1)



Control Model → Predicted Y(0)



Uplift = Y(1) - Y(0)

```



Evaluation results:



```text

Mean estimated uplift = 4.2988

Observed treatment effect = 4.0706

Standard deviation = 1.1047

Minimum uplift = 1.2987

Maximum uplift = 7.5329

Correlation with simulated true effect = 0.4109

```



\---



\# 10. S-Learner



The S-Learner uses a single model with treatment included as an input feature.



Results:



```text

Mean estimated uplift = 4.3112

Standard deviation = 1.0923

Minimum uplift = 0.9007

Maximum uplift = 7.7199

Correlation with simulated true effect = 0.4155

```



\---



\# 11. Uplift Evaluation



The system evaluates uplift behavior using:



\* Uplift curve

\* Qini curve

\* Qini area

\* Simulated true-effect comparison

\* Policy evaluation

\* Calibration analysis



Current Qini results:



| Evaluation          |    Value |

| ------------------- | -------: |

| T-Learner Qini Area | 58632.65 |

| S-Learner Qini Area | 60035.09 |

| Random Reference    | 60651.61 |



The results are based on the current held-out evaluation split.



The current T-Learner Qini result does not exceed the random reference, which is documented as an important limitation and motivates further experimentation.



\---



\# 12. Policy Evaluation



The platform evaluates different intervention policies.



S-Learner model-based policy values:



| Policy         | Estimated Policy Value |

| -------------- | ---------------------: |

| Treat Nobody   |                11.1003 |

| Treat Top 10%  |                11.7221 |

| Treat Top 25%  |                12.5260 |

| Treat Top 50%  |                13.6956 |

| Treat Everyone |                15.4116 |



These are model-based evaluation values and should not be interpreted as causal proof of real-world intervention effectiveness.



\---



\# 13. Recommendation Engine



The recommendation engine currently uses the S-Learner estimated uplift.



Threshold:



```text

5.0629

```



Decision rule:



```text

Estimated Uplift >= 5.0629

&#x20;       ↓

Recommend Intervention

```



Otherwise:



```text

No Intervention

```



The threshold is currently based on the 75th percentile of the estimated uplift distribution.



\---



\# 14. Subgroup Analysis



Estimated uplift:



| Group  | Records | Mean Estimated Uplift |

| ------ | ------: | --------------------: |

| Low    |     178 |                4.1378 |

| Medium |     196 |                4.4651 |

| High   |     226 |                4.3144 |



Recommendation rates:



| Group  | Recommended | Total |   Rate |

| ------ | ----------: | ----: | -----: |

| Low    |          28 |   178 | 15.73% |

| Medium |          67 |   196 | 34.18% |

| High   |          55 |   226 | 24.34% |



Maximum recommendation-rate difference:



```text

18.45 percentage points

```



This is treated as an audit finding rather than a standalone fairness conclusion.



\---



\# 15. Confidence Interval



Observed treatment effect:



```text

4.0706

```



95% confidence interval:



```text

\[3.5367, 4.6045]

```



This describes uncertainty around the observed treatment-control difference in the current evaluation.



\---



\# 16. Explainability



The platform provides several analysis outputs:



\* Predicted control outcome

\* Predicted treatment outcome

\* Estimated uplift

\* Feature importance

\* Uplift curve

\* Qini curve

\* Subgroup analysis

\* Calibration analysis



Feature importance:



| Feature               | Importance |

| --------------------- | ---------: |

| assignments\_completed |     0.3746 |

| treatment             |     0.2786 |

| previous\_score        |     0.1152 |

| study\_hours           |     0.1068 |

| attendance\_rate       |     0.0838 |

| age                   |     0.0410 |



Feature importance represents predictive model behavior and should not be interpreted as causal importance.



\---



\# 17. Robustness Testing



The system was tested against invalid conditions.



Tested cases:



\* Missing feature

\* Invalid treatment value

\* Missing value

\* Empty dataset

\* Invalid API input



Example:



```text

attendance\_rate = 150

```



produces:



```text

HTTP 422

```



Dataset validation rejects invalid conditions before downstream processing.



\---



\# 18. Automated Testing



Pytest result:



```text

4 passed in 0.93s

```



The test suite provides automated checks for important project functionality.



Additional robustness tests were performed separately.



\---



\# 19. API



The FastAPI service provides:



```text

GET /

POST /predict

```



API URL:



```text

http://localhost:8000

```



Interactive API documentation:



```text

http://localhost:8000/docs

```



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



Example result:



```text

Predicted Control: 12.9032

Predicted Treatment: 19.1506

Estimated Uplift: 6.2474

Recommendation: Recommend Intervention

Model Version: v1

```



\---



\# 20. Streamlit Dashboard



The interactive dashboard provides:



\* Learner input

\* Prediction

\* Estimated uplift

\* Recommendation

\* Recommendation summary

\* Uplift distribution

\* Qini visualization



Dashboard URL:



```text

http://localhost:8502

```



\---



\# 21. Monitoring



Prediction events are stored in:



```text

results/audit\_log.jsonl

```



Monitoring script:



```text

python src\\monitoring.py

```



Monitoring report:



```text

results/monitoring\_report.txt

```



Current monitoring snapshot:



```text

Total Predictions: 14



Average Estimated Uplift: 5.7840

Minimum Estimated Uplift: 3.0886

Maximum Estimated Uplift: 6.2474



Recommend Intervention: 11

No Intervention: 3

```



These values change as new predictions are generated.



\---



\# 22. Docker Deployment



The application is containerized using Docker Compose.



Start:



```cmd

docker compose up -d --build

```



Check:



```cmd

docker ps

```



Stop:



```cmd

docker compose down

```



Services:



```text

API

Dashboard

```



Ports:



```text

API       → 8000

Dashboard → 8502

```



\---



\# 23. Quick Start



\## Step 1 — Navigate to project



```cmd

cd C:\\MDS02\_Uplift\_Learning

```



\## Step 2 — Start Docker



Make sure Docker Desktop is running.



\## Step 3 — Build and start



```cmd

docker compose up -d --build

```



\## Step 4 — Check containers



```cmd

docker ps

```



\## Step 5 — Open API



```text

http://localhost:8000/docs

```



\## Step 6 — Open Dashboard



```text

http://localhost:8502

```



\---



\# 24. Local Development



Activate the virtual environment:



```cmd

venv\\Scripts\\activate

```



Install dependencies:



```cmd

pip install -r requirements.txt

```



Run tests:



```cmd

pytest -q

```



Run monitoring:



```cmd

python src\\monitoring.py

```



Run validation:



```cmd

python src\\data\_validation.py

```



Run robustness checks:



```cmd

python src\\robustness\_check.py

```



Run privacy audit:



```cmd

python src\\privacy\_audit.py

```



\---



\# 25. Documentation



The project documentation is available in:



```text

docs/

```



Important documents:



```text

docs/project\_summary.md

docs/architecture.md

docs/api\_data\_contract.md

docs/threat\_model.md

docs/test\_strategy.md

docs/experiment\_evaluation.md

docs/model\_card.md

docs/system\_card.md

docs/user\_admin\_guide.md

```



These documents cover:



\* Project objectives

\* Architecture

\* Data flow

\* API contract

\* Threat model

\* Testing

\* Experiments

\* Model behavior

\* System behavior

\* User/admin operation



\---



\# 26. Responsible AI



The platform is designed as a decision-support system.



Important principles:



\### Human Oversight



Model recommendations require human review.



\### Privacy



The current dataset is simulated and does not use real student records.



\### Fairness Monitoring



Subgroup recommendation rates are monitored.



\### Explainability



Model outputs and feature-level analyses are available.



\### Transparency



Limitations and evaluation results are documented.



\### Safety



The system should not be used as the sole basis for high-impact educational decisions.



\---



\# 27. Security



The project includes:



\* Input validation

\* Dataset validation

\* Error handling

\* Audit logging

\* Basic privacy audit

\* Threat modeling

\* Docker isolation

\* No secrets committed to source code



Potential production controls include:



\* Authentication

\* Authorization

\* HTTPS

\* Secrets management

\* Dependency scanning

\* Access logging

\* Network restrictions



\---



\# 28. Limitations



The current prototype has several limitations:



1\. The dataset is simulated.

2\. External real-world validation has not been performed.

3\. The main evaluation uses a held-out test split.

4\. Current uplift ranking requires further experimentation.

5\. The current Qini analysis does not establish production-level effectiveness.

6\. Model-based policy values are not causal proof.

7\. Long-term learner outcomes are not modeled.

8\. Intervention cost and capacity constraints are not fully represented.

9\. Production-grade authentication is not yet implemented.

10\. Monitoring is currently basic.



\---



\# 29. Future Work



Potential future improvements include:



\* Real-world or approved benchmark data

\* Repeated cross-validation

\* Hyperparameter optimization

\* Additional uplift algorithms

\* Gradient-boosting uplift models

\* Doubly robust estimation

\* Bootstrap confidence intervals

\* Threshold sensitivity analysis

\* Advanced fairness metrics

\* Temporal validation

\* Drift detection

\* API load testing

\* Authentication and authorization

\* CI/CD

\* Security scanning

\* Production observability



\---



\# 30. Project Acceptance Evidence



The prototype addresses the major capstone requirements through:



| Requirement              | Evidence                             |

| ------------------------ | ------------------------------------ |

| End-to-end system        | API + dashboard + model workflow     |

| Treatment-control design | `data/learners.csv`                  |

| Baseline comparison      | Baseline analysis + Random Forest    |

| Uplift modeling          | T-Learner + S-Learner                |

| Policy evaluation        | Policy evaluation scripts            |

| Subgroup analysis        | Subgroup analysis                    |

| Recommendation system    | Recommendation engine                |

| API                      | FastAPI                              |

| Dashboard                | Streamlit                            |

| Testing                  | Pytest                               |

| Robustness               | Robustness tests                     |

| Security                 | Threat model                         |

| Privacy                  | Privacy audit                        |

| Deployment               | Docker Compose                       |

| Monitoring               | Audit log + monitoring report        |

| Explainability           | Feature importance + uplift analysis |

| Human oversight          | Model/System Card                    |

| Documentation            | `docs/` package                      |



\---



\# 31. Current Project Status



```text

Data Generation              ✓

Data Validation              ✓

Baseline Model               ✓

T-Learner                    ✓

S-Learner                    ✓

Uplift Evaluation            ✓

Qini Evaluation              ✓

Policy Evaluation            ✓

Subgroup Analysis            ✓

Recommendation Engine        ✓

FastAPI                      ✓

Streamlit Dashboard          ✓

Docker Deployment             ✓

Audit Logging                ✓

Monitoring                   ✓

Robustness Testing           ✓

Privacy Audit                ✓

Automated Testing            ✓

Model Card                   ✓

System Card                  ✓

User/Admin Guide             ✓

Experiment Documentation     ✓

```



\---



\# 32. Demo Flow



A short project demonstration can follow this sequence:



```text

1\. Explain the problem

&#x20;       ↓

2\. Show dataset

&#x20;       ↓

3\. Explain treatment vs control

&#x20;       ↓

4\. Explain uplift

&#x20;       ↓

5\. Show model evaluation

&#x20;       ↓

6\. Open FastAPI

&#x20;       ↓

7\. Generate prediction

&#x20;       ↓

8\. Open Streamlit dashboard

&#x20;       ↓

9\. Show uplift/Qini visualization

&#x20;       ↓

10\. Show audit log

&#x20;       ↓

11\. Show monitoring

&#x20;       ↓

12\. Show automated tests

&#x20;       ↓

13\. Explain limitations and human oversight

```



\---



\# 33. Key Project Message



The main contribution of the project is the integration of \*\*uplift/causal-effect-oriented analysis into an end-to-end personalized learning intervention workflow\*\*.



Instead of only asking:



```text

"Which learner is likely to perform poorly?"

```



the system investigates:



```text

"Which learners are estimated to have a larger difference

between intervention and no-intervention outcomes?"

```



This distinction forms the central motivation for the MDS-02 platform.



\---



\# 34. Final Note



This project is a research and prototype implementation.



The current results demonstrate the complete technical workflow from simulated treatment-control data to uplift estimation, recommendation, API deployment, dashboard interaction and monitoring.



The system should not be interpreted as a validated real-world educational intervention system until independent validation, privacy review, security review, fairness assessment and prospective evaluation have been completed.



