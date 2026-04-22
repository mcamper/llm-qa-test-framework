# Week 2 Summary — LLM Evaluation Test Framework
**Repo:** mcamper/llm-qa-test-framework  
**Framework:** DeepEval | **Model:** GPT-4o | **Python:** 3.13 | **Environment:** PyCharm 2026.1

---

## Overview

Week 2 focus: Hallucination detection and faithfulness evaluation using DeepEval metrics.  
Migrated from `gpt-4` to `gpt-4o` due to structured outputs compatibility requirement.

---

## Test Files Completed

| File | Metric | Tests | Status |
|---|---|---|---|
| `test_hallucination_detection.py` | HallucinationMetric | 4 | ✅ Complete |
| `test_faithfulness.py` | FaithfulnessMetric | — | 🔄 In Progress |

---

## Results Log

### `test_hallucination_detection.py`
**Threshold:** 0.5 (default) | 0.3 (partial hallucination test)  
**Run time:** ~11 sec 864 ms

| Test Case | Result | Notes |
|---|---|---|
| `test_grounded_response` | ✅ PASSED | Output fully supported by context |
| `test_hallucinated_response` | ❌ FAILED | 60-day policy fabricated — correctly caught |
| `test_partial_hallucination` | ✅ PASSED | See finding below |
| `test_no_context_provided` | ❌ FAILED | Ungrounded claim correctly caught |

---

## Findings

### Finding 001 — GPT-4o Leniency on Additive Hallucinations
**Severity:** Medium  
**File:** `test_hallucination_detection.py::test_partial_hallucination`  
**Description:**  
GPT-4o does not flag additive claims — fabricated details that do not directly contradict the context but are not supported by it. Two unsupported claims (cryptocurrency, Klarna buy-now-pay-later) were added to a response grounded in a Visa/Mastercard/PayPal context. HallucinationMetric scored below threshold at both 0.5 and 0.3.  
**Implication:**  
HallucinationMetric alone is insufficient for strict RAG pipelines. Additive hallucinations require FaithfulnessMetric for reliable detection.  
**Resolution:** Pair HallucinationMetric with FaithfulnessMetric in production RAG test suites.

---

## Environment Notes

| Item | Detail |
|---|---|
| DeepEval version | 3.9.7 |
| Model switched | `gpt-4` → `gpt-4o` (structured outputs requirement) |
| Known issue | `gpt-4` throws `BadRequestError: response_format json_schema not supported` |

---

## Week 2 Goals

- [x] Build `test_hallucination_detection.py`
- [x] Resolve gpt-4 → gpt-4o model compatibility issue
- [x] Document GPT-4o additive hallucination leniency finding
- [ ] Build `test_faithfulness.py`
- [ ] Document faithfulness findings
- [ ] Commit all Week 2 files to GitHub

---

*Last updated: April 22, 2026*

