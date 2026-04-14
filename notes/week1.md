## What is RAG?

RAG (Retrieval Augmented Generation) works in two flows:

**Flow 1 — Data Ingestion:**
Proprietary data is fed in, embedded, stored in a Vector database, 
and probabilistically distributed for retrieval.

**Flow 2 — User Query:**
User query is embedded, matched against the Vector database, 
retrieved results are sent to the LLM, converted to human language, 
and returned to the end user.

**Why it matters:** RAG reduces hallucinations by grounding the LLM 
in real retrieved data instead of relying on training memory alone.

## What is LLM Evaluation?

LLM Evaluation measures the quality of LLM outputs against criteria 
such as accuracy, consistency, relevance, and faithfulness to the 
source data.

**Why "evaluation" and not "testing"?**
Traditional QA testing compares expected results vs. actual results 
with clear pass/fail outcomes. LLM outputs are probabilistic — the 
same prompt can return different responses, so there is no single 
"correct" answer to assert against. Evaluation uses scoring and 
judgment instead of binary pass/fail.

**Key evaluation criteria:**
- Accuracy — is the response factually correct?
- Consistency — does it give the same answer to the same question?
- Relevance — does it actually answer what was asked?
- Faithfulness — does it stay grounded in the source data (RAG)?
