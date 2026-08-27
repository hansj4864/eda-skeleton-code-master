"""Question catalogue for the EDA Skeleton Code Master MVP."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Literal

import pandas as pd


Difficulty = Literal["초급", "중급", "고급"]
QuestionKind = Literal["mcq", "code_blank"]


@dataclass(frozen=True)
class Question:
    id: str
    title: str
    topic: str
    difficulty: Difficulty
    kind: QuestionKind
    prompt: str
    data_factory: Callable[[], pd.DataFrame]
    preview_config: dict[str, Any] = field(default_factory=lambda: {"rows": 8})
    immutable_template: str = ""
    blank_prompt: str = ""
    choices: tuple[str, ...] = ()
    correct_choice: int | None = None
    validator_id: str | None = None
    allowed_methods: frozenset[str] = frozenset()
    hint: str = ""
    solution: str = ""
    explanation: str = ""


def missing_basic_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": ["민지", "준호", "서연", "도윤", "하린"],
            "age": [22.0, None, 35.0, None, 28.0],
            "city": ["서울", "부산", None, "서울", "대전"],
        }
    )


def missing_advanced_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "age": [20.0, None, 30.0, 40.0, None],
            "city": ["서울", None, "부산", "서울", None],
            "score": [80.0, 90.0, None, 70.0, 60.0],
        }
    )


def iqr_basic_data() -> pd.DataFrame:
    return pd.DataFrame({"score": [10, 12, 13, 14, 15, 100]})


def iqr_medium_data() -> pd.DataFrame:
    return pd.DataFrame({"student": list("ABCDEF"), "score": [50, 51, 49, 52, 48, 120]})


def iqr_advanced_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sample": list("ABCDEFGH"),
            "value": [10, 11, 12, 13, 14, 15, 80, -30],
        }
    )


def sales_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "employee": ["가영", "나영", "다영", "라영", "마영", "바영"],
            "department": ["Sales", "HR", "Sales", "Dev", "Sales", "Dev"],
            "sales": [100, 90, 140, 160, 120, 130],
        }
    )


def sales_dirty_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "department": ["Sales", "Sales", "HR", "HR", "Dev", "Dev"],
            "sales": ["100", "140", "90", "bad", "160", "120"],
        }
    )


def chart_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "month": ["1월", "2월", "3월", "4월"],
            "sales": [100, 125, 118, 150],
            "ad_cost": [20, 25, 22, 31],
        }
    )


QUESTIONS: tuple[Question, ...] = (
    Question(
        id="missing_beginner",
        title="결측치 개수 확인하기",
        topic="결측치",
        difficulty="초급",
        kind="mcq",
        prompt="각 열의 결측치 개수를 한 번에 확인하는 코드로 가장 알맞은 것을 고르세요.",
        data_factory=missing_basic_data,
        choices=(
            'df.dropna()',
            'df.isna().sum()',
            'df.fillna(0)',
            'df.nunique()',
        ),
        correct_choice=1,
        hint="결측 여부를 True/False로 만든 뒤 열별로 합계를 구합니다.",
        solution="df.isna().sum()",
        explanation="isna()는 결측값을 True로 표시하고, sum()은 True를 1로 계산해 열별 결측치 수를 반환합니다. dropna()는 결측 행을 제거하므로 탐색 단계의 답이 아닙니다.",
    ),
    Question(
        id="missing_medium",
        title="중앙값으로 나이 채우기",
        topic="결측치",
        difficulty="중급",
        kind="code_blank",
        prompt="`age` 열의 결측값을 해당 열의 중앙값으로 채우세요. 오른쪽에는 대입문의 우변만 입력합니다.",
        data_factory=missing_basic_data,
        immutable_template='df["age"] = {{answer}}',
        blank_prompt='예: df["age"].어떤함수(...)',
        validator_id="missing_medium",
        allowed_methods=frozenset({"fillna", "median"}),
        hint="먼저 age 열의 median()을 구하고, 그 값을 fillna()에 전달하세요.",
        solution='df["age"].fillna(df["age"].median())',
        explanation="평균보다 이상치의 영향을 덜 받는 중앙값은 수치형 결측치 대체에 자주 사용됩니다. 원본 열에 다시 대입해야 변경 결과가 df에 남습니다.",
    ),
    Question(
        id="missing_advanced",
        title="혼합 결측치 처리 파이프라인",
        topic="결측치",
        difficulty="고급",
        kind="code_blank",
        prompt="age는 중앙값, city는 최빈값으로 채운 뒤 아직 결측치가 남은 행을 제거하세요. 핵심 처리 코드 3줄을 작성합니다.",
        data_factory=missing_advanced_data,
        immutable_template="{{answer}}",
        blank_prompt="3줄의 pandas 변환 코드를 입력하세요.",
        validator_id="missing_advanced",
        allowed_methods=frozenset({"fillna", "median", "mode", "dropna"}),
        hint="mode()는 Series를 반환하므로 첫 번째 값을 선택해야 합니다. 마지막에는 df를 dropna() 결과로 갱신하세요.",
        solution='df["age"] = df["age"].fillna(df["age"].median())\ndf["city"] = df["city"].fillna(df["city"].mode()[0])\ndf = df.dropna()',
        explanation="수치형 age에는 중앙값, 범주형 city에는 최빈값을 적용합니다. score처럼 별도 대체 규칙이 없는 결측 행은 마지막에 제거합니다.",
    ),
    Question(
        id="iqr_beginner",
        title="IQR 공식 고르기",
        topic="이상치·IQR",
        difficulty="초급",
        kind="mcq",
        prompt="IQR(사분위 범위)을 계산하는 코드로 올바른 것을 고르세요.",
        data_factory=iqr_basic_data,
        choices=(
            'df["score"].max() - df["score"].min()',
            'df["score"].quantile(0.25) + df["score"].quantile(0.75)',
            'df["score"].quantile(0.75) - df["score"].quantile(0.25)',
            'df["score"].std() * 2',
        ),
        correct_choice=2,
        hint="IQR은 제3사분위수(Q3)와 제1사분위수(Q1)의 차이입니다.",
        solution='df["score"].quantile(0.75) - df["score"].quantile(0.25)',
        explanation="IQR = Q3 - Q1입니다. 전체 범위(max-min)와 달리 양끝 극단값의 영향을 상대적으로 덜 받습니다.",
    ),
    Question(
        id="iqr_medium",
        title="IQR 범위로 이상치 제거",
        topic="이상치·IQR",
        difficulty="중급",
        kind="code_blank",
        prompt="서버가 계산해 둔 `lower`, `upper`를 사용해 정상 범위의 행만 남기세요. 대입문의 우변만 입력합니다.",
        data_factory=iqr_medium_data,
        immutable_template="df = {{answer}}",
        blank_prompt='예: df[df["score"].어떤함수(lower, upper)]',
        validator_id="iqr_medium",
        allowed_methods=frozenset({"between"}),
        hint="Series.between(lower, upper)는 양 끝값을 포함하는 불리언 마스크를 반환합니다.",
        solution='df[df["score"].between(lower, upper)]',
        explanation="between()으로 하한 이상·상한 이하인 행만 선택합니다. 이 문제의 120점은 상한을 넘어 제거됩니다.",
    ),
    Question(
        id="iqr_advanced",
        title="IQR 경계 직접 계산하기",
        topic="이상치·IQR",
        difficulty="고급",
        kind="code_blank",
        prompt="value 열에서 Q1, Q3, IQR과 경계를 직접 계산하고 정상 범위 행만 남기세요. 최대 5개의 문장을 사용할 수 있습니다.",
        data_factory=iqr_advanced_data,
        immutable_template="{{answer}}",
        blank_prompt="Q1, Q3, IQR 계산과 필터링 코드를 입력하세요.",
        validator_id="iqr_advanced",
        allowed_methods=frozenset({"quantile", "between"}),
        hint="마지막 문장은 df = df[df['value'].between(...)] 형태로 작성할 수 있습니다.",
        solution='q1 = df["value"].quantile(0.25)\nq3 = df["value"].quantile(0.75)\niqr = q3 - q1\ndf = df[df["value"].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)]',
        explanation="Q1-1.5×IQR과 Q3+1.5×IQR 사이만 남기는 전형적인 Tukey 방식입니다. 경계값은 정상 범위에 포함합니다.",
    ),
    Question(
        id="filter_beginner",
        title="조건 필터링 코드 찾기",
        topic="필터링·요약",
        difficulty="초급",
        kind="mcq",
        prompt="Sales 부서 직원만 선택하는 올바른 코드를 고르세요.",
        data_factory=sales_data,
        choices=(
            'df[df["department"] = "Sales"]',
            'df[df["department"] == "Sales"]',
            'df.select("department" == "Sales")',
            'df.where("Sales")',
        ),
        correct_choice=1,
        hint="비교에는 대입 연산자 하나가 아니라 등호 두 개를 사용합니다.",
        solution='df[df["department"] == "Sales"]',
        explanation="Series 비교로 만들어진 불리언 마스크를 df의 대괄호 안에 넣으면 조건에 맞는 행만 선택됩니다.",
    ),
    Question(
        id="filter_medium",
        title="복합 조건으로 행 선택",
        topic="필터링·요약",
        difficulty="중급",
        kind="code_blank",
        prompt="Sales 부서이면서 sales가 120 이상인 행만 남기세요. 대입문의 우변만 입력합니다.",
        data_factory=sales_data,
        immutable_template="df = {{answer}}",
        blank_prompt='df[(조건1) & (조건2)]',
        validator_id="filter_medium",
        allowed_methods=frozenset(),
        hint="pandas 복합 조건은 각 비교식을 괄호로 묶고 `&`로 연결합니다.",
        solution='df[(df["department"] == "Sales") & (df["sales"] >= 120)]',
        explanation="파이썬의 and가 아니라 원소별 논리 연산자 &를 사용합니다. 연산자 우선순위 때문에 각 조건의 괄호도 중요합니다.",
    ),
    Question(
        id="summary_advanced",
        title="문자열 매출 정제와 그룹 요약",
        topic="필터링·요약",
        difficulty="고급",
        kind="code_blank",
        prompt="sales를 숫자로 변환하고 변환 실패 행을 제거한 뒤, 부서별 평균 매출 DataFrame을 만드세요. 핵심 코드 3줄을 작성합니다.",
        data_factory=sales_dirty_data,
        immutable_template="{{answer}}",
        blank_prompt="자료형 변환 → 결측 제거 → 그룹 평균 순서로 작성하세요.",
        validator_id="summary_advanced",
        allowed_methods=frozenset({"to_numeric", "dropna", "groupby", "mean"}),
        hint="pd.to_numeric(..., errors='coerce')로 변환 실패값을 NaN으로 만든 뒤, groupby(..., as_index=False)를 사용하세요.",
        solution='df["sales"] = pd.to_numeric(df["sales"], errors="coerce")\ndf = df.dropna(subset=["sales"])\ndf = df.groupby("department", as_index=False)["sales"].mean()',
        explanation="errors='coerce'는 잘못된 문자열을 NaN으로 바꿉니다. 제거 후 as_index=False로 그룹 키가 일반 열인 결과를 만듭니다.",
    ),
    Question(
        id="viz_beginner",
        title="추세를 보여주는 차트",
        topic="시각화",
        difficulty="초급",
        kind="mcq",
        prompt="월별 매출의 시간 흐름에 따른 추세를 보여주기에 가장 적절한 코드를 고르세요.",
        data_factory=chart_data,
        choices=(
            'plt.plot(df["month"], df["sales"])',
            'plt.pie(df["sales"])',
            'plt.hist(df["month"])',
            'plt.scatter(df["month"], df["month"])',
        ),
        correct_choice=0,
        hint="시간 순서에 따른 연속적인 변화를 강조하는 차트를 생각하세요.",
        solution='plt.plot(df["month"], df["sales"])',
        explanation="선 그래프는 순서가 있는 시간축에서 값의 상승·하락 추세를 확인하기 좋습니다.",
    ),
    Question(
        id="viz_medium",
        title="축 라벨 올바르게 지정하기",
        topic="시각화",
        difficulty="중급",
        kind="mcq",
        prompt="월별 매출 막대그래프에 x축과 y축 라벨을 올바르게 붙이는 코드 묶음을 고르세요.",
        data_factory=chart_data,
        choices=(
            'plt.bar(df["month"], df["sales"]); plt.xlabel("월"); plt.ylabel("매출")',
            'plt.bar(df["sales"], df["month"]); plt.xlabel("월"); plt.ylabel("매출")',
            'plt.bar(df["month"], df["sales"]); plt.title("월"); plt.legend("매출")',
            'plt.hist(df["sales"]); plt.xlabel("월"); plt.ylabel("매출")',
        ),
        correct_choice=0,
        hint="bar(x, height)의 첫 인자는 범주, 두 번째는 막대 높이입니다.",
        solution='plt.bar(df["month"], df["sales"]); plt.xlabel("월"); plt.ylabel("매출")',
        explanation="월이 x축 범주이고 매출이 막대 높이입니다. xlabel과 ylabel은 각각 해당 축의 의미를 설명해야 합니다.",
    ),
    Question(
        id="viz_advanced",
        title="두 수치 변수의 관계 확인하기",
        topic="시각화",
        difficulty="고급",
        kind="mcq",
        prompt="광고비와 매출의 관계를 살펴보고 싶을 때 가장 적절한 코드와 해석을 고르세요.",
        data_factory=chart_data,
        choices=(
            'plt.scatter(df["ad_cost"], df["sales"]); 점의 패턴으로 두 변수의 관계를 본다.',
            'plt.pie(df["ad_cost"]); 두 변수의 상관계수를 직접 계산한다.',
            'plt.hist(df["month"]); 광고비와 매출의 인과관계를 증명한다.',
            'plt.bar(df["month"], df["sales"]); 두 수치 변수의 분포를 동시에 비교한다.',
        ),
        correct_choice=0,
        hint="두 수치형 변수의 짝을 좌표평면에 점으로 나타내는 그래프를 고르세요.",
        solution='plt.scatter(df["ad_cost"], df["sales"])',
        explanation="산점도는 두 수치 변수의 방향·형태·이상치를 탐색하는 데 적합합니다. 관찰된 연관성만으로 인과관계를 증명할 수는 없습니다.",
    ),
)


QUESTION_BY_ID = {question.id: question for question in QUESTIONS}

