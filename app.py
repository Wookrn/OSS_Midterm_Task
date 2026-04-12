import streamlit as st
import pandas as pd


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


# -----------------------------
# 가상 사용자 DB
# 실제 서비스에서는 DB 사용
# -----------------------------
USER_DB = {
    "admin": "1234",
    "user1": "pass1",
    "guest": "guest"
}



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
# 로그인 성공 후 페이지
# -----------------------------
else:
    st.title("퀴즈")
    st.success(f"{st.session_state.username} 님 로그인되었습니다.")

    st.write("로그인 성공")
    st.write("퀴즈 페이지 예정")

    if st.button("로그아웃"):
        logout()
        st.rerun()
