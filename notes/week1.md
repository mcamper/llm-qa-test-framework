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
