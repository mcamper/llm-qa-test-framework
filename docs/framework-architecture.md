# LLM QA Framework Architecture (DeepEval-Based)

## Overview

This project uses **DeepEval** as the primary evaluation framework for testing LLM behavior in Retrieval-Augmented Generation (RAG) systems.

All legacy RAGAS-style manual rubric definitions have been removed in favor of standardized, framework-driven evaluation metrics.

---

## Framework Transition

| Framework | Status | Reason |
|-----------|--------|--------|
| RAGAS | Deprecated (Legacy Reference Only) | Async instability on Python 3.13, manual rubric overhead |
| DeepEval | Active | Stable, production-ready, built-in metrics, pytest integration |

---

## Evaluation Philosophy

This framework follows a **metric-driven evaluation model**:

### Old Approach (RAGAS-style)
- Manually defined rubrics
- Prompt-based scoring instructions
- Custom LLM judge behavior per test
- High flexibility, low standardization

### Current Approach (DeepEval-style)
- Prebuilt evaluation metrics
- Standardized scoring logic
- Internal rubric handling (abstracted)
- Normalized scoring (0–1 scale)
- Consistent, reproducible results

---

## Core Evaluation Metrics Used

### 1. Hallucination Detection
Detects whether the model introduces unsupported or fabricated information.

### 2. Faithfulness Evaluation
Measures whether responses are fully supported by the provided context.

### 3. Answer Relevance (Optional Expansion)
Evaluates whether responses align with the user query intent.

---

## Scoring Model

DeepEval internally normalizes all outputs to:
- 0.0 → 1.0 scale
  
Where:
- 0.0 = completely incorrect / ungrounded
- 1.0 = fully correct / fully grounded

Thresholds are defined per test case:
- Example: 0.5 default pass threshold
- Adjustable based on severity requirements

---

## Why Custom Rubrics Are No Longer Used

Manual rubric definitions (e.g., 1–5 scoring systems) are not required because:

- DeepEval already defines evaluation criteria internally
- Metrics are standardized across test runs
- Scoring is normalized and comparable
- Custom rubrics introduce inconsistency in production testing

---

## Current Evaluation Workflow

1. Input prompt + context (RAG pipeline)
2. Generate LLM response (GPT-4o)
3. Pass output to DeepEval metric
4. Framework evaluates response against:
   - context
   - expected behavior
   - metric-specific criteria
5. Score is normalized (0–1)
6. Pass/fail determined via threshold

---

## System Benefits

- Consistent evaluation across test cases
- Reduced manual prompt engineering
- Better reproducibility in CI/CD pipelines
- Easier scaling for multiple test suites
- Cleaner separation between testing logic and evaluation logic

---

## Key Design Principle

> Evaluation logic is handled by the framework, not manually embedded in rubrics.

This ensures:
- standardization
- repeatability
- production readiness

---
