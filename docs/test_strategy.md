\# Test Strategy and Test Results



\## 1. Purpose



This document defines the testing strategy for the MDS-02 Uplift Modeling Platform.



The objective is to verify that the system:



\* Accepts valid data correctly.

\* Rejects invalid data.

\* Produces valid model predictions.

\* Calculates uplift correctly.

\* Provides valid API responses.

\* Handles failure conditions safely.

\* Maintains reproducible behavior.

\* Produces auditable prediction records.



Testing covers data validation, machine learning components, API validation, robustness, privacy-oriented checks and deployment behavior.



\---



\## 2. Testing Levels



The project uses multiple levels of testing:



1\. Unit testing

2\. Data validation testing

3\. Model testing

4\. API testing

5\. Robustness testing

6\. Privacy-oriented testing

7\. Integration testing

8\. Deployment testing

9\. Monitoring validation



\---



\## 3. Test Environment



The project is developed and tested on Windows using Python and Docker.



Main technologies:



\* Python

\* Pytest

\* Pandas

\* NumPy

\* Scikit-learn

\* FastAPI

\* Streamlit

\* Docker

\* Docker Compose



The project uses a fixed random state where applicable to improve reproducibility.



\---



\# 4. Unit Testing



Automated unit tests are maintained under:



`tests/`



The project currently contains automated tests covering core data and application behavior.



Command used:



```text

pytest -q

```



Current result:



```text

4 passed in 0.93s

```



This confirms that the implemented automated test cases completed successfully.



\---



\# 5. Data Validation Testing



The data validation layer checks whether the dataset satisfies the expected contract.



The following conditions are tested:



\* Required columns exist.

\* Dataset is not empty.

\* Treatment contains only valid values.

\* Missing values are detected.

\* Expected dataset structure is maintained.



\---



\## 5.1 Required Column Test



\### Test



Remove one required feature from the dataset.



Example:



```text

study\_hours

```



\### Expected Result



Validation should fail and identify the missing column.



\### Observed Result



```text

Validation failed

Missing columns: \['study\_hours']

```



\### Status



\*\*PASS\*\*



\---



\# 6. Invalid Treatment Test



\### Test



Insert an invalid treatment value:



```text

5

```



Valid treatment values are:



```text

0 = Control

1 = Treatment

```



\### Expected Result



The dataset should be rejected.



\### Observed Result



```text

Validation failed

Invalid treatment values detected

```



\### Status



\*\*PASS\*\*



\---



\# 7. Missing Value Test



\### Test



Introduce a missing value into:



```text

previous\_score

```



\### Expected Result



The validation layer should detect the missing value.



\### Observed Result



```text

Validation failed

Missing values found:

{'previous\_score': 1}

```



\### Status



\*\*PASS\*\*



\---



\# 8. Empty Dataset Test



\### Test



Provide an empty dataset.



\### Expected Result



The validation process should reject the dataset.



\### Observed Result



```text

Validation failed

Dataset is empty

```



\### Status



\*\*PASS\*\*



\---



\# 9. Robustness Test Summary



| Test              | Expected Behavior | Result                  | Status |

| ----------------- | ----------------- | ----------------------- | ------ |

| Missing feature   | Reject dataset    | Missing column detected | PASS   |

| Invalid treatment | Reject dataset    | Invalid value detected  | PASS   |

| Missing value     | Reject dataset    | Missing value detected  | PASS   |

| Empty dataset     | Reject dataset    | Empty dataset detected  | PASS   |



These tests demonstrate that invalid datasets are not silently passed to the modeling pipeline.



\---



\# 10. API Validation Testing



The FastAPI service uses Pydantic validation.



The following input constraints are enforced:



| Field                 | Minimum | Maximum |

| --------------------- | ------: | ------: |

| age                   |      18 |     100 |

| study\_hours           |       0 |      24 |

| attendance\_rate       |       0 |     100 |

| previous\_score        |       0 |     100 |

| assignments\_completed |       0 |      10 |



\---



\## 10.1 Valid API Request



Example:



```json

{

&#x20; "age": 22,

&#x20; "study\_hours": 6.5,

&#x20; "attendance\_rate": 85,

&#x20; "previous\_score": 65,

&#x20; "assignments\_completed": 8

}

```



\### Expected Result



The API should return:



\* Predicted control outcome

\* Predicted treatment outcome

\* Estimated uplift

\* Recommendation

\* Model version



\### Observed Result



```text

Predicted Control: 12.9032

Predicted Treatment: 19.1506

Estimated Uplift: 6.2474

Recommendation: Recommend Intervention

Model Version: v1

```



\### Status



\*\*PASS\*\*



\---



\# 11. Invalid API Request



\### Test



Submit:



```text

attendance\_rate = 150

```



The valid range is:



```text

0–100

```



\### Expected Result



The request should be rejected before model prediction.



\### Observed Result



```text

HTTP 422 Unprocessable Entity

```



The validation response identified the invalid `attendance\_rate` value.



\### Status



\*\*PASS\*\*



\---



\# 12. Model Testing



The uplift modeling system contains:



\* T-Learner

\* S-Learner

\* Random Forest models



Model evaluation uses a held-out test split.



The project evaluates:



\* Mean estimated uplift

\* Observed treatment effect

\* Correlation with simulated true effect

\* Uplift curve

\* Qini area

\* Policy evaluation



\---



\# 13. T-Learner Test Results



Evaluation test set:



```text

600 records

```



Treatment/control distribution:



```text

Control: 302

Treatment: 298

```



Observed treatment effect:



```text

4.0706

```



Mean estimated uplift:



```text

4.2988

```



Estimated uplift standard deviation:



```text

1.1047

```



Estimated uplift range:



```text

1.2987 – 7.5329

```



Correlation between estimated uplift and simulated true effect:



```text

0.4109

```



\### Status



\*\*PASS — model executed and produced valid evaluation outputs\*\*



The metrics are treated as experimental evidence and not as proof of causal effectiveness in real-world learners.



\---



\# 14. S-Learner Test Results



Mean estimated uplift:



```text

4.3112

```



Estimated uplift standard deviation:



```text

1.0923

```



Estimated uplift range:



```text

0.9007 – 7.7199

```



Correlation with simulated true effect:



```text

0.4155

```



\### Status



\*\*PASS — model executed and produced valid evaluation outputs\*\*



The S-Learner result is documented as a comparison experiment rather than an overall model ranking.



\---



\# 15. Qini Evaluation



Qini analysis was performed to evaluate the ordering of learners by estimated uplift.



Current T-Learner Qini area:



```text

58632.65

```



Random reference:



```text

60651.61

```



Difference:



```text

\-2018.96

```



\### Interpretation



The current T-Learner ranking did not exceed the random reference on this evaluation test set.



This is recorded as an important limitation and indicates that further model and feature experimentation may be required.



The result is not interpreted as evidence that uplift modeling cannot work for the problem.



\---



\# 16. Policy Evaluation



The project evaluates different intervention policies.



The policies include:



\* Treat Nobody

\* Treat Top 10%

\* Treat Top 25%

\* Treat Top 50%

\* Treat Everyone



For the current S-Learner policy analysis:



```text

Treat Nobody:   11.1003

Top 10%:        11.7221

Top 25%:        12.5260

Top 50%:        13.6956

Treat Everyone: 15.4116

```



These are model-based policy estimates on the evaluation data.



They should not be interpreted as causal proof or as evidence that one policy is universally preferable.



\---



\# 17. Confidence Interval Test



Observed treatment effect:



```text

4.0706

```



95% confidence interval:



```text

\[3.5367, 4.6045]

```



The interval provides uncertainty information around the observed treatment-control difference.



\### Status



\*\*PASS\*\*



\---



\# 18. Subgroup Testing



Subgroup analysis was performed using previous-score groups.



| Group  | Records | Mean Estimated Uplift |

| ------ | ------: | --------------------: |

| Low    |     178 |                4.1378 |

| Medium |     196 |                4.4651 |

| High   |     226 |                4.3144 |



The analysis demonstrates that estimated uplift varies across groups.



This is useful for error analysis and responsible-AI review.



\---



\# 19. Recommendation-Rate Audit



The recommendation engine uses the uplift threshold:



```text

5.0629

```



Recommendation rates:



| Group  | Recommended | Total |   Rate |

| ------ | ----------: | ----: | -----: |

| Low    |          28 |   178 | 15.73% |

| Medium |          67 |   196 | 34.18% |

| High   |          55 |   226 | 24.34% |



Maximum observed difference:



```text

18.45 percentage points

```



\### Interpretation



This is an audit finding.



A fairness conclusion cannot be made from this single statistic without defining the applicable fairness criterion, context and acceptable threshold.



\---



\# 20. Calibration Testing



The project includes a simulation-based calibration analysis.



The model compares predicted uplift groups with simulated true treatment effects.



Example results:



| Group | Predicted | Simulated True |   Error |

| ----- | --------: | -------------: | ------: |

| Q1    |    2.7913 |         4.0226 | -1.2312 |

| Q2    |    3.7232 |         4.1897 | -0.4665 |

| Q3    |    4.2883 |         4.3070 | -0.0187 |

| Q4    |    4.9101 |         4.3920 |  0.5181 |

| Q5    |    5.8433 |         4.6042 |  1.2390 |



This analysis is simulation-based and should not be treated as real-world calibration validation.



\---



\# 21. Privacy Testing



The project includes an automated privacy-oriented dataset audit.



The audit checks for obvious sensitive or identifying columns.



Current dataset fields:



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



The project uses simulated data.



\### Limitation



The automated audit checks column names and dataset structure. It cannot prove that a dataset contains no privacy risk.



\### Status



\*\*PASS — prototype privacy check completed\*\*



\---



\# 22. Audit Logging Test



Prediction requests are recorded in:



```text

results/audit\_log.jsonl

```



The monitoring system reads these records and calculates:



\* Total predictions

\* Average uplift

\* Minimum uplift

\* Maximum uplift

\* Recommendation counts



Current monitoring snapshot:



```text

Total Predictions: 14

Average Estimated Uplift: 5.7840

Minimum Estimated Uplift: 3.0886

Maximum Estimated Uplift: 6.2474



Recommend Intervention: 11

No Intervention: 3

```



\### Status



\*\*PASS\*\*



\---



\# 23. Docker Integration Testing



The application was deployed using Docker Compose with:



```text

API container

Dashboard container

```



The API was exposed through:



```text

localhost:8000

```



The dashboard was exposed through:



```text

localhost:8502

```



The dashboard successfully communicated with the API using the Docker Compose service name.



\### Status



\*\*PASS\*\*



\---



\# 24. Failure-Mode Testing



The project explicitly tests failure conditions rather than testing only successful inputs.



Tested failure modes include:



\* Missing dataset feature

\* Invalid treatment value

\* Missing dataset value

\* Empty dataset

\* Invalid API range

\* Unexpected prediction failure handling



The system is designed to reject invalid data instead of silently continuing.



\---



\# 25. Test Coverage Matrix



| Component             | Test Type        | Status |

| --------------------- | ---------------- | ------ |

| Data loader           | Functional       | PASS   |

| Data validation       | Unit/robustness  | PASS   |

| Baseline model        | Functional       | PASS   |

| T-Learner             | Model evaluation | PASS   |

| S-Learner             | Model evaluation | PASS   |

| Uplift calculation    | Functional       | PASS   |

| Qini evaluation       | Evaluation       | PASS   |

| Policy evaluation     | Evaluation       | PASS   |

| Recommendation engine | Functional       | PASS   |

| Subgroup analysis     | Analytical       | PASS   |

| API validation        | Integration      | PASS   |

| API prediction        | Integration      | PASS   |

| Audit logging         | Integration      | PASS   |

| Monitoring            | Functional       | PASS   |

| Privacy audit         | Security/privacy | PASS   |

| Docker deployment     | Integration      | PASS   |

| Automated tests       | Pytest           | PASS   |



\---



\# 26. Known Testing Limitations



The following areas require additional testing before real-world deployment:



1\. Load testing has not been completed.

2\. Authentication testing has not been implemented.

3\. Authorization testing has not been implemented.

4\. Dependency vulnerability scanning should be added.

5\. Long-term model drift testing requires future outcome data.

6\. External validation data is not currently available.

7\. Real-world fairness evaluation requires stakeholder-defined criteria.

8\. Adversarial ML testing is not yet comprehensive.



\---



\# 27. Acceptance Criteria



The current prototype satisfies the following acceptance conditions:



\* \[x] Valid data can be processed.

\* \[x] Invalid dataset structures are detected.

\* \[x] Invalid treatment values are rejected.

\* \[x] Missing values are detected.

\* \[x] Empty datasets are rejected.

\* \[x] Invalid API values are rejected.

\* \[x] Valid API predictions are generated.

\* \[x] Uplift is calculated.

\* \[x] Recommendations are generated.

\* \[x] Prediction events are logged.

\* \[x] Monitoring output is generated.

\* \[x] Automated tests pass.

\* \[x] Docker deployment works.

\* \[x] Robustness testing is documented.

\* \[x] Privacy-oriented checks are documented.

\* \[x] Model limitations are documented.



\---



\# 28. Final Test Summary



The current MDS-02 prototype has been tested at data, model, API, robustness, privacy, integration and deployment levels.



The automated Pytest suite currently reports:



```text

4 passed

```



Additional validation and failure-mode experiments successfully detect invalid datasets and invalid API inputs.



The system therefore has documented evidence of functional correctness and failure handling for the implemented prototype.



Further security, scalability, external-validation and real-world fairness testing should be completed before production use.



