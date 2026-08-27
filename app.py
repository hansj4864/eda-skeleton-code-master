"""Streamlit UI for EDA Skeleton Code Master."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from grading import GradeResult, grade_submission
from questions import QUESTION_BY_ID, QUESTIONS, Question

try:
    from streamlit_ace import st_ace
except ImportError:  # The app remains usable if the optional component fails to load.
    st_ace = None


st.set_page_config(
    page_title="EDA 스켈레톤 코드 마스터",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="auto",
)


st.markdown(
    """
    <style>
    :root {
        --ink: #17233c;
        --muted: #64748b;
        --navy: #17315f;
        --blue: #3266d6;
        --mint: #25a78d;
        --paper: #f7f9fc;
        --line: #dfe7f1;
    }
    .stApp { background: var(--paper); color: var(--ink); }
    [data-testid="stSidebar"] { background: #eef3f9; border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: var(--navy); }
    .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1450px; }
    .hero {
        position: relative; overflow: hidden; padding: 2.2rem 2.4rem; margin-bottom: 1.4rem;
        border-radius: 24px; color: white;
        background: linear-gradient(125deg, #142b52 0%, #254f96 60%, #238d86 115%);
        box-shadow: 0 18px 50px rgba(23, 49, 95, .18);
    }
    .hero::after {
        content: ""; position: absolute; width: 240px; height: 240px; border-radius: 50%;
        right: -65px; top: -105px; background: rgba(255,255,255,.1);
    }
    .hero-kicker { font-size: .78rem; font-weight: 800; letter-spacing: .14em; opacity: .78; }
    .hero h1 { color: white; font-size: clamp(2rem, 4vw, 3.45rem); line-height: 1.02; margin: .5rem 0 .7rem; }
    .hero p { margin: 0; max-width: 650px; color: rgba(255,255,255,.83); font-size: 1rem; }
    .eyebrow { color: var(--blue); font-size: .76rem; font-weight: 850; letter-spacing: .11em; margin-bottom: .4rem; }
    .question-title { font-size: 1.6rem; line-height: 1.25; font-weight: 850; color: var(--navy); margin-bottom: .8rem; }
    .badge {
        display: inline-block; padding: .28rem .68rem; margin-right: .35rem; border-radius: 999px;
        background: #e7efff; color: #2959bd; font-size: .76rem; font-weight: 800;
    }
    .badge.green { background: #ddf5ee; color: #187866; }
    .panel-note {
        border: 1px solid var(--line); background: white; border-radius: 14px;
        padding: .9rem 1rem; color: var(--muted); font-size: .9rem; margin: .8rem 0 1rem;
    }
    .result-detail {
        border-left: 3px solid #8aa7d9; background: #f1f5fb; padding: .72rem .9rem;
        border-radius: 0 10px 10px 0; color: #41516e; margin: .6rem 0 1rem;
    }
    div[data-testid="stMetric"] {
        background: white; border: 1px solid var(--line); padding: .85rem 1rem;
        border-radius: 14px; box-shadow: 0 5px 18px rgba(30,58,100,.04);
    }
    div[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
    .stButton > button { border-radius: 10px; min-height: 2.7rem; font-weight: 750; }
    .stButton > button[kind="primary"] { background: var(--blue); border-color: var(--blue); }
    .footer { color: #8491a8; text-align: center; padding-top: 2.2rem; font-size: .8rem; }
    @media (max-width: 780px) {
        .block-container { padding: 1rem .9rem 2rem; }
        .hero { padding: 1.55rem 1.35rem; border-radius: 18px; }
        .hero h1 { font-size: 2rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def _initialize_state() -> None:
    if "progress" not in st.session_state:
        st.session_state.progress = {
            question.id: {"attempts": 0, "passed": False, "result": None}
            for question in QUESTIONS
        }
    if "correct_submissions" not in st.session_state:
        st.session_state.correct_submissions = 0


def _answer_key(question: Question) -> str:
    return f"answer_{question.id}"


def _clear_answer(question: Question) -> None:
    st.session_state.progress[question.id]["result"] = None
    key = _answer_key(question)
    if key in st.session_state:
        del st.session_state[key]


def _go_next(current_id: str) -> None:
    ids = [question.id for question in QUESTIONS]
    next_id = ids[(ids.index(current_id) + 1) % len(ids)]
    st.session_state.topic_filter = "전체"
    st.session_state.difficulty_filter = "전체"
    st.session_state.question_selector = next_id


def _record_submission(question: Question, result: GradeResult) -> None:
    entry = st.session_state.progress[question.id]
    entry["attempts"] += 1
    entry["passed"] = bool(entry["passed"] or result.passed)
    entry["result"] = result
    if result.passed:
        st.session_state.correct_submissions += 1


def _format_question(question_id: str) -> str:
    question = QUESTION_BY_ID[question_id]
    number = [item.id for item in QUESTIONS].index(question_id) + 1
    return f"{number:02d}. {question.title}"


def _render_sidebar() -> Question:
    progress = st.session_state.progress
    completed = sum(1 for item in progress.values() if item["passed"])
    attempts = sum(int(item["attempts"]) for item in progress.values())
    accuracy = (st.session_state.correct_submissions / attempts * 100) if attempts else 0.0

    with st.sidebar:
        st.markdown("## 🧭 EDA Master")
        st.caption("짧게 풀고, 바로 이해하는 실전 연습")
        st.progress(completed / len(QUESTIONS), text=f"완료 {completed} / {len(QUESTIONS)}")
        metric_left, metric_right = st.columns(2)
        metric_left.metric("시도", attempts)
        metric_right.metric("정답률", f"{accuracy:.0f}%")
        st.markdown("---")

        topics = ["전체", *dict.fromkeys(question.topic for question in QUESTIONS)]
        difficulties = ["전체", "초급", "중급", "고급"]
        topic = st.selectbox("학습 주제", topics, key="topic_filter")
        difficulty = st.selectbox("난이도", difficulties, key="difficulty_filter")

        filtered = [
            question
            for question in QUESTIONS
            if (topic == "전체" or question.topic == topic)
            and (difficulty == "전체" or question.difficulty == difficulty)
        ]
        filtered_ids = [question.id for question in filtered]
        if st.session_state.get("question_selector") not in filtered_ids:
            st.session_state.question_selector = filtered_ids[0]

        selected_id = st.selectbox(
            "문제 번호",
            filtered_ids,
            format_func=_format_question,
            key="question_selector",
        )
        st.markdown("---")
        st.caption("학습 기록은 현재 브라우저 세션에만 보관됩니다.")
        if st.button("세션 기록 초기화", width="stretch"):
            for item in progress.values():
                item.update({"attempts": 0, "passed": False, "result": None})
            st.session_state.correct_submissions = 0
            for question in QUESTIONS:
                st.session_state.pop(_answer_key(question), None)
            st.rerun()

    return QUESTION_BY_ID[selected_id]


def _render_data_preview(question: Question) -> None:
    df = question.data_factory().copy(deep=True)
    preview_rows = int(question.preview_config.get("rows", 8))
    st.markdown("#### 초기 데이터")
    st.dataframe(df.head(preview_rows), width="stretch", hide_index=True)

    rows, columns, missing = st.columns(3)
    rows.metric("행", f"{df.shape[0]}")
    columns.metric("열", f"{df.shape[1]}")
    missing.metric("결측치", f"{int(df.isna().sum().sum())}")

    with st.expander("열 정보 자세히 보기"):
        schema = pd.DataFrame(
            {
                "dtype": df.dtypes.astype(str),
                "결측치": df.isna().sum(),
                "고유값": df.nunique(dropna=True),
            }
        )
        st.dataframe(schema, width="stretch")


def _render_answer_input(question: Question) -> int | str | None:
    key = _answer_key(question)
    if question.kind == "mcq":
        st.markdown("#### 정답 선택")
        return st.radio(
            "가장 알맞은 보기를 고르세요.",
            options=list(range(len(question.choices))),
            format_func=lambda index: question.choices[index],
            index=None,
            key=key,
            label_visibility="collapsed",
        )

    st.markdown("#### 코드 완성")
    display_template = question.immutable_template.replace("{{answer}}", "# ⬜ 여기에 답안을 작성하세요")
    st.code(display_template, language="python")
    st.markdown(f'<div class="panel-note">{question.blank_prompt}</div>', unsafe_allow_html=True)

    if question.difficulty == "중급":
        return st.text_input(
            "한 줄 답안",
            key=key,
            placeholder=question.blank_prompt,
            label_visibility="collapsed",
        )

    if st_ace is not None:
        return st_ace(
            value="",
            language="python",
            theme="tomorrow_night_blue",
            key=key,
            height=180,
            font_size=14,
            tab_size=4,
            show_gutter=True,
            wrap=True,
            auto_update=True,
            placeholder=question.blank_prompt,
        )
    st.warning("코드 에디터를 불러오지 못해 기본 입력창으로 전환했습니다.")
    return st.text_area(
        "여러 줄 답안",
        key=key,
        height=180,
        placeholder=question.blank_prompt,
        label_visibility="collapsed",
    )


def _render_result(question: Question, result: GradeResult) -> None:
    st.markdown("---")
    st.markdown("#### 채점 결과")
    if result.passed:
        st.success(result.summary, icon="✅")
    else:
        st.error(result.summary, icon="🧩")
    if result.error_type:
        st.caption(f"분류: {result.error_type}")
    if result.feedback:
        with st.container(border=True):
            st.write(result.feedback)

    st.markdown("##### 모범 코드")
    st.code(question.solution, language="python")
    st.markdown("##### 핵심 해설")
    st.info(question.explanation, icon="💡")

    retry, next_question = st.columns(2)
    retry.button(
        "다시 풀기",
        width="stretch",
        on_click=_clear_answer,
        args=(question,),
    )
    next_question.button(
        "다음 문제 →",
        type="primary",
        width="stretch",
        on_click=_go_next,
        args=(question.id,),
    )


_initialize_state()
selected_question = _render_sidebar()
question_number = [question.id for question in QUESTIONS].index(selected_question.id) + 1

st.markdown(
    """
    <section class="hero">
        <div class="hero-kicker">MONTH-END EDA PRACTICE</div>
        <h1>코드를 외우지 말고,<br>패턴을 익히세요.</h1>
        <p>작은 데이터로 직접 판단하고 작성한 뒤, 즉시 채점과 해설로 빈틈을 메우는 12문제 실전 코스입니다.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([0.45, 0.55], gap="large")

with left:
    st.markdown(f'<div class="eyebrow">QUESTION {question_number:02d} / {len(QUESTIONS):02d}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="question-title">{selected_question.title}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<span class="badge">{selected_question.topic}</span>'
        f'<span class="badge green">{selected_question.difficulty}</span>',
        unsafe_allow_html=True,
    )
    st.markdown("")
    st.markdown(selected_question.prompt)
    with st.expander("힌트 보기"):
        st.write(selected_question.hint)
    _render_data_preview(selected_question)

with right:
    answer = _render_answer_input(selected_question)
    if st.button("답안 제출", type="primary", width="stretch"):
        result = grade_submission(selected_question, answer)
        _record_submission(selected_question, result)
        st.rerun()

    stored_result = st.session_state.progress[selected_question.id]["result"]
    if isinstance(stored_result, GradeResult):
        _render_result(selected_question, stored_result)

st.markdown(
    '<div class="footer">EDA Skeleton Code Master · 세션 기반 학습 · 서버에 개인 답안을 저장하지 않습니다</div>',
    unsafe_allow_html=True,
)
