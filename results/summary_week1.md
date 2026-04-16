# Test Results Summary — Week 1

## Framework: LLM QA Test Framework (RAG)
## Tester: Maria Camper
## Date: April 2026

---

## Test Cases Executed

| TC ID  | Test Name              | Criteria       | Runs | Pass | Fail | Status |
|--------|------------------------|----------------|------|------|------|--------|
| TC-001 | Consistency/Relevance  | Consistency,   | 5    | 5    | 0    | PASS   |
|        |                        | Relevance      |      |      |      |        |
| TC-002 | Faithfulness           | Faithfulness   | 5    | 5    | 0    | PASS   |
| TC-003 | Accuracy               | Accuracy       | 5    | 5    | 0    | PASS   |

---

## Key Findings

### Finding 1 — TC-001: LLM Expands Beyond Source Document
- Without document grounding, LLM added causes not in the source
- Consistency and Relevance passed but Faithfulness was flagged
- **Implication:** Always ground prompts with source documents 
  in RAG implementations

### Finding 2 — TC-002: Synonym Variance in Faithful Responses
- Run 4 used synonymous language while remaining factually faithful
- **Implication:** Faithfulness criteria must define 
  tolerance for synonym variance

### Finding 3 — TC-003: Grounded Prompts Improve Consistency
- When document was provided directly, all 5 runs matched 
  ground truth exactly
- Zero variance observed vs TC-001
- **Implication:** Prompt grounding directly improves 
  accuracy and consistency

---

## Overall Assessment
All 3 test cases passed. Two actionable findings identified 
for framework improvement. Faithfulness and Accuracy are 
distinct criteria requiring separate test cases.

---

## Next Steps
- Build TC-004: Hallucination Detection
- Automate test runs using Python
- Expand source documents for broader coverage
