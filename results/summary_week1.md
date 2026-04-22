# Week 1 — LLM Evaluation Baseline (RAG System)

**Repo:** mcamper/llm-qa-test-framework  
**Framework:** DeepEval  
**Model:** GPT-4  
**Focus:** Baseline evaluation of consistency, faithfulness, and accuracy in a Retrieval-Augmented Generation (RAG) system  

---

## Overview

Week 1 establishes a baseline LLM QA framework for evaluating response quality in RAG systems.  
The goal is to measure consistency, faithfulness to source documents, and overall accuracy under controlled test conditions.

This phase also introduces rubric-based scoring using DeepEval’s GEval metric to move beyond binary pass/fail evaluation.

---

## Test Cases Executed

| TC ID  | Test Name              | Criteria                  | Runs | Pass | Fail | Status | Notes |
|--------|------------------------|---------------------------|------|------|------|--------|------|
| TC-001 | Consistency/Relevance  | Consistency, Relevance    | 5    | 5    | 0    | PASS (With Defect) | Ungrounded expansion observed |
| TC-002 | Faithfulness           | Faithfulness              | 5    | 5    | 0    | PASS | Synonym variance observed |
| TC-003 | Accuracy               | Accuracy                  | 5    | 5    | 0    | PASS | Fully grounded responses |
| TC-004 | Rubric-Based Scoring   | Response Quality (GEval)  | 1    | 1    | 0    | LIMITED | Single-run validation only |

---

## Key Findings & Defects

### Finding 001 — Ungrounded Expansion Without Context
**Test Case:** TC-001  
**Severity:** Medium (High in regulated domains)  

**Description:**  
When prompts were not grounded in a source document, the LLM introduced additional causes not present in the reference material. While responses remained relevant and internally consistent, they were not fully faithful to the source.

**Defect Type:** Additive Hallucination (Ungrounded Content)

**Business Impact:**  
- Inaccurate summaries of critical documents  
- Risk of misinformation in healthcare, legal, or financial contexts  
- Reduced trust in AI-generated outputs  

**Recommendation:**  
Enforce strict prompt grounding using retrieved documents in all RAG implementations.

---

### Finding 002 — Synonym Variance in Faithful Responses
**Test Case:** TC-002  
**Severity:** Low  

**Description:**  
One test run produced a response using synonymous phrasing while remaining factually correct and fully grounded in the source document.

**Defect Type:** None (Expected Model Behavior)

**Business Impact:**  
- No negative impact  
- Improves naturalness and readability of responses  

**Recommendation:**  
Define acceptable tolerance levels for semantic equivalence in faithfulness evaluation criteria.

---

### Finding 003 — Prompt Grounding Eliminates Variance
**Test Case:** TC-003  
**Severity:** Informational  

**Description:**  
When the source document was explicitly provided in the prompt, all outputs matched the ground truth exactly across five runs. No variation or hallucination was observed.

**Business Impact:**  
- Increased reliability of outputs  
- Deterministic responses suitable for high-stakes use cases  

**Recommendation:**  
Adopt grounded prompting as a standard design pattern in RAG systems.

---

### Finding 004 — Rubric-Based Scoring Improves Evaluation Precision
**Test Case:** TC-004  
**Severity:** Medium  

**Description:**  
Implemented rubric-based evaluation using DeepEval’s GEval metric. The system successfully distinguished between:
- Fully correct responses  
- Partially correct responses  

However, testing was limited to a single execution.

**Business Impact:**  
- Enables granular quality scoring beyond pass/fail  
- Supports production-grade evaluation pipelines  

**Limitations:**  
- Insufficient sample size (n=1)  
- Requires expanded test coverage for reliability  

**Recommendation:**  
Increase test runs and include edge cases to validate scoring consistency.

---

## Evaluation Limitations Identified

- Binary pass/fail evaluation is insufficient for LLM quality assessment  
- Hallucination risk increases significantly without prompt grounding  
- Single-metric evaluation may miss nuanced response issues  
- Rubric scoring requires multiple runs to ensure stability  

---

## Overall Assessment

All test cases met baseline acceptance criteria.  
However, **one defect (additive hallucination due to lack of grounding)** was identified and logged.

Week 1 establishes:
- A functional LLM QA testing framework  
- Initial evaluation criteria and methodology  
- The need for multi-metric evaluation in RAG systems  

---

## Framework Decision Log

| Framework | Status      | Reason                                      |
|-----------|-------------|---------------------------------------------|
| RAGAS     | Deprecated  | Async hang on Python 3.13, version instability |
| DeepEval  | Active      | Stable, fast, clean pytest integration      |

---

## Next Steps

- Build TC-005: Hallucination Detection using DeepEval HallucinationMetric  
- Expand rubric-based scoring with multiple test runs  
- Introduce defect classification for hallucination types  
- Increase dataset and prompt variability  
- Connect project to GitHub for version control  

---

## Key Takeaway

Prompt grounding is the single most important factor in controlling LLM output quality.  
Unconstrained models may produce responses that are coherent but not factually supported—introducing risk in real-world applications.
