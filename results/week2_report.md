# Week 2 — Hallucination Detection & Faithfulness Evaluation (RAG System)

**Repo:** mcamper/llm-qa-test-framework  
**Framework:** DeepEval  
**Model:** GPT-4o  
**Python:** 3.13  
**Environment:** PyCharm 2026.1  
**Focus:** Hallucination detection and faithfulness evaluation in a Retrieval-Augmented Generation (RAG) system  

---

## Overview

Week 2 expands the LLM QA framework to include hallucination detection and deeper evaluation of response faithfulness.

The objective is to identify and classify hallucination behaviors, evaluate detection reliability using DeepEval metrics, and validate whether single-metric approaches are sufficient for production RAG systems.

This phase also introduces threshold tuning, RAG pipeline baseline testing, and highlights evaluator limitations.

---

## Hallucination Types Evaluated

This test suite evaluates multiple hallucination patterns commonly observed in production systems:

- **Full Fabrication** — Completely invented claims (no grounding in context)
- **Contradiction** — Response conflicts with provided context
- **Additive Hallucination** — Unsupported claims added to otherwise correct responses
- **No Context / Retrieval Failure** — Model generates responses without retrieved context

---

## Test Cases Executed

| TC ID  | Test Name                | Metric                                        | Runs | Pass | Fail | Status                    | Notes                                          |
|--------|--------------------------|-----------------------------------------------|------|------|------|---------------------------|------------------------------------------------|
| TC-005 | Hallucination Detection  | HallucinationMetric                           | 4    | 2    | 2    | PASS (With Defects Logged)| Additive hallucination gap identified          |
| TC-006 | Faithfulness Evaluation  | FaithfulnessMetric                            | 3    | 3    | 0    | PASS (Prompt-Sensitive)   | See v1 & v2 evidence                           |
| TC-007 | RAG Pipeline Baseline    | FaithfulnessMetric, ContextualRelevancyMetric | 3    | 3    | 0    | PASS (With Defect)        | DEF-001 logged — see TC-008 through TC-010     |

---

## TC-007 Sub-Tests

TC-007 is composed of three sub-tests executed in test_rag_pipeline_w2.py.

| TC ID  | Test Name               | Metric                    | Runs | Pass | Fail | Status             | Notes                                         |
|--------|-------------------------|---------------------------|------|------|------|--------------------|-----------------------------------------------|
| TC-008 | Ingestion Faithful      | FaithfulnessMetric        | 1    | 1    | 0    | PASS               | Grounded response confirmed                   |
| TC-009 | Chunk Quality Relevance | ContextualRelevancyMetric | 1    | 1    | 0    | PASS               | Context relevance validated                   |
| TC-010 | Retrieval Failure Drift | FaithfulnessMetric        | 1    | 1    | 0    | PASS (With Defect) | DEF-001: Evaluator blind spot on empty context|

---

## Results Summary

**HallucinationMetric Thresholds:**
- Default: 0.5
- Adjusted (partial hallucination test): 0.3

**Execution Time:** ~40.99 seconds (TC-007 through TC-010)

| Test Scenario           | Result              | Notes                                              |
|-------------------------|---------------------|----------------------------------------------------|
| Grounded Response       | PASS                | Fully supported by context                         |
| Hallucinated Response   | FAIL                | Fabricated "60-day policy" correctly detected      |
| Partial Hallucination   | PASS (False Negative)| Unsupported additions not flagged                 |
| No Context Provided     | FAIL                | Ungrounded claim correctly detected                |
| Ingestion Faithful      | PASS                | Grounded response confirmed                        |
| Chunk Quality Relevance | PASS                | Context relevance validated                        |
| Retrieval Failure Drift | PASS (With Defect)  | Model hallucinated — evaluator returned PASS       |

---

## Key Findings & Defects

### Finding 001 — Additive Hallucination Not Detected by HallucinationMetric
**Test Case:** TC-005  
**Severity:** Medium (High in regulated domains)

**Description:**
The model generated responses containing additional claims not present in the source context
(e.g., cryptocurrency support, buy-now-pay-later services). These claims did not contradict
the source but were unsupported.

HallucinationMetric failed to flag these additions at both tested thresholds (0.5 and 0.3),
resulting in false negatives.

**Defect Type:** Additive Hallucination (Unsupported Content)

**Business Impact:**
- False confidence in model accuracy  
- Risk of subtle misinformation in production systems  
- Increased difficulty in detecting non-obvious hallucinations  

**Recommendation (System Controls):**
- Combine HallucinationMetric with FaithfulnessMetric  
- Implement claim-level validation (check each statement against context)  
- Flag responses containing information not explicitly supported by retrieved context  

---

### Finding 002 — Hallucination Detection is Reliable for Contradictory and Ungrounded Claims
**Test Case:** TC-005  
**Severity:** Low  

**Description:**
HallucinationMetric successfully detected:
- Fully fabricated claims (e.g., "60-day policy")  
- Responses generated without any supporting context  

**Defect Type:** None (Expected Behavior)

**Business Impact:**
- Confirms effectiveness for clear hallucination scenarios  
- Suitable for baseline detection  

**Recommendation:**
- Use HallucinationMetric as part of a layered evaluation strategy, not as a standalone solution  

---

### Finding 003 — Metric Sensitivity Limited for Partial Hallucinations
**Test Case:** TC-005  
**Severity:** Medium  

**Description:**
Lowering the threshold from 0.5 to 0.3 did not improve detection of additive hallucinations.
Unsupported claims continued to pass evaluation.

**Business Impact:**
- Threshold tuning alone cannot resolve detection gaps  
- Risk of misclassifying partially incorrect responses as valid  

**Recommendation (System Controls):**
- Introduce multi-metric evaluation strategy  
- Add rule-based validation for unsupported claims  
- Avoid relying on threshold tuning as a primary control mechanism  

---

### DEF-001 — FaithfulnessMetric Blind Spot on Empty Context
**Test Case:** TC-010  
**Severity:** High  

**Description:**
Empty context was provided to simulate retrieval failure. The model generated a confident
10-item Python library list from parametric memory. DeepEval FaithfulnessMetric returned
PASS despite the hallucinated output. The metric has no baseline to compare against when
context is empty, defaulting to PASS.

**Defect Type:** Evaluator Limitation (False Negative on Empty Context)

**Business Impact:**
- False confidence in evaluation results  
- Undetected hallucination in production RAG systems where retrieval silently fails  
- Prompt-dependent reliability risk  

**Recommendation (System Controls):**
- Block generation when `retrieval_context == empty`  
- Return fallback response (e.g., "I don’t have enough information to answer")  
- Add pre-evaluation assertion to verify context presence  
- Pair FaithfulnessMetric with HallucinationMetric for empty-context scenarios  
- Never treat a FaithfulnessMetric PASS as valid without confirmed retrieval  

---

## Evaluation Limitations Identified

- HallucinationMetric does not reliably detect additive hallucinations  
- FaithfulnessMetric cannot detect hallucination when retrieval_context is empty  
- Threshold adjustments have limited impact on detection sensitivity  
- Single-metric evaluation leads to false negatives in complex responses  
- Detection performance varies based on hallucination type  

---

## Business Impact Summary (Client-Facing)

The findings from this evaluation highlight critical risks for production AI systems:

- Users may receive **confident but unsupported answers**  
- Retrieval failures may go **undetected while appearing valid**  
- Evaluation metrics may produce **false confidence in system accuracy**  
- Subtle hallucinations can bypass detection and impact decision-making  

Without proper controls, these risks can lead to:
- Misinformation exposure  
- Loss of user trust  
- Increased operational and compliance risk  

---

## Overall Assessment

Week 2 successfully validates hallucination detection and faithfulness evaluation behavior,
while exposing critical limitations in current evaluation approaches.

Defects identified:
- Additive hallucination not detected (false negative) — TC-005  
- Metric sensitivity limitations — TC-005  
- Evaluator blind spot on empty context — TC-010 (DEF-001)  

Week 2 establishes:
- A working hallucination detection test suite  
- A RAG pipeline baseline (TC-007 through TC-010)  
- Classification of hallucination types  
- The need for layered, multi-metric evaluation strategies  

**Conclusion:**
Single-metric evaluation is insufficient for production RAG systems. Reliable validation
requires both generation correctness and retrieval validation.

---

## Environment Notes

| Item              | Detail                                      |
|-------------------|---------------------------------------------|
| DeepEval Version  | 3.9.7                                       |
| Model Change      | GPT-4 → GPT-4o                              |
| Reason            | Structured outputs requirement              |
| Known Issue       | GPT-4 does not support response_format=json_schema |
| Test File         | test_rag_pipeline_w2.py                     |

---

## Next Steps (Week 3)

- Build TC-011 through TC-017 in test_rag_pipeline_w3.py  
- Expand retrieval evaluation: precision, recall, ranking  
- Add generation evaluation: answer grounding, GEval scoring  
- Implement full end-to-end pipeline test (TC-017)  
- Build combined metric evaluation (Hallucination + Faithfulness)  
- Commit Week 2 final updates to GitHub  

---

## Key Takeaway

Not all hallucinations are equal. Blatant fabrications are easily detected, but additive
hallucinations and evaluator blind spots on empty context create silent failure modes in
production RAG systems. A layered, multi-metric approach is required for reliable LLM validation.
