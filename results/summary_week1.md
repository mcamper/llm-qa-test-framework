# Test Results Summary — Week 1
## Framework: LLM QA Test Framework (RAG)
## Tester: Maria Camper
## Date: April 2026

---

## Test Cases Executed

| TC ID  | Test Name              | Criteria                  | Runs | Pass | Fail | Status |
|--------|------------------------|---------------------------|------|------|------|--------|
| TC-001 | Consistency/Relevance  | Consistency, Relevance    | 5    | 5    | 0    | PASS   |
| TC-002 | Faithfulness           | Faithfulness              | 5    | 5    | 0    | PASS   |
| TC-003 | Accuracy               | Accuracy                  | 5    | 5    | 0    | PASS   |
| TC-004 | Rubric-Based Scoring   | Response Quality (GEval)  | 1    | 1    | 0    | PASS   |

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

### Finding 4 — TC-004: Rubric Scoring Enables Granular Quality Assessment
- Implemented rubric-based criteria scoring using DeepEval GEval metric
- Response scored against a 4-tier rubric (0-2, 3-5, 6-8, 9-10)
- A high-quality response ("The Eiffel Tower is located in Paris, France.")
  scored above threshold (0.5) and passed
- A low-quality response ("located in Europe and part of France")
  correctly scored below threshold — demonstrating rubric sensitivity
- Test completed in 3.78 seconds with no async issues
- **Implication:** Rubric scoring can distinguish between
  partially correct and fully correct responses — critical for
  client-facing LLM quality gates

---

## Overall Assessment

All 4 test cases passed. Three actionable findings identified
in Week 1. TC-004 introduces automated rubric-based scoring
using DeepEval as the primary evaluation framework going forward.
DeepEval selected over RAGAS due to stability, speed, and
Python 3.13 compatibility.

---

## Framework Decision Log

| Framework | Status    | Reason                                      |
|-----------|-----------|---------------------------------------------|
| RAGAS     | Deprecated| Async hang on Python 3.13, version instability |
| DeepEval  | Active    | Stable, fast, clean pytest integration      |

---

## Next Steps
- Build TC-005: Hallucination Detection using DeepEval HallucinationMetric
- Automate test runs using Python
- Expand source documents for broader coverage
- Connect LLMEvaluation project to GitHub via git remote
