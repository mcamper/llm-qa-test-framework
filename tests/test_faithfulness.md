# Test Case: Faithfulness (RAG)

## Test ID: TC-002

## Objective
Evaluate whether the LLM's response is grounded strictly in the 
source document — no invented or expanded information.

## Evaluation Criteria
- **Faithfulness:** Does the answer contain ONLY information 
  from the source document?

## Source Document (Simulated)
Patients are readmitted due to three primary factors: 
inadequate discharge planning, lack of follow-up care, 
and unmanaged chronic conditions.

## Test Prompt
"Based on the following document, what are the main causes 
of hospital readmissions?"

[Document]: Patients are readmitted due to three primary factors: 
inadequate discharge planning, lack of follow-up care, 
and unmanaged chronic conditions.

## Runs

| Run | Answer Summary | Stays Within Source? | Faithful? |
|-----|---------------|----------------------|-----------|
| 1   |               |                      |           |
| 2   |               |                      |           |
| 3   |               |                      |           |
| 4   |               |                      |           |
| 5   |               |                      |           |

## Pass Criteria
- Answer contains only the 3 factors from the source document
- No additional causes introduced by the LLM

## Status: [ ] Not Started
