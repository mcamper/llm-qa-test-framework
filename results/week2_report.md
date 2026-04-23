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

This phase also introduces threshold tuning and highlights evaluator limitations.

---

## Test Cases Executed

| TC ID  | Test Name                     | Metric                | Runs | Pass | Fail | Status | Notes |
|--------|------------------------------|----------------------|------|------|------|--------|------|
| TC-005 | Hallucination Detection      | HallucinationMetric  | 4    | 2    | 2    | PASS (With Defects Logged) | Additive hallucination gap identified |
| TC-006 | Faithfulness Evaluation      | FaithfulnessMetric   | 3    | 3    | 0    | PASS (Prompt-Sensitive) | See v1 & v2 evidence |
| TC-007 | [Reserved for New Test Case] | TBD                  | —    | —    | —    | PLANNED | To be implemented |

---

## Results Summary

**HallucinationMetric Thresholds:**  
- Default: 0.5  
- Adjusted (partial hallucination test): 0.3  

**Execution Time:** ~11.8 seconds  

| Test Scenario              | Result | Notes |
|---------------------------|--------|------|
| Grounded Response         | PASS   | Fully supported by context |
| Hallucinated Response     | FAIL   | Fabricated “60-day policy” correctly detected |
| Partial Hallucination     | PASS (False Negative) | Unsupported additions not flagged |
| No Context Provided       | FAIL   | Ungrounded claim correctly detected |

---

## Key Findings & Defects

### Finding 001 — Additive Hallucination Not Detected by HallucinationMetric
**Test Case:** TC-005  
**Severity:** Medium (High in regulated domains)  

**Description:**  
The model generated responses containing additional claims not present in the source context (e.g., cryptocurrency support, buy-now-pay-later services). These claims did not contradict the source but were unsupported.

HallucinationMetric failed to flag these additions at both tested thresholds (0.5 and 0.3), resulting in false negatives.

**Defect Type:** Additive Hallucination (Unsupported Content)

**Business Impact:**  
- False confidence in model accuracy  
- Risk of subtle misinformation in production systems  
- Increased difficulty in detecting non-obvious hallucinations  

**Recommendation:**  
Do not rely solely on HallucinationMetric for RAG validation. Combine with FaithfulnessMetric to detect unsupported claims.

---

### Finding 002 — Hallucination Detection is Reliable for Contradictory and Ungrounded Claims
**Test Case:** TC-005  
**Severity:** Low  

**Description:**  
HallucinationMetric successfully detected:
- Fully fabricated claims (e.g., “60-day policy”)  
- Responses generated without any supporting context  

**Defect Type:** None (Expected Behavior)

**Business Impact:**  
- Confirms effectiveness for clear hallucination scenarios  
- Suitable for baseline hallucination detection  

**Recommendation:**  
Use HallucinationMetric as part of a layered evaluation strategy, not as a standalone solution.

---

### Finding 003 — Metric Sensitivity Limited for Partial Hallucinations
**Test Case:** TC-005  
**Severity:** Medium  

**Description:**  
Lowering the threshold from 0.5 to 0.3 did not improve detection of additive hallucinations. Unsupported claims continued to pass evaluation.

**Business Impact:**  
- Threshold tuning alone cannot resolve detection gaps  
- Risk of misclassifying partially incorrect responses as valid  

**Recommendation:**  
Introduce complementary evaluation metrics (e.g., FaithfulnessMetric) rather than relying on threshold adjustments.

---

## Evaluation Limitations Identified

- HallucinationMetric does not reliably detect additive hallucinations  
- Threshold adjustments have limited impact on detection sensitivity  
- Single-metric evaluation leads to false negatives in complex responses  
- Detection performance varies based on hallucination type  

---

## Overall Assessment

TC-005 successfully validates hallucination detection behavior and exposes a critical limitation in the evaluation framework.

Two defects were identified:
- Additive hallucination not detected (false negative)  
- Metric sensitivity limitations  

Week 2 establishes:
- A working hallucination detection test suite  
- Classification of hallucination types  
- The need for multi-metric evaluation strategies in RAG systems  

---

## Environment Notes

| Item | Detail |
|------|--------|
| DeepEval Version | 3.9.7 |
| Model Change | GPT-4 → GPT-4o |
| Reason | Structured outputs requirement |
| Known Issue | GPT-4 does not support `response_format=json_schema` |

---

## Next Steps

- Complete TC-006: Faithfulness Evaluation using FaithfulnessMetric  
- Implement TC-007: Additional test case (TBD)  
- Build combined metric evaluation (Hallucination + Faithfulness)  
- Expand test coverage with edge and adversarial cases  
- Commit Week 2 updates to GitHub  

---

## Key Takeaway

Not all hallucinations are equal.  
While blatant fabrications are easily detected, **additive hallucinations—plausible but unsupported claims—can bypass standard evaluation metrics**, requiring a layered, multi-metric approach for reliable LLM validation.

---
