\#  Experiment and Evaluation Summary



\## 1. Purpose



This document records the experiments performed for the MDS-02 Uplift Modeling Platform.



The experiments are designed to answer the following questions:



1\. Does the treatment-control dataset contain a measurable outcome difference?

2\. Can uplift models estimate heterogeneous treatment effects?

3\. How well do the models rank learners according to estimated uplift?

4\. How do different intervention policies behave?

5\. Are there meaningful differences across learner subgroups?

6\. What uncertainty and limitations are present in the current results?



The experiments are based on safely simulated learner data.



\---



\# 2. Experimental Dataset



The dataset contains:



```text

3000 learners

8 columns

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



Treatment assignment contains:



```text

0 = Control

1 = Treatment

```



The simulated data was designed to contain heterogeneous treatment effects.



A fixed random state of:



```text

42

```



is used where applicable to improve reproducibility.



\---



\# 3. Experiment 1: Baseline Treatment-Control Analysis



\## Objective



Establish a simple baseline before using individual-level uplift models.



\## Method



The average outcome of the treatment and control groups was compared.



\## Results



| Group     | Average Outcome |

| --------- | --------------: |

| Control   |           11.14 |

| Treatment |           15.32 |



Observed difference:



```text

15.32 - 11.14 = 4.18

```



Therefore, the simple baseline treatment-control difference is approximately:



```text

4.18

```



\## Interpretation



The treatment and control groups show different average outcomes in the simulated dataset.



However, this simple difference does not by itself establish an individual-level causal treatment effect.



It also does not identify which learners are most likely to benefit from intervention.



\---



\# 4. Experiment 2: Random Forest Baseline



\## Objective



Establish a predictive machine-learning baseline.



\## Model



Random Forest Regressor.



Configuration:



```text

n\_estimators = 100

```



Train/test split:



```text

80% training

20% testing

```



\## Result



Test Mean Squared Error:



```text

4.5004

```



\## Purpose



This model provides a conventional predictive baseline against which the uplift-oriented approach can be discussed.



The model predicts outcomes but does not directly estimate individualized treatment effects.



\---



\# 5. Experiment 3: Segment Treatment Effect



\## Objective



Examine whether treatment effects vary across broad learner segments.



Learners were grouped using previous academic score.



Groups:



\* Low

\* Medium

\* High



\## Results



| Segment | Estimated Treatment Effect |

| ------- | -------------------------: |

| Low     |                     4.3536 |

| Medium  |                     4.0004 |

| High    |                     4.2851 |



\## Interpretation



The treatment-control differences vary across the segments.



The differences are relatively small in this analysis, demonstrating why more detailed individual-level uplift modeling is useful for investigating treatment heterogeneity.



\---



\# 6. Experiment 4: T-Learner



\## Objective



Estimate individualized uplift using separate treatment and control models.



\## Method



Two Random Forest models were trained:



```text

Treatment Model

Control Model

```



For each learner:



```text

Estimated Uplift =

Predicted Treatment Outcome

\-

Predicted Control Outcome

```



\---



\## Evaluation Dataset



The held-out evaluation set contains:



```text

600 learners

```



Treatment distribution:



```text

Control = 302

Treatment = 298

```



\---



\## Results



Observed treatment effect:



```text

4.0706

```



Mean estimated uplift:



```text

4.2988

```



Standard deviation:



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



Correlation between estimated uplift and simulated true treatment effect:



```text

0.4109

```



\---



\# 7. T-Learner Uplift Curve



The uplift curve was calculated at different population fractions.



| Population Fraction | Observed Uplift |

| ------------------: | --------------: |

|                 10% |          3.2215 |

|                 20% |          3.4548 |

|                 30% |          3.5932 |

|                 40% |          3.5881 |

|                 50% |          3.7596 |

|                 60% |          4.2486 |

|                 70% |          4.1371 |

|                 80% |          4.0021 |

|                 90% |          3.9761 |

|                100% |          4.0706 |



The curve provides a view of cumulative treatment-effect behavior as increasingly larger portions of the population are considered.



\---



\# 8. Experiment 5: Qini Evaluation



\## Objective



Evaluate the ability of the uplift ranking to prioritize learners according to estimated treatment benefit.



\## T-Learner Result



Qini area:



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



\## Interpretation



On the current held-out test set, the T-Learner Qini area did not exceed the random reference.



This is an important experimental limitation.



It indicates that the current model's ranking of learners by estimated uplift requires further investigation and improvement before being relied upon for operational intervention allocation.



\---



\# 9. Experiment 6: S-Learner



\## Objective



Evaluate an alternative uplift modeling approach.



\## Method



A single Random Forest model was trained with treatment included as an input feature.



Potential outcomes under treatment conditions were used to derive estimated uplift.



\---



\## Results



Mean estimated uplift:



```text

4.3112

```



Standard deviation:



```text

1.0923

```



Minimum:



```text

0.9007

```



Maximum:



```text

7.7199

```



Correlation with simulated true treatment effect:



```text

0.4155

```



\---



\# 10. S-Learner Qini Experiment



S-Learner Qini area:



```text

60035.09

```



T-Learner Qini area:



```text

58632.65

```



Difference:



```text

1402.44

```



\## Interpretation



The S-Learner produced a different Qini-area result from the T-Learner on this evaluation split.



This is reported as an experimental comparison.



No universal model ranking is concluded from this single test split.



Further repeated cross-validation and sensitivity analysis would provide stronger evidence.



\---



\# 11. Experiment 7: True Effect vs Estimated Effect



Because the dataset is simulated, the known simulated treatment effect can be compared with model estimates.



Mean simulated true effect:



```text

4.3031

```



Mean T-Learner estimated uplift:



```text

4.2988

```



Correlation:



```text

0.4109

```



The close mean values indicate that the aggregate simulated effect and average estimated uplift are numerically similar.



However, the correlation shows that individual-level ranking is not perfect.



This distinction is important:



```text

Good aggregate estimate

&#x20;       ≠

Perfect individual ranking

```



\---



\# 12. Experiment 8: Policy Evaluation



Different intervention policies were evaluated.



Policies considered:



\* Treat Nobody

\* Treat Top 10%

\* Treat Top 25%

\* Treat Top 50%

\* Treat Everyone



S-Learner model-based policy values:



| Policy         | Estimated Policy Value |

| -------------- | ---------------------: |

| Treat Nobody   |                11.1003 |

| Treat Top 10%  |                11.7221 |

| Treat Top 25%  |                12.5260 |

| Treat Top 50%  |                13.6956 |

| Treat Everyone |                15.4116 |



These values are model-based estimates on the evaluation data.



They should not be interpreted as causal proof or as a universal recommendation for intervention policy.



\---



\# 13. Experiment 9: Recommendation Threshold



The recommendation engine uses the 75th percentile of estimated S-Learner uplift.



Current threshold:



```text

5.0629

```



Decision rule:



```text

Estimated uplift >= 5.0629

&#x20;       ↓

Recommend Intervention

```



Otherwise:



```text

No Intervention

```



This produces targeted intervention recommendations rather than recommending intervention for every learner.



\---



\# 14. Experiment 10: Subgroup Analysis



Subgroup analysis was performed using previous-score groups.



\## Results



| Group  | Records | Mean Estimated Uplift |

| ------ | ------: | --------------------: |

| Low    |     178 |                4.1378 |

| Medium |     196 |                4.4651 |

| High   |     226 |                4.3144 |



The results indicate that estimated uplift differs across learner subgroups.



This supports the need for subgroup-level analysis when evaluating an intervention allocation model.



\---



\# 15. Experiment 11: Recommendation-Rate Audit



Recommendation rates were calculated for the same subgroups.



| Group  | Recommended | Total |   Rate |

| ------ | ----------: | ----: | -----: |

| Low    |          28 |   178 | 15.73% |

| Medium |          67 |   196 | 34.18% |

| High   |          55 |   226 | 24.34% |



Maximum difference:



```text

18.45 percentage points

```



\## Interpretation



This is an audit finding rather than a fairness verdict.



A formal fairness conclusion requires:



\* A predefined fairness criterion

\* Stakeholder agreement

\* Appropriate statistical uncertainty

\* Context-specific interpretation



\---



\# 16. Experiment 12: Confidence Interval



The observed treatment effect was:



```text

4.0706

```



The 95% confidence interval was:



```text

\[3.5367, 4.6045]

```



The confidence interval provides an estimate of uncertainty around the observed treatment-control difference.



\---



\# 17. Experiment 13: Feature Importance



Random Forest predictive feature importance was analysed.



| Feature               | Importance |

| --------------------- | ---------: |

| assignments\_completed |     0.3746 |

| treatment             |     0.2786 |

| previous\_score        |     0.1152 |

| study\_hours           |     0.1068 |

| attendance\_rate       |     0.0838 |

| age                   |     0.0410 |



\## Interpretation



`assignments\_completed` had the highest predictive importance in the fitted model.



However, feature importance is predictive information.



It does not establish that the feature causally produces the outcome or treatment effect.



\---



\# 18. Experiment 14: Calibration Analysis



A simulation-based calibration analysis compared predicted uplift groups with simulated true effects.



| Group | Predicted Uplift | True Effect |   Error |

| ----- | ---------------: | ----------: | ------: |

| Q1    |           2.7913 |      4.0226 | -1.2312 |

| Q2    |           3.7232 |      4.1897 | -0.4665 |

| Q3    |           4.2883 |      4.3070 | -0.0187 |

| Q4    |           4.9101 |      4.3920 |  0.5181 |

| Q5    |           5.8433 |      4.6042 |  1.2390 |



The results indicate that prediction error varies across uplift groups.



This is a simulation-based diagnostic and should not be considered real-world calibration validation.



\---



\# 19. Experiment 15: Robustness Testing



The system was deliberately tested with invalid inputs.



\## Test Cases



\### Missing Feature



```text

study\_hours

```



Result:



```text

Validation failed

```



\### Invalid Treatment



```text

treatment = 5

```



Result:



```text

Validation failed

```



\### Missing Value



```text

previous\_score = missing

```



Result:



```text

Validation failed

```



\### Empty Dataset



Result:



```text

Validation failed

```



These tests demonstrate that invalid datasets are detected before downstream modeling.



\---



\# 20. Experiment 16: API Validation



A valid learner request successfully produced:



```text

Predicted Control: 12.9032

Predicted Treatment: 19.1506

Estimated Uplift: 6.2474

Recommendation: Recommend Intervention

Model Version: v1

```



An invalid attendance value:



```text

150

```



was rejected with:



```text

HTTP 422 Unprocessable Entity

```



This demonstrates input validation at the API boundary.



\---



\# 21. Experiment 17: Monitoring



Prediction audit records were generated through the deployed API.



Current monitoring snapshot:



```text

Total Predictions: 14



Average Estimated Uplift: 5.7840

Minimum Estimated Uplift: 3.0886

Maximum Estimated Uplift: 6.2474



Recommend Intervention: 11

No Intervention: 3

```



The monitoring report is stored in:



`results/monitoring\_report.txt`



Prediction audit records are stored in:



`results/audit\_log.jsonl`



\---



\# 22. Experiment 18: Deployment



The system was deployed using Docker Compose.



Services:



```text

API

Dashboard

```



API:



```text

http://localhost:8000

```



Dashboard:



```text

http://localhost:8502

```



The dashboard communicates with the API using the Docker Compose service name:



```text

http://api:8000/predict

```



Both services were successfully started using Docker Compose.



\---



\# 23. Overall Experimental Findings



The experiments demonstrate that:



1\. The simulated dataset contains a treatment-control outcome difference.

2\. Individual-level uplift estimates can be generated using T-Learner and S-Learner approaches.

3\. Estimated uplift varies across learners.

4\. The models produce numerically meaningful aggregate uplift estimates.

5\. Individual-level uplift ranking remains imperfect.

6\. The current T-Learner Qini result does not exceed the random reference on the evaluation split.

7\. S-Learner produces a different Qini result on the same evaluation framework.

8\. Subgroup recommendation rates differ and require audit.

9\. The system can produce intervention recommendations.

10\. Invalid datasets and invalid API inputs are detected.

11\. Predictions can be served through an API and dashboard.

12\. Prediction activity can be logged and monitored.



\---



\# 24. Current Limitations



The main experimental limitations are:



\### 1. Simulated Data



The dataset is simulated and therefore does not represent a validated real-world learner population.



\### 2. Qini Performance



The current T-Learner Qini area is below the random reference on the held-out evaluation split.



\### 3. Limited Validation



The experiments use a single main evaluation split.



Repeated cross-validation and sensitivity analysis would provide stronger evidence.



\### 4. Causal Interpretation



The project uses simulated treatment-control data, but model predictions should not automatically be interpreted as causal effects in real-world deployment.



\### 5. Generalization



External validation on an independent educational dataset has not yet been performed.



\### 6. Real Intervention Costs



The current policy analysis does not fully incorporate intervention capacity, financial cost or learner-specific intervention burden.



\### 7. Long-Term Outcomes



Longitudinal learner outcomes are not available in the current simulated dataset.



\---



\# 25. Future Experiments



Future work should include:



1\. Repeated cross-validation.

2\. Multiple random train/test splits.

3\. Hyperparameter optimization.

4\. Additional uplift models.

5\. Gradient-boosting-based uplift models.

6\. Doubly robust estimation.

7\. Bootstrap confidence intervals for uplift metrics.

8\. Sensitivity analysis for recommendation thresholds.

9\. Formal fairness metrics.

10\. External dataset validation.

11\. Temporal validation.

12\. Model drift experiments.

13\. Load testing of the API.

14\. Security testing of the deployed service.



\---



\# 26. Reproducibility



The experiments can be reproduced using the project source code.



Important reproducibility elements include:



\* Fixed random state

\* Structured source files

\* Requirements file

\* Dockerfile

\* Docker Compose configuration

\* Stored experiment results

\* Stored model artifacts

\* Documented evaluation methodology



Experiment outputs are stored under:



`results/`



Model artifacts are stored under:



`models/`



\---



\# 27. Evaluation Conclusion



The current prototype demonstrates a complete experimental workflow for uplift modeling:



```text

Dataset

&#x20;  ↓

Baseline

&#x20;  ↓

Uplift Models

&#x20;  ↓

Individual Uplift

&#x20;  ↓

Qini / Uplift Evaluation

&#x20;  ↓

Policy Evaluation

&#x20;  ↓

Subgroup Analysis

&#x20;  ↓

Recommendation

&#x20;  ↓

API

&#x20;  ↓

Dashboard

&#x20;  ↓

Monitoring

```



The experiments demonstrate technical feasibility of the end-to-end platform while also identifying important limitations in uplift ranking, generalization, fairness assessment and causal interpretation.



The current findings therefore provide a basis for further controlled experimentation rather than a claim of production-ready intervention effectiveness.



