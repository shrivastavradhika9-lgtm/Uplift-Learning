\#: Threat Model and Security \& Misuse Analysis



\## 1. Purpose



This document identifies potential security, privacy, reliability and misuse risks associated with the Uplift Modeling Platform.



The platform processes learner information, estimates intervention uplift and produces intervention recommendations.



The threat analysis focuses on protecting:



\* Learner data

\* Prediction integrity

\* API availability

\* Audit information

\* Model behavior

\* Recommendation workflow



\---



\## 2. System Assets



The main assets requiring protection are:



| Asset              | Description                              |

| ------------------ | ---------------------------------------- |

| Learner Dataset    | Input learner information                |

| Trained Models     | T-Learner and S-Learner model artifacts  |

| Prediction API     | FastAPI service                          |

| Dashboard          | Streamlit user interface                 |

| Audit Logs         | Prediction and operational records       |

| Configuration      | Model threshold and application settings |

| Source Code        | Application and ML implementation        |

| Evaluation Results | Uplift, Qini and analysis outputs        |



\---



\## 3. Trust Boundaries



The system contains several trust boundaries.



```text

External User

&#x20;    │

&#x20;    │ Untrusted Input

&#x20;    ▼

Streamlit Dashboard

&#x20;    │

&#x20;    ▼

FastAPI API

&#x20;    │

&#x20;    ▼

Validation Layer

&#x20;    │

&#x20;    ▼

Prediction Models

&#x20;    │

&#x20;    ▼

Audit Logging

```



The main boundary is between user-provided input and the prediction service.



All externally supplied prediction values should be treated as untrusted until validated.



\---



\## 4. Threat Categories



The main threat categories considered are:



1\. Invalid input

2\. Data poisoning

3\. Model manipulation

4\. Unauthorized access

5\. Privacy leakage

6\. Audit-log manipulation

7\. API abuse

8\. Denial of service

9\. Recommendation misuse

10\. Model drift

11\. Data leakage

12\. Dependency vulnerabilities



\---



\## 5. Threat: Invalid Input



\### Description



A user may send values outside the expected ranges.



Examples:



\* Attendance above 100

\* Negative study hours

\* Invalid age

\* Invalid assignment count



\### Potential Impact



Invalid inputs may produce incorrect predictions or cause application errors.



\### Existing Mitigation



FastAPI/Pydantic validation checks input ranges before prediction.



\### Test Evidence



An attendance value of `150` was rejected with HTTP `422 Unprocessable Entity`.



\### Future Improvement



Add automated API fuzz testing and additional schema-level validation.



\---



\## 6. Threat: Malicious or Corrupted Dataset



\### Description



A corrupted or manipulated dataset could contain:



\* Missing columns

\* Invalid treatment values

\* Missing values

\* Incorrect records

\* Unexpected data types



\### Potential Impact



The model could be trained using invalid data.



\### Existing Mitigation



The project contains automated dataset validation.



The robustness tests successfully detect:



\* Missing `study\_hours`

\* Invalid treatment value

\* Missing `previous\_score`

\* Empty dataset



\### Future Improvement



Add dataset checksums, data-version tracking and automated data-quality monitoring.



\---



\## 7. Threat: Data Poisoning



\### Description



An attacker or faulty upstream process could intentionally or unintentionally modify training data.



\### Potential Impact



Model behavior and estimated uplift could be affected.



\### Mitigation



Recommended controls include:



\* Version-controlled datasets

\* Dataset validation

\* Training-data review

\* Data-quality monitoring

\* Reproducible training

\* Experiment tracking



\### Current Status



The current prototype includes validation and reproducibility controls.



Production-grade dataset signing and version tracking remain future improvements.



\---



\## 8. Threat: Model Manipulation



\### Description



An unauthorized user could replace or modify a trained model artifact.



\### Potential Impact



The API could produce incorrect predictions or recommendations.



\### Existing Mitigation



Model files are stored separately from application source code.



\### Future Improvement



Production deployment should include:



\* Model artifact versioning

\* Model integrity checks

\* Restricted filesystem access

\* Signed model artifacts

\* Controlled model promotion



\---



\## 9. Threat: Unauthorized API Access



\### Description



An unauthorized user could access the prediction endpoint.



\### Potential Impact



This could expose prediction functionality or create excessive prediction requests.



\### Current Status



The prototype does not implement production authentication and authorization.



\### Future Controls



A production implementation should include:



\* Authentication

\* Role-based authorization

\* API keys or OAuth

\* HTTPS/TLS

\* Rate limiting

\* Access logging



\---



\## 10. Threat: Privacy Leakage



\### Description



Learner information could accidentally be exposed through:



\* API responses

\* Logs

\* Error messages

\* Dashboard output

\* Dataset files



\### Potential Impact



Sensitive educational information could be disclosed.



\### Existing Mitigation



The project uses simulated learner data.



The privacy audit performs an automated check for obvious identifier/sensitive-looking columns.



The API avoids exposing internal implementation details during unexpected failures.



\### Limitation



The privacy audit is a column-level automated check and is not a complete privacy assessment.



\### Future Improvement



If real learner data is used:



\* Minimize collected information.

\* Apply access control.

\* Encrypt sensitive data.

\* Define retention policies.

\* Review logs for accidental disclosure.

\* Apply appropriate institutional privacy requirements.



\---



\## 11. Threat: Audit Log Manipulation



\### Description



An attacker with filesystem access could modify prediction audit records.



\### Potential Impact



Monitoring and traceability could become unreliable.



\### Current Mitigation



Prediction records are stored separately in:



`results/audit\_log.jsonl`



\### Future Improvement



Production systems should use:



\* Append-only logging

\* Centralized log management

\* Restricted write permissions

\* Log integrity checks

\* Timestamp validation



\---



\## 12. Threat: API Abuse



\### Description



An attacker could send a large number of prediction requests.



\### Potential Impact



Possible consequences include:



\* Excessive resource consumption

\* Increased latency

\* Service unavailability

\* Excessive log generation



\### Current Status



The prototype does not implement rate limiting.



\### Future Improvement



Add:



\* Rate limiting

\* Request quotas

\* Authentication

\* Monitoring alerts

\* Reverse proxy controls



\---



\## 13. Threat: Denial of Service



\### Description



Large or repeated requests could consume API resources.



\### Existing Mitigation



Input validation limits individual numeric values.



\### Future Improvement



Production deployment should add:



\* Request-size limits

\* Rate limiting

\* Container resource limits

\* Health checks

\* Autoscaling where appropriate



\---



\## 14. Threat: Recommendation Misuse



\### Description



A user could treat the model recommendation as an automatic decision rather than a decision-support signal.



\### Potential Impact



A learner could receive or be denied an intervention based solely on an imperfect model estimate.



\### Existing Mitigation



The system is explicitly designed with human oversight.



The recommendation engine produces:



\* Recommend Intervention

\* No Intervention



These are model outputs rather than automatic final decisions.



\### Future Improvement



The dashboard should clearly display:



> Model recommendation — human review required.



\---



\## 15. Threat: Model Bias or Unequal Recommendations



\### Description



The model may produce different recommendation rates across learner subgroups.



\### Observed Audit Finding



Recommendation rates were:



| Group                 | Recommendation Rate |

| --------------------- | ------------------: |

| Low previous score    |              15.73% |

| Medium previous score |              34.18% |

| High previous score   |              24.34% |



Maximum observed difference:



`18.45 percentage points`



\### Interpretation



This difference is an audit finding requiring investigation.



It does not by itself establish whether the system satisfies a particular fairness criterion.



\### Future Improvement



Perform:



\* Predefined fairness metric evaluation

\* Confidence intervals

\* Additional subgroup definitions

\* Error analysis

\* Stakeholder review

\* Threshold sensitivity analysis



\---



\## 16. Threat: Data Leakage



\### Description



Information from the evaluation set could accidentally influence training.



\### Potential Impact



Evaluation metrics could become overly optimistic.



\### Existing Mitigation



The project uses separate training and evaluation splits for uplift modeling.



Evaluation metrics are calculated on the held-out test split.



\### Future Improvement



Add automated checks for:



\* Duplicate records across splits

\* Feature leakage

\* Temporal leakage

\* Treatment leakage

\* Target leakage



\---



\## 17. Threat: Model Drift



\### Description



Learner behavior or intervention effectiveness may change over time.



\### Potential Impact



A model trained on historical data may become less reliable.



\### Existing Monitoring



The system tracks prediction activity and estimated uplift statistics.



\### Future Improvement



Add monitoring for:



\* Feature distribution drift

\* Prediction drift

\* Treatment-effect drift

\* Recommendation-rate drift

\* Performance degradation when outcome labels become available



\---



\## 18. Threat: Dependency Vulnerabilities



\### Description



Third-party Python packages may contain security vulnerabilities.



\### Current Dependencies



The application uses packages including:



\* FastAPI

\* Pandas

\* NumPy

\* Scikit-learn

\* Joblib

\* Streamlit

\* Requests

\* Matplotlib



\### Future Improvement



Add automated dependency scanning to CI/CD.



Recommended checks include:



\* Dependency vulnerability scanning

\* Version pinning

\* Regular updates

\* Removal of unnecessary packages



\---



\## 19. Misuse Scenarios



\### Misuse Scenario 1: Automatic Intervention



A user treats `Recommend Intervention` as a mandatory decision.



\*\*Risk:\*\* Human judgment and contextual information are ignored.



\*\*Control:\*\* Clearly define the model as decision support and require human review.



\---



\### Misuse Scenario 2: Using Uplift as a Learner Score



A user interprets uplift as a measure of learner ability.



\*\*Risk:\*\* Uplift is not an overall learner-performance score.



\*\*Control:\*\* Explain that uplift estimates the difference between treatment and control outcomes.



\---



\### Misuse Scenario 3: Treating Feature Importance as Causality



A user interprets Random Forest feature importance as causal evidence.



\*\*Risk:\*\* Predictive importance does not establish causal relationships.



\*\*Control:\*\* Clearly document this limitation.



\---



\### Misuse Scenario 4: Applying the Model Outside Its Valid Context



The model is used with a different population or intervention without validation.



\*\*Risk:\*\* Predictions may not generalize.



\*\*Control:\*\* Require validation on new populations and interventions before deployment.



\---



\### Misuse Scenario 5: Ignoring Uncertainty



A user treats every uplift prediction as exact.



\*\*Risk:\*\* Model uncertainty is ignored.



\*\*Control:\*\* Provide confidence intervals and uncertainty analysis where appropriate.



\---



\## 20. Security Controls Matrix



| Threat                | Current Control            | Future Control                  |

| --------------------- | -------------------------- | ------------------------------- |

| Invalid input         | Pydantic validation        | API fuzz testing                |

| Invalid dataset       | Data validation            | Automated data-quality pipeline |

| Data poisoning        | Validation                 | Dataset versioning/signing      |

| Model manipulation    | Controlled model files     | Artifact signing                |

| Unauthorized access   | Prototype-local deployment | Authentication/authorization    |

| Privacy leakage       | Simulated data             | Encryption/access controls      |

| Log manipulation      | Audit file                 | Centralized append-only logging |

| API abuse             | Basic validation           | Rate limiting                   |

| DoS                   | Containerization           | Resource limits/autoscaling     |

| Recommendation misuse | Human oversight            | Strong UI warnings/workflow     |

| Subgroup differences  | Audit analysis             | Formal fairness evaluation      |

| Data leakage          | Train/test split           | Automated leakage checks        |

| Model drift           | Prediction monitoring      | Drift detection                 |

| Dependency risk       | Requirements file          | Security scanning               |



\---



\## 21. Security Testing Evidence



The current project includes practical failure tests.



\### Test 1: Missing Feature



Result:



```text

Validation failed

Missing columns: \['study\_hours']

```



\### Test 2: Invalid Treatment



Result:



```text

Validation failed

Invalid treatment values detected

```



\### Test 3: Missing Value



Result:



```text

Validation failed

Missing values detected

```



\### Test 4: Empty Dataset



Result:



```text

Validation failed

Dataset is empty

```



\### API Validation



An invalid attendance value of `150` produced:



```text

HTTP 422 Unprocessable Entity

```



These tests demonstrate that invalid inputs are not silently accepted.



\---



\## 22. Security Acceptance Criteria



The prototype should satisfy the following minimum criteria:



\* Invalid API inputs are rejected.

\* Invalid treatment values are rejected.

\* Missing required dataset columns are detected.

\* Empty datasets are rejected.

\* Unexpected internal errors are not exposed directly.

\* No real learner PII is included in the prototype dataset.

\* Prediction events can be audited.

\* Recommendation outputs include human-oversight context.

\* Security limitations are documented.



\---



\## 23. Residual Risks



Even after the current controls, the following risks remain:



1\. Production authentication is not implemented.

2\. Production authorization is not implemented.

3\. Rate limiting is not implemented.

4\. Centralized secure logging is not implemented.

5\. Model artifact signing is not implemented.

6\. Real-world privacy controls have not been evaluated.

7\. External-dataset generalization has not been demonstrated.

8\. Long-term model drift monitoring requires outcome data.

9\. Fairness criteria require explicit stakeholder definition.



These residual risks should be addressed before deployment in a real educational environment.



\---



\## 24. Security Conclusion



The current prototype incorporates input validation, data validation, robustness testing, privacy-oriented checks, controlled API errors, audit logging and human-oversight considerations.



The threat model also identifies additional controls required for production deployment.



Therefore, security is treated as an ongoing engineering requirement rather than a one-time implementation step.



