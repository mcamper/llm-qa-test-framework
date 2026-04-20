import os
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import GEval
from deepeval.metrics.g_eval import Rubric

os.environ["OPENAI_API_KEY"] = ""

def test_rubric_score():
    test_case = LLMTestCase(
        input="Where is the Eiffel Tower located?",
        actual_output="The Eiffel Tower is located in Paris, France.",
        expected_output="The Eiffel Tower is located in Paris."
    )

    rubric_metric = GEval(
        name="Location Accuracy",
        criteria="Evaluate how accurately the response answers the location question based on the expected output.",
        evaluation_params=[
            LLMTestCaseParams.ACTUAL_OUTPUT,
            LLMTestCaseParams.EXPECTED_OUTPUT
        ],
        rubric=[
            Rubric(score_range=(0, 2), expected_outcome="Incorrect or irrelevant answer."),
            Rubric(score_range=(3, 5), expected_outcome="Partially correct but missing key details."),
            Rubric(score_range=(6, 8), expected_outcome="Mostly correct with minor gaps."),
            Rubric(score_range=(9, 10), expected_outcome="Fully accurate and complete answer."),
        ],
        threshold=0.5
    )

    assert_test(test_case, [rubric_metric])