# Faithfulness Test Findings — test_faithfulness.py
Date: 04/22/2026
Model: gpt-4o | Framework: pytest

## Results: 3/3 passed

---

### Test 1: Supported Claim
- Context: Eiffel Tower completed in 1889, 330m tall
- Question: When was it completed?
- Answer: "The Eiffel Tower was completed in 1889."
- Verdict: faithful
- Finding: Model answered accurately and within context boundaries.

---

### Test 2: Contradiction Detection
- Injected answer: "The Eiffel Tower is 500 meters tall."
- Context states: 330 meters
- Verdict: unfaithful
- Finding: LLM-as-judge successfully identified factual contradiction.
  The evaluator prompt works as a faithfulness detector.

---

### Test 3: Drift Beyond Context
- Context: Python created by Guido van Rossum (no libraries mentioned)
- Question: What are Python's most popular libraries?
- Answer: "Not found in context."
- Verdict: faithful (from evaluator)
- Finding: GPT-4o respected the grounding instruction and declined to answer.
  This is prompt-enforced grounding, not natural model behavior.
  A weaker prompt may produce drift — this is a test design gap to close later.

---

## Key Distinction Documented
| Hallucination test         | Faithfulness test               |
|----------------------------|---------------------------------|
| Detects invented facts     | Detects context contradiction   |
| No context provided        | Context always provided         |
| Model generates freely     | Model should stay grounded      |

## Next: test_rag_pipeline.py
Combine retrieval simulation + faithfulness scoring in one pipeline test.
