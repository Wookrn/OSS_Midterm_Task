import streamlit as st
import pandas as pd
import os


st.set_page_config(
    page_title="퀴즈 웹"
)


# 세션 상태 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "score" not in st.session_state:
    st.session_state.score = 0

if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False


# csv 파일
QUIZ_FILE = "quiz_data.csv"
RESULT_FILE = "result_data.csv"
USER_DB = "users.csv"


if not os.path.exists(RESULT_FILE):
    survey_df = pd.DataFrame(columns=["username", "score", "comment"])
    survey_df.to_csv(RESULT_FILE, index=False, encoding="utf-8-sig")



# 캐싱 적용 (퀴즈 데이터 로딩)
@st.cache_data
def load_quiz_data():
    df = pd.read_csv(QUIZ_FILE)
    return df

# 캐싱 적용 (사용자 DB 로딩)
@st.cache_data
def load_user_db():
    u_df = pd.read_csv(USER_DB)
    return u_df

# 로그인 함수

def login(user_id, user_pw):
    df = load_user_db()
    
    # 입력받은 아이디가 데이터프레임에 존재하는지 확인
    user_row = df[df['id'] == user_id]
    
    if not user_row.empty:
        # 비밀번호 확인 (문자열 타입으로 비교)
        if str(user_row.iloc[0]['password']) == str(user_pw):
            return True
    return False

# 로그아웃 함수
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""


# 로그인 안 된 상태 (초기 화면)
if not st.session_state.logged_in:

    st.title("🔐 로그인 페이지")

    st.markdown('## 2020204088 구본욱')

    user_id = st.text_input("아이디")
    user_pw = st.text_input("비밀번호", type="password")

    login_btn = st.button("로그인")

    # 로그인 버튼 클릭 시 DB의 로그인 정보와 확인하여 로그인 처리
    if login_btn:
        if login(user_id, user_pw):
            st.session_state.logged_in = True
            st.session_state.username = user_id
            st.success("로그인 성공!")
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호가 올바르지 않습니다.")


# 로그인 성공 후 퀴즈 페이지
elif not st.session_state.quiz_done:
    st.title("게임 정보 퀴즈")
    st.success(f"{st.session_state.username} 님 로그인되었습니다.")

    quiz_df = load_quiz_data()

    answers = []

    with st.form("quiz_form"):
        for i, row in quiz_df.iterrows():
            st.subheader(f"{i+1}. {row['question']}")

            user_answer = st.radio(
                "",
                [row["A"], row["B"], row["C"], row["D"]],
                key=f"q{i}"
            )
            answers.append(user_answer)

        comment = st.text_area("좋아하는 게임 분야가 있다면 적어주세요")

        submitted = st.form_submit_button("제출하기")


    #제출 버튼 클릭 시 점수 계산 및 결과 저장
    if submitted:
        score = 0

        for i, row in quiz_df.iterrows():
            if answers[i] == row["answer"]:
                score += 1

        st.session_state.score = score

        new_row = pd.DataFrame([{
            "username": st.session_state.username,
            "score": score,
            "comment": comment
        }])

        new_row.to_csv(RESULT_FILE, mode="a", header=False, index=False, encoding="utf-8-sig")

        st.session_state.quiz_done = True
        st.rerun()

    if st.button("로그아웃"):
        logout()
        st.rerun()



# 결과 페이지
else:
    st.title("📊 결과 확인")

    total = len(load_quiz_data())
    score = st.session_state.score

    if(score == total):
        st.success(f"축하합니다! {st.session_state.username} 님은 만점을 받았습니다! 🎉")

    else:
        st.success(f"{st.session_state.username} 님의 점수는 {score} / {total} 입니다.")


    # 좌우 여백 + 가운데 정렬용 컬럼
    space1,col1, col2, col3, col4,space2 = st.columns([1,2,2,2,2,1])


    # 정답 보기
    with col1:
        if st.button("정답 보기", use_container_width=True):
            show_answer = True


    # 다시 풀기
    with col2:
        if st.button("다시 풀기", use_container_width=True):
            st.session_state.score = 0
            st.session_state.quiz_done = False
            st.rerun()


    # 로그아웃
    with col3:
        if st.button("로그아웃", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.score = 0
            st.session_state.quiz_done = False
            st.rerun()


    # 정답 출력
    if 'show_answer' in locals() and show_answer:
        quiz_df = load_quiz_data()

        st.subheader("정답 목록")

        for i, row in quiz_df.iterrows():
            st.write(f"{i+1}. {row['question']}")
            st.write(f"정답: {row['answer']}")
            st.write(f"해설: {row['commentary']}")
            st.divider()

    #기록 보기
    with col4:
        if st.button("기록 보기",use_container_width=True):
            show_result = True

    if 'show_result' in locals() and show_result:        
        df = pd.read_csv(RESULT_FILE)

        current_user = st.session_state.username

        # 현재 로그인한 사용자 기록만 추출
        user_df = df[df["username"] == current_user]
        

        if user_df.empty:
            st.info("저장된 기록이 없습니다.")
        else:
            # 최고 점수
            best_score = user_df["score"].max()

            # 도전 횟수
            play_count = len(user_df)

            st.subheader("🏆내 플레이 기록")

            st.write(f"사용자 이름 : {current_user}")
            st.write(f"최고 점수 : {best_score}")
            st.write(f"도전 횟수 : {play_count}")