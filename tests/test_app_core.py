from __future__ import annotations

import ast
import concurrent.futures
import unittest
from pathlib import Path

from grading import GradeResult, grade_submission
from questions import QUESTION_BY_ID, QUESTIONS


class QuestionCatalogueTests(unittest.TestCase):
    def test_catalogue_has_expected_mix(self) -> None:
        self.assertEqual(60, len(QUESTIONS))
        self.assertEqual(60, len({question.id for question in QUESTIONS}))
        self.assertEqual(45, sum(question.topic != "시각화" for question in QUESTIONS))
        self.assertEqual(15, sum(question.topic == "시각화" for question in QUESTIONS))
        self.assertEqual(30, sum(question.kind == "mcq" for question in QUESTIONS))
        self.assertEqual(30, sum(question.kind == "code_blank" for question in QUESTIONS))
        for topic in ("결측치", "이상치·IQR", "필터링·요약", "시각화"):
            self.assertEqual(15, sum(question.topic == topic for question in QUESTIONS))
        for difficulty in ("초급", "중급", "고급"):
            self.assertEqual(20, sum(question.difficulty == difficulty for question in QUESTIONS))

    def test_every_question_has_learning_feedback(self) -> None:
        for question in QUESTIONS:
            with self.subTest(question=question.id):
                self.assertTrue(question.prompt)
                self.assertTrue(question.hint)
                self.assertTrue(question.solution)
                self.assertTrue(question.explanation)
                self.assertFalse(question.data_factory().empty)

    def test_data_factories_return_fresh_dataframes(self) -> None:
        question = QUESTION_BY_ID["missing_medium"]
        first = question.data_factory()
        first.loc[0, "age"] = 999
        second = question.data_factory()
        self.assertNotEqual(999, second.loc[0, "age"])


class GradingTests(unittest.TestCase):
    def test_all_official_solutions_pass(self) -> None:
        for question in QUESTIONS:
            answer = question.correct_choice if question.kind == "mcq" else question.solution
            with self.subTest(question=question.id):
                result = grade_submission(question, answer)
                self.assertTrue(result.passed, result)

    def test_all_mcq_questions_reject_a_wrong_choice_and_blank(self) -> None:
        for question in (item for item in QUESTIONS if item.kind == "mcq"):
            wrong = next(index for index in range(len(question.choices)) if index != question.correct_choice)
            with self.subTest(question=question.id):
                self.assertFalse(grade_submission(question, wrong).passed)
                blank = grade_submission(question, None)
                self.assertFalse(blank.passed)
                self.assertEqual("미입력", blank.error_type)

    def test_code_questions_reject_blank_syntax_error_and_wrong_result(self) -> None:
        question = QUESTION_BY_ID["missing_medium"]
        cases = (
            ("", "미입력"),
            ('df["age"].fillna(', "SyntaxError"),
            ('df["age"].fillna(0)', "결과 불일치"),
        )
        for answer, expected_error in cases:
            with self.subTest(answer=answer):
                result = grade_submission(question, answer)
                self.assertFalse(result.passed)
                self.assertEqual(expected_error, result.error_type)

    def test_repeated_submission_always_starts_from_fresh_data(self) -> None:
        question = QUESTION_BY_ID["missing_advanced"]
        first = grade_submission(question, question.solution)
        wrong = grade_submission(question, 'df = df.dropna()')
        second = grade_submission(question, question.solution)
        self.assertTrue(first.passed)
        self.assertFalse(wrong.passed)
        self.assertTrue(second.passed)

    def test_security_payloads_are_never_run(self) -> None:
        question = QUESTION_BY_ID["missing_advanced"]
        payloads = (
            "import os",
            'open("should-not-exist.txt", "w")',
            "while True:\n    pass",
            "df.__class__",
            'exec("df = None")',
            'eval("1 + 1")',
            '__import__("os")',
        )
        for payload in payloads:
            with self.subTest(payload=payload):
                result = grade_submission(question, payload)
                self.assertIsInstance(result, GradeResult)
                self.assertFalse(result.passed)
                self.assertIn(result.error_type, {"제한 위반", "SyntaxError"})
        self.assertFalse(Path("should-not-exist.txt").exists())

    def test_grader_does_not_call_python_exec_or_eval(self) -> None:
        source = Path("grading.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        dangerous_calls = [
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in {"exec", "eval"}
        ]
        self.assertEqual([], dangerous_calls)

    def test_twenty_concurrent_submissions_are_isolated(self) -> None:
        question = QUESTION_BY_ID["summary_advanced"]
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
            results = list(pool.map(lambda _: grade_submission(question, question.solution), range(20)))
        self.assertEqual(20, len(results))
        self.assertTrue(all(result.passed for result in results))


if __name__ == "__main__":
    unittest.main()
