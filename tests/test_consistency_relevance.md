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
| 1   |               |             |           |
| 2   |               |             |           |
| 3   |               |             |           |
| 4   |               |             |           |
| 5   |               |             |           |

## Pass Criteria
- 4 out of 5 runs return consistent answers
- All answers scoped to source document content

## Status: [ ] Not Started
