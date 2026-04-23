# TC-006 — Faithfulness Evaluation (v2: Prompt Sensitivity Test)

## Objective
Evaluate how prompt grounding strength impacts model faithfulness.

---

## Test Variation

| Mode   | Instruction |
|--------|------------|
| strict | Answer ONLY using context |
| soft   | Answer based on context if possible |
| none   | No grounding instruction |

---

## Results

| Mode   | Answer Behavior | Verdict | Notes |
|--------|---------------|--------|------|
| strict | "Not found in context" | faithful | Prompt-constrained |
| soft   | Generated libraries (NumPy, Pandas, etc.) | unfaithful | Drift beyond context |
| none   | Confident full answer | unfaithful | Hallucination |

---

## Key Finding

**Faithfulness is highly sensitive to prompt constraints.**

Strong grounding instructions can suppress hallucinations, but this behavior is not inherent to the model.

---

## Risk Identified

- False confidence in evaluation results  
- Prompt-dependent reliability  
- Increased hallucination risk in real-world usage where prompts are less strict  

---

## Recommendation

- Test across multiple prompt strengths  
- Do not rely on single prompt configurations  
- Combine FaithfulnessMetric with adversarial prompt testing  

---
