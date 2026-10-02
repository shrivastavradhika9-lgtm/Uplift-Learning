\#  API and Data Contract



\## 1. Purpose



This document defines the data contract and API contract for the MDS-02 Uplift Modeling Platform.



The contract specifies:



\* Required input fields

\* Data types

\* Valid ranges

\* Prediction response structure

\* Error handling

\* Model version information

\* Audit information



The purpose is to ensure consistent communication between the Streamlit dashboard, FastAPI service and uplift prediction system.



\---



\## 2. API Service



The prediction service is implemented using FastAPI.



Application:



`MDS-02 Uplift Modeling API`



Current version:



`1.0.0`



Model version:



`v1`



Base URL during local deployment:



`http://localhost:8000`



\---



\## 3. API Endpoints



\### 3.1 Root Endpoint



\*\*Method:\*\*



`GET`



\*\*Endpoint:\*\*



`/`



\*\*Purpose:\*\*



Checks whether the API service is running.



Example response:



```json

{

&#x20; "message": "MDS-02 Uplift Modeling API is running",

&#x20; "model\_version": "v1"

}

```



\---



\## 4. Prediction Endpoint



\### Endpoint



`POST /predict`



\### Purpose



The endpoint receives learner information and estimates:



1\. Expected outcome under control

2\. Expected outcome under treatment

3\. Estimated individual uplift

4\. Intervention recommendation

5\. Model version



\---



\## 5. Request Data Contract



The prediction request contains the following fields:



| Field                 | Type  | Required | Valid Range | Description             |

| --------------------- | ----- | -------- | ----------- | ----------------------- |

| age                   | float | Yes      | 18–100      | Learner age             |

| study\_hours           | float | Yes      | 0–24        | Study hours             |

| attendance\_rate       | float | Yes      | 0–100       | Attendance percentage   |

| previous\_score        | float | Yes      | 0–100       | Previous academic score |

| assignments\_completed | float | Yes      | 0–10        | Completed assignments   |



\---



\## 6. Example Request



```json

{

&#x20; "age": 22,

&#x20; "study\_hours": 6.5,

&#x20; "attendance\_rate": 85,

&#x20; "previous\_score": 65,

&#x20; "assignments\_completed": 8

}

```



\---



\## 7. Request Validation



Input validation is performed using Pydantic/FastAPI.



The following checks are applied:



\### Age



```text

18 <= age <= 100

```



\### Study Hours



```text

0 <= study\_hours <= 24

```



\### Attendance Rate



```text

0 <= attendance\_rate <= 100

```



\### Previous Score



```text

0 <= previous\_score <= 100

```



\### Assignments Completed



```text

0 <= assignments\_completed <= 10

```



Invalid values are rejected before prediction.



\---



\## 8. Prediction Processing



After successful validation, the API performs the following operations:



```text

Request

&#x20;  ↓

Validate Input

&#x20;  ↓

Prepare Features

&#x20;  ↓

Control Model Prediction

&#x20;  ↓

Treatment Model Prediction

&#x20;  ↓

Calculate Estimated Uplift

&#x20;  ↓

Apply Recommendation Threshold

&#x20;  ↓

Generate Response

&#x20;  ↓

Write Audit Record

```



\---



\## 9. Uplift Calculation Contract



The estimated uplift is calculated as:



```text

Estimated Uplift =

Predicted Treatment Outcome

\-

Predicted Control Outcome

```



For example:



```text

Predicted Control  = 12.9032

Predicted Treatment = 19.1506



Estimated Uplift = 19.1506 - 12.9032

&#x20;                = 6.2474

```



\---



\## 10. Recommendation Contract



The current recommendation threshold is:



```text

5.0629

```



Decision rule:



```text

If estimated\_uplift >= 5.0629

&#x20;   → Recommend Intervention



Otherwise

&#x20;   → No Intervention

```



The recommendation is a model-generated decision-support output.



It is not intended to automatically determine the final educational intervention.



\---



\## 11. Response Data Contract



The successful prediction response contains:



| Field               | Type   | Description                                          |

| ------------------- | ------ | ---------------------------------------------------- |

| predicted\_control   | float  | Estimated outcome under control                      |

| predicted\_treatment | float  | Estimated outcome under treatment                    |

| estimated\_uplift    | float  | Difference between treatment and control predictions |

| recommendation      | string | Intervention recommendation                          |

| model\_version       | string | Version of deployed model                            |



\---



\## 12. Example Response



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



\## 13. Recommendation Values



The `recommendation` field can contain:



```text

Recommend Intervention

```



or



```text

No Intervention

```



These values should be treated as categorical decision-support outputs.



\---



\## 14. Error Contract



The API uses HTTP validation errors for invalid input.



For example, if:



```json

{

&#x20; "age": 22,

&#x20; "study\_hours": 6,

&#x20; "attendance\_rate": 150,

&#x20; "previous\_score": 65,

&#x20; "assignments\_completed": 8

}

```



is submitted, the request is rejected because:



```text

attendance\_rate > 100

```



Example HTTP status:



`422 Unprocessable Entity`



Example response structure:



```json

{

&#x20; "detail": \[

&#x20;   {

&#x20;     "type": "less\_than\_equal",

&#x20;     "loc": \[

&#x20;       "body",

&#x20;       "attendance\_rate"

&#x20;     ],

&#x20;     "msg": "Input should be less than or equal to 100",

&#x20;     "input": 150

&#x20;   }

&#x20; ]

}

```



\---



\## 15. Internal Failure Handling



Unexpected prediction failures are handled internally by the API.



The system:



1\. Logs the internal error.

2\. Avoids exposing internal implementation details.

3\. Returns a controlled error response.



This reduces unnecessary exposure of internal application information.



\---



\## 16. Audit Contract



Prediction requests are recorded in:



`results/audit\_log.jsonl`



The audit log is used for operational monitoring and traceability.



The record includes prediction-related information such as:



\* Input learner information

\* Prediction values

\* Estimated uplift

\* Recommendation

\* Model version

\* Timestamp



The audit log should not contain unnecessary personally identifiable information.



\---



\## 17. Dashboard-to-API Contract



The Streamlit dashboard acts as an API client.



```text

Streamlit

&#x20;   │

&#x20;   │ POST /predict

&#x20;   │ JSON Request

&#x20;   ▼

FastAPI

&#x20;   │

&#x20;   │ JSON Response

&#x20;   ▼

Streamlit

```



Inside Docker Compose, the dashboard communicates with the API using the service name:



```text

http://api:8000/predict

```



The host-facing API remains available at:



```text

http://localhost:8000

```



\---



\## 18. Data Schema Contract



The main dataset schema is:



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



\### Treatment



Allowed values:



```text

0 = Control

1 = Treatment

```



\### Outcome



Numeric learner outcome used for treatment-effect analysis.



\---



\## 19. Dataset Validation Contract



Before model processing, the dataset must satisfy:



\* Dataset must not be empty.

\* Required columns must exist.

\* Required values must not contain unexpected missing values.

\* Treatment must contain only valid values.

\* Data must follow the expected schema.



Validation failure prevents invalid data from entering the modeling pipeline.



\---



\## 20. Model Version Contract



The deployed prediction service currently identifies the model as:



```text

model\_version: v1

```



Future model releases should use a new version identifier, for example:



```text

v2

v3

```



This allows prediction records to be associated with the model version that generated them.



\---



\## 21. API Security Considerations



The current prototype includes:



\* Input validation

\* Controlled error responses

\* Audit logging

\* No hard-coded secret credentials

\* Containerized deployment



For production deployment, additional controls should be considered:



\* Authentication

\* Authorization

\* HTTPS/TLS

\* Rate limiting

\* Secure secret management

\* Access logging

\* Network restrictions

\* Stronger audit-log protection



These production controls are identified as future hardening requirements rather than claims that they are already implemented.



\---



\## 22. Data Privacy Considerations



The project uses simulated learner data.



The system should avoid storing unnecessary personal information.



If real educational data is introduced in the future:



\* Appropriate authorization should be required.

\* Personally identifiable information should be minimized.

\* Access should be restricted.

\* Sensitive fields should be protected.

\* Data retention should be defined.

\* Audit logging should be reviewed for privacy leakage.



\---



\## 23. Contract Testing



The API contract can be tested using:



\* Valid prediction request

\* Missing required field

\* Invalid numeric value

\* Out-of-range value

\* Successful prediction response

\* Error response

\* Model version presence



Automated tests are maintained under:



`tests/`



Current automated test result:



```text

4 passed

```



\---



\## 24. OpenAPI Documentation



FastAPI automatically provides API documentation through OpenAPI.



During local execution, the documentation can be accessed through:



```text

http://localhost:8000/docs

```



The OpenAPI interface provides an interactive representation of the available API endpoints and request/response schemas.



\---



\## 25. Contract Summary



```text

CLIENT

&#x20; │

&#x20; │ JSON Request

&#x20; ▼

POST /predict

&#x20; │

&#x20; ▼

Input Validation

&#x20; │

&#x20; ├── Invalid → HTTP 422

&#x20; │

&#x20; └── Valid

&#x20;       │

&#x20;       ▼

&#x20;  Model Prediction

&#x20;       │

&#x20;       ▼

&#x20;  Uplift Calculation

&#x20;       │

&#x20;       ▼

&#x20;Recommendation

&#x20;       │

&#x20;       ▼

&#x20;JSON Response

&#x20;       │

&#x20;       ▼

&#x20;Audit Log

```



This contract provides a consistent interface between the data, prediction service and user-facing dashboard while supporting validation, traceability and future model versioning.



