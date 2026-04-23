import openai
import pytest

client = openai.OpenAI()

# --- Test fixtures: context + question + expected behavior ---

RAG_CASES = [
    {
        "id": "supported_claim",
        "context": "The Eiffel Tower was completed in 1889 and stands 330 meters tall.",
        "question": "When was the Eiffel Tower completed?",
        "expect": "faithful",
    },
    {
        "id": "contradiction",
        "context": "The Eiffel Tower was completed in 1889 and stands 330 meters tall.",
        "question": "How tall is the Eiffel Tower?",
        "inject_bad_answer": "The Eiffel Tower is 500 meters tall.",  # forced wrong answer
        "expect": "unfaithful",
    },
    {
        "id": "drift_beyond_context",
        "context": "Python is a high-level programming language created by Guido van Rossum.",
        "question": "What are Python's most popular libraries?",
        "expect": "unfaithful",  # context doesn't mention libraries — model will drift
    },
]


def ask_model(context: str, question: str) -> str:
    prompt = f"""You are a helpful assistant. Answer ONLY using the context below.
If the answer is not in the context, say: 'Not found in context.'

Context:
{context}

Question: {question}
Answer:"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


def evaluate_faithfulness(answer: str, context: str) -> str:
    """Ask GPT-4o to judge whether the answer is faithful to the context."""
    judge_prompt = f"""You are a strict QA evaluator.

Context: {context}
Answer: {answer}

Is this answer faithful to the context?
- 'faithful' = answer is supported by or consistent with the context
- 'faithful' = answer says 'not found in context' or declines to answer (this is correct behavior)
- 'unfaithful' = answer contradicts or fabricates information not in the context

Respond with exactly one word: faithful or unfaithful."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": judge_prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip().lower()


# --- Tests ---

class TestFaithfulness:

    def test_supported_claim(self):
        case = next(c for c in RAG_CASES if c["id"] == "supported_claim")
        answer = ask_model(case["context"], case["question"])
        verdict = evaluate_faithfulness(answer, case["context"])
        print(f"\n[supported_claim]\nAnswer: {answer}\nVerdict: {verdict}")
        assert verdict == "faithful", f"Expected faithful, got: {verdict}"

    def test_contradiction_detected(self):
        case = next(c for c in RAG_CASES if c["id"] == "contradiction")
        # Use the injected bad answer directly to test the evaluator
        bad_answer = case["inject_bad_answer"]
        verdict = evaluate_faithfulness(bad_answer, case["context"])
        print(f"\n[contradiction]\nAnswer: {bad_answer}\nVerdict: {verdict}")
        assert verdict == "unfaithful", f"Expected unfaithful, got: {verdict}"

    def test_drift_soft_prompt(self):
        """Soft grounding — model may drift when instruction is weak."""
        context = "Python is a high-level programming language created by Guido van Rossum."
        question = "What are Python's most popular libraries?"

        prompt = f"""Answer based on the context if possible.

    Context: {context}

    Question: {question}
    Answer:"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        answer = response.choices[0].message.content.strip()
        verdict = evaluate_faithfulness(answer, context)

        print(f"\n[drift_soft_prompt]\nAnswer: {answer}\nVerdict: {verdict}")

        # Document the behavior — don't force a pass/fail yet
        # This is an observation test
        assert verdict in ["faithful", "unfaithful"], "Evaluator returned unexpected value"

    def test_drift_no_grounding(self):
        """No grounding instruction — model answers freely from training data."""
        context = "Python is a high-level programming language created by Guido van Rossum."
        question = "What are Python's most popular libraries?"

        prompt = f"""Context: {context}

    Question: {question}
    Answer:"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        answer = response.choices[0].message.content.strip()
        verdict = evaluate_faithfulness(answer, context)

        print(f"\n[drift_no_grounding]\nAnswer: {answer}\nVerdict: {verdict}")

        # Hypothesis: model will drift and evaluator should catch it
        assert verdict == "unfaithful", (
            f"FINDING: Model stayed grounded even without instruction.\n"
            f"Answer: {answer}"
        )

    def test_drift_ambiguous_context(self):
        """Ambiguous context — model may fill gaps with assumptions."""
        context = "NumPy is widely used in scientific computing. Many developers rely on it daily."
        question = "What are the most popular Python libraries for data science?"

        prompt = f"""You are a helpful assistant. Answer ONLY using the context below.
    If the answer is not in the context, say: 'Not found in context.'

    Context: {context}

    Question: {question}
    Answer:"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        answer = response.choices[0].message.content.strip()
        verdict = evaluate_faithfulness(answer, context)

        print(f"\n[drift_ambiguous_context]\nAnswer: {answer}\nVerdict: {verdict}")

        # Context mentions NumPy but not "data science libraries" broadly
        # Model may extrapolate — that's the drift we're catching
        # Replace the assert with this:
        assert verdict == "faithful" or "not found" in answer.lower(), (
            f"FINDING: Evaluator flagged a valid refusal as unfaithful.\n"
            f"Answer: {answer}\nVerdict: {verdict}\n"
            f"Note: Model correctly refused. Evaluator needs refusal handling."
        )

    # def test_drift_beyond_context(self):
    #     case = next(c for c in RAG_CASES if c["id"] == "drift_beyond_context")
    #     answer = ask_model(case["context"], case["question"])
    #     verdict = evaluate_faithfulness(answer, case["context"])
    #     print(f"\n[drift]\nAnswer: {answer}\nVerdict: {verdict}")
    #     # Model should say 'Not found in context' OR evaluator catches the drift
    #     assert verdict == "unfaithful" or "not found" in answer.lower(), \
    #         f"Expected drift to be caught. Answer: {answer}, Verdict: {verdict}"