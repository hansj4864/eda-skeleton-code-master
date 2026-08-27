"""Additional question bank: 48 questions and their expected DataFrames."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pandas as pd

from question_models import Difficulty, Question


def missing_people_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": ["가람", "나래", "다온", "라온", "마루", "보라"],
            "age": [21.0, None, None, 32.0, 28.0, 35.0],
            "city": ["서울", None, "부산", "서울", None, "대전"],
            "score": [88.0, 91.0, None, 76.0, 84.0, None],
        }
    )


def missing_class_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "class": ["A", "A", "A", "B", "B", "B", None],
            "score": [80.0, None, 100.0, 70.0, 90.0, None, 85.0],
            "attendance": [10.0, 9.0, None, 8.0, None, 10.0, 7.0],
        }
    )


def missing_sensor_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sensor": list("ABCDEF"),
            "value": [12.0, -999.0, 15.0, None, 18.0, -999.0],
            "status": ["ok", "error", "ok", "error", "ok", "error"],
        }
    )


def missing_income_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": ["윤서", "지후", None, "서준", "하윤"],
            "income": ["3200", "unknown", "4100", None, "3700"],
        }
    )


def outlier_value_data() -> pd.DataFrame:
    return pd.DataFrame({"id": list("ABCDEFGHIJ"), "value": [10, 11, 12, 12, 13, 14, 15, 16, 70, -25]})


def standardized_value_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id": list("ABCDEFGHIJ"),
            "value": [-0.8, -0.4, -0.2, 0.0, 0.2, 0.4, 0.8, 1.1, 2.9, -3.2],
        }
    )


def outlier_sales_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "store": list("ABCDEFGH"),
            "sales": [105, 110, 112, 115, 119, 125, 480, 40],
        }
    )


def grouped_outlier_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "group": ["A"] * 6 + ["B"] * 6,
            "value": [10, 11, 11, 12, 13, 50, 100, 102, 103, 104, 105, 180],
        }
    )


def employee_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "employee": ["가영", "나영", "다영", "라영", "마영", "바영", "사영", "아영"],
            "department": ["Sales", "HR", "Sales", "Dev", "Sales", "Dev", "HR", "Dev"],
            "sales": [100, 90, 145, 160, 120, 130, 105, 175],
        }
    )


def dirty_order_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order": list("ABCDEFGH"),
            "category": ["Book", "Book", "Food", "Food", "Tech", "Tech", "Book", "Food"],
            "amount": ["30", "45", "20", "bad", "120", "80", "25", "35"],
        }
    )


def quarterly_sales_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "department": ["Sales", "Sales", "Dev", "Dev", "HR", "HR"],
            "quarter": ["Q1", "Q2", "Q1", "Q2", "Q1", "Q2"],
            "sales": [100, 130, 150, 170, 80, 90],
            "employee": ["가", "나", "다", "라", "마", "바"],
        }
    )


def chart_category_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "category": ["A", "B", "C", "D"],
            "value": [32, 45, 28, 51],
            "cost": [20, 30, 25, 38],
        }
    )


def chart_distribution_data() -> pd.DataFrame:
    return pd.DataFrame({"score": [55, 62, 67, 70, 72, 74, 78, 81, 84, 90, 96]})


def chart_dense_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "x": [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
            "y": [2, 2.1, 2.2, 3, 3.1, 3.2, 4, 4.1, 4.2, 5, 5.1, 5.2],
        }
    )


def _mcq(
    question_id: str,
    title: str,
    topic: str,
    difficulty: Difficulty,
    prompt: str,
    data_factory: Callable[[], pd.DataFrame],
    choices: tuple[str, ...],
    correct_choice: int,
    hint: str,
    solution: str,
    explanation: str,
) -> Question:
    return Question(
        id=question_id,
        title=title,
        topic=topic,
        difficulty=difficulty,
        kind="mcq",
        prompt=prompt,
        data_factory=data_factory,
        choices=choices,
        correct_choice=correct_choice,
        hint=hint,
        solution=solution,
        explanation=explanation,
    )


def _code(
    question_id: str,
    title: str,
    topic: str,
    difficulty: Difficulty,
    prompt: str,
    data_factory: Callable[[], pd.DataFrame],
    template: str,
    blank_prompt: str,
    allowed_methods: set[str],
    hint: str,
    solution: str,
    explanation: str,
) -> Question:
    return Question(
        id=question_id,
        title=title,
        topic=topic,
        difficulty=difficulty,
        kind="code_blank",
        prompt=prompt,
        data_factory=data_factory,
        immutable_template=template,
        blank_prompt=blank_prompt,
        validator_id=question_id,
        allowed_methods=frozenset(allowed_methods),
        hint=hint,
        solution=solution,
        explanation=explanation,
    )


EXTRA_QUESTIONS: tuple[Question, ...] = (
    # 결측치: 초급 4개
    _mcq(
        "missing_beginner_any",
        "결측치가 있는 열 찾기",
        "결측치",
        "초급",
        "열마다 결측치가 하나라도 있는지 확인하는 코드를 고르세요.",
        missing_people_data,
        ("df.isna().any()", "df.isna().all()", "df.dropna()", "df.empty"),
        0,
        "any()는 하나라도 True인지 확인합니다.",
        "df.isna().any()",
        "isna()가 만든 불리언 DataFrame에 any()를 적용하면 열별 결측치 존재 여부를 얻습니다. all()은 모든 값이 결측인지 확인하므로 의미가 다릅니다.",
    ),
    _mcq(
        "missing_beginner_drop_subset",
        "특정 열 기준으로 행 제거",
        "결측치",
        "초급",
        "score가 결측인 행만 제거하는 코드를 고르세요.",
        missing_people_data,
        ('df.dropna(subset=["score"])', 'df.dropna(axis=1)', 'df["score"].drop_duplicates()', 'df.fillna("score")'),
        0,
        "dropna의 subset에 기준 열 이름을 리스트로 전달합니다.",
        'df.dropna(subset=["score"])',
        "subset을 사용하면 다른 열에 결측치가 있더라도 score가 유효한 행은 유지됩니다. axis=1은 결측치가 있는 열 자체를 제거합니다.",
    ),
    _mcq(
        "missing_beginner_constant",
        "범주형 결측치 상수 대체",
        "결측치",
        "초급",
        "city의 결측값을 '미정'으로 바꾸는 코드를 고르세요.",
        missing_people_data,
        ('df["city"].fillna("미정")', 'df["city"].dropna("미정")', 'df.fillna("city")', 'df["city"].isna("미정")'),
        0,
        "값을 채우는 Series 메서드를 찾으세요.",
        'df["city"].fillna("미정")',
        "fillna에 상수를 전달하면 결측 위치만 해당 값으로 대체합니다. 반환값을 원본 열에 대입해야 DataFrame 변경이 유지됩니다.",
    ),
    _mcq(
        "missing_beginner_notna",
        "유효값 개수 세기",
        "결측치",
        "초급",
        "각 열에서 결측치가 아닌 값의 개수를 계산하는 코드를 고르세요.",
        missing_people_data,
        ("df.notna().sum()", "df.isna().sum()", "df.count(axis=1)", "df.size"),
        0,
        "notna()는 유효값을 True로 표시합니다.",
        "df.notna().sum()",
        "notna().sum()은 열별 유효값 개수를 반환합니다. isna().sum()은 반대로 결측값 개수를 반환합니다.",
    ),
    # 결측치: 중급 4개
    _code(
        "missing_medium_ffill",
        "직전 값으로 결측치 채우기",
        "결측치",
        "중급",
        "age의 결측값을 바로 앞의 유효값으로 채우세요. 우변만 입력합니다.",
        missing_people_data,
        'df["age"] = {{answer}}',
        'df["age"].어떤함수()',
        {"ffill"},
        "앞 방향 채우기는 forward fill입니다.",
        'df["age"].ffill()',
        "ffill()은 위에서 아래로 진행하며 마지막으로 관측된 유효값을 전달합니다. 첫 행이 결측이면 앞 값이 없으므로 그대로 남을 수 있습니다.",
    ),
    _code(
        "missing_medium_constant",
        "도시 미상값 표시하기",
        "결측치",
        "중급",
        "city 결측값을 '미정'으로 채우세요. 우변만 입력합니다.",
        missing_people_data,
        'df["city"] = {{answer}}',
        'df["city"].어떤함수("미정")',
        {"fillna"},
        "fillna에 문자열을 전달하세요.",
        'df["city"].fillna("미정")',
        "범주형 열은 업무 의미가 분명한 별도 범주로 대체할 수 있습니다. '미정'은 실제 도시와 결측 상태를 구분해 줍니다.",
    ),
    _code(
        "missing_medium_drop_score",
        "점수 결측 행만 제거하기",
        "결측치",
        "중급",
        "score가 결측인 행만 제거한 DataFrame을 만드세요. 우변만 입력합니다.",
        missing_people_data,
        "df = {{answer}}",
        'df.dropna(subset=["열이름"])',
        {"dropna"},
        "subset에는 문자열이 아니라 열 이름 리스트를 전달합니다.",
        'df.dropna(subset=["score"])',
        "분석의 핵심 변수만 subset으로 지정하면 불필요한 데이터 손실을 줄일 수 있습니다. 다른 열의 결측치는 이 단계에서 행 제거 조건이 아닙니다.",
    ),
    _code(
        "missing_medium_group_mean",
        "반별 평균으로 점수 채우기",
        "결측치",
        "중급",
        "각 class의 평균 score로 같은 반의 결측 score를 채우세요. 우변만 입력합니다.",
        missing_class_data,
        'df["score"] = {{answer}}',
        "groupby와 transform을 조합한 한 줄 표현식",
        {"fillna", "groupby", "transform"},
        "그룹 평균을 원래 행 길이로 돌려주는 transform('mean')을 사용하세요.",
        'df["score"].fillna(df.groupby("class")["score"].transform("mean"))',
        "transform은 그룹별 통계를 원본과 같은 길이의 Series로 확장합니다. 따라서 class별 평균을 각 행에 맞춰 결측 위치에 채울 수 있습니다.",
    ),
    # 결측치: 고급 4개
    _code(
        "missing_advanced_mixed",
        "혼합형 대체와 핵심행 유지",
        "결측치",
        "고급",
        "age는 평균, city는 최빈값으로 채우고 score 결측 행을 제거하세요.",
        missing_people_data,
        "{{answer}}",
        "3줄의 처리 파이프라인",
        {"fillna", "mean", "mode", "dropna"},
        "수치형과 범주형을 다르게 처리한 뒤 subset으로 제거하세요.",
        'df["age"] = df["age"].fillna(df["age"].mean())\ndf["city"] = df["city"].fillna(df["city"].mode()[0])\ndf = df.dropna(subset=["score"])',
        "age에는 평균, city에는 최빈값을 사용합니다. score는 분석 핵심값이라는 가정으로 임의 대체하지 않고 해당 행만 제거합니다.",
    ),
    _code(
        "missing_advanced_sentinel",
        "센티널 값을 결측치로 정리",
        "결측치",
        "고급",
        "value의 -999를 NaN으로 바꾸고 중앙값으로 모든 value 결측치를 채우세요.",
        missing_sensor_data,
        "{{answer}}",
        "센티널 변환과 중앙값 대체 2줄",
        {"replace", "nan", "fillna", "median"},
        "np.nan으로 바꾼 뒤 같은 열의 median을 사용하세요.",
        'df["value"] = df["value"].replace(-999, np.nan)\ndf["value"] = df["value"].fillna(df["value"].median())',
        "-999처럼 시스템이 결측을 대신해 저장한 값은 통계 계산 전에 실제 NaN으로 통일해야 합니다. 그렇지 않으면 중앙값과 평균이 왜곡될 수 있습니다.",
    ),
    _code(
        "missing_advanced_income",
        "문자형 소득 정제하기",
        "결측치",
        "고급",
        "income을 숫자로 변환하고 실패값을 중앙값으로 채운 뒤 name 결측 행을 제거하세요.",
        missing_income_data,
        "{{answer}}",
        "자료형 변환, 대체, 제거 3줄",
        {"to_numeric", "fillna", "median", "dropna"},
        "to_numeric의 errors='coerce'를 사용하세요.",
        'df["income"] = pd.to_numeric(df["income"], errors="coerce")\ndf["income"] = df["income"].fillna(df["income"].median())\ndf = df.dropna(subset=["name"])',
        "문자열 unknown과 None을 숫자 변환 과정에서 NaN으로 통일합니다. 숫자로 변환된 유효값의 중앙값을 사용한 뒤 식별자 name이 없는 행은 제거합니다.",
    ),
    _code(
        "missing_advanced_class",
        "그룹 대체와 출석값 정리",
        "결측치",
        "고급",
        "반별 평균 score로 결측치를 채우고 attendance 결측치는 0으로 채운 뒤 class 결측 행을 제거하세요.",
        missing_class_data,
        "{{answer}}",
        "그룹 대체, 상수 대체, 행 제거 3줄",
        {"fillna", "groupby", "transform", "dropna"},
        "score에는 transform('mean'), attendance에는 0을 사용하세요.",
        'df["score"] = df["score"].fillna(df.groupby("class")["score"].transform("mean"))\ndf["attendance"] = df["attendance"].fillna(0)\ndf = df.dropna(subset=["class"])',
        "그룹별 수준 차이가 있는 score는 전체 평균보다 반별 평균이 자연스럽습니다. 출석 결측을 0으로 보는 규칙은 문제의 업무 가정이며, 실제 분석에서는 결측 의미를 먼저 확인해야 합니다.",
    ),
    # 이상치·IQR: 초급 4개
    _mcq(
        "iqr_beginner_q1",
        "제1사분위수 계산",
        "이상치·IQR",
        "초급",
        "value 열의 Q1을 계산하는 코드를 고르세요.",
        outlier_value_data,
        ('df["value"].quantile(0.25)', 'df["value"].quantile(0.50)', 'df["value"].quantile(0.75)', 'df["value"].mean()'),
        0,
        "Q1은 데이터의 25% 지점입니다.",
        'df["value"].quantile(0.25)',
        "Q1은 25번째 백분위수이므로 quantile(0.25)를 사용합니다. 0.50은 중앙값, 0.75는 Q3입니다.",
    ),
    _mcq(
        "iqr_beginner_bounds",
        "IQR 이상치 경계 공식",
        "이상치·IQR",
        "초급",
        "Tukey 방식의 정상 범위 경계로 올바른 것을 고르세요.",
        outlier_value_data,
        ("Q1 - 1.5*IQR, Q3 + 1.5*IQR", "Q1 - IQR, Q3 + IQR", "평균 - IQR, 평균 + IQR", "최솟값, 최댓값"),
        0,
        "사분위수에서 IQR의 1.5배만큼 바깥으로 확장합니다.",
        "lower = Q1 - 1.5*IQR; upper = Q3 + 1.5*IQR",
        "1.5×IQR 규칙은 이상치 후보를 탐색하는 흔한 기준입니다. 경계를 벗어났다고 무조건 삭제하기보다 데이터 오류인지 실제 희귀 사례인지 확인해야 합니다.",
    ),
    _mcq(
        "iqr_beginner_boxplot",
        "박스플롯의 상자 이해하기",
        "이상치·IQR",
        "초급",
        "일반적인 박스플롯에서 상자의 아래·위 경계가 나타내는 값을 고르세요.",
        outlier_value_data,
        ("Q1과 Q3", "최솟값과 최댓값", "평균과 표준편차", "0과 중앙값"),
        0,
        "상자의 높이가 바로 IQR입니다.",
        "상자 아래=Q1, 상자 위=Q3",
        "박스 자체는 중앙 50% 구간인 Q1부터 Q3까지를 나타냅니다. 상자 내부 선은 보통 중앙값이고, 수염 밖의 점은 이상치 후보입니다.",
    ),
    _mcq(
        "iqr_beginner_robust",
        "이상치에 강한 통계량",
        "이상치·IQR",
        "초급",
        "극단값이 있는 데이터의 중심과 산포를 요약하기에 상대적으로 안정적인 조합을 고르세요.",
        outlier_value_data,
        ("중앙값과 IQR", "평균과 범위", "합계와 최댓값", "평균과 분산만"),
        0,
        "순위에 기반한 통계량을 찾으세요.",
        "중앙값과 IQR",
        "중앙값과 IQR은 값의 순위에 기반하므로 극단값 하나가 결과를 크게 끌어당기지 않습니다. 평균과 표준편차도 유용하지만 이상치에 더 민감합니다.",
    ),
    # 이상치·IQR: 중급 4개
    _code(
        "iqr_medium_upper_quantile",
        "상위 5% 극단값 제거",
        "이상치·IQR",
        "중급",
        "value의 95번째 백분위수 이하인 행만 남기세요. 우변만 입력합니다.",
        outlier_value_data,
        "df = {{answer}}",
        "quantile(0.95)를 조건에 직접 사용",
        {"quantile"},
        "불리언 필터의 오른쪽에 95% 분위수를 계산하세요.",
        'df[df["value"] <= df["value"].quantile(0.95)]',
        "분위수 기반 절단은 분포 형태를 가정하지 않는 간단한 방법입니다. 다만 표본이 작으면 분위수 경계가 불안정할 수 있습니다.",
    ),
    _code(
        "iqr_medium_clip_quantile",
        "분위수 경계로 값 제한",
        "이상치·IQR",
        "중급",
        "value를 5% 분위수와 95% 분위수 사이로 clip하세요. 우변만 입력합니다.",
        outlier_value_data,
        'df["value"] = {{answer}}',
        "Series.clip(하한, 상한)",
        {"clip", "quantile"},
        "clip의 두 인자에 각각 0.05, 0.95 분위수를 전달하세요.",
        'df["value"].clip(df["value"].quantile(0.05), df["value"].quantile(0.95))',
        "clip은 행을 삭제하지 않고 경계 밖 값을 경계값으로 바꿉니다. 표본 수를 유지해야 하는 경우 사용할 수 있지만 원래 극단값 정보가 사라진다는 점을 기록해야 합니다.",
    ),
    _code(
        "iqr_medium_middle_half",
        "중앙 50% 데이터 선택",
        "이상치·IQR",
        "중급",
        "Q1부터 Q3까지 중앙 50%에 해당하는 행만 남기세요. 우변만 입력합니다.",
        outlier_value_data,
        "df = {{answer}}",
        "between(Q1, Q3)",
        {"between", "quantile"},
        "Q1은 0.25, Q3는 0.75 분위수입니다.",
        'df[df["value"].between(df["value"].quantile(0.25), df["value"].quantile(0.75))]',
        "Q1~Q3 구간은 IQR 자체에 해당하는 중앙 50%입니다. 이는 일반적인 이상치 제거보다 훨씬 강한 필터이므로 분석 목적에 맞을 때만 사용합니다.",
    ),
    _code(
        "iqr_medium_standardized",
        "표준화 값 절댓값 필터",
        "이상치·IQR",
        "중급",
        "이미 표준화된 value에서 절댓값이 3 이하인 행만 남기세요. 우변만 입력합니다.",
        standardized_value_data,
        "df = {{answer}}",
        "Series.abs()를 사용한 조건 필터",
        {"abs"},
        "-3~3을 두 조건으로 쓰거나 abs() 하나로 표현할 수 있습니다.",
        'df[df["value"].abs() <= 3]',
        "표준화 점수의 절댓값을 사용하면 양쪽 꼬리를 한 번에 검사할 수 있습니다. ±3 기준은 흔한 경험칙이지만 모든 분포에 자동 적용할 규칙은 아닙니다.",
    ),
    # 이상치·IQR: 고급 4개
    _code(
        "iqr_advanced_zscore",
        "Z-score 계산과 필터링",
        "이상치·IQR",
        "고급",
        "value의 평균과 표준편차로 zscore 열을 만들고 |zscore|가 2 이하인 행만 남기세요.",
        outlier_value_data,
        "{{answer}}",
        "평균, 표준편차, zscore, 필터링 4줄",
        {"mean", "std", "abs"},
        "zscore = (value - mean) / std입니다.",
        'mean = df["value"].mean()\nstd = df["value"].std()\ndf["zscore"] = (df["value"] - mean) / std\ndf = df[df["zscore"].abs() <= 2]',
        "Z-score는 평균에서 표준편차 몇 배만큼 떨어졌는지 나타냅니다. 정규성에 크게 어긋나거나 극단값이 평균·표준편차 자체를 왜곡하는 데이터에서는 IQR 방식과 함께 비교해야 합니다.",
    ),
    _code(
        "iqr_advanced_clip",
        "IQR 경계로 윈저라이징",
        "이상치·IQR",
        "고급",
        "IQR 경계를 계산하고 value의 경계 밖 값을 clip으로 제한하세요.",
        outlier_value_data,
        "{{answer}}",
        "Q1, Q3, IQR, clip 4줄",
        {"quantile", "clip"},
        "마지막 줄에서 Q1-1.5*IQR과 Q3+1.5*IQR을 사용하세요.",
        'q1 = df["value"].quantile(0.25)\nq3 = df["value"].quantile(0.75)\niqr = q3 - q1\ndf["value"] = df["value"].clip(q1 - 1.5 * iqr, q3 + 1.5 * iqr)',
        "IQR 윈저라이징은 행 수를 유지하면서 극단값의 영향력을 제한합니다. 원본 값이 변경되므로 재현성을 위해 경계와 처리 여부를 별도로 기록하는 것이 좋습니다.",
    ),
    _code(
        "iqr_advanced_sorted_sales",
        "매출 이상치 제거 후 정렬",
        "이상치·IQR",
        "고급",
        "sales의 IQR 경계를 계산해 이상치를 제거하고 sales 오름차순으로 정렬한 뒤 인덱스를 초기화하세요.",
        outlier_sales_data,
        "{{answer}}",
        "경계 계산과 체이닝을 최대 5줄로 작성",
        {"quantile", "between", "sort_values", "reset_index"},
        "필터 결과에 sort_values와 reset_index를 이어 붙일 수 있습니다.",
        'q1 = df["sales"].quantile(0.25)\nq3 = df["sales"].quantile(0.75)\niqr = q3 - q1\ndf = df[df["sales"].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)].sort_values("sales").reset_index(drop=True)',
        "이상치 필터링 뒤 정렬과 인덱스 초기화를 명시하면 결과 비교와 후속 시각화가 쉬워집니다. 필터 전후 행 수를 함께 기록하면 데이터 손실 규모도 확인할 수 있습니다.",
    ),
    _code(
        "iqr_advanced_grouped",
        "그룹별 IQR 이상치 제거",
        "이상치·IQR",
        "고급",
        "각 group 안에서 Q1·Q3·IQR을 계산해 그룹별 정상 범위 행만 남기세요.",
        grouped_outlier_data,
        "{{answer}}",
        "transform('quantile', 분위수)를 활용한 5줄",
        {"groupby", "transform", "between"},
        "그룹별 분위수를 원본 길이로 맞추려면 transform을 사용하세요.",
        'q1 = df.groupby("group")["value"].transform("quantile", 0.25)\nq3 = df.groupby("group")["value"].transform("quantile", 0.75)\niqr = q3 - q1\nlow_bound = q1 - 1.5 * iqr\ndf = df[df["value"].between(low_bound, q3 + 1.5 * iqr)]',
        "그룹의 값 수준이 크게 다르면 전체 경계 하나보다 그룹별 경계가 적절할 수 있습니다. transform으로 계산한 경계는 각 원본 행과 같은 인덱스를 유지해 바로 필터에 사용할 수 있습니다.",
    ),
    # 필터링·요약: 초급 4개
    _mcq(
        "filter_beginner_columns",
        "여러 열 선택하기",
        "필터링·요약",
        "초급",
        "department와 sales 두 열만 DataFrame으로 선택하는 코드를 고르세요.",
        employee_data,
        ('df[["department", "sales"]]', 'df["department", "sales"]', 'df("department", "sales")', 'df.columns("department", "sales")'),
        0,
        "여러 열 이름을 리스트로 묶어 이중 대괄호를 사용합니다.",
        'df[["department", "sales"]]',
        "단일 대괄호 안에 열 이름 리스트를 전달하면 DataFrame이 반환됩니다. 튜플처럼 쉼표만 사용하면 일반 DataFrame 열 선택 문법이 아닙니다.",
    ),
    _mcq(
        "filter_beginner_or",
        "OR 복합 조건",
        "필터링·요약",
        "초급",
        "Sales 또는 Dev 부서를 선택하는 조건으로 올바른 것을 고르세요.",
        employee_data,
        ('(df["department"] == "Sales") | (df["department"] == "Dev")', '(df["department"] == "Sales") & (df["department"] == "Dev")', 'df["department"] == "Sales" or "Dev"', 'df["department"] in ["Sales", "Dev"]'),
        0,
        "Series의 원소별 OR는 | 입니다.",
        '(df["department"] == "Sales") | (df["department"] == "Dev")',
        "pandas Series 조건은 각 비교를 괄호로 묶고 |로 연결합니다. 파이썬 or는 Series 전체의 참·거짓을 하나로 판단하려 해 오류가 납니다.",
    ),
    _mcq(
        "filter_beginner_sort",
        "매출 내림차순 정렬",
        "필터링·요약",
        "초급",
        "sales가 큰 행부터 정렬하는 코드를 고르세요.",
        employee_data,
        ('df.sort_values("sales", ascending=False)', 'df.sort_values("sales", ascending=True)', 'df.sort_index("sales")', 'df.rank("sales")'),
        0,
        "ascending=False가 큰 값부터 정렬합니다.",
        'df.sort_values("sales", ascending=False)',
        "sort_values는 지정 열의 값을 기준으로 정렬합니다. descending이라는 인자 대신 ascending=False를 사용합니다.",
    ),
    _mcq(
        "filter_beginner_group_mean",
        "부서별 평균 계산",
        "필터링·요약",
        "초급",
        "부서별 sales 평균을 계산하는 코드를 고르세요.",
        employee_data,
        ('df.groupby("department")["sales"].mean()', 'df.groupby("sales")["department"].mean()', 'df["sales"].mean("department")', 'df.mean().groupby("department")'),
        0,
        "그룹 기준 열을 groupby에, 집계 열을 그 뒤에 선택합니다.",
        'df.groupby("department")["sales"].mean()',
        "department로 행을 묶은 뒤 sales만 선택해 mean을 적용합니다. 그룹 기준과 집계 대상의 순서를 바꾸면 의미와 자료형이 달라집니다.",
    ),
    # 필터링·요약: 중급 4개
    _code(
        "filter_medium_isin",
        "여러 부서 한 번에 선택",
        "필터링·요약",
        "중급",
        "Sales와 Dev 부서의 행만 남기세요. 우변만 입력합니다.",
        employee_data,
        "df = {{answer}}",
        "Series.isin([...])을 사용",
        {"isin"},
        "department가 허용 목록에 포함되는지 확인하세요.",
        'df[df["department"].isin(["Sales", "Dev"])]',
        "isin은 여러 값에 대한 OR 비교를 간결하게 표현합니다. 허용값이 늘어나도 조건식을 길게 반복할 필요가 없습니다.",
    ),
    _code(
        "filter_medium_between",
        "매출 구간 필터링",
        "필터링·요약",
        "중급",
        "sales가 100 이상 140 이하인 행만 남기세요. 우변만 입력합니다.",
        employee_data,
        "df = {{answer}}",
        "between(하한, 상한)",
        {"between"},
        "between은 기본적으로 양 끝값을 포함합니다.",
        'df[df["sales"].between(100, 140)]',
        "between은 두 비교식을 &로 연결한 것과 같은 결과를 읽기 쉽게 표현합니다. 기본 inclusive 설정에서는 100과 140도 포함됩니다.",
    ),
    _code(
        "filter_medium_sort",
        "매출 내림차순 정렬",
        "필터링·요약",
        "중급",
        "sales 기준 내림차순으로 df를 정렬하세요. 우변만 입력합니다.",
        employee_data,
        "df = {{answer}}",
        "sort_values와 ascending 사용",
        {"sort_values"},
        "ascending=False를 지정하세요.",
        'df.sort_values("sales", ascending=False)',
        "정렬 결과는 새로운 DataFrame이므로 df에 다시 대입합니다. 기존 인덱스는 행의 출처를 보존하기 위해 그대로 유지됩니다.",
    ),
    _code(
        "filter_medium_top3",
        "매출 상위 3명 선택",
        "필터링·요약",
        "중급",
        "sales가 가장 큰 3개 행을 선택하세요. 우변만 입력합니다.",
        employee_data,
        "df = {{answer}}",
        "DataFrame.nlargest 사용",
        {"nlargest"},
        "nlargest(개수, 열이름) 순서입니다.",
        'df.nlargest(3, "sales")',
        "nlargest는 전체 정렬 후 head를 호출하는 패턴을 간결하게 표현합니다. 동점 처리와 반환 순서가 중요한 문제에서는 요구사항을 추가로 확인해야 합니다.",
    ),
    # 필터링·요약: 고급 4개
    _code(
        "summary_advanced_category_sum",
        "주문 금액 정제와 합계",
        "필터링·요약",
        "고급",
        "amount를 숫자로 변환하고 실패 행을 제거한 뒤 category별 합계를 계산하세요.",
        dirty_order_data,
        "{{answer}}",
        "변환, 제거, 그룹 합계 3줄",
        {"to_numeric", "dropna", "groupby", "sum"},
        "errors='coerce'와 as_index=False를 사용하세요.",
        'df["amount"] = pd.to_numeric(df["amount"], errors="coerce")\ndf = df.dropna(subset=["amount"])\ndf = df.groupby("category", as_index=False)["amount"].sum()',
        "집계 전 자료형을 숫자로 통일하고 변환 실패값을 명시적으로 제거합니다. as_index=False는 category를 일반 열로 유지해 후속 저장과 시각화를 편하게 합니다.",
    ),
    _code(
        "summary_advanced_agg",
        "부서별 평균과 인원수",
        "필터링·요약",
        "고급",
        "부서별 sales 평균과 employee 개수를 계산하고 employee 열을 headcount로 바꾼 뒤 평균 내림차순으로 정렬하세요.",
        employee_data,
        "{{answer}}",
        "agg, rename, sort/reset 3줄",
        {"groupby", "agg", "rename", "sort_values", "reset_index"},
        "agg에 열별 집계 함수 딕셔너리를 전달하세요.",
        'df = df.groupby("department", as_index=False).agg({"sales": "mean", "employee": "count"})\ndf = df.rename(columns={"employee": "headcount"})\ndf = df.sort_values("sales", ascending=False).reset_index(drop=True)',
        "agg는 여러 열에 서로 다른 집계를 한 번에 적용합니다. 집계 결과의 의미가 명확하도록 count 열을 headcount로 바꾸고 정렬 후 인덱스를 정리합니다.",
    ),
    _code(
        "summary_advanced_pivot",
        "분기별 매출 피벗",
        "필터링·요약",
        "고급",
        "department를 행, quarter를 열로 하는 sales 합계 피벗 테이블을 만들고 인덱스를 일반 열로 바꾸세요.",
        quarterly_sales_data,
        "{{answer}}",
        "pivot_table과 reset_index를 사용한 2줄 이내 코드",
        {"pivot_table", "reset_index"},
        "pd.pivot_table의 index, columns, values, aggfunc를 지정하세요.",
        'df = pd.pivot_table(df, index="department", columns="quarter", values="sales", aggfunc="sum", fill_value=0)\ndf = df.reset_index()',
        "피벗 테이블은 긴 형식 데이터를 교차표 형태로 요약합니다. reset_index를 호출하면 department가 인덱스가 아닌 일반 열이 되어 비교와 내보내기가 쉬워집니다.",
    ),
    _code(
        "summary_advanced_share",
        "부서 내 매출 비중 계산",
        "필터링·요약",
        "고급",
        "부서별 총매출을 각 행에 맞춰 계산하고 share 열을 만든 뒤 부서·비중 순으로 정렬하고 인덱스를 초기화하세요.",
        employee_data,
        "{{answer}}",
        "transform 합계, 비중, 다중 정렬 3줄",
        {"groupby", "transform", "sort_values", "reset_index"},
        "transform('sum')은 원본 행 수를 유지합니다.",
        'department_total = df.groupby("department")["sales"].transform("sum")\ndf["share"] = df["sales"] / department_total\ndf = df.sort_values(["department", "share"], ascending=[True, False]).reset_index(drop=True)',
        "transform으로 구한 부서 합계는 각 직원 행과 같은 길이이므로 바로 나눗셈할 수 있습니다. share는 부서 내부 기여도를 나타내며 부서별 합계가 1이 되는지 검산할 수 있습니다.",
    ),
    # 시각화: 초급 4개
    _mcq(
        "viz_beginner_hist",
        "분포를 보는 히스토그램",
        "시각화",
        "초급",
        "score 값의 분포 형태를 확인하기에 가장 적절한 코드를 고르세요.",
        chart_distribution_data,
        ('plt.hist(df["score"], bins=5)', 'plt.plot(df["score"], df["score"])', 'plt.pie(df["score"])', 'plt.bar("score", 1)'),
        0,
        "연속형 값의 구간별 빈도를 보여주는 그래프입니다.",
        'plt.hist(df["score"], bins=5)',
        "히스토그램은 연속형 변수를 구간으로 나누어 빈도를 표시합니다. bins 선택에 따라 분포 인상이 달라질 수 있으므로 여러 구간 수를 비교하는 것이 좋습니다.",
    ),
    _mcq(
        "viz_beginner_bar",
        "범주별 값 비교",
        "시각화",
        "초급",
        "category별 value 크기를 직접 비교하기 좋은 코드를 고르세요.",
        chart_category_data,
        ('plt.bar(df["category"], df["value"])', 'plt.hist(df["category"])', 'plt.scatter(df["category"], df["category"])', 'plt.pie(df["cost"], df["value"])'),
        0,
        "범주 이름과 막대 높이를 각각 전달합니다.",
        'plt.bar(df["category"], df["value"])',
        "막대그래프는 공통 기준선에서 길이를 비교하므로 범주별 크기 차이를 읽기 쉽습니다. 범주가 너무 많으면 정렬이나 가로 막대를 고려합니다.",
    ),
    _mcq(
        "viz_beginner_pie",
        "전체 대비 비율 표현",
        "시각화",
        "초급",
        "category별 value가 전체에서 차지하는 비율을 원형 차트로 그리는 코드를 고르세요.",
        chart_category_data,
        ('plt.pie(df["value"], labels=df["category"])', 'plt.pie(df["category"], labels=df["value"])', 'plt.plot(df["value"])', 'plt.hist(df["category"])'),
        0,
        "pie의 첫 인자는 조각 크기, labels는 범주명입니다.",
        'plt.pie(df["value"], labels=df["category"])',
        "원형 차트는 전체 대비 구성비를 보여줍니다. 범주가 많거나 값 차이가 작으면 막대그래프가 더 정확하게 비교됩니다.",
    ),
    _mcq(
        "viz_beginner_scatter",
        "비용과 값의 관계",
        "시각화",
        "초급",
        "cost와 value 두 수치 변수의 관계를 확인할 코드를 고르세요.",
        chart_category_data,
        ('plt.scatter(df["cost"], df["value"])', 'plt.hist(df["cost"], df["value"])', 'plt.pie(df["cost"])', 'plt.bar(df["cost"] + df["value"])'),
        0,
        "두 수치값을 x, y 좌표로 배치합니다.",
        'plt.scatter(df["cost"], df["value"])',
        "산점도는 두 변수의 방향성, 비선형 패턴, 군집과 이상치를 탐색합니다. 점의 패턴은 연관성을 보여주지만 그 자체로 인과관계를 증명하지 않습니다.",
    ),
    # 시각화: 중급 4개
    _mcq(
        "viz_medium_legend",
        "두 선에 범례 붙이기",
        "시각화",
        "중급",
        "value와 cost 두 선을 그리고 올바른 범례를 표시하는 코드 묶음을 고르세요.",
        chart_category_data,
        ('plt.plot(df["category"], df["value"], label="value"); plt.plot(df["category"], df["cost"], label="cost"); plt.legend()', 'plt.plot(df["value"]); plt.title("legend")', 'plt.legend(df["value"], df["cost"])', 'plt.bar(df["value"], label=df["cost"])'),
        0,
        "각 선에 label을 지정한 뒤 legend를 호출합니다.",
        'plt.plot(..., label="value"); plt.plot(..., label="cost"); plt.legend()',
        "범례는 각 시리즈의 label을 수집해 표시합니다. 선을 그릴 때 의미 있는 이름을 지정하면 색이나 선 스타일만으로 구분해야 하는 부담이 줄어듭니다.",
    ),
    _mcq(
        "viz_medium_boxplot",
        "이상치 후보 시각화",
        "시각화",
        "중급",
        "score의 중앙값, IQR과 이상치 후보를 한 번에 확인하기 적절한 코드를 고르세요.",
        chart_distribution_data,
        ('plt.boxplot(df["score"])', 'plt.pie(df["score"])', 'plt.scatter(df["score"], df["score"])', 'plt.imshow(df["score"])'),
        0,
        "상자와 수염으로 분포를 요약하는 그래프입니다.",
        'plt.boxplot(df["score"])',
        "박스플롯은 중앙값, Q1, Q3와 수염 밖의 점을 압축적으로 표시합니다. 표본의 실제 분포 모양이나 다봉성은 숨길 수 있어 히스토그램과 함께 보면 좋습니다.",
    ),
    _mcq(
        "viz_medium_horizontal",
        "긴 범주명의 가로 막대",
        "시각화",
        "중급",
        "범주명이 길어 x축 라벨이 겹칠 때 가장 읽기 좋은 대안을 고르세요.",
        chart_category_data,
        ('plt.barh(df["category"], df["value"])', 'plt.bar(df["category"], df["value"], width=10)', 'plt.axis("off")', 'plt.pie(df["value"])'),
        0,
        "범주명을 y축으로 옮기면 가로 공간을 활용할 수 있습니다.",
        'plt.barh(df["category"], df["value"])',
        "가로 막대는 긴 범주명을 자연스럽게 읽게 해 줍니다. 값을 정렬하면 순위 비교도 더 쉬워집니다.",
    ),
    _mcq(
        "viz_medium_grid",
        "수치 판독을 돕는 격자",
        "시각화",
        "중급",
        "선 그래프에서 y값을 더 쉽게 비교하도록 옅은 격자를 추가하는 코드를 고르세요.",
        chart_category_data,
        ('plt.grid(axis="y", alpha=0.3)', 'plt.axis("off")', 'plt.legend(False)', 'plt.figure(alpha=0)'),
        0,
        "y축 방향 값 비교에는 수평 격자가 유용합니다.",
        'plt.grid(axis="y", alpha=0.3)',
        "옅은 수평 격자는 점의 y값을 기준선과 연결해 판독을 돕습니다. 너무 진하거나 양축 모두 촘촘한 격자는 데이터보다 시선을 끌 수 있습니다.",
    ),
    # 시각화: 고급 4개
    _mcq(
        "viz_advanced_alpha",
        "점 겹침 완화하기",
        "시각화",
        "고급",
        "산점도에서 같은 위치 주변의 점이 많이 겹칠 때 밀도를 드러내는 간단한 설정을 고르세요.",
        chart_dense_data,
        ('plt.scatter(df["x"], df["y"], alpha=0.3)', 'plt.scatter(df["x"], df["y"], alpha=1)', 'plt.axis("off")', 'plt.scatter(df["x"], df["y"], s=1000)'),
        0,
        "점에 투명도를 주면 겹친 영역이 진해집니다.",
        'plt.scatter(df["x"], df["y"], alpha=0.3)',
        "alpha를 낮추면 여러 점이 겹친 영역이 더 진하게 보여 관측 밀도를 짐작할 수 있습니다. 데이터가 매우 많다면 hexbin이나 2차원 밀도 그래프도 고려합니다.",
    ),
    _mcq(
        "viz_advanced_log",
        "큰 범위의 값 로그축 표현",
        "시각화",
        "고급",
        "양수 값이 여러 자릿수 규모에 걸쳐 있을 때 작은 값과 큰 값을 함께 비교하기 좋은 설정을 고르세요.",
        chart_category_data,
        ('plt.yscale("log")', 'plt.ylim(0, 1)', 'plt.axis("off")', 'plt.yticks([])'),
        0,
        "곱셈 비율을 같은 간격으로 보여주는 축입니다.",
        'plt.yscale("log")',
        "로그축은 10, 100, 1000 같은 배수 변화를 같은 간격으로 표현합니다. 0이나 음수에는 그대로 적용할 수 없고, 독자에게 로그축임을 명확히 알려야 합니다.",
    ),
    _mcq(
        "viz_advanced_truncated_axis",
        "잘린 축의 왜곡 피하기",
        "시각화",
        "고급",
        "막대그래프에서 작은 차이를 과장하지 않는 가장 적절한 원칙을 고르세요.",
        chart_category_data,
        ("특별한 이유가 없다면 값축을 0에서 시작한다.", "항상 최솟값 바로 위에서 축을 시작한다.", "축 눈금을 모두 숨긴다.", "가장 큰 막대만 표시한다."),
        0,
        "막대 길이는 공통 기준선에서 비교됩니다.",
        "막대그래프의 값축은 원칙적으로 0에서 시작",
        "막대 길이는 값 자체를 인코딩하므로 기준선을 자르면 차이가 실제보다 커 보일 수 있습니다. 불가피하게 축을 자를 때는 시각적 표시와 설명을 추가해야 합니다.",
    ),
    _mcq(
        "viz_advanced_hexbin",
        "대규모 산점도의 밀도 표현",
        "시각화",
        "고급",
        "수만 개 점이 겹쳐 산점도를 읽기 어려울 때 영역별 관측 밀도를 보여줄 코드를 고르세요.",
        chart_dense_data,
        ('plt.hexbin(df["x"], df["y"], gridsize=30, cmap="Blues")', 'plt.scatter(df["x"], df["y"], s=1000)', 'plt.pie(df["x"])', 'plt.bar(df["x"], df["y"])'),
        0,
        "평면을 육각형 구간으로 나누어 개수를 집계합니다.",
        'plt.hexbin(df["x"], df["y"], gridsize=30, cmap="Blues")',
        "hexbin은 좌표 공간을 육각형 셀로 나누고 셀별 관측 수를 색으로 표시합니다. gridsize가 너무 작으면 세부 패턴이 사라지고 너무 크면 다시 희소해질 수 있습니다.",
    ),
)


def _expected_missing_ffill() -> pd.DataFrame:
    df = missing_people_data()
    df["age"] = df["age"].ffill()
    return df


def _expected_missing_constant() -> pd.DataFrame:
    df = missing_people_data()
    df["city"] = df["city"].fillna("미정")
    return df


def _expected_missing_drop_score() -> pd.DataFrame:
    return missing_people_data().dropna(subset=["score"])


def _expected_missing_group_mean() -> pd.DataFrame:
    df = missing_class_data()
    df["score"] = df["score"].fillna(df.groupby("class")["score"].transform("mean"))
    return df


def _expected_missing_mixed() -> pd.DataFrame:
    df = missing_people_data()
    df["age"] = df["age"].fillna(df["age"].mean())
    df["city"] = df["city"].fillna(df["city"].mode()[0])
    return df.dropna(subset=["score"])


def _expected_missing_sentinel() -> pd.DataFrame:
    df = missing_sensor_data()
    df["value"] = df["value"].replace(-999, np.nan)
    df["value"] = df["value"].fillna(df["value"].median())
    return df


def _expected_missing_income() -> pd.DataFrame:
    df = missing_income_data()
    df["income"] = pd.to_numeric(df["income"], errors="coerce")
    df["income"] = df["income"].fillna(df["income"].median())
    return df.dropna(subset=["name"])


def _expected_missing_class() -> pd.DataFrame:
    df = missing_class_data()
    df["score"] = df["score"].fillna(df.groupby("class")["score"].transform("mean"))
    df["attendance"] = df["attendance"].fillna(0)
    return df.dropna(subset=["class"])


def _expected_upper_quantile() -> pd.DataFrame:
    df = outlier_value_data()
    return df[df["value"] <= df["value"].quantile(0.95)]


def _expected_clip_quantile() -> pd.DataFrame:
    df = outlier_value_data()
    df["value"] = df["value"].clip(df["value"].quantile(0.05), df["value"].quantile(0.95))
    return df


def _expected_middle_half() -> pd.DataFrame:
    df = outlier_value_data()
    return df[df["value"].between(df["value"].quantile(0.25), df["value"].quantile(0.75))]


def _expected_standardized() -> pd.DataFrame:
    df = standardized_value_data()
    return df[df["value"].abs() <= 3]


def _expected_zscore() -> pd.DataFrame:
    df = outlier_value_data()
    mean = df["value"].mean()
    std = df["value"].std()
    df["zscore"] = (df["value"] - mean) / std
    return df[df["zscore"].abs() <= 2]


def _expected_iqr_clip() -> pd.DataFrame:
    df = outlier_value_data()
    q1 = df["value"].quantile(0.25)
    q3 = df["value"].quantile(0.75)
    iqr = q3 - q1
    df["value"] = df["value"].clip(q1 - 1.5 * iqr, q3 + 1.5 * iqr)
    return df


def _expected_sorted_sales() -> pd.DataFrame:
    df = outlier_sales_data()
    q1 = df["sales"].quantile(0.25)
    q3 = df["sales"].quantile(0.75)
    iqr = q3 - q1
    return df[df["sales"].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)].sort_values("sales").reset_index(drop=True)


def _expected_grouped_iqr() -> pd.DataFrame:
    df = grouped_outlier_data()
    q1 = df.groupby("group")["value"].transform("quantile", 0.25)
    q3 = df.groupby("group")["value"].transform("quantile", 0.75)
    iqr = q3 - q1
    return df[df["value"].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)]


def _expected_filter_isin() -> pd.DataFrame:
    df = employee_data()
    return df[df["department"].isin(["Sales", "Dev"])]


def _expected_filter_between() -> pd.DataFrame:
    df = employee_data()
    return df[df["sales"].between(100, 140)]


def _expected_filter_sort() -> pd.DataFrame:
    return employee_data().sort_values("sales", ascending=False)


def _expected_filter_top3() -> pd.DataFrame:
    return employee_data().nlargest(3, "sales")


def _expected_category_sum() -> pd.DataFrame:
    df = dirty_order_data()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])
    return df.groupby("category", as_index=False)["amount"].sum()


def _expected_agg() -> pd.DataFrame:
    df = employee_data().groupby("department", as_index=False).agg({"sales": "mean", "employee": "count"})
    df = df.rename(columns={"employee": "headcount"})
    return df.sort_values("sales", ascending=False).reset_index(drop=True)


def _expected_pivot() -> pd.DataFrame:
    df = pd.pivot_table(
        quarterly_sales_data(),
        index="department",
        columns="quarter",
        values="sales",
        aggfunc="sum",
        fill_value=0,
    )
    return df.reset_index()


def _expected_share() -> pd.DataFrame:
    df = employee_data()
    department_total = df.groupby("department")["sales"].transform("sum")
    df["share"] = df["sales"] / department_total
    return df.sort_values(["department", "share"], ascending=[True, False]).reset_index(drop=True)


EXTRA_VALIDATORS: dict[str, Callable[[], pd.DataFrame]] = {
    "missing_medium_ffill": _expected_missing_ffill,
    "missing_medium_constant": _expected_missing_constant,
    "missing_medium_drop_score": _expected_missing_drop_score,
    "missing_medium_group_mean": _expected_missing_group_mean,
    "missing_advanced_mixed": _expected_missing_mixed,
    "missing_advanced_sentinel": _expected_missing_sentinel,
    "missing_advanced_income": _expected_missing_income,
    "missing_advanced_class": _expected_missing_class,
    "iqr_medium_upper_quantile": _expected_upper_quantile,
    "iqr_medium_clip_quantile": _expected_clip_quantile,
    "iqr_medium_middle_half": _expected_middle_half,
    "iqr_medium_standardized": _expected_standardized,
    "iqr_advanced_zscore": _expected_zscore,
    "iqr_advanced_clip": _expected_iqr_clip,
    "iqr_advanced_sorted_sales": _expected_sorted_sales,
    "iqr_advanced_grouped": _expected_grouped_iqr,
    "filter_medium_isin": _expected_filter_isin,
    "filter_medium_between": _expected_filter_between,
    "filter_medium_sort": _expected_filter_sort,
    "filter_medium_top3": _expected_filter_top3,
    "summary_advanced_category_sum": _expected_category_sum,
    "summary_advanced_agg": _expected_agg,
    "summary_advanced_pivot": _expected_pivot,
    "summary_advanced_share": _expected_share,
}
