# TC-010 — Retrieval Failure Drift

**Date:** 04/23/2026  
**Model:** gpt-4o  
**Framework:** DeepEval  

---

## Result: PASSED (With Defect)

---

## What Happened

Empty context was provided to simulate retrieval failure.

The model generated a confident 10-item Python library list from parametric memory (no grounding in retrieved data).

DeepEval **FaithfulnessMetric** evaluated the response as **FAITHFUL (PASS)**.

---

## Defect Logged

**DEF-001: Evaluator Blind Spot — FaithfulnessMetric returns false positives when retrieval_context is empty**

**Defect Type:** False Negative (Evaluator Limitation)

**Description:**
FaithfulnessMetric requires source context to validate response grounding. When `retrieval_context` is empty, the metric has no baseline for comparison and defaults to PASS.

This results in **false positives**, where hallucinated responses are incorrectly classified as faithful.

---

## Impact

- False confidence in evaluation results  
- Undetected hallucinations in production RAG systems  
- Silent failure mode when retrieval fails upstream  
- Increased risk of users receiving confident but ungrounded answers  

---

## Key Finding

A passing FaithfulnessMetric score **does not indicate correctness** when context is absent.

In empty-context scenarios:
- PASS = **evaluator limitation**
- NOT = grounded or reliable response

FaithfulnessMetric is only meaningful when **retrieval context is present and valid**.

---

## Recommendation (System Controls)

- **Block generation** when `retrieval_context == empty`  
- Return fallback response (e.g., *"I don’t have enough information to answer"*)  
- Add **pre-evaluation assertion** to verify context presence  
- Pair with **HallucinationMetric** for empty-context detection  
- Treat any FaithfulnessMetric PASS as **invalid** unless retrieval is confirmed  

---

## QA Insight

This test exposes a critical gap in RAG evaluation:

Evaluation frameworks can report **high confidence scores even when the system fails at retrieval**.

This reinforces the need for:
- Retrieval validation (not just generation evaluation)  
- Multi-metric evaluation strategies  
- System-level safeguards, not metric-only validation  
