# Test Case: Consistency & Relevance (RAG)

## Test ID: TC-001

## Objective
Evaluate whether an LLM returns consistent and relevant answers 
when given the same prompt multiple times against the same source document.

## Evaluation Criteria
- **Consistency:** Do the answers align across 5 runs?
- **Relevance:** Do the answers stay scoped to the source document?

## Test Prompt
"What are the main causes of hospital readmissions?"

## Source Document (Simulated)
Patients are readmitted due to three primary factors: 
inadequate discharge planning, lack of follow-up care, 
and unmanaged chronic conditions.

## Runs

| Run | Answer Summary | Consistent? | Relevant? |
|-----|---------------|-------------|-----------|
| 1   |   Poor discharge planning, lack of follow-up care, medication errors or non-adherence, complications from the original condition, and inadequate patient education on managing their condition at home.            |      Yes       |   Yes        |
| 2   |    Inadequate discharge planning, poor care coordination, medication issues, lack of follow-up, and worsening of the patient’s condition after discharge.           |   Yes          |   Yes        |
| 3   |     Poor discharge planning, medication errors or non-adherence, lack of timely follow-up care, complications or relapse of the original condition, and insufficient patient education/support after discharge.        |    Yes         |   Yes        |
| 4   |    Poor discharge planning, medication issues (errors or non-adherence), lack of follow-up care, complications from the original illness, and inadequate patient education or support after leaving the hospital.           |     Yes        |  Yes         |
| 5   |    Poor discharge planning, medication problems, lack of follow-up care, complications or worsening of the original condition, and insufficient patient education/support after discharge.         |      Yes       |   Yes        |

## Pass Criteria
- 4 out of 5 runs return consistent answers
- All answers scoped to source document content

## Results
- 5/5 runs returned consistent answers (exceeds pass criteria)
- All answers scoped to source document content
- Notable: LLM expanded beyond the 3 factors in the source document
  (added medication errors, patient education) — answers relevant but not strictly faithful

## Status: [x] PASS — with Faithfulness flag
