"""Safe, deterministic grading without Python exec/eval."""

from __future__ import annotations

import ast
import operator
from dataclasses import dataclass
from typing import Any, Callable

import numpy as np
import pandas as pd

from questions import (
    Question,
    iqr_advanced_data,
    iqr_medium_data,
    missing_advanced_data,
    missing_basic_data,
    sales_data,
    sales_dirty_data,
)


@dataclass(frozen=True)
class GradeResult:
    passed: bool
    summary: str
    error_type: str | None = None
    feedback: str = ""


class SafeCodeError(ValueError):
    def __init__(self, message: str, line: int | None = None) -> None:
        super().__init__(message)
        self.line = line


_BINARY_OPERATORS: dict[type[ast.operator], Callable[[Any, Any], Any]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.BitAnd: operator.and_,
    ast.BitOr: operator.or_,
}

_UNARY_OPERATORS: dict[type[ast.unaryop], Callable[[Any], Any]] = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Invert: operator.invert,
    ast.Not: operator.not_,
}

_COMPARE_OPERATORS: dict[type[ast.cmpop], Callable[[Any, Any], Any]] = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.In: lambda left, right: left in right,
    ast.NotIn: lambda left, right: left not in right,
    ast.Is: operator.is_,
    ast.IsNot: operator.is_not,
}


class SafeAstEvaluator:
    """A deliberately small interpreter for the pandas syntax used in this app."""

    def __init__(self, environment: dict[str, Any], allowed_methods: frozenset[str]) -> None:
        self.environment = environment
        self.allowed_methods = allowed_methods
        self._protected_names = {"pd", "np", "lower", "upper"}

    def run(self, tree: ast.Module) -> dict[str, Any]:
        for statement in tree.body:
            self._statement(statement)
        return self.environment

    def _statement(self, node: ast.stmt) -> None:
        if isinstance(node, ast.Assign):
            if len(node.targets) != 1:
                raise SafeCodeError("한 문장에서는 하나의 대상에만 대입할 수 있습니다.", node.lineno)
            value = self._expression(node.value)
            self._assign(node.targets[0], value)
            return
        if isinstance(node, ast.Expr):
            self._expression(node.value)
            return
        raise SafeCodeError(f"{type(node).__name__} 문법은 이 연습장에서 사용할 수 없습니다.", getattr(node, "lineno", None))

    def _assign(self, target: ast.expr, value: Any) -> None:
        if isinstance(target, ast.Name):
            if target.id.startswith("_") or target.id in self._protected_names:
                raise SafeCodeError(f"'{target.id}' 이름에는 대입할 수 없습니다.", target.lineno)
            self.environment[target.id] = value
            return
        if isinstance(target, ast.Subscript):
            container = self._expression(target.value)
            key = self._expression(target.slice)
            container[key] = value
            return
        raise SafeCodeError("변수 또는 DataFrame 열에만 대입할 수 있습니다.", getattr(target, "lineno", None))

    def _expression(self, node: ast.expr) -> Any:
        if isinstance(node, ast.Name):
            if node.id not in self.environment:
                raise SafeCodeError(f"허용되지 않았거나 아직 정의되지 않은 이름입니다: {node.id}", node.lineno)
            return self.environment[node.id]
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.List):
            return [self._expression(item) for item in node.elts]
        if isinstance(node, ast.Tuple):
            return tuple(self._expression(item) for item in node.elts)
        if isinstance(node, ast.Dict):
            return {
                self._expression(key): self._expression(value)
                for key, value in zip(node.keys, node.values, strict=True)
            }
        if isinstance(node, ast.Subscript):
            return self._expression(node.value)[self._expression(node.slice)]
        if isinstance(node, ast.Slice):
            return slice(
                self._expression(node.lower) if node.lower else None,
                self._expression(node.upper) if node.upper else None,
                self._expression(node.step) if node.step else None,
            )
        if isinstance(node, ast.Attribute):
            if node.attr.startswith("_"):
                raise SafeCodeError("밑줄로 시작하는 속성에는 접근할 수 없습니다.", node.lineno)
            if node.attr not in self.allowed_methods:
                raise SafeCodeError(f"이 문제에서 허용되지 않은 메서드입니다: {node.attr}", node.lineno)
            return getattr(self._expression(node.value), node.attr)
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Attribute):
                raise SafeCodeError("문제에서 허용한 pandas 메서드만 호출할 수 있습니다.", node.lineno)
            function = self._expression(node.func)
            args = [self._expression(argument) for argument in node.args]
            kwargs: dict[str, Any] = {}
            for keyword in node.keywords:
                if keyword.arg is None:
                    raise SafeCodeError("**kwargs 확장은 사용할 수 없습니다.", node.lineno)
                kwargs[keyword.arg] = self._expression(keyword.value)
            return function(*args, **kwargs)
        if isinstance(node, ast.BinOp):
            operation = _BINARY_OPERATORS.get(type(node.op))
            if operation is None:
                raise SafeCodeError("허용되지 않은 이항 연산자입니다.", node.lineno)
            return operation(self._expression(node.left), self._expression(node.right))
        if isinstance(node, ast.UnaryOp):
            operation = _UNARY_OPERATORS.get(type(node.op))
            if operation is None:
                raise SafeCodeError("허용되지 않은 단항 연산자입니다.", node.lineno)
            return operation(self._expression(node.operand))
        if isinstance(node, ast.Compare):
            left = self._expression(node.left)
            comparison = None
            for operation_node, comparator_node in zip(node.ops, node.comparators, strict=True):
                operation = _COMPARE_OPERATORS.get(type(operation_node))
                if operation is None:
                    raise SafeCodeError("허용되지 않은 비교 연산자입니다.", node.lineno)
                right = self._expression(comparator_node)
                current = operation(left, right)
                comparison = current if comparison is None else operator.and_(comparison, current)
                left = right
            return comparison
        raise SafeCodeError(f"{type(node).__name__} 표현식은 사용할 수 없습니다.", getattr(node, "lineno", None))


def _initial_environment(question: Question) -> dict[str, Any]:
    df = question.data_factory().copy(deep=True)
    environment: dict[str, Any] = {"df": df, "pd": pd, "np": np}
    if question.id == "iqr_medium":
        q1 = df["score"].quantile(0.25)
        q3 = df["score"].quantile(0.75)
        iqr = q3 - q1
        environment.update({"lower": q1 - 1.5 * iqr, "upper": q3 + 1.5 * iqr})
    return environment


def _expected_missing_medium() -> pd.DataFrame:
    df = missing_basic_data()
    df["age"] = df["age"].fillna(df["age"].median())
    return df


def _expected_missing_advanced() -> pd.DataFrame:
    df = missing_advanced_data()
    df["age"] = df["age"].fillna(df["age"].median())
    df["city"] = df["city"].fillna(df["city"].mode()[0])
    return df.dropna()


def _expected_iqr_medium() -> pd.DataFrame:
    df = iqr_medium_data()
    q1 = df["score"].quantile(0.25)
    q3 = df["score"].quantile(0.75)
    iqr = q3 - q1
    return df[df["score"].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)]


def _expected_iqr_advanced() -> pd.DataFrame:
    df = iqr_advanced_data()
    q1 = df["value"].quantile(0.25)
    q3 = df["value"].quantile(0.75)
    iqr = q3 - q1
    return df[df["value"].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)]


def _expected_filter_medium() -> pd.DataFrame:
    df = sales_data()
    return df[(df["department"] == "Sales") & (df["sales"] >= 120)]


def _expected_summary_advanced() -> pd.DataFrame:
    df = sales_dirty_data()
    df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
    df = df.dropna(subset=["sales"])
    return df.groupby("department", as_index=False)["sales"].mean()


VALIDATORS: dict[str, Callable[[], pd.DataFrame]] = {
    "missing_medium": _expected_missing_medium,
    "missing_advanced": _expected_missing_advanced,
    "iqr_medium": _expected_iqr_medium,
    "iqr_advanced": _expected_iqr_advanced,
    "filter_medium": _expected_filter_medium,
    "summary_advanced": _expected_summary_advanced,
}


def _compare_dataframe(actual: Any, expected: pd.DataFrame) -> GradeResult:
    if not isinstance(actual, pd.DataFrame):
        return GradeResult(False, "결과가 DataFrame이 아닙니다.", "결과 형식", "마지막 결과를 df에 다시 대입했는지 확인하세요.")
    try:
        pd.testing.assert_frame_equal(actual, expected, check_dtype=True, check_like=False)
    except AssertionError as error:
        detail = " ".join(str(error).split())
        if len(detail) > 300:
            detail = f"{detail[:297]}..."
        return GradeResult(
            False,
            "실행은 완료됐지만 기대한 DataFrame과 다릅니다.",
            "결과 불일치",
            f"현재 크기 {actual.shape}, 기대 크기 {expected.shape}. {detail}",
        )
    return GradeResult(True, "정답입니다! 기대한 데이터 상태와 정확히 일치합니다.", feedback="핵심 변환과 결과의 dtype·인덱스·열 순서까지 확인했습니다.")


def grade_mcq(question: Question, selected_index: int | None) -> GradeResult:
    if selected_index is None:
        return GradeResult(False, "보기를 먼저 선택해 주세요.", "미입력", "정답이라고 생각하는 코드 하나를 고르세요.")
    if selected_index == question.correct_choice:
        return GradeResult(True, "정답입니다!", feedback="코드의 목적과 결과를 올바르게 판단했습니다.")
    return GradeResult(False, "선택한 보기는 정답이 아닙니다.", "오답", question.hint)


def grade_code(question: Question, user_code: str) -> GradeResult:
    code = user_code.strip()
    if not code:
        return GradeResult(False, "코드를 입력해 주세요.", "미입력", question.blank_prompt)
    if len(code) > 800:
        return GradeResult(False, "입력 코드가 너무 깁니다.", "제한 위반", "핵심 변환 코드만 800자 이내로 작성하세요.")

    nonempty_lines = [line for line in code.splitlines() if line.strip()]
    max_statements = 1 if question.difficulty == "중급" else 5
    if len(nonempty_lines) > max_statements:
        return GradeResult(False, f"이 문제는 최대 {max_statements}줄까지 입력할 수 있습니다.", "제한 위반", "핵심 변환만 남겨 주세요.")

    source = question.immutable_template.replace("{{answer}}", code)
    try:
        tree = ast.parse(source, mode="exec")
    except SyntaxError as error:
        line = f" ({error.lineno}번째 줄)" if error.lineno else ""
        return GradeResult(False, f"파이썬 문법을 확인해 주세요{line}.", "SyntaxError", error.msg)

    if len(tree.body) > max_statements:
        return GradeResult(False, f"이 문제는 최대 {max_statements}개의 문장만 허용합니다.", "제한 위반", "세미콜론으로 여러 문장을 연결하지 마세요.")
    if sum(1 for _ in ast.walk(tree)) > 140:
        return GradeResult(False, "코드 구조가 너무 복잡합니다.", "제한 위반", "문제에서 요구한 pandas 변환만 작성하세요.")

    environment = _initial_environment(question)
    try:
        evaluated = SafeAstEvaluator(environment, question.allowed_methods).run(tree)
    except SafeCodeError as error:
        line = f" ({error.line}번째 줄)" if error.line else ""
        return GradeResult(False, f"안전 규칙에 따라 실행하지 않았습니다{line}.", "제한 위반", str(error))
    except Exception as error:  # Deliberately sanitized: no server traceback or paths.
        message = " ".join(str(error).split())[:240]
        return GradeResult(False, "코드를 실행하는 중 오류가 발생했습니다.", type(error).__name__, message)

    if question.validator_id not in VALIDATORS:
        return GradeResult(False, "이 문제의 채점기를 찾을 수 없습니다.", "설정 오류", "관리자에게 문제 ID를 알려 주세요.")
    return _compare_dataframe(evaluated.get("df"), VALIDATORS[question.validator_id]())


def grade_submission(question: Question, answer: int | str | None) -> GradeResult:
    if question.kind == "mcq":
        return grade_mcq(question, answer if isinstance(answer, int) else None)
    return grade_code(question, answer if isinstance(answer, str) else "")
