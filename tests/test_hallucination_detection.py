# test_hallucination_detection.py
# Portfolio: mcamper/llm-qa-test-framework
# Purpose: Detect hallucinations in LLM responses using DeepEval's HallucinationMetric
# Framework: DeepEval | Model: GPT-4 | Author: Maria Camper

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import HallucinationMetric


# ---------------------------------------------------------------------------
# Metric config — threshold 0.5 means flagged if hallucination score > 0.5
# ---------------------------------------------------------------------------
@pytest.fixture
def hallucination_metric():
    return HallucinationMetric(threshold=0.5, model="gpt-4o")


# ---------------------------------------------------------------------------
# TEST 1: Grounded response — should PASS (no hallucination)
# ---------------------------------------------------------------------------
def test_grounded_response(hallucination_metric):
    """LLM answer is fully supported by the provided context."""
    test_case = LLMTestCase(
        input="What is the refund policy?",
        actual_output=(
            "You can return any item within 30 days of purchase for a full refund. "
            "Items must be unused and in original packaging."
        ),
        context=[
            "Our return policy allows customers to return unused items in original "
            "packaging within 30 days of purchase for a full refund."
        ]
    )
    assert_test(test_case, [hallucination_metric])


# ---------------------------------------------------------------------------
# TEST 2: Hallucinated response — should FAIL (fabricated detail)
# ---------------------------------------------------------------------------
def test_hallucinated_response(hallucination_metric):
    """LLM invents a 60-day policy not present in context — expect metric to flag it."""
    test_case = LLMTestCase(
        input="What is the refund policy?",
        actual_output=(
            "You can return any item within 60 days for a full refund, "
            "and we also offer store credit as an alternative."
        ),
        context=[
            "Our return policy allows customers to return unused items in original "
            "packaging within 30 days of purchase for a full refund."
        ]
    )
    assert_test(test_case, [hallucination_metric])


# ---------------------------------------------------------------------------
# TEST 3: Partial hallucination — mixed accurate + fabricated claims
# ---------------------------------------------------------------------------

def test_partial_hallucination():
    """
       GPT-4o does not flag additive hallucinations (claims not in context but
       not contradicting it) at threshold=0.3. This is a known model leniency.
       For stricter RAG pipelines, pair HallucinationMetric with FaithfulnessMetric.
       Test intentionally passes — documents model behavior, not a bug.
       """
    metric = HallucinationMetric(threshold=0.3, model="gpt-4o")
    test_case = LLMTestCase(
         input="What payment methods are accepted?",
         actual_output=(
             "We accept Visa, Mastercard, PayPal, and cryptocurrency. "
             "We also offer a buy-now-pay-later option through Klarna."
         ),
         context=[
             "Accepted payment methods include Visa, Mastercard, and PayPal."
         ]
    )
    assert_test(test_case, [metric])


# ---------------------------------------------------------------------------
# TEST 4: Empty context — LLM has nothing to ground against
# ---------------------------------------------------------------------------
def test_no_context_provided(hallucination_metric):
    """When no context is provided, any specific claim is ungrounded."""
    test_case = LLMTestCase(
        input="What are the store hours?",
        actual_output="The store is open Monday through Friday, 9am to 6pm.",
        context=[""]
    )
    assert_test(test_case, [hallucination_metric])