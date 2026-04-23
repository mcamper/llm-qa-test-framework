import openai
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    FaithfulnessMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
)

client = openai.OpenAI()

# --- RAG pipeline test cases ---
RAG_CASES = [
    {
        "id": "tc008_ingestion",
        "context": "Python was created by Guido van Rossum and released in 1991.",
        "question": "Who created Python?",
        "expect": "faithful",
    },
    {
        "id": "tc009_chunk_quality",
        "context": "Python is used for web development, data science, and automation.",
        "question": "What is Python used for?",
        "expect": "faithful",
    },
    {
        "id": "tc010_retrieval_failure",
        "context": "",  # empty context — expect drift
        "question": "What are Python's most popular libraries?",
        "expect": "unfaithful",
    },
]

# --- helper: call OpenAI with grounding instruction ---
def get_answer(question, context, strict=True):
    grounding = (
        "Answer ONLY using the context provided. "
        "If the answer is not in the context, say 'Not found in context.'"
        if strict else
        "Answer based on context if possible."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": grounding},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"},
        ],
    )
    return response.choices[0].message.content


# ── TC-008: Faithful answer from grounded context ──────────────────
def test_tc008_ingestion_faithful():
    case_data = RAG_CASES[0]
    answer = get_answer(case_data["question"], case_data["context"])
    case = LLMTestCase(
        input=case_data["question"],
        actual_output=answer,
        retrieval_context=[case_data["context"]],
    )
    metric = FaithfulnessMetric(threshold=0.7)
    assert_test(case, [metric])


# ── TC-009: Context relevance for chunk quality ────────────────────
def test_tc009_chunk_quality_relevance():
    case_data = RAG_CASES[1]
    answer = get_answer(case_data["question"], case_data["context"])
    case = LLMTestCase(
        input=case_data["question"],
        actual_output=answer,
        retrieval_context=[case_data["context"]],
    )
    metric = ContextualRelevancyMetric(threshold=0.7)
    assert_test(case, [metric])


# ── TC-010: Retrieval failure — document drift behavior ───────────
def test_tc010_retrieval_failure_drift():
    """
    Empty context simulates retrieval failure.
    FAIL = drift detected = log as defect, not a bug.
    """
    case_data = RAG_CASES[2]
    answer = get_answer(case_data["question"], case_data["context"], strict=False)
    print(f"\n[TC-010] Answer with no context: {answer}")
    case = LLMTestCase(
        input=case_data["question"],
        actual_output=answer,
        retrieval_context=[""],
    )
    metric = FaithfulnessMetric(threshold=0.7)
    try:
        assert_test(case, [metric])
        print("[TC-010] Result: FAITHFUL — no drift detected")
    except AssertionError:
        print("[TC-010] Result: DRIFT DETECTED — log as defect")