# Test Case: Accuracy (RAG)

## Test ID: TC-003

## Objective
Evaluate whether the LLM's response matches a known, 
verified ground truth — independent of the source document.

## Evaluation Criteria
- **Accuracy:** Does the answer match the expected correct answer?

## Ground Truth (Known Correct Answer)
Hospital readmissions are primarily caused by three factors:
inadequate discharge planning, lack of follow-up care, 
and unmanaged chronic conditions.

## Test Prompt
"Based on the following document, what are the main causes 
of hospital readmissions?"

[Document]: Patients are readmitted due to three primary factors: 
inadequate discharge planning, lack of follow-up care, 
and unmanaged chronic conditions.

## Runs

| Run | Answer Summary | Matches Ground Truth? | Accurate? |
|-----|---------------|----------------------|-----------|
| 1   |   Inadequate discharge planning, lack of follow-up care, and unmanaged chronic conditions.            |       Yes               |   Yes        |
| 2   |   Inadequate discharge planning, lack of follow-up care, and unmanaged chronic conditions.           |           Yes           |     Yes      |
| 3   |   Inadequate discharge planning, lack of follow-up care, and unmanaged chronic conditions.           |            Yes          |    Yes       |
| 4   |   Inadequate discharge planning, lack of follow-up care, and unmanaged chronic conditions.           |          Yes            |    Yes       |
| 5   |   Inadequate discharge planning, lack of follow-up care, and unmanaged chronic conditions.           |        Yes              |    Yes       |

## Pass Criteria
- Answer matches all 3 factors in the ground truth
- No critical factors missing or substituted

## Results
- 5/5 runs matched ground truth exactly
- No missing or substituted factors
- No synonym variance observed (contrast with TC-002 Run 4)

## Status: [x] PASS
