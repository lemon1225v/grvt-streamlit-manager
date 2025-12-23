import streamlit as st

st.set_page_config(page_title="GRVT Account Manager", layout="wide")

st.title("📊 GRVT 계정 관리 대시보드")

st.write("이 페이지는 GRVT API를 이용해 여러 계정을 관리하기 위한 웹앱입니다.")

account = st.selectbox(
    "관리할 계정을 선택하세요",
    ["Account 1", "Account 2", "Account 3", "Account 4", "Account 5", "Account 6"]
)

st.success(f"{account} 선택됨")

if st.button("잔고 조회"):
    st.info("여기에 GRVT API를 통한 잔고 조회 코드가 들어갈 예정입니다.")
