import streamlit as st
import pandas as pd
import os


st.set_page_config(
    page_title="퀴즈 웹"
)

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "score" not in st.session_state:
    st.session_state.score = 0

if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False

# -----------------------------
# 가상 사용자 DB
# 실제 서비스에서는 DB 사용
# -----------------------------
USER_DB = {
    "admin": "1234",
    "user1": "pass1",
    "guest": "guest"
}

# -----------------------------------
# 퀴즈 CSV 자동 생성 (최초 1회)
# -----------------------------------
QUIZ_FILE = "quiz_data.csv"

if not os.path.exists(QUIZ_FILE):
    quiz_df = pd.DataFrame([
        ["1 + 1 = ?", "2", "1", "3", "4", "2"],
        ["파이썬 제작자는?", "Guido van Rossum", "Elon Musk", "Tom", "Bill Gates", "Guido van Rossum"],
        ["대한민국 수도는?", "서울", "부산", "대전", "인천", "서울"]
    ], columns=["question", "A", "B", "C", "D", "answer"])

    quiz_df.to_csv(QUIZ_FILE, index=False, encoding="utf-8-sig")

# -----------------------------------
# 캐싱 적용 퀴즈 데이터 로딩
# -----------------------------------
@st.cache_data
def load_quiz_data():
    df = pd.read_csv(QUIZ_FILE)
    return df


# -----------------------------
# 로그인 함수
# -----------------------------
def login(user_id, user_pw):
    if user_id in USER_DB:
        if USER_DB[user_id] == user_pw:
            return True
    return False

# -----------------------------
# 로그아웃 함수
# -----------------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""

# -----------------------------
# 로그인 안 된 상태
# -----------------------------
if not st.session_state.logged_in:

    st.title("🔐 로그인 페이지")

    st.markdown('## 2020204088 구본욱')

    user_id = st.text_input("아이디")
    user_pw = st.text_input("비밀번호", type="password")

    login_btn = st.button("로그인")


    if login_btn:
        if login(user_id, user_pw):
            st.session_state.logged_in = True
            st.session_state.username = user_id
            st.success("로그인 성공!")
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

# -----------------------------
# 로그인 성공 후 퀴즈 페이지
# -----------------------------
elif not st.session_state.quiz_done:
    st.title("퀴즈")
    st.success(f"{st.session_state.username} 님 로그인되었습니다.")

    quiz_df = load_quiz_data()

    answers = []

    with st.form("quiz_form"):
        for i, row in quiz_df.iterrows():
            st.subheader(f"{i+1}. {row['question']}")

            user_answer = st.radio(
                "정답 선택",
                [row["A"], row["B"], row["C"], row["D"]],
                key=f"q{i}"
            )
            answers.append(user_answer)

        submitted = st.form_submit_button("제출하기")

    if submitted:
        score = 0

        for i, row in quiz_df.iterrows():
            if answers[i] == row["answer"]:
                score += 1

        st.session_state.score = score
        st.session_state.quiz_done = True
        st.rerun()

    if st.button("로그아웃"):
        logout()
        st.rerun()


# -----------------------------------
# 결과 페이지
# -----------------------------------
else:
    st.title("📊 결과 확인")

    total = len(load_quiz_data())
    score = st.session_state.score

    st.success(f"{st.session_state.username} 님의 점수는 {score} / {total} 입니다.")


    # 좌우 여백 + 가운데 정렬용 컬럼
    space1, col1, col2, col3, space2 = st.columns([1, 2, 2, 2, 1])



    # -------------------------
    # 정답 보기
    # -------------------------
    with col1:
        if st.button("정답 보기", use_container_width=True):
            quiz_df = load_quiz_data()

            st.subheader("정답 목록")

            for i, row in quiz_df.iterrows():
                st.write(f"{i+1}. {row['question']}")
                st.write(f"정답: {row['answer']}")
                st.divider()

    # -------------------------
    # 다시 풀기
    # -------------------------
    with col2:
        if st.button("다시 풀기", use_container_width=True):
            st.session_state.score = 0
            st.session_state.quiz_done = False
            st.rerun()

    # -------------------------
    # 로그아웃
    # -------------------------
    with col3:
        if st.button("로그아웃", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.score = 0
            st.session_state.quiz_done = False
            st.rerun()