\# Uplift Modeling Platform — Model Card



\## 1. Model Overview



\### Model Name



Personalized Learning Uplift Model



\### Model Version



```text

v1

```



\### Project



\*\*Uplift Modeling Platform for Personalized Learning Intervention Allocation\*\*



\### Model Type



The platform currently implements two uplift modeling approaches:



\* T-Learner

\* S-Learner



The recommendation engine currently uses the \*\*S-Learner estimated uplift\*\*.



\---



\# 2. Intended Purpose



The model is designed to estimate which learners may have a higher expected outcome under an intervention compared with no intervention.



The intended workflow is:



```text

Learner Data

&#x20;    ↓

Treatment / Control Modeling

&#x20;    ↓

Potential Outcome Prediction

&#x20;    ↓

Estimated Uplift

&#x20;    ↓

Recommendation

&#x20;    ↓

Human Review

&#x20;    ↓

Intervention Decision

```



The purpose is to support personalized learning intervention allocation.



The model is a \*\*decision-support system\*\*, not an autonomous decision-maker.



\---



\# 3. Problem Definition



A learner who has a low predicted academic outcome is not necessarily the learner who would benefit most from an intervention.



The platform therefore attempts to estimate:



```text

Uplift =

Expected Outcome with Intervention

\-

Expected Outcome without Intervention

```



A higher estimated uplift indicates a larger predicted difference between the two intervention conditions.



\---



\# 4. Training Dataset



The current project uses a safely simulated learner dataset.



Dataset size:



```text

3000 learners

```



Number of columns:



```text

8

```



Features:



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



The simulated data includes heterogeneous treatment effects so that the project can demonstrate uplift modeling.



\---



\# 5. Data Generation



The dataset was generated programmatically rather than collected from real students.



The simulation includes learner characteristics such as:



\* Age

\* Study hours

\* Attendance

\* Previous score

\* Assignment completion



Treatment effects were simulated to vary according to learner characteristics.



This makes the dataset suitable for demonstrating the technical workflow while avoiding the use of real student personal information.



\---



\# 6. Sensitive and Personal Data



The current dataset does not contain real student records.



An automated privacy audit checks for obvious personal or sensitive columns.



Checked columns include:



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



The current privacy audit found no obvious direct PII columns.



This check is not a guarantee that all possible privacy risks have been eliminated.



\---



\# 7. Model Architecture



\## T-Learner



The T-Learner trains separate models for treatment and control groups.



```text

&#x20;                Learner Features

&#x20;                      |

&#x20;             +--------+--------+

&#x20;             |                 |

&#x20;         Treatment          Control

&#x20;          Model              Model

&#x20;             |                 |

&#x20;       Predicted Y(1)    Predicted Y(0)

&#x20;             |                 |

&#x20;             +--------+--------+

&#x20;                      |

&#x20;                 Difference

&#x20;                      |

&#x20;                Uplift Estimate

```



Formula:



```text

Uplift = Y(1) - Y(0)

```



\---



\## S-Learner



The S-Learner uses one model with treatment as an input feature.



```text

Learner Features + Treatment

&#x20;           ↓

&#x20;      Single Model

&#x20;           ↓

&#x20;  Predict with Treatment = 1

&#x20;           ↓

&#x20;  Predict with Treatment = 0

&#x20;           ↓

&#x20;      Difference

&#x20;           ↓

&#x20;    Uplift Estimate

```



\---



\# 8. Current Recommendation Model



The recommendation engine uses S-Learner estimated uplift.



The current recommendation threshold is:



```text

5.0629

```



Decision rule:



```text

If estimated uplift >= 5.0629:

&#x20;   Recommend Intervention



Otherwise:

&#x20;   No Intervention

```



The threshold corresponds to the 75th percentile of the current estimated uplift distribution.



\---



\# 9. Model Inputs



The prediction API accepts the following learner attributes.



| Input                 | Type    | Valid Range |

| --------------------- | ------- | ----------- |

| age                   | integer | 18–100      |

| study\_hours           | float   | 0–24        |

| attendance\_rate       | float   | 0–100       |

| previous\_score        | float   | 0–100       |

| assignments\_completed | integer | 0–10        |



The treatment condition is handled internally when estimating potential outcomes.



\---



\# 10. Model Outputs



The prediction API returns:



```text

predicted\_control

predicted\_treatment

estimated\_uplift

recommendation

model\_version

```



Example:



```text

Predicted Control:

12.9032



Predicted Treatment:

19.1506



Estimated Uplift:

6.2474



Recommendation:

Recommend Intervention



Model Version:

v1

```



\---



\# 11. Model Performance Summary



\## T-Learner



Mean estimated uplift:



```text

4.2988

```



Observed treatment effect:



```text

4.0706

```



Standard deviation of estimated uplift:



```text

1.1047

```



Minimum estimated uplift:



```text

1.2987

```



Maximum estimated uplift:



```text

7.5329

```



Correlation with simulated true treatment effect:



```text

0.4109

```



\---



\## S-Learner



Mean estimated uplift:



```text

4.3112

```



Standard deviation:



```text

1.0923

```



Minimum estimated uplift:



```text

0.9007

```



Maximum estimated uplift:



```text

7.7199

```



Correlation with simulated true treatment effect:



```text

0.4155

```



\---



\# 12. Qini Evaluation



The Qini metric was used to examine uplift ranking performance.



T-Learner Qini area:



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



S-Learner Qini area:



```text

60035.09

```



Difference between S-Learner and T-Learner:



```text

1402.44

```



These results are based on the current held-out evaluation split.



The results should not be interpreted as proof that one model will perform better on future or real-world datasets.



\---



\# 13. Policy Evaluation



The system evaluates several possible intervention policies.



S-Learner model-based policy values:



| Policy         | Estimated Policy Value |

| -------------- | ---------------------: |

| Treat Nobody   |                11.1003 |

| Treat Top 10%  |                11.7221 |

| Treat Top 25%  |                12.5260 |

| Treat Top 50%  |                13.6956 |

| Treat Everyone |                15.4116 |



These are model-based estimates.



They should not be interpreted as causal proof of real-world intervention effectiveness.



\---



\# 14. Uncertainty



The observed treatment effect is:



```text

4.0706

```



The estimated 95% confidence interval is:



```text

\[3.5367, 4.6045]

```



This interval describes uncertainty around the observed treatment-control difference in the current evaluation.



\---



\# 15. Subgroup Analysis



Estimated uplift was analysed across previous-score groups.



| Group  | Records | Mean Estimated Uplift |

| ------ | ------: | --------------------: |

| Low    |     178 |                4.1378 |

| Medium |     196 |                4.4651 |

| High   |     226 |                4.3144 |



The results show variation in estimated uplift across groups.



\---



\# 16. Recommendation-Rate Audit



Current recommendation rates:



| Group  | Recommended | Total |   Rate |

| ------ | ----------: | ----: | -----: |

| Low    |          28 |   178 | 15.73% |

| Medium |          67 |   196 | 34.18% |

| High   |          55 |   226 | 24.34% |



Maximum observed recommendation-rate difference:



```text

18.45 percentage points

```



This is an audit finding.



It is not by itself a determination of unfairness.



Formal fairness assessment would require predefined criteria, appropriate statistical analysis and stakeholder agreement.



\---



\# 17. Feature Importance



The predictive feature importance results were:



| Feature               | Importance |

| --------------------- | ---------: |

| assignments\_completed |     0.3746 |

| treatment             |     0.2786 |

| previous\_score        |     0.1152 |

| study\_hours           |     0.1068 |

| attendance\_rate       |     0.0838 |

| age                   |     0.0410 |



These values describe predictive model behavior.



They should not be interpreted as causal importance.



\---



\# 18. Calibration Analysis



A simulation-based calibration analysis produced the following results:



| Group | Predicted Uplift | True Effect |   Error |

| ----- | ---------------: | ----------: | ------: |

| Q1    |           2.7913 |      4.0226 | -1.2312 |

| Q2    |           3.7232 |      4.1897 | -0.4665 |

| Q3    |           4.2883 |      4.3070 | -0.0187 |

| Q4    |           4.9101 |      4.3920 |  0.5181 |

| Q5    |           5.8433 |      4.6042 |  1.2390 |



This analysis is based on simulated data and should be treated as a diagnostic rather than real-world calibration validation.



\---



\# 19. Robustness



The platform performs input and dataset validation.



The following failure cases were tested:



\* Missing feature

\* Invalid treatment value

\* Missing value

\* Empty dataset

\* Invalid API input



Example invalid API input:



```text

attendance\_rate = 150

```



Result:



```text

HTTP 422

```



Invalid dataset conditions are rejected before downstream processing.



\---



\# 20. Explainability



The system provides several forms of interpretability:



1\. Estimated individual uplift

2\. Predicted control outcome

3\. Predicted treatment outcome

4\. Feature importance

5\. Uplift curve

6\. Qini curve

7\. Subgroup analysis

8\. Calibration analysis



The explanations are intended to support human review.



They should not be interpreted as proof of causal mechanisms.



\---



\# 21. Human Oversight



The system is designed with human oversight.



The recommendation:



```text

Recommend Intervention

```



should be treated as a decision-support signal.



A human stakeholder should consider additional information before taking action.



The model should not independently make high-impact educational decisions without appropriate review.



\---



\# 22. Known Limitations



\### Simulated Data



The current dataset is simulated and does not establish performance on real educational data.



\### Limited Evaluation



The main evaluation currently uses a held-out test split.



\### Ranking Limitations



The Qini results indicate that individual-level uplift ranking requires further experimentation.



\### Causal Limitations



Model estimates should not automatically be treated as causal effects in a real deployment.



\### External Validation



The system has not yet been validated on an independent real-world educational dataset.



\### Longitudinal Effects



Long-term learner outcomes are not currently modeled.



\### Intervention Cost



The current policy evaluation does not fully model intervention cost or limited staff capacity.



\---



\# 23. Intended Users



Potential users include:



\* Academic advisors

\* Learning-support teams

\* Educational administrators

\* Student-success teams

\* Data science teams



The platform is intended to support these users rather than replace their judgment.



\---



\# 24. Out-of-Scope Uses



The model should not be used as the sole basis for:



\* Student punishment

\* Academic exclusion

\* Scholarship denial

\* Admission decisions

\* Permanent student labeling

\* High-impact decisions without human review



The estimated uplift should be treated as a predictive decision-support signal.



\---



\# 25. Monitoring



Prediction events are logged in:



```text

results/audit\_log.jsonl

```



Monitoring output is stored in:



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



Monitoring should be continued after deployment to detect changes in:



\* Input distributions

\* Estimated uplift distributions

\* Recommendation rates

\* Model performance

\* Subgroup behavior

\* API errors



\---



\# 26. Security and Privacy Considerations



The system includes:



\* API input validation

\* Dataset validation

\* Audit logging

\* Dockerized deployment

\* No secrets stored in source code

\* Basic privacy-column audit

\* Error handling without exposing internal exception details

\* Threat-model documentation



Residual risks include:



\* Unauthorized API access

\* Data poisoning

\* Model manipulation

\* Log manipulation

\* Dependency vulnerabilities

\* Privacy leakage

\* Distribution drift



These risks require continued operational controls in a real deployment.



\---



\# 27. Model Maintenance



The model should be reviewed when:



\* New training data becomes available

\* Input distributions change

\* Recommendation rates change significantly

\* Uplift performance decreases

\* Subgroup differences change materially

\* New intervention strategies are introduced



Any retraining should include:



1\. Data validation

2\. Leakage checks

3\. Reproducible splitting

4\. Baseline comparison

5\. Uplift evaluation

6\. Qini evaluation

7\. Policy evaluation

8\. Subgroup analysis

9\. Robustness testing

10\. Model documentation update



\---



\# 28. Reproducibility



The project includes:



\* Source code

\* Requirements file

\* Dockerfile

\* Docker Compose configuration

\* Stored model artifacts

\* Evaluation results

\* Documentation

\* Automated tests



The project can be reproduced in a clean environment using the documented deployment configuration.



\---



\# 29. Model Card Summary



| Category                     | Current Status                |

| ---------------------------- | ----------------------------- |

| Model type                   | T-Learner + S-Learner         |

| Current recommendation model | S-Learner                     |

| Version                      | v1                            |

| Dataset                      | Simulated learner data        |

| Dataset size                 | 3000                          |

| Recommendation threshold     | 5.0629                        |

| API                          | FastAPI                       |

| Dashboard                    | Streamlit                     |

| Deployment                   | Docker Compose                |

| Monitoring                   | Audit log + monitoring report |

| Testing                      | Automated + robustness tests  |

| Human oversight              | Required                      |

| Real-world validation        | Not yet performed             |



\---



\# 30. Responsible Use Statement



This model is a research and prototype decision-support system.



Its predictions should be interpreted together with contextual information and human judgment.



The current results demonstrate the technical workflow and experimental methodology but do not establish that the system will produce the same performance, fairness characteristics or intervention effects in a real educational environment.



Before real-world deployment, the system would require appropriate stakeholder review, independent validation, privacy assessment, fairness assessment, security review and prospective evaluation.

## Explainability

The system uses model feature importance as a predictive explainability method.

The current feature-importance analysis identifies which input variables contribute most to the model's predictions. It should not be interpreted as evidence of causal importance or as proof that changing a feature will directly change the learner's outcome.

Feature importance results are stored in `results/feature_importance.csv`.

This distinction is important because the platform is designed for uplift-based intervention decisions, where predictive relationships and causal treatment effects are different concepts.

## Error Analysis and Limitations

The uplift model was evaluated by comparing estimated treatment effects with the known treatment-effect structure available in the simulated dataset.

The T-Learner produced an estimated mean uplift of approximately 4.30 points, while the known average treatment effect in the simulated data was approximately 4.30 points.

The correlation between estimated and known treatment effects was approximately 0.41, indicating that the model captures part of the heterogeneous treatment-effect pattern but does not perfectly rank individual learners.

The Qini evaluation also showed that uplift ranking performance can vary on the test split. Therefore, individual intervention recommendations should not be interpreted as certain causal effects.

These results highlight the limitations of the current simulated-data experiment and support the need for validation on real treatment-control data before operational use.